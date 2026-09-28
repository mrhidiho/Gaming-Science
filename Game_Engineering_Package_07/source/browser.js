
'use strict';
const IDS=["26.1", "26.2", "26.3", "26.4", "27.1", "27.2", "27.3", "27.4", "28.1", "28.2", "28.3", "28.4", "29.1", "29.2", "29.3", "29.4", "30.1", "30.2", "30.3", "30.4"];
const KEY='game-engineering-package07-volume06-v1';
let state={};
const notice=document.getElementById('notice');
function normalize(value){
 if(!value || value.version!==1 || value.package!==7 || value.volume!==6 || !value.lessons || typeof value.lessons!=='object' || Array.isArray(value.lessons))throw new Error('Not a Package 07 Volume 06 progress file.');
 const clean={};
 for(const id of Object.keys(value.lessons)){
  if(!IDS.includes(id))throw new Error('Unknown lesson ID.');
  const row=value.lessons[id];
  if(!row || typeof row!=='object' || Array.isArray(row) || Object.keys(row).some(k=>!['read','lab','score'].includes(k)))throw new Error('Invalid lesson fields.');
  if(typeof row.read!=='boolean' || typeof row.lab!=='boolean' || !(row.score===null || (Number.isInteger(row.score)&&row.score>=0&&row.score<=10)))throw new Error('Invalid lesson values.');
  clean[id]={read:row.read,lab:row.lab,score:row.score};
 }
 return clean;
}
function envelope(){return {version:1,package:7,volume:6,exported_at:new Date().toISOString(),lessons:state};}
function save(){try{localStorage.setItem(KEY,JSON.stringify(envelope()));}catch(e){notice.textContent='Browser storage is unavailable. Your current progress is in memory; export JSON before closing.';}}
function redraw(){
 let completed=0;
 for(const id of IDS){
  const row=state[id]||{read:false,lab:false,score:null};
  const article=document.querySelector('[data-id="'+id+'"].lesson');
  for(const control of article.querySelectorAll('input[data-field]')){
   const field=control.dataset.field;
   if(field==='score')control.value=row.score===null?'':row.score;else control.checked=row[field];
  }
  const okay=row.read&&row.lab&&row.score!==null&&row.score>=8;
  if(okay)completed++;
  article.querySelector('.status').textContent=okay?'Recorded review target met — evidence still requires review.':'In progress — reading, full lab/transfer and quiz remain separate.';
 }
 document.getElementById('totals').textContent=completed+' / 20 lessons meet the recorded review target';
}
try{const saved=localStorage.getItem(KEY);if(saved)state=normalize(JSON.parse(saved));}catch(e){notice.textContent='Stored progress could not be read. Import a valid backup or start a new record.';}
for(const control of document.querySelectorAll('input[data-field]'))control.addEventListener('change',()=>{
 const id=control.dataset.id;const field=control.dataset.field;const row=state[id]||{read:false,lab:false,score:null};
 if(field==='score'){
  const text=control.value;const value=text===''?null:Number(text);
  if(value!==null&&(!Number.isInteger(value)||value<0||value>10)){notice.textContent='Enter a whole-number quiz score from 0 to 10.';redraw();return;}
  row.score=value;
 }else row[field]=control.checked;
 state[id]=row;save();redraw();
});
document.getElementById('search').addEventListener('input',event=>{
 const q=event.target.value.trim().toLocaleLowerCase();let count=0;
 for(const a of document.querySelectorAll('article.lesson')){a.hidden=!!q&&!a.textContent.toLocaleLowerCase().includes(q);if(!a.hidden)count++;}
 for(const m of document.querySelectorAll('section.module'))m.hidden=!Array.from(m.querySelectorAll('article.lesson')).some(a=>!a.hidden);
 document.getElementById('search-count').textContent=count+' lesson'+(count===1?'':'s')+' shown';
});
document.getElementById('export').addEventListener('click',()=>{
 const url=URL.createObjectURL(new Blob([JSON.stringify(envelope(),null,2)],{type:'application/json'}));
 const a=document.createElement('a');a.href=url;a.download='volume06-progress.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);notice.textContent='Progress JSON export created. Keep it with your study records.';
});
document.getElementById('import-button').addEventListener('click',()=>document.getElementById('import').click());
document.getElementById('import').addEventListener('change',async event=>{
 const file=event.target.files[0];if(!file)return;
 try{if(file.size>100000)throw new Error('Progress file is too large.');const incoming=normalize(JSON.parse(await file.text()));if(!window.confirm('Replace this browser’s recorded progress with the imported file?'))return;state=incoming;save();redraw();notice.textContent='Progress imported. This remains a self-reported learning record.';}
 catch(error){notice.textContent='Import rejected: '+error.message;}
 finally{event.target.value='';}
});
document.getElementById('reset').addEventListener('click',()=>{if(window.confirm('Reset recorded progress? Export a backup first.')){state={};save();redraw();notice.textContent='Recorded progress reset.';}});
redraw();
