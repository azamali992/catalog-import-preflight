import hashlib,json,pathlib,sys,time
from collections import Counter
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from core import quantity,baseline,audit
rows=json.loads((ROOT/'data/source.json').read_text(encoding='utf8'))
assert hashlib.sha256((ROOT/'data/source.json').read_bytes()).hexdigest()=='520931fd9a12f568b9b5992496c7ab68a017606e6877cb15dc100c9a435fe1ed', 'Fresh cohort requires new manual annotations; refusing stale scoring'
labels=json.loads((ROOT/'data/annotations.json').read_text(encoding='utf8'))
def score(fn):
    correct=wrong=covered=disposition=0
    for a in labels:
        p=fn(a['raw_quantity']); covered+=p['value'] is not None
        exact=p['status']==a['expected_status'] and p['value']==a['expected_value']
        disposition+=exact
        if p['value'] is not None: correct+=exact;wrong+=not exact
    return {'annotation_rows':len(labels),'normalized':covered,'correct_normalized':correct,'wrong_normalized':wrong,'unresolved':len(labels)-covered,'disposition_agreement':disposition}
start=time.perf_counter();results=[audit(x) for x in rows];elapsed=time.perf_counter()-start
report={'dataset_rows':len(rows),'baseline':score(baseline),'normalizer':score(quantity),'quantity_status_counts':dict(Counter(x['parsed']['status'] for x in results)),'ready_rows':sum(x['status']=='ready' for x in results),'review_rows':sum(x['status']=='review' for x in results),'quantity_diffs':sum(x['changed'] for x in results),'source_preserved_rows':sum(x['original']==r for x,r in zip(results,rows)),'processing_ms':round(elapsed*1000,3),'source_sha256':hashlib.sha256((ROOT/'data/source.json').read_bytes()).hexdigest(),'note':'Single-author rubric agreement on nonrepresentative publisher-order prefix; not packaging/product fact accuracy or measured manual-time savings.'}
(ROOT/'data/results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
(ROOT/'data/derived.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(report,indent=2))
