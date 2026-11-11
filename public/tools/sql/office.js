/* SQL Visual Laboratory v0.3 — Office tasks and guided SQL: browser-only,
 * no eval, no network and no arbitrary SQL engine. */
(function(root,factory){const api=factory();if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.SQLOffice=api;})(typeof globalThis!=='undefined'?globalThis:this,function(){'use strict';
const base=(typeof module!=='undefined'&&module.exports)?require('./engine.js'):globalThis.SQLLab;
const choices=Object.freeze({
 summary:{label:'Riepilogo per cliente',description:'Somma e conta gli ordini per cliente, senza moltiplicare le righe con payments.'},
 missing:{label:'Ordini senza pagamenti',description:'Trova ordini senza alcun pagamento corrispondente (NOT EXISTS).'},
 duplicates:{label:'Codici ordine ripetuti',description:'Individua gli order_id presenti in più righe; NULL esclusi come in WHERE order_id IS NOT NULL.'},
 filter:{label:'Filtra gli ordini per importo',description:'Mostra gli ordini sopra una soglia; NULL esclusi dal confronto.'},
 paymentcount:{label:'Conteggio pagamenti per ordine',description:'LEFT JOIN sui pagamenti preaggregati, per evitare la moltiplicazione degli ordini.'}
});
const fmtId=id=>id===null?'(senza cliente)':id;
const numeric=n=>n===null?'NULL':String(n);
function compute(task,rawO,rawP,opts={}){
 if(!Object.prototype.hasOwnProperty.call(choices,task))throw Error('Operazione non supportata.');
 const {orders,payments}=base.cleanRows(rawO,rawP);
 let columns=[],rows=[],sql='',explanation='';
 if(task==='summary'){
  columns=['customer_id','numero_ordini','totale_importi','media_importi'];
  const buckets=new Map();for(const o of orders){let k=o.customer_id; if(!buckets.has(k))buckets.set(k,{customer_id:k,numero_ordini:0,totale_importi:0,media_importi:null,n:0});const t=buckets.get(k);t.numero_ordini++;if(o.amount!==null){t.totale_importi+=o.amount;t.n++;}}
  rows=[...buckets.values()].map(t=>({customer_id:t.customer_id,numero_ordini:t.numero_ordini,totale_importi:t.n?t.totale_importi:null,media_importi:t.n?t.totale_importi/t.n:null}));
  rows.sort((a,b)=>a.customer_id===null?-1:b.customer_id===null?1:a.customer_id.localeCompare(b.customer_id));
  sql='SELECT customer_id, COUNT(*) AS numero_ordini, SUM(amount) AS totale_importi, AVG(amount) AS media_importi\nFROM orders\nGROUP BY customer_id\nORDER BY customer_id;';
  explanation='Ogni ordine è contato una volta perché non uniamo payments. I valori NULL sono ignorati da SUM e AVG; un cliente senza importi validi ha totale NULL.';
 }else if(task==='missing'){
  columns=['order_id','customer_id','amount'];rows=orders.filter(o=>!payments.some(p=>o.order_id!==null&&p.order_id!==null&&o.order_id===p.order_id)).map(o=>({...o}));
  sql='SELECT o.order_id, o.customer_id, o.amount\nFROM orders AS o\nWHERE NOT EXISTS (\n  SELECT 1 FROM payments AS p\n  WHERE p.order_id = o.order_id\n);';
  explanation='NOT EXISTS non moltiplica gli ordini; anche gli ordini con ID NULL sono senza corrispondenza, come prevede SQL.';
 }else if(task==='duplicates'){
  columns=['order_id','ripetizioni'];const counts=new Map();for(const o of orders){if(o.order_id!==null)counts.set(o.order_id,(counts.get(o.order_id)||0)+1)}rows=[...counts].filter(([,n])=>n>1).map(([order_id,ripetizioni])=>({order_id,ripetizioni})).sort((a,b)=>a.order_id.localeCompare(b.order_id));
  sql='SELECT order_id, COUNT(*) AS ripetizioni\nFROM orders\nWHERE order_id IS NOT NULL\nGROUP BY order_id\nHAVING COUNT(*) > 1\nORDER BY order_id;';
  explanation='Il controllo rileva codici ripetuti nella tabella orders. Non rileva direttamente duplicazioni create da una JOIN.';
 }else if(task==='filter'){
  const min=opts.minimum===undefined?50:base.normalAmount(opts.minimum);if(min===null)throw Error('Inserisci una soglia numerica.');columns=['order_id','customer_id','amount'];rows=orders.filter(o=>o.amount!==null&&o.amount>=min).map(o=>({...o})).sort((a,b)=>b.amount-a.amount);
  sql='SELECT order_id, customer_id, amount\nFROM orders\nWHERE amount >= '+numeric(min)+'\nORDER BY amount DESC;';
  explanation='Sono inclusi gli ordini con importo maggiore o uguale alla soglia. I NULL non superano il filtro.';
 }else if(task==='paymentcount'){
  columns=['order_id','customer_id','amount','numero_pagamenti'];const counts=new Map();for(const p of payments){if(p.order_id!==null)counts.set(p.order_id,(counts.get(p.order_id)||0)+1)}rows=orders.map(o=>({...o,numero_pagamenti:o.order_id!==null?(counts.get(o.order_id)||0):0}));
  sql='WITH payment_counts AS (\n  SELECT order_id, COUNT(*) AS numero_pagamenti\n  FROM payments\n  WHERE order_id IS NOT NULL\n  GROUP BY order_id\n)\nSELECT o.order_id, o.customer_id, o.amount,\n       COALESCE(p.numero_pagamenti, 0) AS numero_pagamenti\nFROM orders AS o\nLEFT JOIN payment_counts AS p\n  ON p.order_id = o.order_id;';
  explanation='I pagamenti sono conteggiati prima della LEFT JOIN: ogni riga originaria orders resta una riga. Eventuali duplicati già presenti in orders rimangono.';
 }
 return {task,columns,rows,sql,explanation,count:rows.length};
}
function quoteCSV(x){const s=x===null||x===undefined?'':String(x);return /[",\n\r]/.test(s)?'"'+s.replace(/"/g,'""')+'"':s}
function exportCSV(output){if(!output||!Array.isArray(output.columns)||!Array.isArray(output.rows))throw Error('Risultato CSV mancante');return [output.columns.join(','),...output.rows.map(row=>output.columns.map(c=>quoteCSV(row[c])).join(','))].join('\r\n')+'\r\n'}
return {choices,compute,exportCSV};
});
