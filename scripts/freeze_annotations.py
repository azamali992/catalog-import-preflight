"""Recreate manually reviewed labels; no parser/publisher normalization fields used."""
import hashlib, json, pathlib, random
ROOT = pathlib.Path(__file__).resolve().parents[1]
# Human-readable transcription, frozen before implementation. Canonical: grams or mL.
REVIEWED = {
3:('mass','80'),10:('missing',None),15:('volume','700'),17:('unsupported',None),19:('mass','300'),20:('mass','1000'),27:('mass','590'),30:('mass','610'),44:('mass','1000'),55:('mass','78.9'),64:('missing',None),65:('unsupported',None),66:('mass','250'),74:('mass','920'),76:('missing',None),95:('missing',None),98:('unsupported',None),102:('mass','100'),111:('volume','700'),116:('unsupported',None),119:('mass','500'),130:('unsupported',None),148:('mass','200'),149:('missing',None),153:('unsupported',None),155:('mass','100'),156:('unsupported',None),158:('missing',None),160:('mass','500'),161:('volume','455'),164:('missing',None),166:('missing',None),171:('mass','500'),174:('missing',None),175:('unsupported',None),185:('mass','125'),193:('missing',None),199:('volume','700'),208:('missing',None),232:('mass','800'),235:('unsupported',None),244:('mass','100'),252:('missing',None),255:('missing',None),261:('mass','40'),262:('unsupported',None),265:('missing',None),266:('mass','450'),269:('missing',None),288:('volume','700')}
assert hashlib.sha256((ROOT/'data/source.json').read_bytes()).hexdigest()=='520931fd9a12f568b9b5992496c7ab68a017606e6877cb15dc100c9a435fe1ed', 'New source cohort: manually re-annotate; frozen labels cannot be reused'
rows = json.loads((ROOT/'data/source.json').read_text(encoding='utf8'))
ids = sorted(i+1 for i in random.Random(20261003).sample(range(len(rows)),50))
assert ids == sorted(REVIEWED), 'frozen cohort mismatch'
labels = [{'source_row':i,'raw_quantity':rows[i-1]['quantity'],'expected_status':REVIEWED[i][0],'expected_value':REVIEWED[i][1]} for i in ids]
(ROOT/'data/annotations.json').write_text(json.dumps(labels,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('50 manual annotations frozen; no model/parser called')
