from pathlib import Path
import re

p=Path('index.html')
s=p.read_text()

bad='devJobs:state.devJobs}))}))}'
good='devJobs:state.devJobs}))}'
assert bad in s
s=s.replace(bad,good,1)

old='return hashData()+"|"+state.view+"|"+state.query+"|"+(state.inlineEditId||"")+"|"+[...state.collapsed].sort().join(",")'
new='return hashData()+"|"+state.view+"|"+state.query+"|"+(state.inlineEditId||"")+"|"+(state.editingId||"")+"|"+[...state.collapsed].sort().join(",")'
assert old in s
s=s.replace(old,new,1)

# Public repo safety: never publish backlog text via a GitHub issue from the browser.
pattern=r'function handoffDevJob\(id\)\{.*?\}\nfunction setDevJobStatus'
replacement='''async function handoffDevJob(id){const j=state.devJobs.find(x=>x.id===id);if(!j)return;try{await navigator.clipboard.writeText(j.prompt);j.status="handed-off";j.updatedAt=new Date().toISOString();save();render();notice("Agent-handoff förberedd · prompt kopierad")}catch{notice("Kunde inte kopiera agent-handoff")}}\nfunction setDevJobStatus'''
s,n=re.subn(pattern,replacement,s,count=1,flags=re.S)
assert n==1
s=s.replace('GitHub-handoff öppnar ett förifyllt uppdrag utan att lagra GitHub/OpenAI-hemligheter i appen.','Agent-handoff är privat och copy-only tills en separat autentiserad bridge är kopplad. Appen publicerar aldrig backlogtext till GitHub.')
s=s.replace('>Öppna GitHub-uppdrag</button>','>Förbered agent-handoff</button>')

# v6 import/export parity for development jobs.
old_import='''function importData(txt){const trimmed=txt.trim();if(!trimmed)return 0;let imported,importedBacklog=null;if(trimmed.startsWith("{")||trimmed.startsWith("[")){const obj=JSON.parse(trimmed);imported=Array.isArray(obj)?obj:obj.tasks;if(!Array.isArray(imported))throw new Error("JSON saknar tasks-lista");if(!Array.isArray(obj)&&Array.isArray(obj.backlog))importedBacklog=obj.backlog.map(normalizeBacklogItem);imported=imported.map(normalizeTask)}else imported=parseMarkdown(trimmed);pushUndo("import");state.tasks=imported;if(importedBacklog)state.backlog=importedBacklog;save();render();return imported.length}'''
new_import='''function importData(txt){const trimmed=txt.trim();if(!trimmed)return 0;let imported,importedBacklog=null,importedDevJobs=null;if(trimmed.startsWith("{")||trimmed.startsWith("[")){const obj=JSON.parse(trimmed);imported=Array.isArray(obj)?obj:obj.tasks;if(!Array.isArray(imported))throw new Error("JSON saknar tasks-lista");if(!Array.isArray(obj)&&Array.isArray(obj.backlog))importedBacklog=obj.backlog.map(normalizeBacklogItem);if(!Array.isArray(obj)&&Array.isArray(obj.devJobs))importedDevJobs=obj.devJobs.map(normalizeDevJob);imported=imported.map(normalizeTask)}else imported=parseMarkdown(trimmed);pushUndo("import");state.tasks=imported;if(importedBacklog)state.backlog=importedBacklog;if(importedDevJobs)state.devJobs=importedDevJobs;save();render();return imported.length}'''
assert old_import in s
s=s.replace(old_import,new_import,1)

test_anchor='await test("Data version is 6",()=>assert(DATA_VERSION===6));'
assert test_anchor in s
s=s.replace(test_anchor,test_anchor+'\nawait test("v6 JSON import restores development jobs",()=>{state.devJobs=[];importData(JSON.stringify({version:6,tasks:[{title:"t"}],backlog:[],devJobs:[{id:"j-import",prompt:"private prompt",backlogIds:["b"]}]}));assert(state.devJobs.length===1&&state.devJobs[0].id==="j-import")});',1)

old_test='await test("Remote payload contains todos and backlog",()=>{const p=remotePayload();assert(Array.isArray(p.tasks)&&Array.isArray(p.backlog)&&p.version===5)});'
new_test='await test("Remote payload contains todos, backlog and development jobs",()=>{const p=remotePayload();assert(Array.isArray(p.tasks)&&Array.isArray(p.backlog)&&Array.isArray(p.devJobs)&&p.version===6)});'
assert old_test in s
s=s.replace(old_test,new_test,1)

p.write_text(s)
print('hardened',len(s),'bytes')
