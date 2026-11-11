/* v0.6 – static-site browser SQLite worker, with bounded execution. */
(function(){'use strict';
const $=id=>document.getElementById(id),core=globalThis.SQLLabEditorCore;
if(!core||!$('sqlEditorRun'))return;
function cell(row,value,tag='td'){const x=document.createElement(tag);x.textContent=value===null?'NULL':String(value);row.append(x);}
function inputRows(id,fields){return [...$(id).querySelectorAll('tr')].map(tr=>{const ins=tr.querySelectorAll('input');return Object.fromEntries(fields.map((key,index)=>[key,ins[index]?.value??'']));});}
function read(){return globalThis.SQLLab.cleanRows(inputRows('ordersRows',['order_id','customer_id','amount']),inputRows('paymentsRows',['payment_id','order_id','channel']));}
function render(out){
 const table=$('sqlEditorResult');table.replaceChildren();
 const header=document.createElement('thead'),h=document.createElement('tr');
 for(const name of out.columns)cell(h,name,'th');header.append(h);table.append(header);
 const body=document.createElement('tbody');for(const row of out.rows){const tr=document.createElement('tr');for(const value of row)cell(tr,value);body.append(tr);}table.append(body);
 $('sqlEditorMeta').textContent=out.rows.length+(out.truncated?'+':'')+' righe · SQLite WebAssembly'+(out.truncated?' · max 250 visualizzate':'');
}
function executeWithWorker(data,sql){
 return new Promise((resolve,reject)=>{
  let worker,timeout,settled=false;
  try{worker=new Worker('./sql-editor-worker.js');}catch(err){reject(Error('Web Worker non disponibile: apri il progetto tramite HTTP/HTTPS, non file://.'));return;}
  function done(error,result){if(settled)return;settled=true;clearTimeout(timeout);worker.terminate();error?reject(error):resolve(result);}
  worker.addEventListener('message',event=>{const response=event.data||{};if(response.id!==1)return;if(response.ok)done(null,response.result);else done(Error(response.error||'Errore SQLite.'));});
  worker.addEventListener('error',()=>done(Error('SQLite non disponibile: verifica vendor/sql-wasm.js e vendor/sql-wasm.wasm e apri la pagina tramite HTTP/HTTPS.')));
  timeout=setTimeout(()=>done(Error('Query interrotta dopo 5 secondi per proteggere la pagina.')),5000);
  worker.postMessage({action:'execute',id:1,sql,orders:data.orders,payments:data.payments});
 });
}
$('sqlEditorCode').value=core.examples.join;
$('sqlEditorExample').addEventListener('change',()=>{$('sqlEditorCode').value=core.examples[$('sqlEditorExample').value]||core.examples.join;});
$('sqlEditorReset').addEventListener('click',()=>{$('sqlEditorExample').value='join';$('sqlEditorCode').value=core.examples.join;$('sqlEditorStatus').textContent='Query ripristinata.';});
$('sqlEditorRun').addEventListener('click',async()=>{
 const button=$('sqlEditorRun'),status=$('sqlEditorStatus');button.disabled=true;status.textContent='Esecuzione SQLite nel browser…';
 try{const query=core.validate($('sqlEditorCode').value),data=read();const result=await executeWithWorker(data,query);render(result);status.textContent='Risultato calcolato nel tuo browser, senza inviare dati a un backend.';}
 catch(err){$('sqlEditorMeta').textContent='Nessun risultato';$('sqlEditorResult').replaceChildren();status.textContent='Non eseguita: '+(err.message||'errore inatteso');}
 finally{button.disabled=false;}
});
})();
