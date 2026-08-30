# Based on yesterday's WORKING eval script. One adapter per run (arg).
# Usage: python3 bridge_hit_v2.py full    OR    python3 bridge_hit_v2.py nobridge
import os, sys, json, random, re
import numpy as np, torch
sys.path.insert(0, '/workspace')
random.seed(0); np.random.seed(0)

which = sys.argv[1] if len(sys.argv) > 1 else 'full'
ADP = {'full':'/workspace/outputs/rl_dqd_fresh/best',
       'nobridge':'/workspace/outputs/rl_dqd_nobridge/best'}[which]
print('>>> variant:', which, '->', ADP, flush=True)

NB = '/workspace/rl_dqd_fresh_fixed.ipynb'
def run_cells(idxs, drop_calls=False):
    nb = json.load(open(NB))
    for i in idxs:
        out = []
        for l in ''.join(nb['cells'][i]['source']).split('\n'):
            st = l.strip()
            if st.startswith(('!', '%')): continue
            if drop_calls and re.match(r'^(full_eval_no_sf|quick_eval|res\s*=)', st):
                continue
            out.append(l)
        exec(compile('\n'.join(out), '<c%d>' % i, 'exec'), globals())

# same cells as yesterday's working eval (12=model, skip 14/18/24 training)
run_cells([2, 4, 6, 8, 10, 12])
run_cells([16, 20], drop_calls=True)   # helpers only, NOT cell 30 (avoid its inline call)

# load adapter onto the 'default' created by cell 12
model.load_adapter(ADP, adapter_name='default', is_trainable=False)
model.set_adapter('default')
model.eval()
print('>>> active adapter:', model.active_adapter, flush=True)

# sanity
e = tok(build_prompt(test[0]['question']), return_tensors='pt').to(model.device)
oo = model.generate(**e, do_sample=False, max_new_tokens=CFG['MAX_NEW'], pad_token_id=tok.pad_token_id)
print('>>> sample:', tok.decode(oo[0][e['input_ids'].shape[1]:], skip_special_tokens=True)[:90], flush=True)

# eval loop with bridge-hit (inline, no dependence on cell 30)
@torch.no_grad()
def run_eval():
    tp=fp=fn=0; f1s=[]; bhits=[]
    for k, ex in enumerate(test[:CFG['EVAL_N']]):
        enc = tok(build_prompt(ex['question']), return_tensors='pt').to(model.device)
        o = model.generate(**enc, do_sample=False, max_new_tokens=CFG['MAX_NEW'],
                           pad_token_id=tok.pad_token_id)
        txt = tok.decode(o[0][enc['input_ids'].shape[1]:], skip_special_tokens=True)
        env = env_execute(parse_subqueries(txt), ex)
        bid = kg.lookup(ex['bridge']) if ex.get('bridge') else None
        bhits.append(1.0 if (bid and bid in env['hop1']) else 0.0)
        P = {p.lower() for p in env['pred_names']}; G = {g.lower() for g in ex['gold']}
        tpi=len(P&G); tp+=tpi; fp+=len(P-G); fn+=len(G-P)
        pr=tpi/len(P) if P else 0; rc=tpi/len(G) if G else 0
        f1s.append(2*pr*rc/(pr+rc) if pr+rc else 0.0)
        if (k+1)%150==0: print('   eval %d/764' % (k+1), flush=True)
    pr=tp/(tp+fp) if tp+fp else 0; rc=tp/(tp+fn) if tp+fn else 0
    return dict(micro=2*pr*rc/(pr+rc) if pr+rc else 0,
                macro=float(np.mean(f1s)), bridge_hit=float(np.mean(bhits)))

print('>>> eval 764 ...', flush=True)
r = run_eval()
print('\n' + '='*50)
print('%s : micro=%.4f  macro=%.4f  bridge_hit=%.4f' %
      (which, r['micro'], r['macro'], r['bridge_hit']))
print('='*50)
json.dump(r, open('/workspace/outputs/bridgehit_%s.json' % which, 'w'), indent=2)
print('saved bridgehit_%s.json' % which)
