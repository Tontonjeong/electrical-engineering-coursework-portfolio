export function lineCase({vll,x,b,length}) {
  const values=[vll,x,b,length].map(Number);
  if(values.some(v=>!Number.isFinite(v)||v<=0)) throw new Error('모든 입력은 0보다 큰 숫자여야 합니다.');
  const [kv,xohm,bMicro,len]=values, zc=Math.sqrt(xohm/(bMicro*1e-6)), silMW=(kv*1000)**2/zc/1e6, currentA=silMW*1e6/(Math.sqrt(3)*kv*1000);
  return {zc,silMW,currentA,length:len};
}
if(typeof document!=='undefined'){const form=document.querySelector('#calculator'),out=document.querySelector('#result'),err=document.querySelector('.form-error');
function render(){try{const r=lineCase(Object.fromEntries(new FormData(form)));err.hidden=true;out.innerHTML=`<div class="result-grid"><div class="result-item"><span>Surge impedance</span><strong>${r.zc.toFixed(2)} Ω</strong></div><div class="result-item"><span>SIL</span><strong>${r.silMW.toFixed(1)} MW</strong></div><div class="result-item"><span>3φ current at SIL</span><strong>${r.currentA.toFixed(1)} A</strong></div><div class="result-item"><span>Documented length</span><strong>${r.length.toFixed(0)} km</strong></div></div><p>Zc=√(x/b), SIL=VLL²/Zc. For this lossless characteristic approximation, length does not change Zc or SIL.</p>`}catch(e){err.textContent=e.message;err.hidden=false;out.innerHTML='';}}
form.addEventListener('submit',e=>{e.preventDefault();render()});form.addEventListener('reset',()=>setTimeout(render));render();}
