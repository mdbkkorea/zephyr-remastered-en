const draftPrefix='zephyr-review-draft-v1:';
let savedSuggestions={}, saveToken=null;
const draftMemory={};
const serviceStatus=node('p','Connecting to NAS suggestion storage…',document.querySelector('main'));
serviceStatus.setAttribute('role','status');
function draftKey(r){return draftPrefix+r.key}
function readDraft(r){
 if(draftMemory[r.key])return draftMemory[r.key];
 try{const value=JSON.parse(localStorage.getItem(draftKey(r))||'null');if(value)draftMemory[r.key]=value;return value}catch{return null}
}
function keepDraft(r,value){
 draftMemory[r.key]=value;
 try{localStorage.setItem(draftKey(r),JSON.stringify(value));return true}catch{return false}
}
function newRequestID(){const bytes=new Uint8Array(16);crypto.getRandomValues(bytes);return Array.from(bytes,b=>b.toString(16).padStart(2,'0')).join('')}
function addSuggestionForm(r,article){
 const form=node('section','',article);form.className='suggestion-form';
 const existing=savedSuggestions[r.id];const draft=readDraft(r);
 const fields={};
 for(const [name,label] of [['suggestion','Translation suggestion / 번역 제안'],['explanation','Explanation / 설명']]){
  const labelNode=node('label',label,form);labelNode.htmlFor=r.id+'-'+name;
  const area=node('textarea','',form);area.id=labelNode.htmlFor;area.rows=name==='suggestion'?3:2;area.maxLength=20000;
  area.value=draft?draft[name]:(existing&&existing.key===r.key?existing[name]:'');fields[name]=area;
 }
 const button=node('button','Save suggestion',form);button.type='button';
 const status=node('span','',form);status.className='save-status';status.setAttribute('role','status');
 function showState(){
  status.textContent=readDraft(r)?'Draft in this browser — not saved to NAS.':existing?(existing.status==='applied'?'Applied to translation source · included in the next build.':'Saved to NAS · pending your instruction.'):'Not saved yet.';
  if(existing&&existing.key!==r.key)status.textContent='A suggestion exists for an older entry. It remains in NAS history.';
 }
 showState();
 let revision=draft?draft.revision:(existing?existing.request_id:null);
 function changed(){
  const value={suggestion:fields.suggestion.value,explanation:fields.explanation.value,revision,en:r.en,request_id:newRequestID()};
  const persisted=keepDraft(r,value);status.textContent=persisted?'Draft in this browser — click Save suggestion to save to NAS.':'Draft is only in this tab. Click Save before closing it.';
 }
 fields.suggestion.oninput=changed;fields.explanation.oninput=changed;
 button.onclick=async()=>{
  if(!saveToken){status.textContent='NAS saving is unavailable in this tab. Copy your draft, then double-click Launch Review in Safari.command in the NAS review folder and use http://127.0.0.1:8766/. Paste your draft there and save. Keep the launcher Terminal open.';return}
  if(!fields.suggestion.value.trim()&&!fields.explanation.value.trim()){status.textContent='Enter a suggestion or explanation first.';return}
  if(!readDraft(r))changed();
  const snapshot={...readDraft(r)};
  if(snapshot.en!==r.en){status.textContent='The English text changed since this draft. Review it and edit either field before saving.';return}
  button.disabled=true;status.textContent='Saving to NAS…';
  try{
   const response=await fetch('/api/suggestions',{method:'POST',headers:{'Content-Type':'application/json','X-Review-Token':saveToken},body:JSON.stringify({id:r.id,key:r.key,...snapshot})});
   const result=await response.json();if(!response.ok)throw new Error(result.error||'Save failed');
   savedSuggestions[r.id]=result.record;revision=result.record.request_id;
   const current=readDraft(r);
   if(current&&current.request_id===snapshot.request_id){delete draftMemory[r.key];try{localStorage.removeItem(draftKey(r))}catch{};status.textContent='Saved to NAS · '+result.record.filename+' · pending.'}
   else if(current){keepDraft(r,{...current,revision});status.textContent='Previous text saved. Your newer edits are still a draft.'}
  }catch(error){status.textContent='Not saved: '+error.message+' Your draft is kept.'}
  finally{button.disabled=false}
 };
}
const originalRender=render;
render=function(){originalRender();for(const article of items.children){const row=rows.find(r=>r.id===article.id);if(row)addSuggestionForm(row,article)}};
async function loadSuggestions(){
 try{
  const response=await fetch('/api/suggestions',{cache:'no-store'});if(!response.ok)throw new Error('Unavailable');
  const data=await response.json();if(!data.token||!data.saved)throw new Error('Not the review service');
  saveToken=data.token;savedSuggestions=data.saved;
  serviceStatus.textContent='NAS saving ready. Saved suggestions stay pending until you ask for implementation.';
 }catch{serviceStatus.textContent='To save to NAS, double-click Launch Review in Safari.command in the NAS review folder and use http://127.0.0.1:8766/. Copy drafts before switching: drafts in a file tab do not transfer to the website. Keep the launcher Terminal open.'}
 render();
}
window.addEventListener('beforeunload',event=>{if(Object.keys(draftMemory).length){event.preventDefault();event.returnValue=''}});
render();loadSuggestions();
