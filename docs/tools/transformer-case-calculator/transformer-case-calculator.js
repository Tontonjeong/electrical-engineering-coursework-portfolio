export function transformerCase({output, copper, core, vnl, vfl}) {
  const values = [output,copper,core,vnl,vfl].map(Number);
  if (values.some(v => !Number.isFinite(v) || v <= 0)) throw new Error('모든 입력은 0보다 큰 숫자여야 합니다.');
  const [p,pcu,pfe,noLoad,fullLoad] = values;
  const loss = pcu + pfe;
  return {loss, efficiency:100*p/(p+loss), regulation:100*(noLoad-fullLoad)/fullLoad};
}
if(typeof document!=='undefined'){const form=document.querySelector('#calculator'), out=document.querySelector('#result'), err=document.querySelector('.form-error');
function render(){try{const r=transformerCase(Object.fromEntries(new FormData(form)));err.hidden=true;out.innerHTML=`<div class="result-grid"><div class="result-item"><span>Total loss</span><strong>${r.loss.toFixed(4)} W</strong></div><div class="result-item"><span>Efficiency</span><strong>${r.efficiency.toFixed(4)}%</strong></div><div class="result-item"><span>Regulation</span><strong>${r.regulation.toFixed(4)}%</strong></div></div><p>η=Pout/(Pout+Pcu+Pcore), VR=(VNL−VFL)/VFL×100</p>`}catch(e){err.textContent=e.message;err.hidden=false;out.innerHTML='';}}
form.addEventListener('submit',e=>{e.preventDefault();render()});form.addEventListener('reset',()=>setTimeout(render));render();}
