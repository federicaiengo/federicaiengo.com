/* SQL Visual Laboratory v0.1 — join semantics demonstrator.
 * No network, no arbitrary SQL execution; CommonJS/browser exports.
 */
(function(root, factory) {
  const api = factory();
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.SQLLab = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function() {
  'use strict';
  const presets = Object.freeze({
    duplication: {
      label: 'Duplicazione dopo JOIN',
      orders: [
        {order_id:'O-101',customer_id:'C-1',amount:100},
        {order_id:'O-102',customer_id:'C-2',amount:50},
        {order_id:'O-103',customer_id:'C-3',amount:75}
      ],
      payments: [
        {payment_id:'P-1',order_id:'O-101',channel:'Carta'},
        {payment_id:'P-2',order_id:'O-101',channel:'Contanti'},
        {payment_id:'P-3',order_id:'O-102',channel:'Carta'}
      ]
    },
    unmatched: {
      label:'Ordini senza pagamenti',
      orders:[
        {order_id:'O-201',customer_id:'C-4',amount:20},
        {order_id:'O-202',customer_id:'C-5',amount:40},
        {order_id:'O-203',customer_id:'C-6',amount:60}
      ],
      payments:[{payment_id:'P-4',order_id:'O-201',channel:'Carta'}]
    },
    nulls: {
      label:'NULL e aggregazioni',
      orders:[
        {order_id:'O-301',customer_id:'C-7',amount:null},
        {order_id:'O-302',customer_id:'C-8',amount:0},
        {order_id:null,customer_id:'C-9',amount:15}
      ],
      payments:[
        {payment_id:'P-5',order_id:'O-302',channel:'Carta'},
        {payment_id:'P-6',order_id:null,channel:'Bonifico'}
      ]
    }
  });
  const own = (o,k) => Object.prototype.hasOwnProperty.call(o,k);
  function normalKey(value) {
    if (value === null || value === undefined || String(value).trim() === '') return null;
    return String(value).trim();
  }
  function normalAmount(value) {
    if (value === null || value === undefined || String(value).trim() === '') return null;
    const n = Number(value);
    if (!Number.isFinite(n)) throw new Error('Importo non valido: ' + String(value));
    if (Math.abs(n) > 1e12) throw new Error('Importo troppo grande (limite: 1.000 miliardi).');
    return n;
  }
  function cleanRows(orders,payments) {
    if (!Array.isArray(orders) || !Array.isArray(payments)) throw new Error('Servono due tabelle.');
    if (orders.length > 40 || payments.length > 40) throw new Error('Massimo 40 righe per tabella.');
    const o=orders.map(r=>({order_id:normalKey(r.order_id),customer_id:normalKey(r.customer_id),amount:normalAmount(r.amount)}));
    const p=payments.map(r=>({payment_id:normalKey(r.payment_id),order_id:normalKey(r.order_id),channel:normalKey(r.channel)}));
    return {orders:o,payments:p};
  }
  function join(orders,payments,kind='LEFT') {
    if (kind !== 'LEFT' && kind !== 'INNER') throw new Error('JOIN non supportata.');
    const out=[];
    for(let i=0;i<orders.length;i++) {
      const o=orders[i]; let matched=false;
      for(let j=0;j<payments.length;j++) {
        const p=payments[j];
        // ANSI SQL: NULL = NULL is UNKNOWN, never a match in ON a=b.
        if(o.order_id!==null && p.order_id!==null && o.order_id===p.order_id) {
          out.push({order_index:i, payment_index:j, order_id:o.order_id, customer_id:o.customer_id,
                    amount:o.amount, payment_id:p.payment_id, channel:p.channel, matched:true}); matched=true;
        }
      }
      if(!matched && kind==='LEFT') out.push({order_index:i,payment_index:null,order_id:o.order_id,
        customer_id:o.customer_id,amount:o.amount,payment_id:null,channel:null,matched:false});
    }
    return out;
  }
  function agg(rows) {
    const values=rows.map(r=>r.amount).filter(v=>v!==null);
    const sum=values.reduce((a,b)=>a+b,0);
    const nonNullIds=rows.map(r=>r.order_id).filter(x=>x!==null);
    return { countStar:rows.length,
      countOrderId: nonNullIds.length,
      countDistinctOrderId:new Set(nonNullIds).size,
      countAmount:values.length,
      sumAmount:values.length?sum:null,
      avgAmount:values.length ? sum/values.length : null
    };
  }
  function analyze(rawOrders,rawPayments,kind='LEFT') {
    const {orders,payments}=cleanRows(rawOrders,rawPayments);
    const joined=join(orders,payments,kind);
    const before=agg(orders), after=agg(joined);
    const multipliers=orders.map((o,i)=>({order_index:i,order_id:o.order_id,
      count:joined.filter(r=>r.order_index===i).length,
      matches:payments.filter(p=>o.order_id!==null && o.order_id===p.order_id).length}));
    const duplicateOrders=multipliers.filter(x=>x.count>1);
    const unmatchedOrders=multipliers.filter(x=>x.matches===0);
    return {orders,payments,joined,before,after,multipliers,duplicateOrders,unmatchedOrders,kind,
      // Count of rows with non-null amount may differ from count of rows.
      inflatedSum:after.sumAmount!==null && before.sumAmount!==null && after.sumAmount>before.sumAmount && kind==='LEFT',
      changedSum:after.sumAmount!==before.sumAmount && (after.sumAmount===null || before.sumAmount===null || Math.abs(after.sumAmount-before.sumAmount)>1e-8)};
  }
  function exampleSQL(kind='LEFT') {
    return `SELECT\n  o.order_id, o.customer_id, o.amount,\n  p.payment_id, p.channel\nFROM orders AS o\n${kind} JOIN payments AS p\n  ON o.order_id = p.order_id;`;
  }
  function metricSQL(kind='LEFT') {
    return `SELECT\n  COUNT(*) AS count_rows,\n  COUNT(o.order_id) AS count_id,\n  COUNT(DISTINCT o.order_id) AS unique_orders,\n  COUNT(o.amount) AS count_amount,\n  SUM(o.amount) AS total_amount,\n  AVG(o.amount) AS avg_amount\nFROM orders AS o\n${kind} JOIN payments AS p\n  ON o.order_id = p.order_id;`;
  }
  return {presets,normalKey,normalAmount,cleanRows,join,agg,analyze,exampleSQL,metricSQL};
});
