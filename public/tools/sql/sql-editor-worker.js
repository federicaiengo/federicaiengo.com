/* SQL Visual Laboratory v0.6 – Worker for local sql.js 1.13.0. */
'use strict';
importScripts('./sql-editor-core.js');
let initPromise;
function init(){
  if(!initPromise){
    initPromise=Promise.resolve().then(()=>{
      importScripts('./vendor/sql-wasm.js');
      if(typeof self.initSqlJs!=='function')throw Error('sql-wasm.js non valido.');
      return self.initSqlJs({locateFile: name=>'./vendor/'+name});
    });
  }
  return initPromise;
}
self.addEventListener('message',async e=>{
  const request=e.data||{};
  if(request.action!=='execute')return;
  try{
    const SQL=await init();
    const result=self.SQLLabEditorCore.sqliteRun(SQL,{orders:request.orders,payments:request.payments},request.sql);
    self.postMessage({id:request.id,ok:true,result});
  }catch(err){
    self.postMessage({id:request.id,ok:false,error:err instanceof Error?err.message:'Errore SQL non specificato.'});
  }
});
