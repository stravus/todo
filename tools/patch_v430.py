from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def one(old,new,label):
    global s
    n=s.count(old)
    assert n==1, f'{label}: expected 1 occurrence, got {n}'
    s=s.replace(old,new,1)

def sub(pattern,repl,label,flags=0):
    global s
    s2,n=re.subn(pattern,repl,s,count=1,flags=flags)
    assert n==1, f'{label}: expected 1 replacement, got {n}'
    s=s2

one('const APP_VERSION="4.2.1";','const APP_VERSION="4.3.0";','version bump')

anchor='const AUTO_REAUTH_KEY="doctrin-todo-auto-reauth-v1";\n'
insert=anchor+'''const APP_PIN_KEY="todo-app-version-pin-v1";\nconst APP_SHELLS=[\n {version:"4.3.0",dataVersion:6,path:"app-versions/v4.3.0.html",date:"2026-08-22"},\n {version:"4.2.1",dataVersion:6,path:"app-versions/v4.2.1.html",date:"2026-08-16"},\n {version:"4.2.0",dataVersion:6,path:"app-versions/v4.2.0.html",date:"2026-08-16"}\n];\n'''
one(anchor,insert,'app shell constants')

history_anchor='const VERSION_HISTORY=[\n'
one(history_anchor,history_anchor+' {version:"4.3.0",date:"2026-08-22",text:"Tool-version snapshots and local app-shell restore, isolated from todo/Dropbox data; restore is allowed only between compatible data schemas."},\n','version history')

marker='function historyHtml(){'
assert s.count(marker)==1
functions=r'''function appShellByVersion(version){return APP_SHELLS.find(x=>x.version===version)||null}
function appShellCompatible(shell){return!!shell&&Number(shell.dataVersion)===DATA_VERSION}
function appPinVersion(){return localStorage.getItem(APP_PIN_KEY)||""}
function appDataFingerprint(){return hashData(state.tasks,state.backlog,state.devJobs)}
function pinAppVersion(version){const shell=appShellByVersion(version);if(!shell){notice("Verktygsversionen saknas");return false}if(!appShellCompatible(shell)){notice("Kan inte återställa: annat dataschema");return false}if(version===APP_VERSION){localStorage.removeItem(APP_PIN_KEY);notice("Du kör redan senaste versionen");return true}localStorage.setItem(APP_PIN_KEY,version);location.reload();return true}
function clearAppVersionPin(){localStorage.removeItem(APP_PIN_KEY);location.href="./"}
function appVersionsHtml(){const pin=appPinVersion();return`<h3>Verktygssnapshots</h3><div class="item-copy">Återställer endast verktygskoden. Todos, backlog, development jobs och Dropbox-filen ändras inte. Endast versioner med samma dataschema kan köras skrivbart.</div>${APP_SHELLS.map(x=>{const current=x.version===APP_VERSION,compatible=appShellCompatible(x),pinned=pin===x.version;return`<div class="version-item" data-appshell="${esc(x.version)}"><div class="item-title">v${esc(x.version)} ${current?`<span class="pill done">Current</span>`:""}${pinned?`<span class="pill">Pinned</span>`:""}</div><div class="item-copy">${esc(x.date)} · dataschema ${x.dataVersion}${compatible?" · kompatibel":" · ej skrivkompatibel"}</div><div class="snap-actions">${current?`<button disabled>Aktuell version</button>`:compatible?`<button data-apprestore="${esc(x.version)}">Kör denna version</button>`:`<button disabled>Restore blockerad</button>`}</div></div>`}).join("")}${pin&&pin!==APP_VERSION?`<div class="snap-actions"><button id="clearAppPinBtn">Återgå till senaste</button></div>`:""}`}
function injectAppVersionBanner(html,version){const safe=String(version).replace(/[^0-9A-Za-z._-]/g,"");const banner=`<div id="appVersionPinBanner" style="position:fixed;z-index:99999;left:50%;top:10px;transform:translateX(-50%);display:flex;gap:10px;align-items:center;background:#302e2a;color:#fff;padding:8px 11px;border-radius:10px;box-shadow:0 8px 24px rgba(0,0,0,.18);font:12px -apple-system,BlinkMacSystemFont,Segoe UI,sans-serif">Kör verktyg v${safe} · data ligger kvar <button style="border:0;border-radius:7px;padding:5px 8px;cursor:pointer" onclick="localStorage.removeItem('${APP_PIN_KEY}');location.href='./'">Återgå till senaste</button></div>`;return html.replace(/<body([^>]*)>/i,`<body$1>${banner}`)}
async function maybeLoadPinnedApp(){const pinned=appPinVersion();if(!pinned||pinned===APP_VERSION)return false;const shell=appShellByVersion(pinned);if(!appShellCompatible(shell)){localStorage.removeItem(APP_PIN_KEY);return false}const before=localStorage.getItem(STORAGE_KEY);try{const res=await fetch(shell.path,{cache:"no-store"});if(!res.ok)throw new Error(`snapshot ${res.status}`);let html=await res.text();if(!html.includes(`const APP_VERSION="${pinned}"`)||!html.includes(`const DATA_VERSION=${DATA_VERSION};`))throw new Error("snapshot mismatch");html=injectAppVersionBanner(html,pinned);document.open();document.write(html);document.close();return true}catch(e){if(before!==null)localStorage.setItem(STORAGE_KEY,before);localStorage.removeItem(APP_PIN_KEY);console.error("App snapshot restore failed",e);return false}}
'''
s=s.replace(marker,functions+marker,1)

one('<h3>Snapshots & rollback</h3>','${appVersionsHtml()}<h3>Datasnapshots & rollback</h3>','history app shell UI')
one('Snapshots innehåller nu både todos och backlog. Restore synkar den återställda datan till Dropbox.','Datasnapshots innehåller todos, backlog och development jobs. Restore synkar den återställda datan till Dropbox.','data snapshot clarification')

listener='document.querySelectorAll("[data-restore]").forEach(b=>b.addEventListener("click",()=>restoreSnapshot(b.dataset.restore)))'
one(listener,listener+';document.querySelectorAll("[data-apprestore]").forEach(b=>b.addEventListener("click",()=>pinAppVersion(b.dataset.apprestore)));document.getElementById("clearAppPinBtn")?.addEventListener("click",clearAppVersionPin)','bind app restore')

oldtest='await test("Current version is 4.2.1",()=>assert(VERSION_HISTORY[0].version==="4.2.1"));'
newtests='''await test("App shell registry includes current snapshot",()=>{const x=appShellByVersion("4.3.0");assert(x&&x.dataVersion===DATA_VERSION&&x.path.includes("v4.3.0"))});\nawait test("App shell registry keeps compatible v4.2 snapshots",()=>assert(appShellCompatible(appShellByVersion("4.2.1"))&&appShellCompatible(appShellByVersion("4.2.0"))));\nawait test("App shell restore blocks data-schema mismatch",()=>assert(!appShellCompatible({version:"old",dataVersion:DATA_VERSION-1})));\nawait test("App shell pin is local-only",()=>assert(!Object.prototype.hasOwnProperty.call(remotePayload(),"appVersionPin")));\nawait test("Current version is 4.3.0",()=>assert(VERSION_HISTORY[0].version==="4.3.0"));'''
one(oldtest,newtests,'self tests')

# Replace only the final init invocation.
assert s.rstrip().endswith('init();\n</script>\n</body>\n</html>') or s.rstrip().endswith('init();\n</script>\n</body>\n</html>')
idx=s.rfind('\ninit();')
assert idx!=-1
s=s[:idx]+'\nasync function boot(){if(await maybeLoadPinnedApp())return;await init()}\nboot();'+s[idx+len('\ninit();'):]

# Compatibility invariants.
assert 'const DATA_VERSION=6;' in s
assert 'const STORAGE_KEY="doctrin-things-todo-v1";' in s
assert 'const DROPBOX_FILE="/todos.json";' in s
assert 'remotePayload(){return{app:"Todo",version:DATA_VERSION' in s
assert 'todo-app-version-pin-v1' in s
assert 'app-versions/v4.2.1.html' in s

p.write_text(s,encoding='utf-8')
print('Patched index.html to v4.3.0')
