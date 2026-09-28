
(function(){
'use strict';
const key='game-engine-v09-progress-v1';
const ids=JSON.parse(document.getElementById('lesson-ids').textContent);
const boxes=Array.from(document.querySelectorAll('input[data-lesson]'));
let completed=new Set();let storage=true;
const status=document.getElementById('status');
function valid(payload){
 if(!payload||payload.package!==10||payload.volume!==9||payload.schema!==1||!Array.isArray(payload.completed)||payload.completed.some(x=>typeof x!=='string'||!ids.includes(x)))throw new Error('Not a compatible Volume 9 progress file.');
 return payload;
}
function payload(){return {schema:1,package:10,volume:9,edition:'2026-09-28',completed:Array.from(completed).sort()};}
function sync(){boxes.forEach(b=>{b.checked=completed.has(b.dataset.lesson);});status.textContent=completed.size+' / '+ids.length+' lessons marked complete by you. Evidence review is separate.';}
try{const raw=localStorage.getItem(key);if(raw){completed=new Set(valid(JSON.parse(raw)).completed);}}catch(e){storage=false;document.getElementById('storage-note').textContent='Local storage is unavailable or contains invalid data. Export progress before closing.';}
function save(){if(storage){try{localStorage.setItem(key,JSON.stringify(payload()));}catch(e){storage=false;document.getElementById('storage-note').textContent='Progress cannot be saved locally. Export it before closing.';}}sync();}
boxes.forEach(b=>b.addEventListener('change',()=>{if(b.checked)completed.add(b.dataset.lesson);else completed.delete(b.dataset.lesson);save();}));
const search=document.getElementById('search');
function filter(){const term=search.value.toLowerCase().trim();let shown=0;document.querySelectorAll('article.lesson').forEach(a=>{const match=!term||a.textContent.toLowerCase().includes(term);a.hidden=!match;if(match)shown++;});document.querySelectorAll('.module-header').forEach(h=>{h.hidden=!!term;});document.getElementById('search-status').textContent=term?shown+' matching lessons. Supplementary guides remain available.':'';}
search.addEventListener('input',filter);
document.getElementById('clear-search').addEventListener('click',()=>{search.value='';filter();search.focus();});
document.querySelectorAll('nav a[href^="#lesson-"]').forEach(a=>a.addEventListener('click',()=>{search.value='';filter();}));
document.getElementById('export').addEventListener('click',()=>{const blob=new Blob([JSON.stringify(payload(),null,2)],{type:'application/json'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download='volume09_progress.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});
document.getElementById('import').addEventListener('click',()=>document.getElementById('import-file').click());
document.getElementById('import-file').addEventListener('change',async event=>{const file=event.target.files[0];if(!file)return;try{if(file.size>1000000)throw new Error('Progress file is too large.');const value=valid(JSON.parse(await file.text()));completed=new Set(value.completed);save();document.getElementById('storage-note').textContent='Imported compatible progress. Export regularly to keep a backup.';}catch(e){document.getElementById('storage-note').textContent='Import failed: '+e.message;}finally{event.target.value='';}});
sync();
})();
