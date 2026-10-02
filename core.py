"""Conservative, source-preserving metric quantity import audit."""
import re
from decimal import Decimal

UNITS = {'g':('mass',1),'gram':('mass',1),'grams':('mass',1),'gr':('mass',1),'kg':('mass',1000),'ml':('volume',1),'cl':('volume',10),'l':('volume',1000)}
PATTERN = re.compile(r'^([0-9]+(?:[.,][0-9]{1,6})?)\s*(g|gram|grams|gr|kg|ml|cl|l)$', re.I)

def quantity(raw):
    text = str(raw or '').strip()
    if not text: return {'status':'missing','value':None,'unit':None,'reason':'Quantity missing; no value inferred'}
    if len(text)>80: return {'status':'unsupported','value':None,'unit':None,'reason':'Quantity exceeds bounded input length'}
    match = PATTERN.fullmatch(text)
    if not match: return {'status':'unsupported','value':None,'unit':None,'reason':'Outside single metric mass/volume grammar; check source'}
    value = Decimal(match[1].replace(',','.'))
    kind, factor = UNITS[match[2].lower()]
    value *= factor
    if value <= 0 or value > 1_000_000_000: return {'status':'unsupported','value':None,'unit':None,'reason':'Outside positive bounded quantity policy'}
    formatted = format(value, 'f').rstrip('0').rstrip('.') if '.' in format(value,'f') else format(value,'f')
    return {'status':kind,'value':formatted,'unit':'g' if kind=='mass' else 'mL','reason':'Single metric quantity; exact decimal conversion'}

def baseline(raw):
    """Destination accepts only canonical strings, unchanged (g or mL)."""
    if re.fullmatch(r'[0-9]+(?:\.[0-9]{1,6})? (?:g|mL)',str(raw or '')):
        return quantity(raw)
    return {'status':'missing' if not raw else 'unsupported','value':None,'unit':None}

def audit(row):
    parsed = quantity(row.get('quantity',''))
    issues = []
    if not str(row.get('product_name','')).strip(): issues.append('Product name missing')
    if not re.fullmatch(r'[0-9]{8,14}', str(row.get('code',''))): issues.append('Code outside 8–14 digit destination policy')
    if parsed['value'] is None: issues.append(parsed['reason'])
    canonical = None if parsed['value'] is None else parsed['value']+' '+parsed['unit']
    return {'source_row':row['source_row'],'original':dict(row),'parsed':parsed,'canonical':canonical,'issues':issues,'status':'review' if issues else 'ready','changed':canonical is not None and canonical!=row.get('quantity','')}
