import copy,json,pathlib,subprocess,sys,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from core import audit,quantity
class AuditTest(unittest.TestCase):
    def test_no_guessing(self):
        for raw in ('300 g e','14 x 35 g','1.2-2.1 kg','100','6 oz','-3 g','0 g','1'*90+'g'):
            self.assertIsNone(quantity(raw)['value'],raw)
    def test_exact_units(self):
        self.assertEqual(quantity('1,5 L')['value'],'1500')
        self.assertEqual(quantity('78,9g')['value'],'78.9')
        self.assertEqual(quantity('33 cl')['unit'],'mL')
        self.assertEqual(quantity('1 kg')['unit'],'g')
    def test_source_immutability(self):
        row={'source_row':1,'code':'12345678','product_name':'Example','quantity':'1 kg'}
        before=copy.deepcopy(row);a=audit(row);self.assertEqual(row,before);self.assertEqual(a['canonical'],'1000 g');a['original']['quantity']='x';self.assertEqual(row,before)
    def test_js_python_parity(self):
        rows=json.loads((ROOT/'data/source.json').read_text(encoding='utf8'))
        actual=json.loads(subprocess.check_output(['node','-e',"const fs=require('fs'),p=require('./parser.js');console.log(JSON.stringify(JSON.parse(fs.readFileSync('data/source.json','utf8')).map(p.audit)));"],cwd=ROOT))
        self.assertEqual(actual,[audit(x) for x in rows])
if __name__=='__main__':unittest.main()
