(function(root){
  const units={g:['mass',1],gram:['mass',1],grams:['mass',1],gr:['mass',1],kg:['mass',1000],ml:['volume',1],cl:['volume',10],l:['volume',1000]};
  function quantity(raw){
    const text=String(raw||'').trim();
    if(!text) return {status:'missing',value:null,unit:null,reason:'Quantity missing; no value inferred'};
    if(text.length>80)return {status:'unsupported',value:null,unit:null,reason:'Quantity exceeds bounded input length'};
    const m=text.match(/^([0-9]+(?:[.,][0-9]{1,6})?)\s*(g|gram|grams|gr|kg|ml|cl|l)$/i);
    if(!m)return {status:'unsupported',value:null,unit:null,reason:'Outside single metric mass/volume grammar; check source'};
    const [kind,factor]=units[m[2].toLowerCase()], pieces=m[1].replace(',','.').split('.'), places=(pieces[1]||'').length;
    const integer=BigInt(pieces.join(''))*BigInt(factor), scale=10n**BigInt(places);
    if(integer<=0n||integer>1000000000n*scale)return {status:'unsupported',value:null,unit:null,reason:'Outside positive bounded quantity policy'};
    let value=integer.toString().padStart(places+1,'0');
    if(places)value=value.slice(0,-places)+'.'+value.slice(-places);
    if(value.includes('.'))value=value.replace(/0+$/,'').replace(/\.$/,'');
    value=value.replace(/^0+(?=\d)/,'');
    return {status:kind,value,unit:kind==='mass'?'g':'mL',reason:'Single metric quantity; exact decimal conversion'};
  }
  function audit(row){
    const parsed=quantity(row.quantity),issues=[];
    if(!String(row.product_name||'').trim())issues.push('Product name missing');
    if(!/^[0-9]{8,14}$/.test(String(row.code||'')))issues.push('Code outside 8–14 digit destination policy');
    if(parsed.value===null)issues.push(parsed.reason);
    const canonical=parsed.value===null?null:parsed.value+' '+parsed.unit;
    return {source_row:row.source_row,original:{...row},parsed,canonical,issues,status:issues.length?'review':'ready',changed:canonical!==null&&canonical!==row.quantity};
  }
  const api={quantity,audit};if(typeof module!=='undefined')module.exports=api;else root.Catalog=api;
})(typeof globalThis==='undefined'?this:globalThis);
