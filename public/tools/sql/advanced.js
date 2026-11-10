/* SQL Visual Laboratory educational enhancements; no dynamic SQL execution. */
(function(root,factory){const api=factory();if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.SQLAdvanced=api;})(typeof globalThis!=='undefined'?globalThis:this,function(){'use strict';
 const base=(typeof module!=='undefined'&&module.exports)?require('./engine.js'):globalThis.SQLLab;
 const csvCols={orders:['order_id','customer_id','amount'],payments:['payment_id','order_id','channel']};
 function parseCSV(src,kind){
  if(!csvCols[kind])throw Error('Tabella CSV sconosciuta');if(typeof src!=='string'||src.length>25000)throw Error('CSV vuoto o troppo grande (limite 25 KB).');
  src=src.replace(/^\uFEFF/,'');const records=[];let row=[],field='',quoted=false,wasQuote=false;
  for(let i=0;i<src.length;i++){let c=src[i];if(quoted){if(c==='"'){if(src[i+1]==='"'){field+='"';i++;}else{quoted=false;wasQuote=true;}}else field+=c;continue;}
   if(c==='"'&&field===''){quoted=true;continue;}
   if(c==='"')throw Error('Virgolette CSV malformate');
   if(c===','||c==='\n'||c==='\r'){
    row.push(field);field='';wasQuote=false;
    if(c!==','){if(row.some(x=>x!==''))records.push(row);row=[];if(c==='\r'&&src[i+1]==='\n')i++;}continue;
   }
   if(wasQuote&&c!==' '&&c!=='\t')throw Error('Carattere dopo virgolette CSV');
   field+=c;
  }
  if(quoted)throw Error('Virgolette CSV non chiuse');row.push(field);if(row.some(x=>x!==''))records.push(row);
  if(!records.length)throw Error('CSV senza intestazione');
  const headers=records.shift().map(x=>x.trim().toLowerCase());const expected=csvCols[kind];
  if(headers.length!==expected.length||new Set(headers).size!==headers.length||expected.some(x=>!headers.includes(x)))throw Error('Intestazione richiesta: '+expected.join(', '));
  if(records.length>40)throw Error('Massimo 40 righe per tabella');
  const result=records.map((r,i)=>{if(r.length!==headers.length)throw Error('Numero colonne errato alla riga '+(i+2));const out={};expected.forEach(key=>out[key]=r[headers.indexOf(key)]);return out;});
  // validate numeric columns and normalize immediately so wrong data cannot silently replace UI
  base.cleanRows(kind==='orders'?result:[],kind==='payments'?result:[]);
  return result;
 }
 function csvCell(value){const s=value==null?'':String(value);return /[",\r\n]/.test(s)?'"'+s.replace(/"/g,'""')+'"':s;}
 function toCSV(rows,columns){return [columns.join(','),...rows.map(row=>columns.map(col=>csvCell(row[col])).join(','))].join('\r\n')+'\r\n';}
 function deduplicatedPayments(payments){const seen=new Set(),out=[];for(const p of payments){if(p.order_id===null)continue;if(!seen.has(p.order_id)){seen.add(p.order_id);out.push({...p,payment_id:'('+payments.filter(x=>x.order_id===p.order_id).length+' pagamenti)',channel:null});}}return out;}
 function strategies(rawOrders,rawPayments,kind='LEFT'){
  const {orders,payments}=base.cleanRows(rawOrders,rawPayments);const normal=base.analyze(orders,payments,kind);
  const grouped=base.analyze(orders,deduplicatedPayments(payments),kind);
  const filtered=orders.filter(o=>o.order_id!==null&&payments.some(p=>p.order_id!==null&&p.order_id===o.order_id));
  const exists=base.agg(filtered);
  const matchedSourceRows=filtered.length;
  return {normal,grouped,exists,source:base.agg(orders),matchedSourceRows,notes:{grouped:'GROUP BY riduce payments a una riga per chiave; non deduplica eventuali order_id già duplicati in orders.',exists:'EXISTS tiene solo gli ordini con almeno un pagamento, senza moltiplicarli: non preserva quelli senza match.'}};
 }
 function groupedSQL(kind='LEFT'){
  return `WITH payment_counts AS (\n  SELECT order_id, COUNT(*) AS payment_count\n  FROM payments\n  WHERE order_id IS NOT NULL\n  GROUP BY order_id\n)\nSELECT o.order_id, o.customer_id, o.amount, p.payment_count\nFROM orders AS o\n${kind} JOIN payment_counts AS p\n  ON o.order_id = p.order_id;`;
 }
 function existsSQL(){return 'SELECT o.order_id, o.customer_id, o.amount\nFROM orders AS o\nWHERE EXISTS (\n  SELECT 1 FROM payments AS p\n  WHERE p.order_id = o.order_id\n);';}
 return {parseCSV,toCSV,strategies,groupedSQL,existsSQL,csvCols};
});
