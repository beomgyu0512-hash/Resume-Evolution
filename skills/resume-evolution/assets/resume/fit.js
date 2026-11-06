(function () {
  'use strict';
  const sizes = [10.5, 10.25, 10, 9.75, 9.5, 9.25, 9];
  const availableMm = 273;
  function choose(measure) {
    let last;
    for (const bodyPt of sizes) {
      last = {bodyPt, compact:false, contentHeightMm:measure(bodyPt,false)};
      if (last.contentHeightMm <= availableMm) return {...last, overflow:false};
    }
    last = {bodyPt:9, compact:true, contentHeightMm:measure(9,true)};
    return {...last, overflow:last.contentHeightMm > availableMm};
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = {choose,sizes,availableMm};
  if (typeof document === 'undefined') return;
  let running = false;
  function fit() {
    if(running) return;
    running = true;
    const main = document.querySelector('main.resume');
    const root = document.documentElement;
    const probe = main.cloneNode(true);
    probe.setAttribute('aria-hidden','true');
    Object.assign(probe.style,{position:'absolute',left:'-10000px',top:'0',visibility:'hidden',width:'182mm',minHeight:'0',padding:'0',margin:'0',display:'flow-root'});
    document.body.appendChild(probe);
    function apply(bodyPt,compact) {
      root.style.setProperty('--body-size',bodyPt+'pt');
      root.style.setProperty('--aux-size',Math.max(8.5,bodyPt-1.25)+'pt');
      root.style.setProperty('--section-gap',compact?'3.5mm':'4.5mm');
      root.style.setProperty('--entry-gap',compact?'2.5mm':'3mm');
      root.style.setProperty('--bullet-gap',compact?'.5mm':'.8mm');
    }
    const result=choose((pt,compact)=>{apply(pt,compact);return probe.getBoundingClientRect().height*25.4/96;});
    apply(result.bodyPt,result.compact);
    probe.remove();
    const report={...result,minBodyPt:9,maxBodyPt:10.5,availableHeightMm:availableMm,characterCount:main.textContent.replace(/\s/g,'').length};
    window.resumeLayoutReport=report;
    main.dataset.bodyPt=result.bodyPt;
    main.dataset.overflow=String(result.overflow);
    const box=document.querySelector('.layout-report');
    box.textContent=result.overflow
      ? '内容过多：正文已到最小字号 9 pt，仍超出一页。请精简内容或使用两页；导出前检查实际分页。'
      : '正文 '+result.bodyPt+' pt；内容适配一页。';
    box.dataset.warning=String(result.overflow);
    running=false;
    return report;
  }
  window.fitResume=fit;
  window.addEventListener('beforeprint',fit);
  const ready = document.fonts ? document.fonts.ready : Promise.resolve();
  ready.then(()=>Promise.all(Array.from(document.images).map(img=>img.complete?Promise.resolve():new Promise(resolve=>{img.onload=resolve;img.onerror=resolve;})))).then(fit);
}());
