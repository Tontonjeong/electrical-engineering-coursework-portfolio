export function motorCurrentPi({ra,la,j,kt,fcc,fcs}) {
  const values=[ra,la,j,kt,fcc,fcs].map(Number);
  if(values.some(v=>!Number.isFinite(v)||v<=0)) throw new Error('모든 입력은 0보다 큰 숫자여야 합니다.');
  const [R,L,J,Kt,fcCurrent,fcSpeed]=values, wc=2*Math.PI*fcCurrent, ws=2*Math.PI*fcSpeed;
  return {kpCurrent:L*wc,kiCurrent:R*wc,inertiaTerm:J*ws,normalizedInertia:J*ws/Kt};
}
if(typeof document!=='undefined'){const form=document.querySelector('#calculator'),out=document.querySelector('#result'),err=document.querySelector('.form-error');
function render(){try{const r=motorCurrentPi(Object.fromEntries(new FormData(form)));err.hidden=true;out.innerHTML=`<div class="result-grid"><div class="result-item"><span>Current Kp</span><strong>${r.kpCurrent.toFixed(3)}</strong></div><div class="result-item"><span>Current Ki</span><strong>${r.kiCurrent.toFixed(3)}</strong></div><div class="result-item"><span>J·ωs</span><strong>${r.inertiaTerm.toFixed(3)}</strong></div><div class="result-item"><span>J·ωs/Kt</span><strong>${r.normalizedInertia.toFixed(3)}</strong></div></div><p><strong>Preserved source values:</strong> speed Kp 24.8; report Ki ≈3898; recovered source Ki 3895. These are not silently replaced by the exploratory terms above.</p>`}catch(e){err.textContent=e.message;err.hidden=false;out.innerHTML='';}}
form.addEventListener('submit',e=>{e.preventDefault();render()});form.addEventListener('reset',()=>setTimeout(render));render();}
