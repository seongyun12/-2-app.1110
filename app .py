"""내 재산의 숨은 능력 | 재산 유동성 + 구매 시뮬레이터
배포: GitHub 루트에 app.py와 requirements.txt 업로드 → Streamlit Community
Cloud에서 app.py 지정 → 배포된 https 주소로 QR코드 생성.
실행: pip install -r requirements.txt && streamlit run app.py

모든 금액은 만원. 현금=즉시 인출 가능 예금/현금, 투자=현재 평가액,
묶인 자산=부동산·보증금 등의 현재 추정가치. 중복 계산하지 않습니다.
부채는 잔액을 따로 입력하며 순자산에서 한 번만 차감합니다.
재산 입력·계산·저장은 iframe 안 브라우저에서만 수행합니다.
구매는 현금 일시불 가정. 월 필수비에 정기 대출상환액을 포함하세요.
세금·처분비용·수익률·미래수입·일시 만기도래 부채는 계산하지 않습니다.
비상자금 개월 수는 사용자가 정한 비교 기준이며 안전을 보장하지 않습니다.
"""
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="내 재산의 숨은 능력", page_icon="💎", layout="centered", initial_sidebar_state="collapsed")
st.markdown('''<style>
[data-testid="stHeader"],[data-testid="stToolbar"],footer{display:none!important}
[data-testid="stAppViewContainer"]{background:#eff3f8}
.block-container,[data-testid="stMainBlockContainer"]{padding:0!important;max-width:480px!important}
[data-testid="stVerticalBlock"]{gap:0!important}
iframe{width:100%;height:calc(100svh - 4px)!important;border:0;display:block}
</style>''', unsafe_allow_html=True)

PAGE = r'''<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<style>
*{box-sizing:border-box}html,body{height:100%;margin:0;background:#eff3f8;color:#192a43;font-family:system-ui,-apple-system,'Apple SD Gothic Neo','Nanum Gothic',sans-serif}body{padding:9px 11px}main{height:100%;max-width:456px;margin:auto;display:flex;flex-direction:column;gap:7px}
header{display:flex;align-items:center;justify-content:space-between;flex-shrink:0}h1{font-size:21px;letter-spacing:-1px;margin:0}header p{font-size:11px;color:#52657b;margin:3px 0 0}.gem{background:#192a43;padding:9px;border-radius:13px;font-size:21px}.card{background:#fff;border:1px solid #dee6ef;border-radius:15px;padding:10px;flex-shrink:0}.row{display:flex;align-items:center;justify-content:space-between;gap:5px}.title{font-size:12px;font-weight:750}.muted{font-size:10px;color:#52657b}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:7px;margin-top:7px}label{font-size:10px;color:#425875;display:block}input{width:100%;min-width:0;margin-top:3px;border:1px solid #d4deea;border-radius:8px;background:#f8fafc;color:#192a43;padding:7px 6px;font-size:14px;font-weight:600}input:focus,select:focus,button:focus-visible{outline:2px solid #047857;outline-offset:1px}select{font-size:11px;border:1px solid #d4deea;border-radius:7px;padding:4px;background:white;color:#192a43}
.kpis{display:grid;grid-template-columns:1fr 1fr;gap:7px;margin-top:8px}.kpi{border-radius:11px;background:#f0f4f9;padding:8px;min-width:0}.kpi.accent{background:#e5f5ef}.kpi small{font-size:10px;color:#52657b}.kpi b{display:block;font-size:20px;letter-spacing:-.7px;margin-top:3px;overflow-wrap:anywhere}.accent b{color:#046c4e}.desc{font-size:11px;line-height:1.5;color:#425875;margin:7px 0 0}.mix{display:grid;grid-template-columns:repeat(3,1fr);gap:4px;margin-top:7px}.mix div{font-size:10px;padding:6px 3px;border-radius:7px;text-align:center;background:#f2f5fa}.mix b{display:block;font-size:12px;margin-top:2px}.mix div:first-child{background:#e5f5ef}
.purchase{display:grid;grid-template-columns:1fr 1fr;gap:8px;align-items:end;margin-top:6px}.badge{font-size:10px;font-weight:750;border-radius:20px;padding:4px 7px;background:#edf1f7;color:#425875}.result{font-size:12px;line-height:1.5;margin:7px 0 0;min-height:36px}.actions{display:flex;gap:7px}button{font:inherit;font-size:11px;padding:8px;border:1px solid #cdd8e5;border-radius:9px;background:white;color:#334c69;cursor:pointer;flex:1}button:first-child{background:#192a43;color:white;border-color:#192a43}#notice{font-size:9px;text-align:center;color:#52657b;min-height:12px}footer{margin-top:auto;font-size:9px;line-height:1.45;color:#52657b;text-align:center;padding-bottom:2px}
@media(max-height:690px){body{padding:6px 9px}main{gap:5px}.card{padding:8px}input{padding:5px 6px}.kpi b{font-size:18px}.kpis{margin-top:6px}.mix div{padding:4px}.desc{margin-top:5px}.result{margin-top:5px}h1{font-size:19px}.gem{padding:7px}button{padding:6px}}
@media(max-height:570px){header p{display:none}.card{padding:6px}main{gap:4px}.grid{margin-top:4px;gap:5px}.kpi{padding:5px}.kpi b{font-size:16px}.desc{font-size:10px}.mix{margin-top:4px}.result{font-size:11px;min-height:0}footer{margin-top:0}.gem{padding:4px}.purchase{margin-top:4px}}
</style></head><body><main>
<header><div><h1>내 재산의 숨은 능력</h1><p>얼마 있는지보다, 지금 무엇을 할 수 있는지.</p></div><div class="gem" aria-hidden="true">💎</div></header>
<section class="card"><div class="row"><span class="title">01 · 내 재산 입력</span><span class="muted">모든 금액: 만원</span></div>
<div class="grid">
<label title="즉시 인출 가능한 현금·예금만 입력">바로 쓸 돈 ⓘ<input id="cash" type="number" min="0" max="99999999" step="any" inputmode="decimal" placeholder="현금·예금"></label>
<label title="주식·펀드 등 현재 평가액. 현금 항목과 중복 제외">투자자산 ⓘ<input id="invest" type="number" min="0" max="99999999" step="any" inputmode="decimal" placeholder="주식·펀드"></label>
<label title="부동산·보증금 등 현재 추정가치. 부채 차감 전, 중복 제외">묶인 자산 ⓘ<input id="locked" type="number" min="0" max="99999999" step="any" inputmode="decimal" placeholder="집·보증금"></label>
<label title="대출 등 현재 상환해야 할 잔액 전체">부채 잔액 ⓘ<input id="debt" type="number" min="0" max="99999999" step="any" inputmode="decimal" placeholder="대출 등"></label>
<label title="매달 꼭 필요한 생활비와 정기 대출상환액의 합계">월 필수비 ⓘ<input id="monthly" type="number" min="0" max="99999999" step="any" inputmode="decimal" placeholder="상환액 포함"></label>
<label for="months">비상자금 기준<select id="months"><option value="3">필수비 3개월</option><option value="6" selected>필수비 6개월</option><option value="12">필수비 12개월</option></select></label>
</div></section>
<section class="card" aria-live="polite"><div class="row"><span class="title">02 · 부자인데, 쓸 돈은?</span><span id="liquidBadge" class="badge">입력 대기</span></div>
<div class="kpis"><div class="kpi"><small>순자산 · 자산 − 부채</small><b id="net">—</b></div><div class="kpi accent"><small>총자산 중 바로 쓸 돈</small><b id="ratio">—</b></div></div>
<div class="mix"><div>바로 쓸 돈<b id="cashShare">—</b></div><div>가격이 변하는 돈<b id="investShare">—</b></div><div>묶인 돈<b id="lockedShare">—</b></div></div>
<p id="liquidTip" class="desc">재산을 중복 없이 입력해 주세요. 비율은 부채 차감 전 총자산 기준입니다.</p></section>
<section class="card" aria-live="polite"><div class="row"><span class="title">03 · 이거 사도 괜찮을까?</span><span class="badge" id="buyBadge">가격 입력</span></div>
<div class="purchase"><label>살 물건 가격 · 만원<input id="price" type="number" min="0" max="99999999" step="any" inputmode="decimal" placeholder="예: 150"></label><div class="kpi"><small>구매 후 현금</small><b id="after">—</b></div></div>
<p class="result" id="buyTip">가격과 월 필수비를 넣으면 비상자금 유지 여부를 확인할 수 있어요.</p>
<div class="row muted"><span id="runway">현금 여유 기간 — → —</span><span id="reserve">비상자금 —</span></div>
</section>
<div class="actions"><button type="button" id="example">예시로 체험</button><button type="button" id="reset">입력 초기화</button></div>
<div id="notice" role="status">이 브라우저에만 자동 저장 · 공용 기기에서는 초기화하세요</div>
<footer>현금 일시불·수입 없음 가정. 투자/묶인 자산은 구매재원에서 제외.<br>세금·처분비용·일시 만기부채 미반영. 선택한 기준 비교이며 안전 보장이 아닙니다.</footer>
</main><script>
'use strict';
const ids=['cash','invest','locked','debt','monthly','price'];
const key='wealth-ability-v2', el=id=>document.getElementById(id);
const num=v=>Math.round(v*100)/100;
const money=v=>num(v).toLocaleString('ko-KR',{maximumFractionDigits:2})+'만원';
const pct=v=>v.toLocaleString('ko-KR',{maximumFractionDigits:1})+'%';
const duration=v=>v.toLocaleString('ko-KR',{maximumFractionDigits:1})+'개월';
function analyze(cash,invest,locked,debt,monthly,price,months){
 const total=num(cash+invest+locked),net=num(total-debt),after=num(cash-price);
 const reserve=num(monthly*months),gap=num(Math.max(0,reserve-after));
 const shares=total>0?[cash,invest,locked].map(v=>v/total*100):null;
 const beforeMonths=monthly>0?cash/monthly:null;
 const afterMonths=monthly>0?Math.max(0,after)/monthly:null;
 const state=after<0?'short':monthly<=0?'unknown':after<reserve?'reserve':'within';
 return {total,net,after,reserve,gap,shares,beforeMonths,afterMonths,state};
}
function badge(id,text,tone='neutral'){
 const e=el(id);e.textContent=text;
 const colors={neutral:['#edf1f7','#425875'],green:['#e5f5ef','#046c4e'],amber:['#fff3d9','#805000'],red:['#fff0ed','#b42318']};
 [e.style.background,e.style.color]=colors[tone];
}
function render(save=true){
 const values=ids.map(id=>{const e=el(id);let v=Number(e.value);v=Number.isFinite(v)?Math.min(99999999,Math.max(0,num(v))):0;if(e.value!==''&&Number(e.value)!==v)e.value=v;return v;});
 const [cash,invest,locked,debt,monthly,price]=values,months=Number(el('months').value);
 const a=analyze(cash,invest,locked,debt,monthly,price,months);
 const hasAssets=ids.slice(0,4).some(id=>el(id).value!==''),hasCash=el('cash').value!=='',hasPrice=el('price').value!=='';
 el('net').textContent=hasAssets?money(a.net):'—';
 el('ratio').textContent=a.shares?pct(a.shares[0]):'—';
 ['cashShare','investShare','lockedShare'].forEach((id,i)=>el(id).textContent=a.shares?pct(a.shares[i]):'—');
 if(a.total>0){
  badge('liquidBadge',cash===0?'현금 없음':'현금 비중 확인',cash===0?'amber':'neutral');
  const max=Math.max(cash,invest,locked), labels=['현금·예금','투자자산','묶인 자산'];
  const top=labels.filter((_,i)=>[cash,invest,locked][i]===max).join('·');
  el('liquidTip').textContent='가장 큰 비중: '+top+'. '+(monthly>0?'현재 현금은 필수비 '+duration(a.beforeMonths)+'분입니다.':'월 필수비를 넣으면 현금의 생활 유지 능력도 확인해요.');
 }else{badge('liquidBadge',hasAssets?'총자산 0':'입력 대기');el('liquidTip').textContent=hasAssets?'총자산이 0이면 자산 비율을 계산할 수 없어요.':'재산을 중복 없이 입력해 주세요. 비율은 부채 차감 전 총자산 기준입니다.';}
 if(hasAssets&&a.net<0)el('liquidTip').textContent+=' 부채가 총자산보다 많아요.';
 el('after').textContent=hasCash&&hasPrice?money(a.after):'—';el('after').style.color=a.after<0?'#b42318':'#192a43';
 el('reserve').textContent=monthly>0?'비상자금 '+money(a.reserve):'비상자금 —';
 el('runway').textContent=hasCash&&hasPrice&&monthly>0?'현금 여유 '+duration(a.beforeMonths)+' → '+duration(a.afterMonths):'현금 여유 기간 — → —';
 if(!hasCash||!hasPrice){badge('buyBadge',!hasCash?'현금 입력':'가격 입력');el('buyTip').textContent='바로 쓸 돈과 구매 가격을 입력해 주세요. 현금이 없으면 0을 입력하세요.';}
 else if(a.state==='short'){badge('buyBadge','현금 부족','red');el('buyTip').textContent='현금 일시불 구매에 '+money(-a.after)+'이 부족해요. 투자자산 매각·대출은 가정하지 않았어요.';}
 else if(a.state==='unknown'){badge('buyBadge','필수비 필요','amber');el('buyTip').textContent='현금으로 구매는 가능해요. 월 필수비를 0보다 크게 입력해야 비상자금 유지 여부를 판단할 수 있어요.';}
 else if(a.state==='reserve'){badge('buyBadge','비상자금 미달','amber');el('buyTip').textContent='구매 후 '+months+'개월 기준까지 '+money(a.gap)+'이 부족해요. 기준을 지키는 구매 한도는 '+money(Math.max(0,cash-a.reserve))+'입니다.';}
 else{badge('buyBadge','설정 기준 충족','green');el('buyTip').textContent='구매 후에도 '+months+'개월 비상자금이 남아요. 비상자금 외 여유 현금은 '+money(a.after-a.reserve)+'입니다.';}
 if(hasCash&&hasPrice&&price===0)el('buyTip').textContent='구매 가격 0만원 기준입니다. '+el('buyTip').textContent;
 if(save){try{const data=Object.fromEntries(ids.map(id=>[id,el(id).value]));data.months=el('months').value;localStorage.setItem(key,JSON.stringify(data));}catch(e){el('notice').textContent='브라우저 저장 불가 · 입력은 현재 화면에서만 유지됩니다';}}
}
ids.forEach(id=>el(id).addEventListener('input',()=>render()));el('months').addEventListener('change',()=>render());
el('example').addEventListener('click',()=>{[800,2200,20000,12000,150,200].forEach((v,i)=>el(ids[i]).value=v);el('months').value='6';render();});
let pending=false,timer;
el('reset').addEventListener('click',()=>{if(!pending){pending=true;el('reset').textContent='다시 누르면 삭제';timer=setTimeout(()=>{pending=false;el('reset').textContent='입력 초기화';},3500);return;}clearTimeout(timer);pending=false;el('reset').textContent='입력 초기화';ids.forEach(id=>el(id).value='');el('months').value='6';try{localStorage.removeItem(key);}catch(e){}render(false);});
try{const d=JSON.parse(localStorage.getItem(key)||'null');if(d&&typeof d==='object'){ids.forEach(id=>{if(typeof d[id]==='string'||typeof d[id]==='number')el(id).value=d[id];});if(['3','6','12'].includes(String(d.months)))el('months').value=String(d.months);}}catch(e){el('notice').textContent='저장된 값을 불러오지 못했어요 · 새로 입력해 주세요';}
render(false);
</script></body></html>'''
components.html(PAGE, height=740, scrolling=False)
