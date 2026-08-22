"use strict";
const V440_VERSION="4.4.0";
const V440_FEATURE_VERSION=1;
const coreNormalizeTask=normalizeTask;
const coreLoad=load;
const coreApplyRemote=applyRemote;
const coreRenderTask=renderTask;
const coreOpenDrawer=openDrawer;
const corePrepareConflict=prepareConflict;
let pendingCommentImages=[];
let dragTaskId=null;

function nowIso(){return new Date().toISOString()}
function normalizeImage(x){return{id:String(x?.id||uid()),name:String(x?.name||"bild"),type:String(x?.type||"image/jpeg"),dataUrl:String(x?.dataUrl||"")}}
function normalizeComment(x){return{id:String(x?.id||uid()),text:String(x?.text||""),createdAt:x?.createdAt||nowIso(),images:Array.isArray(x?.images)?x.images.map(normalizeImage).filter(i=>i.dataUrl.startsWith("data:image/")):[]}}
function taskStamp(t){return Date.parse(t?.updatedAt||t?.completedAt||t?.createdAt||0)||0}
function touchTask(t){if(t)t.updatedAt=nowIso()}
function taskOrderValue(t){return Number.isFinite(Number(t?.order))?Number(t.order):Number.MAX_SAFE_INTEGER}
function ensureTaskOrder(tasks=state.tasks){let next=10;for(const t of tasks){if(!Number.isFinite(Number(t.order))||Number(t.order)<=0)t.order=next;next=Math.max(next+10,Number(t.order)+10)}}
function commentsText(t){return(t.comments||[]).map(c=>c.text).join(" ")}
function taskSemantic(t){return[t.id,t.title,t.notes,t.dueDate,t.completed,t.completedAt,t.cleared,t.path,t.tags,!!t.inbox,t.order,t.updatedAt,t.comments]}

normalizeTask=function(t){const base=coreNormalizeTask(t);return{...base,inbox:!!t.inbox,order:Number.isFinite(Number(t.order))?Number(t.order):0,updatedAt:t.updatedAt||t.completedAt||t.createdAt||base.createdAt,comments:Array.isArray(t.comments)?t.comments.map(normalizeComment):[]}}

hashData=function(tasks=state.tasks,backlog=state.backlog,devJobs=state.devJobs){return JSON.stringify({tasks:tasks.map(taskSemantic),backlog:backlog.map(b=>[b.id,b.type,b.title,b.description,b.selected,b.comment,b.status,b.updatedAt]),devJobs:devJobs.map(j=>[j.id,j.status,j.backlogIds,j.prompt,j.note,j.updatedAt])})}

saveLocal=function(touch=true){if(touch)state.updatedAt=nowIso();ensureTaskOrder();localStorage.setItem(STORAGE_KEY,JSON.stringify({version:DATA_VERSION,featureVersion:V440_FEATURE_VERSION,appVersion:V440_VERSION,updatedAt:state.updatedAt,tasks:state.tasks,backlog:state.backlog,devJobs:state.devJobs}))}
remotePayload=function(){ensureTaskOrder();return{app:"Todo",version:DATA_VERSION,featureVersion:V440_FEATURE_VERSION,appVersion:V440_VERSION,updatedAt:state.updatedAt||nowIso(),tasks:state.tasks,backlog:state.backlog,devJobs:state.devJobs}}
exportPayload=function(){return{...remotePayload(),exportedAt:nowIso()}}

load=function(){coreLoad();ensureTaskOrder();state.tasks=state.tasks.map(normalizeTask);saveLocal(false)}
applyRemote=function(data,rev){const oldFeature=Number(data?.featureVersion||0);const needs=coreApplyRemote(data,rev);ensureTaskOrder();state.tasks=state.tasks.map(normalizeTask);saveLocal(false);return needs||oldFeature<V440_FEATURE_VERSION}

createSnapshot=function(reason){if(!state.tasks.length&&!state.backlog.length&&!state.devJobs.length)return;const a=snapshots(),fingerprint=hashData();if(a[0]?.fingerprint===fingerprint)return;a.unshift({id:uid(),createdAt:nowIso(),reason,version:V440_VERSION,fingerprint,tasks:JSON.parse(JSON.stringify(state.tasks)),backlog:JSON.parse(JSON.stringify(state.backlog)),devJobs:JSON.parse(JSON.stringify(state.devJobs))});setSnapshots(a)}

function nextOrderFor(predicate=()=>true){const a=state.tasks.filter(predicate).map(taskOrderValue).filter(Number.isFinite);return(a.length?Math.max(...a):0)+10}
function markSorted(t){if(t.dueDate||t.path?.length||t.tags?.next||t.tags?.followup||t.tags?.some)t.inbox=false}

addTask=function(){const input=document.getElementById("newTitle"),title=input.value.trim();if(!title)return;pushUndo("add todo");const next=state.newFlags.next||state.view==="next",followup=state.newFlags.followup||state.view==="follow",some=state.newFlags.some||state.view==="some",dueDate=document.getElementById("newDate").value,path=parsePath(document.getElementById("newPath").value);const inbox=state.view==="inbox"&&!dueDate&&!path.length&&!next&&!followup&&!some;state.tasks.push(normalizeTask({title,dueDate,path,inbox,order:nextOrderFor(),updatedAt:nowIso(),tags:{next,followup,some,nextWeekFor:next?nextMondayIso():null},createdAt:nowIso()}));input.value="";document.getElementById("newDate").value="";document.getElementById("newPath").value="";state.newFlags={next:false,followup:false,some:false};syncNewFlags();save();render()}

toggleComplete=function(t){recordFrictionEvent("toggle",`complete:${t.id}`,{});pushUndo(t.completed?"reopen todo":"complete todo");t.completed=!t.completed;t.completedAt=t.completed?nowIso():null;t.cleared=false;touchTask(t);save();render();notice(t.completed?"Avklarad – ligger kvar på samma plats tills du rensar":"Återöppnad")}

toggleTag=function(t,tag){recordFrictionEvent("toggle",`${tag}:${t.id}`,{});pushUndo(`toggle ${tag}`);if(tag==="next"){t.tags.next=!t.tags.next;t.tags.nextWeekFor=t.tags.next?nextMondayIso():null}else t.tags[tag]=!t.tags[tag];markSorted(t);touchTask(t);save();render()}

saveInline=function(){const t=findTask(state.inlineEditId);if(!t)return;recordFrictionEvent("edit",`task:${t.id}`,{mode:"inline"});const title=document.getElementById("inlineTitle")?.value.trim(),date=document.getElementById("inlineDate")?.value||"",path=parsePath(document.getElementById("inlinePath")?.value||"");if(title&&(title!==t.title||date!==t.dueDate||pathText(path)!==pathText(t.path))){pushUndo("inline edit");t.title=title;t.dueDate=date;t.path=path;t.level=path.length;markSorted(t);touchTask(t);save()}state.inlineEditId=null;render()}

closeDrawer=function(saveChanges=true){const t=findTask(state.editingId);if(t&&saveChanges)recordFrictionEvent("edit",`task:${t.id}`,{mode:"drawer"});if(t&&saveChanges){const path=parsePath(document.getElementById("editPath").value),updated={title:document.getElementById("editTitle").value.trim()||t.title,dueDate:document.getElementById("editDate").value,notes:document.getElementById("editNotes").value,path,next:document.getElementById("tagNext").classList.contains("on"),followup:document.getElementById("tagFollow").classList.contains("on"),some:document.getElementById("tagSome").classList.contains("on")};const changed=updated.title!==t.title||updated.dueDate!==t.dueDate||updated.notes!==t.notes||pathText(updated.path)!==pathText(t.path)||updated.next!==t.tags.next||updated.followup!==t.tags.followup||updated.some!==t.tags.some;if(changed){pushUndo("edit todo");t.title=updated.title;t.dueDate=updated.dueDate;t.notes=updated.notes;t.path=updated.path;t.level=t.path.length;t.tags.next=updated.next;t.tags.nextWeekFor=updated.next?(t.tags.nextWeekFor||nextMondayIso()):null;t.tags.followup=updated.followup;t.tags.some=updated.some;markSorted(t);touchTask(t);save()}}document.getElementById("drawer").classList.remove("open");document.getElementById("drawerBack").classList.remove("open");state.editingId=null;pendingCommentImages=[];render()}

function clearCompletedGlobal(){const a=state.tasks.filter(t=>t.completed&&!t.cleared);if(!a.length){notice("Inga avklarade att rensa");return}pushUndo("clear all completed");a.forEach(t=>{t.cleared=true;touchTask(t)});save();render();notice(`${a.length} avklarade rensade i alla vyer`)}
clearCompleted=clearCompletedGlobal;
