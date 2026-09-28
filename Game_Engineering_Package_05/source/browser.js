'use strict';
const key='game-engineering-package-05-v1';
const cards=[...document.querySelectorAll('article.lesson')];
const ids=new Set(cards.map(c=>c.dataset.id));
const empty=()=>({read:false,lab:false,transfer:false,score:0});
let state={};
const note=document.querySelector('#storage-note');
function validate(value){
 if(!value || typeof value!=='object' || Array.isArray(value)) throw Error('Progress must be an object.');
 const cleaned={};
 for(const [id,x] of Object.entries(value)){
  if(!ids.has(id)) throw Error('Unknown lesson: '+id);
  if(!x || typeof x!=='object' || Array.isArray(x)) throw Error('Invalid lesson record.');
  if(Object.keys(x).length!==4 || !['read','lab','transfer'].every(k=>typeof x[k]==='boolean') || !Number.isInteger(x.score) || x.score<0 || x.score>10) throw Error('Invalid completion fields or quiz score.');
  cleaned[id]={read:x.read,lab:x.lab,transfer:x.transfer,score:x.score};
 }
 return cleaned;
}
function complete(x){return x.read && x.lab && x.transfer && x.score>=9;}
function update(){
 let done=0;
 for(const card of cards){
  const x=state[card.dataset.id]||empty();
  card.querySelectorAll('.progress input').forEach(input=>{if(input.type==='checkbox')input.checked=x[input.dataset.field];else input.value=x.score;});
  const pass=complete(x); if(pass)done++;
  card.querySelector('.lesson-status').textContent=pass?'Self-recorded complete':'Evidence or quiz threshold still pending';
 }
 document.querySelector('#progress-summary').textContent=done+' / '+ids.size+' lessons self-recorded complete';
}
function save(){try{localStorage.setItem(key,JSON.stringify({schema:1,package:5,lessons:state}));note.textContent='Progress stored in this browser. Export a backup.';}catch(e){note.textContent='Browser storage unavailable. Progress is in memory; export before closing.';}}
try{const stored=localStorage.getItem(key);if(stored){const data=JSON.parse(stored);if(data.schema!==1||data.package!==5)throw Error('Wrong progress format.');state=validate(data.lessons);}note.textContent='Progress is local to this browser; export before moving files.';}catch(e){note.textContent='Saved progress unavailable or invalid. Start here or import a valid backup.';}
update();
document.querySelectorAll('.progress input').forEach(input=>input.addEventListener('change',()=>{
 const id=input.closest('.progress').dataset.id;const x={...(state[id]||empty())};
 if(input.type==='checkbox')x[input.dataset.field]=input.checked;
 else {const n=Number(input.value);if(!Number.isInteger(n)||n<0||n>10){input.value=x.score;note.textContent='Quiz score must be a whole number from 0 to 10.';return;}x.score=n;}
 state[id]=x;update();save();
}));
const search=document.querySelector('#search');
function filter(){const q=search.value.trim().toLowerCase();let count=0;document.body.classList.toggle('searching',!!q);for(const c of cards){const show=!q||c.textContent.toLowerCase().includes(q);c.hidden=!show;if(show)count++;}document.querySelector('#search-status').textContent=q?count+' matching lessons':'';}
search.addEventListener('input',filter);document.querySelector('#clear').addEventListener('click',()=>{search.value='';filter();search.focus();});
document.querySelector('#export').addEventListener('click',()=>{const blob=new Blob([JSON.stringify({schema:1,package:5,lessons:state},null,2)],{type:'application/json'});const u=URL.createObjectURL(blob);const a=document.createElement('a');a.href=u;a.download='game-engineering-package-05-progress.json';a.click();setTimeout(()=>URL.revokeObjectURL(u),1000);});
const file=document.querySelector('#import-file');document.querySelector('#import').addEventListener('click',()=>file.click());
file.addEventListener('change',async()=>{try{const f=file.files[0];if(!f)return;if(f.size>65536)throw Error('Progress file exceeds 64 KiB.');const x=JSON.parse(await f.text());if(x.schema!==1||x.package!==5)throw Error('This is not Package 05 progress.');const next=validate(x.lessons);state=next;update();save();note.textContent='Progress imported. Export a backup after further work.';}catch(e){note.textContent='Import rejected: '+e.message;}finally{file.value='';}});
document.querySelectorAll('aside nav a').forEach(a=>a.addEventListener('click',()=>{search.value='';filter();}));
