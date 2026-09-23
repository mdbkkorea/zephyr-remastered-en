const fs=require('fs'),vm=require('vm'),assert=require('assert'),crypto=require('crypto').webcrypto;
const html=fs.readFileSync('private/Zephyr-Translation-Review.html','utf8');
const scripts=[...html.matchAll(/<script(?: [^>]*)?>([\s\S]*?)<\/script>/g)];
function el(tag=''){return {tag,value:'',textContent:'',children:[],append(n){this.children.push(n)},replaceChildren(){this.children=[]},setAttribute(){}}}
const ids={};for(const id of ['data','query','batch','items','count','prev','next','prevSection','nextSection'])ids[id]=el();ids.data.textContent=scripts[0][1];
const memory=new Map(),main=el('main');let saved={},fail=false,calls=0;
const ctx={document:{getElementById:id=>ids[id],createElement:tag=>el(tag),querySelector:()=>main},URLSearchParams,location:{search:''},window:{scrollTo(){},addEventListener(){}},localStorage:{getItem:k=>memory.get(k),setItem:(k,v)=>memory.set(k,v),removeItem:k=>memory.delete(k)},crypto,Uint8Array,fetch:async(url,opts={})=>{
 if(opts.method!=='POST')return {ok:true,json:async()=>({token:'test-token',saved})};calls++;if(fail)throw Error('offline');
 const data=JSON.parse(opts.body);saved[data.id]={...data,filename:'test.md'};return {ok:true,json:async()=>({record:saved[data.id]})};
}};
vm.createContext(ctx);vm.runInContext(scripts[1][1],ctx);
async function tick(){await new Promise(r=>setImmediate(r))}
function form(){return ids.items.children[0].children.find(x=>x.className==='suggestion-form')}
(async()=>{
 await tick();assert.equal(ids.batch.value,'korean-batch-001');assert(ids.items.children.length>0);
 ids.query.value='R18396';ids.query.oninput();let f=form(),areas=f.children.filter(x=>x.tag==='textarea');
 areas[0].value='New suggestion';areas[0].oninput();areas[1].value='New explanation';areas[1].oninput();
 ids.nextSection.onclick();ids.query.value='R18396';ids.query.oninput();f=form();areas=f.children.filter(x=>x.tag==='textarea');assert.equal(areas[0].value,'New suggestion');assert.equal(areas[1].value,'New explanation');
 await f.children.find(x=>x.tag==='button').onclick();assert.equal(calls,1);assert.equal(memory.size,0);assert(f.children.at(-1).textContent.startsWith('Saved to NAS'));
 ids.query.oninput();f=form();areas=f.children.filter(x=>x.tag==='textarea');assert.equal(areas[0].value,'New suggestion');
 fail=true;areas[0].value='Offline draft';areas[0].oninput();await f.children.find(x=>x.tag==='button').onclick();assert.equal(memory.size,1);assert(f.children.at(-1).textContent.startsWith('Not saved:'));
 ids.query.value='탄검';ids.query.oninput();assert(ids.count.textContent.startsWith('12 matches'));
 ids.query.value='zzzz_unmatched';ids.query.oninput();assert.equal(ids.items.children.length,0);
 console.log('UI passed: search, navigation, draft retention, save confirmation, reload state, offline failure retention.');
})().catch(e=>{console.error(e);process.exit(1)});
