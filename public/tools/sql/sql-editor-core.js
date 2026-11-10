/* SQL Visual Laboratory v0.4 — editor helpers. Execution delegated to real sql.js SQLite. */
(function(root,factory){const api=factory();if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.SQLLabEditorCore=api;})(typeof globalThis!=='undefined'?globalThis:this,function(){
'use strict';
const DEFAULT=`SELECT o.order_id, o.customer_id, o.amount,\n       p.payment_id, p.channel\nFROM orders AS o\nLEFT JOIN payments AS p ON p.order_id = o.order_id\nORDER BY o.order_id, p.payment_id;`;
const examples={join:DEFAULT,summary:`SELECT customer_id, COUNT(*) AS total_orders,\n       SUM(amount) AS total_amount\nFROM orders\nGROUP BY customer_id\nORDER BY total_amount DESC;`,missing:`SELECT o.order_id, o.amount\nFROM orders AS o\nWHERE NOT EXISTS (SELECT 1 FROM payments AS p\n                  WHERE p.order_id = o.order_id);`,fanout:`SELECT o.order_id, COUNT(p.payment_id) AS payments_found,\n       SUM(o.amount) AS potentially_inflated_amount\nFROM orders AS o\nLEFT JOIN payments AS p ON p.order_id = o.order_id\nGROUP BY o.order_id;`};
function validate(sql){
 if(typeof sql!=='string'||!sql.trim())throw Error('Inserisci una query SQL.');
 if(sql.length>5000)throw Error('Query troppo lunga (massimo 5000 caratteri).');
 const t=sql.trim().replace(/;\s*$/,'');
 if(t.includes(';'))throw Error('Una sola istruzione SQL alla volta.');
 if(!/^SELECT\b/i.test(t)&&!/^WITH\b/i.test(t))throw Error('In questo laboratorio sono ammesse solo query SELECT o WITH di lettura.');
 if(/\b(RECURSIVE|ATTACH|DETACH|PRAGMA|VACUUM|CREATE|ALTER|DROP|DELETE|UPDATE|INSERT|REPLACE|ANALYZE|REINDEX|BEGIN|COMMIT|ROLLBACK|LOAD_EXTENSION)\b/i.test(t))throw Error('Comando non disponibile in questa modalità didattica.');
 return t;
}
function prepareRows(orders,payments){if(!Array.isArray(orders)||!Array.isArray(payments))throw Error('Tabelle mancanti.');if(orders.length>40||payments.length>40)throw Error('Massimo 40 righe per tabella.');return {orders,payments};}
function sqliteRun(SQL,input,sql){
 const query=validate(sql),data=prepareRows(input.orders,input.payments);const db=new SQL.Database();
 try{
  db.run('CREATE TABLE orders (order_id TEXT, customer_id TEXT, amount REAL);CREATE TABLE payments (payment_id TEXT, order_id TEXT, channel TEXT);');
  let statement=db.prepare('INSERT INTO orders (order_id,customer_id,amount) VALUES (?,?,?)');
  try{for(const x of data.orders)statement.run([x.order_id,x.customer_id,x.amount]);}finally{statement.free();}
  statement=db.prepare('INSERT INTO payments (payment_id,order_id,channel) VALUES (?,?,?)');
  try{for(const x of data.payments)statement.run([x.payment_id,x.order_id,x.channel]);}finally{statement.free();}
  // Cursor-based reading limits output to avoid huge DOM tables; DB is recreated for every query.
  statement=db.prepare(query);
  try{
   if(statement.getColumnNames().length===0)throw Error('Serve una SELECT che produca colonne.');
   const columns=statement.getColumnNames(),rows=[];let more=false;
   while(statement.step()){if(rows.length>=250){more=true;break;}rows.push(statement.get());}
   return {columns,rows,truncated:more,sql:query};
  }finally{statement.free();}
 }finally{db.close();}
}
return {validate,examples,sqliteRun,prepareRows};
});
