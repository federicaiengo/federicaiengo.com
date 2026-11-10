(function(){'use strict';
const $=id=>document.getElementById(id),office=globalThis.SQLOffice; if(!office)return;
let last=null;
function elt(t,value){const e=document.createElement(t);if(value!==undefined)e.textContent=value;return e}
function source(){function rows(id,fields){return [...$(id).querySelectorAll('tr')].map(tr=>{const inputs=[...tr.querySelectorAll('input')],obj={};fields.forEach((f,i)=>obj[f]=inputs[i]?.value??'');return obj})}
 return {orders:rows('ordersRows',['order_id','customer_id','amount']),payments:rows('paymentsRows',['payment_id','order_id','channel'])};}
function show(){const choice=$('officeTask').value;const info=office.choices[choice];$('officeDescription').textContent=info.description;$('officeThreshold').hidden=choice!=='filter';
 try{const s=source(),opts={minimum:$('officeMin').value};last=office.compute(choice,s.orders,s.payments,opts);$('officeError').textContent='';$('officeSQL').textContent=last.sql;$('officeExplanation').textContent=last.explanation;$('officeCount').textContent=last.count+' righe';
 const table=$('officeTable');table.replaceChildren();const thead=elt('thead'),hrow=elt('tr');last.columns.forEach(x=>hrow.append(elt('th',x)));thead.append(hrow);table.append(thead);const tbody=elt('tbody');last.rows.forEach(r=>{const tr=elt('tr');last.columns.forEach(c=>tr.append(elt('td',r[c]===null?'NULL':String(r[c]))));tbody.append(tr)});if(!last.rows.length){const tr=elt('tr'),td=elt('td','Nessun risultato per questa operazione.');td.colSpan=last.columns.length;tr.append(td);tbody.append(tr)}table.append(tbody);
 $('officeDownload').disabled=false;
 }catch(e){last=null;$('officeError').textContent='Operazione non eseguita: '+e.message;$('officeCount').textContent='Dati non validi';$('officeTable').replaceChildren();$('officeSQL').textContent='';$('officeExplanation').textContent='';$('officeDownload').disabled=true;}
}
$('officeTask').addEventListener('change',show);$('officeMin').addEventListener('input',show);$('officeRun').addEventListener('click',show);
$('officeDownload').addEventListener('click',()=>{if(!last)return;const csv=office.exportCSV(last),url=URL.createObjectURL(new Blob([csv],{type:'text/csv;charset=utf-8'})),a=elt('a');a.href=url;a.download='sql-visual-lab-'+last.task+'.csv';document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000)});
$('officeCopy').addEventListener('click',async()=>{if(!last)return;try{await navigator.clipboard.writeText(last.sql);$('officeAction').textContent='SQL copiato.'}catch(e){$('officeAction').textContent='Seleziona il codice SQL per copiarlo manualmente.'}});
let queued=false;function schedule(){if(queued)return;queued=true;queueMicrotask(()=>{queued=false;show()})}
for(const id of ['ordersRows','paymentsRows']){const el=$(id);el.addEventListener('input',schedule);new MutationObserver(schedule).observe(el,{childList:true,subtree:true})}
$('scenario').addEventListener('change',schedule);show();
})();
