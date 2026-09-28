
(() => {
"use strict";
const ids = Array.from(document.querySelectorAll('.lesson')).map(el => el.dataset.id);
const key = 'game-engineering-package03-volume02-v1';
const blank = () => ({study:false,lab:false,transfer:false,core:0,total:0});
let records = Object.fromEntries(ids.map(id => [id,blank()]));
const note = document.getElementById('storage-note');
function validate(obj) {
  if (!obj || obj.schema_version !== 1 || obj.bundle !== 3 || obj.volume !== 2 || !obj.records || typeof obj.records !== 'object' || Array.isArray(obj.records)) throw new Error('This is not a Package 03 / Volume 02 progress file.');
  const keys = Object.keys(obj.records);
  if (keys.length !== ids.length || keys.some(id => !ids.includes(id))) throw new Error('The file must contain the 20 known lesson identifiers.');
  const result = {};
  for (const id of ids) {
    const r = obj.records[id];
    if (!r || Object.keys(r).sort().join(',') !== 'core,lab,study,total,transfer' || ['study','lab','transfer'].some(k => typeof r[k] !== 'boolean') || !Number.isInteger(r.core) || !Number.isInteger(r.total) || r.core<0 || r.core>6 || r.total<0 || r.total>10 || r.total<r.core || r.total>r.core+4) throw new Error('Invalid score or progress record for '+id+'.');
    result[id] = {study:r.study,lab:r.lab,transfer:r.transfer,core:r.core,total:r.total};
  }
  return result;
}
function payload() { return {schema_version:1,bundle:3,volume:2,saved_at:new Date().toISOString(),records}; }
function save() { try {localStorage.setItem(key,JSON.stringify(payload()));note.textContent='Progress saved in this browser. Export a backup regularly.';} catch(e) {note.textContent='Browser storage is unavailable; progress remains in this page until closed. Export a backup.';} }
function passed(r) {return r.study && r.lab && r.transfer && r.core>=5 && r.total>=8;}
function redraw() {
  let count=0;
  for (const id of ids) {
    const el=document.querySelector('.lesson[data-id="'+id+'"]');const r=records[id];
    for(const field of ['study','lab','transfer']) el.querySelector('[data-field="'+field+'"]').checked=r[field];
    for(const field of ['core','total']) el.querySelector('[data-field="'+field+'"]').value=r[field];
    const complete=passed(r);if(complete)count++;
    el.querySelector('.status').textContent=complete?'Self-recorded requirements met':'In progress — study, practical work, transfer and both quiz thresholds are required';
  }
  document.getElementById('progress-summary').textContent=count+' / 20 lessons meet the self-recorded requirements';
}
try {const raw=localStorage.getItem(key);if(raw)records=validate(JSON.parse(raw));note.textContent='Progress is local to this browser; export a backup.';} catch(e) {note.textContent='Saved progress could not be loaded; this page starts with blank records. Import a valid backup to restore.';}
for (const el of document.querySelectorAll('.lesson')) {
  el.querySelector('.progress').addEventListener('change', event => {
    const field=event.target.dataset.field;if(!field)return;
    const r=records[el.dataset.id];
    if(['study','lab','transfer'].includes(field))r[field]=event.target.checked;
    else if(field==='core') {r.core=Math.max(0,Math.min(6,Math.trunc(Number(event.target.value)||0)));r.total=Math.max(r.core,Math.min(r.core+4,r.total));}
    else if(field==='total') {r.total=Math.max(0,Math.min(10,Math.trunc(Number(event.target.value)||0)));r.core=Math.min(r.total,Math.max(r.total-4,r.core));}
    redraw();save();
  });
}
const search=document.getElementById('search');
function filter() {
  const q=search.value.trim().toLowerCase();let n=0;
  document.body.classList.toggle('searching',Boolean(q));
  for (const el of document.querySelectorAll('.lesson')) {const match=!q||el.dataset.search.includes(q);el.classList.toggle('matched',match);if(match)n++;}
  for (const el of document.querySelectorAll('.module')) el.classList.toggle('matched',Boolean(el.querySelector('.lesson.matched')));
  document.getElementById('search-status').textContent=q?n+' matching lessons':'All 20 lessons shown';
}
search.addEventListener('input',filter);
document.getElementById('clear-search').addEventListener('click',()=>{search.value='';filter();search.focus();});
document.getElementById('export').addEventListener('click',()=>{
  const url=URL.createObjectURL(new Blob([JSON.stringify(payload(),null,2)],{type:'application/json'}));
  const a=document.createElement('a');a.href=url;a.download='package03-progress.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),5000);
});
const input=document.getElementById('import-file');
document.getElementById('import').addEventListener('click',()=>input.click());
input.addEventListener('change', async()=>{
 const file=input.files[0];if(!file)return;
 try {if(file.size>200000)throw new Error('Progress file is too large.');const candidate=validate(JSON.parse(await file.text()));records=candidate;redraw();save();document.getElementById('import-status').textContent='Imported 20 validated lesson records.';}
 catch(e){document.getElementById('import-status').textContent='Import rejected: '+e.message+' Existing progress was not changed.';}
 finally{input.value='';}
});
redraw();filter();
})();
