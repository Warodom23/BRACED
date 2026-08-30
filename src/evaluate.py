import os, sys, json, random, re
from pathlib import Path
import numpy as np, torch
sys.path.insert(0, '/workspace')
random.seed(0); np.random.seed(0)

NB='/workspace/rl_dqd_fresh_fixed.ipynb'
def run_cells(idxs, drop_eval_calls=False):
    nb=json.load(open(NB))
    for i in idxs:
        out=[]
        for l in ''.join(nb['cells'][i]['source']).split('\n'):
            st=l.strip()
            if st.startswith(('!','%')): continue
            if drop_eval_calls and re.match(r'^(full_eval_no_sf|quick_eval)\s*\(', st):
                continue
            out.append(l)
        print(f'>>> cell {i}', flush=True)
        exec(compile('\n'.join(out),f'<c{i}>','exec'),globals())

run_cells([2,4,6,8,10,12])
run_cells([16,20,30], drop_eval_calls=True)

ADP='/workspace/outputs/rl_dqd_fresh/best'      # ★ FULL model (with bridge)
model.load_adapter(ADP, adapter_name='default', is_trainable=False)
model.set_adapter('default')
model.eval()
print(f'\n>>> active={model.active_adapter}  loaded FULL from {ADP}')

ex0=test[0]
enc=tok(build_prompt(ex0['question']),return_tensors='pt').to(model.device)
o=model.generate(**enc,do_sample=False,max_new_tokens=CFG['MAX_NEW'],pad_token_id=tok.pad_token_id)
print('sample decomp:', tok.decode(o[0][enc['input_ids'].shape[1]:],skip_special_tokens=True)[:120])

print('\n>>> eval FULL on test 764...', flush=True)
res=full_eval_no_sf(test)
print('\n'+'='*60); print('FULL (with bridge, w_b=0.4) — test 764, setup วันนี้'); print('='*60)
print(f"  micro={res['micro_f1']:.4f}  macro={res['macro_f1']:.4f}  P={res['precision']:.4f}  R={res['recall']:.4f}")
print(f"  buckets:", {k:round(v[0],4) for k,v in res['bucket_f1'].items()})
json.dump(res,open('/workspace/outputs/rl_dqd_fresh/test_eval_today.json','w'),indent=2,ensure_ascii=False)
print('✓ saved')
