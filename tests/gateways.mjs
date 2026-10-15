// Four gateways checks. Run: node tests/gateways.mjs (needs the playwright package)
import { chromium, webkit, firefox } from 'playwright';
const ROOT=process.env.FR_ROOT||new URL('../flight-recorder',import.meta.url).pathname;
const SHOTS=process.env.SHOTS||null;
const base='file://'+ROOT+'/index.html';
let fails=0;const ok=(n,c)=>{console.log((c?'PASS ':'FAIL ')+n);if(!c)fails++};
for(const [bn,bt] of [['chromium',chromium],['webkit',webkit],['firefox',firefox]]){
 const b=await bt.launch();const p=await b.newPage({viewport:{width:1440,height:900}});const errs=[];p.on('pageerror',e=>errs.push(String(e)));
 // default view: overlay on
 await p.goto(base+'#step1');ok(bn+' default has overlay on',(await p.locator('#gwbanner').count())===1);
 // ?gateways=0: plain view
 await p.goto(base+'?gateways=0#step1');ok(bn+' ?gateways=0 has no overlay',(await p.locator('#gwbanner').count())===0&&await p.locator('#gwbtn').isVisible());
 // toggle on
 await p.click('#gwbtn');ok(bn+' toggle shows G2 on step 1',(await p.locator('#gwbanner').getAttribute('data-gw'))==='G2'&&await p.locator('#ledger >> text=FOUR GATEWAYS VIEW ON').isVisible());
 if(SHOTS&&bn==='chromium')await p.screenshot({path:SHOTS+'/gw-step1.png',fullPage:true});
 await p.click('#next');ok(bn+' step 2 tags G1 and G3',(await p.locator('#gwbanner').getAttribute('data-gw'))==='G1 G3');
 const vals=async()=>p.$$eval('#g1panel .pv',e=>e.map(x=>x.textContent).join('|'));
 let v=await vals();ok(bn+' redacted by default',v.includes('[SSN_REDACTED]')&&!v.includes('000-12-3456')&&!v.includes('example.com'));
 if(SHOTS&&bn==='chromium')await p.locator('#g1panel').screenshot({path:SHOTS+'/gw-redacted.png'});
 await p.click('#redact-toggle');v=await vals();ok(bn+' raw toggle shows synthetic values',v.includes('000-12-3456')&&(await p.locator('#redact-state').innerText()).includes('LOCAL ONLY')&&await p.locator('#ledger >> text=REDACTION APPLIED').isVisible());
 if(SHOTS&&bn==='chromium')await p.locator('#g1panel').screenshot({path:SHOTS+'/gw-raw.png'});
 await p.click('#redact-toggle');ok(bn+' toggles back',(await vals()).includes('[EMAIL_REDACTED]'));
 await p.click('#next');ok(bn+' fail-closed open, no number written',(await p.locator('#failclosed').getAttribute('data-fc'))==='open'&&await p.locator('#ledger >> text=HANDED BACK: UNRECONCILABLE_RECORD').isVisible()&&(await p.locator('[data-res=UNSUPPORTED]').count())===3);
 if(SHOTS&&bn==='chromium')await p.locator('#failclosed').screenshot({path:SHOTS+'/gw-failclosed.png'});
 await p.click('#fc-cedent');ok(bn+' human answer logged',(await p.locator('#failclosed').getAttribute('data-fc'))==='answered'&&(await p.locator('#ledger >> text=HUMAN ANSWERED: RE-CLM-0931').count())===1);
 for(let i=0;i<5;i++)await p.keyboard.press('ArrowRight');
 ok(bn+' closer tagged G4, pack lists gateways',(await p.locator('#gwbanner').getAttribute('data-gw'))==='G4'&&await p.locator('#pack >> text=Four gateways in this run').isVisible());
 // query-string entry point
 await p.goto(base+'?gateways=1#step5');ok(bn+' ?gateways=1 opens with overlay',(await p.locator('#gwbanner').getAttribute('data-gw'))==='G2 G4');
 if(SHOTS&&bn==='chromium')await p.screenshot({path:SHOTS+'/gw-step5.png',fullPage:true});
 ok(bn+' no page errors',errs.length===0);if(errs.length)console.log(errs);
 await b.close()}
// Closer comparison cards: four approaches, bottom line, editable assumptions, sources, in the evidence pack
{
 const b=await chromium.launch();const p=await b.newPage({viewport:{width:1440,height:900},acceptDownloads:true});const errs=[];p.on('pageerror',e=>errs.push(String(e)));
 await p.goto(base+'#step8');
 const rows=await p.locator('#compare [data-cmp]').count();
 ok('compare: four approaches',rows===4);
 const t=await p.locator('#compare').innerText();
 ok('compare: labeled estimates + BLS rate + sources',t.includes('illustrative estimates')&&(await p.locator('#cmp-panel').innerText()).includes('37.51')&&t.includes('bls.gov')===false&&await p.locator('#compare a[href*="bls.gov"]').count()===1&&await p.locator('#compare a[href*="doi.org"]').count()===1);
 const cost=async()=>p.locator('#compare [data-cmp]').first().locator('.cmp-labor').innerText();
 const c1=await cost();ok('compare: default fully-human cost = 30 x 30 min x $38',c1==='$570');
 const bl=async i=>p.locator('#compare [data-cmp]').nth(i).locator('.cmp-bottom').innerText();
 ok('compare: bottom lines at defaults',(await bl(0)).startsWith('$570')&&(await bl(0)).includes('not estimated')&&(await bl(1))==='$380'&&(await bl(2))==='$4,838'&&(await bl(3))==='$105');
 ok('compare: errors, exposure, traps, audit in plain words',(await p.locator('#compare [data-cmp]').nth(2).innerText()).includes('+$4,800 paid')&&(await p.locator('#compare [data-cmp]').nth(2).innerText()).includes('Missed all 27 traps')&&(await p.locator('#compare [data-cmp]').nth(1).innerText()).includes('$6,000 reserve')&&/\d+ of \d+ traps caught/.test(await p.locator('#compare [data-cmp]').nth(3).innerText()));
 const co=await p.locator('#cmp-callout').innerText();ok('compare: callout cheapest to run vs bottom line',co.includes('Cheapest to run: Single-pass AI')&&co.includes('bottom line once errors paid are counted: Agentic'));
 await p.fill('#cmp-herr','2000');ok('compare: human error input adds to bottom line',(await bl(0))==='$2,570');await p.fill('#cmp-herr','0');
 await p.fill('#cmp-batch','60');ok('compare: batch edit recalculates',(await cost())==='$1,140');
 await p.fill('#cmp-rate','50');ok('compare: rate edit recalculates',(await cost())==='$1,500');
 const panelTop=(await p.locator('#cmp-panel').boundingBox()).y<(await p.locator('#dl').boundingBox()).y;ok('compare: inputs panel at top of closer',panelTop);
 await p.fill('#cmp-rate','12.5');ok('compare: decimal rejected, value kept',(await cost())==='$1,500'&&(await p.locator('#cmp-rate').getAttribute('aria-invalid'))==='true');
 await p.fill('#cmp-batch','0');ok('compare: batch 0 rejected',(await cost())==='$1,500');
 await p.click('#cmp-reset');ok('compare: reset to defaults',(await cost())==='$570'&&(await p.inputValue('#cmp-rate'))==='38'&&(await p.inputValue('#cmp-batch'))==='30');
 if(SHOTS)await p.screenshot({path:SHOTS+'/closer-inputs.png'});
 await p.fill('#cmp-batch','60');
 ok('compare: agentic row shows ledger audit trail',(await p.locator('#compare [data-cmp]').nth(3).innerText()).includes('Yes, every step'));
 const [dl]=await Promise.all([p.waitForEvent('download'),p.click('#dl')]);const fp='/tmp/pack-cmp.html';await dl.saveAs(fp);
 const txt=(await import('fs')).readFileSync(fp,'utf8');ok('compare: table in downloaded evidence pack',txt.includes('compare-pack')&&txt.includes('Standard OCR + human review')&&txt.includes('Items per batch 60'));
 ok('compare: no page errors',errs.length===0);if(errs.length)console.log(errs);await b.close();
}
console.log(fails?`${fails} FAILED`:'ALL CHECKS PASS (incl. compare)');process.exit(fails?1:0);
