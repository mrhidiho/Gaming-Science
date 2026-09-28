
const IDS=["01.1", "01.2", "01.3", "01.4", "02.1", "02.2", "02.3", "02.4", "03.1", "03.2", "03.3", "03.4", "04.1", "04.2", "04.3", "04.4", "05.1", "05.2", "05.3", "05.4"];
const KEY='game-engineering-package02-progress-v1';
const blank=()=>Object.fromEntries(IDS.map(id=>[id,{study:false,lab:false,core:0,application:0,note:''}]));
let state=blank();
const status=document.getElementById('status');
function validProgress(data){
 if(!data||data.schema!==KEY||!data.lessons||typeof data.lessons!=='object')throw Error('Wrong progress schema.');
 if(Object.keys(data.lessons).length!==IDS.length||Object.keys(data.lessons).some(id=>!IDS.includes(id)))throw Error('Lesson IDs do not match this package.');
 const clean=blank();
 for(const id of IDS){const v=data.lessons[id];
  if(!v||typeof v.study!=='boolean'||typeof v.lab!=='boolean'||!Number.isInteger(v.core)||v.core<0||v.core>6||!Number.isInteger(v.application)||v.application<0||v.application>4||typeof v.note!=='string'||v.note.length>1000)throw Error('Invalid progress values.');
  clean[id]={study:v.study,lab:v.lab,core:v.core,application:v.application,note:v.note};
 } return clean;
}
function complete(v){return v.study&&v.lab&&v.core>=5&&v.core+v.application>=8;}
function draw(){let done=0;
 for(const id of IDS){const box=document.querySelector(`.progress[data-id="${id}"]`),v=state[id];
  box.querySelectorAll('[data-field]').forEach(input=>{const f=input.dataset.field;if(input.type==='checkbox')input.checked=v[f];else input.value=v[f];});
  const yes=complete(v);if(yes)done++;box.querySelector('.lesson-status').textContent=yes?'Complete (self-recorded; not independently verified)':'Not yet recorded as complete';
 }document.getElementById('progress-summary').textContent=`${done} / ${IDS.length} lessons recorded complete`;
}
function save(){try{localStorage.setItem(KEY,JSON.stringify({schema:KEY,lessons:state}));status.textContent='Saved locally. Export a backup regularly.';}catch(e){status.textContent='Browser storage unavailable. Use Export progress before leaving.';}}
try{const stored=localStorage.getItem(KEY);if(stored)state=validProgress(JSON.parse(stored));}catch(e){status.textContent='Stored progress unavailable or invalid. No imported values were applied.';}
draw();
document.querySelectorAll('.progress').forEach(box=>box.addEventListener('change',event=>{const input=event.target,field=input.dataset.field;if(!field)return;const id=box.dataset.id;
 if(input.type==='checkbox')state[id][field]=input.checked;
 else if(input.type==='number'){const max=field==='core'?6:4;const v=Number(input.value);if(!Number.isInteger(v)||v<0||v>max){input.value=state[id][field];return;}state[id][field]=v;}
 else state[id][field]=input.value.slice(0,1000);save();draw();}));
document.getElementById('export').addEventListener('click',()=>{const blob=new Blob([JSON.stringify({schema:KEY,lessons:state},null,2)],{type:'application/json'});const url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='package02_progress.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),2000);});
const file=document.getElementById('import-file');document.getElementById('import').addEventListener('click',()=>file.click());
file.addEventListener('change',async()=>{if(!file.files.length)return;try{if(file.files[0].size>100000)throw Error('Progress file is too large.');const next=validProgress(JSON.parse(await file.files[0].text()));if(confirm('Replace the current Package 02 progress with this file?')){state=next;save();draw();}}catch(e){status.textContent='Import rejected: '+e.message;}finally{file.value='';}});
const search=document.getElementById('search');function filter(){const q=search.value.trim().toLowerCase();let count=0;document.querySelectorAll('.lesson').forEach(a=>{const match=!q||a.textContent.toLowerCase().includes(q);a.hidden=!match;if(match)count++;});document.getElementById('search-status').textContent=q?`${count} matching lessons`:'All 20 lessons shown';}
search.addEventListener('input',filter);document.getElementById('clear-search').addEventListener('click',()=>{search.value='';filter();});
