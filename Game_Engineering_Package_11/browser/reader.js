
(function(){
  "use strict";
  const key="game-engineering-v10-read-20260928";
  const boxes=Array.from(document.querySelectorAll("[data-progress]"));
  let saved={};
  try{saved=JSON.parse(localStorage.getItem(key)||"{}");}catch(error){saved={};}
  if(!saved || typeof saved!=="object" || Array.isArray(saved)) saved={};
  function update(){
    document.getElementById("progress").textContent=boxes.filter(x=>x.checked).length+" / 20 marked read";
  }
  boxes.forEach(box=>{
    box.checked=saved[box.dataset.progress]===true;
    box.addEventListener("change",()=>{
      saved[box.dataset.progress]=box.checked;
      try{localStorage.setItem(key,JSON.stringify(saved));}catch(error){document.getElementById("storage-note").textContent="Local storage unavailable; use templates/PROGRESS.md.";}
      update();
    });
  });
  update();
  document.getElementById("search").addEventListener("input",event=>{
    const term=event.target.value.trim().toLowerCase();
    let shown=0;
    document.querySelectorAll("article[data-lesson]").forEach(article=>{
      const visible=!term||article.textContent.toLowerCase().includes(term);
      article.classList.toggle("hidden",!visible);
      document.querySelector('[data-nav="'+article.id+'"]').classList.toggle("hidden",!visible);
      if(visible)shown++;
    });
    document.getElementById("results").textContent=shown+" lessons shown";
  });
  document.getElementById("clear-search").addEventListener("click",()=>{
    const search=document.getElementById("search");search.value="";search.dispatchEvent(new Event("input"));
  });
})();
