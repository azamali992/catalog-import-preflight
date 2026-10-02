"""Actual unattended browser flow, reset, assertions, frames and export checks."""
import argparse,csv,functools,http.server,json,pathlib,threading
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parents[1]
def main():
    p=argparse.ArgumentParser();p.add_argument('--url');args=p.parse_args()
    output=ROOT/'artifacts';output.mkdir(exist_ok=True);server=None
    if not args.url:
        handler=functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(ROOT))
        server=http.server.ThreadingHTTPServer(('127.0.0.1',0),handler)
        threading.Thread(target=server.serve_forever,daemon=True).start();args.url=f'http://127.0.0.1:{server.server_port}'
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True)
            context=browser.new_context(viewport={'width':1920,'height':1080},accept_downloads=True)
            page=context.new_page();errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
            page.goto(args.url,wait_until='networkidle');page.evaluate('window.prewarm()')
            page.screenshot(path=str(output/'01-before.png'))
            page.get_by_role('button',name='Review batch').click();page.wait_for_function("document.getElementById('ready').textContent==='107'")
            assert page.locator('#review').inner_text()=='193'
            assert page.locator('#original').inner_text()=='78,9g'
            assert page.locator('#canonical').inner_text()=='78.9 g'
            page.screenshot(path=str(output/'02-normalized.png'))
            page.get_by_role('button',name='Review row 92',exact=True).click()
            assert page.locator('#original').inner_text()=='1.2-2.1 kg'
            assert page.locator('#canonical').inner_text()=='No guess'
            page.screenshot(path=str(output/'03-exception.png'))
            page.locator('#tryinput').fill('750ml');page.get_by_role('button',name='Check',exact=True).click()
            assert page.locator('#tryresult').inner_text()=='750 mL · volume'
            page.screenshot(path=str(output/'04-live-input.png'))
            assert page.locator('#accepted').is_disabled()
            page.locator('#ack').check()
            for button,file,expected in [('Export ready CSV','catalog-ready.csv',107),('Export exceptions CSV','catalog-review.csv',193)]:
                with page.expect_download() as download:page.get_by_role('button',name=button,exact=True).click()
                path=output/file;download.value.save_as(str(path))
                with path.open(encoding='utf-8-sig',newline='') as f:assert len(list(csv.DictReader(f)))==expected
            page.screenshot(path=str(output/'05-handoff.png'))
            assert not errors,errors
            (output/'capture-report.json').write_text(json.dumps({'url':args.url,'viewport':[1920,1080],'asserted_ready_rows':107,'asserted_review_rows':193,'natural_hard_case_source_row':92,'quantity_computation':'750ml -> 750 mL','exports_checked':True,'page_errors':errors},indent=2),encoding='utf8')
            context.close();browser.close()
    finally:
        if server:server.shutdown()
    print('PASS: actual UI, natural exception, different input, both exports and zero page errors')
if __name__=='__main__':main()
