import os, sys, json, inspect
sys.path.insert(0, '/workspace')

NB = '/workspace/rl_dqd_fresh_fixed.ipynb'
def run_cells(idxs):
    nb = json.load(open(NB))
    for i in idxs:
        src = '\n'.join(l for l in ''.join(nb['cells'][i]['source']).split('\n')
                        if not l.strip().startswith(('!', '%')))
        exec(compile(src, '<c%d>' % i, 'exec'), globals())

run_cells([2, 4, 6, 8, 10])

def hr(t): print('\n' + '#'*66 + '\n# ' + t + '\n' + '#'*66)
def sub(t): print('\n[' + t + ']\n' + '-'*50)

hr('GROUP A - HYPERPARAMETERS')

sub('1+9  B_max - bridge fan-out cap')
print('CFG keys with MAX/CAP/BRIDGE:',
      [k for k in CFG if any(x in k.upper() for x in ['MAX', 'CAP', 'BRIDGE', 'FAN'])])
print('\nrun_two_hop source:')
print(inspect.getsource(run_two_hop))
try:
    print('typed_neighbors source:')
    print(inspect.getsource(typed_neighbors))
except Exception:
    pass

sub('2+10  L_sq - format checks sub-query LENGTH?')
print('r_format source:')
print(inspect.getsource(r_format))
print('tests:')
print('  normal   :', r_format(['Find the gene associated with X.', 'Find the disease for that gene.']))
print('  1-word   :', r_format(['gene', 'disease']))
print('  empty    :', r_format([]))
print('  four      :', r_format(['a', 'b', 'c', 'd']))
print('  -> if normal==1-word: length NOT checked -> L_sq has no effect')

sub('3  L_name - min entity name length')
print('extract_entities source:')
print(inspect.getsource(extract_entities))
print('HAVE_AC =', HAVE_AC)

sub('4  N_seed (max_e default)')
print('max_e default =', inspect.signature(extract_entities).parameters['max_e'].default)

sub('6  SFT config')
for k in ['SFT_N', 'SFT_LR', 'SFT_EPOCHS', 'SFT_STEPS', 'SFT_MAX', 'SFT_BS']:
    if k in CFG:
        print('  %s = %s' % (k, CFG[k]))

hr('GROUP B - DATASET')

sub('7  gold-in-KG - which split')
in_kg = tot = 0
def _lookup(g):
    if hasattr(kg, 'lookup'):
        try: return kg.lookup(g)
        except Exception: pass
    return kg.name_to_id.get(g.lower()) if hasattr(kg, 'name_to_id') else None
for ex in test:
    for g in ex['gold']:
        tot += 1
        if _lookup(g): in_kg += 1
print('  TEST split gold-in-KG: %d/%d = %.1f%%' % (in_kg, tot, in_kg/tot*100))
print('  (EXPERIMENT_LOG says 57.7%)')

sub('8  PrimeKG edges')
for attr in ['num_edges', 'n_edges', 'relation_index', 'edges']:
    if hasattr(kg, attr):
        v = getattr(kg, attr)
        print('  kg.%s -> %s' % (attr, len(v) if hasattr(v, '__len__') else v))
print('  (EXPERIMENT_LOG: 8,100,498)')

hr('GROUP D - leak_rate definition')
sub('11  unified_baselines leak lines')
nb2 = json.load(open('/workspace/unified_baselines.ipynb'))
for i, c in enumerate(nb2['cells']):
    s = ''.join(c['source'])
    if 'leak' in s.lower() and c['cell_type'] == 'code':
        for line in s.split('\n'):
            L = line.lower()
            if 'leak' in L or 'gen_set' in L or 'ctx_set' in L or 'rawset' in L or '- ctx' in L:
                print('  cell%d: %s' % (i, line.strip()[:85]))

print('\n' + '='*66)
print('DONE')
print('='*66)
