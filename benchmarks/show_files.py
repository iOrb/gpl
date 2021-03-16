#! /usr/bin/env python3

import os
import glob

ROOT = os.path.dirname(os.path.abspath(__file__))

dir = 'reach_for_the_star/climb_the_pilar_tiny'
list_fn = sorted(glob.glob(os.path.join(ROOT, dir, "*.json")))

print("instances = {")
for i, f in enumerate(list_fn):
#    basename = f.split('/')[-1]
#    new_fn = f.replace(basename, f'cfr_{basename}')
#    os.rename(f, new_fn)
    print(os.path.join(f'\t{i} : "{os.path.join(dir, os.path.basename(f))}",'))
print("}")
