import os
from uuid import uuid4

from tqdm import tqdm

from simulations.input import xe_kr_input

# -------------------------------------------------------------------------------------
# GLOBALS
FF = 'Xe-Kr'
FF_OUT = F'results_{FF}'
IMAGE = 'crh53/raspa2'
RESULTS = 'simulation_results'


# SET UP DIR FOR SIMULATIONS
if not os.path.exists(FF_OUT):
    os.mkdir(FF_OUT)
    os.mkdir(os.path.join(FF_OUT, RESULTS))

os.system(F'cp simulations/{FF}/* {FF_OUT}')  # copy FF files
os.system(F'cp cifs/*.cif {FF_OUT}')  # copy all cif files


# PARAMETERS TO EVALUATE
cifs = [c.replace('.cif', '') for c in os.listdir('cifs') if '.cif' in c]
cuttoff_radii = [18.0, 20.0, 22.0]
n_repeats = 5
n_sims = len(cifs) * len(cuttoff_radii) * n_repeats


# WRITING TASKS
tasks = []
count = 1
for mof in tqdm(cifs):
    for r in cuttoff_radii:
        
        simulation_contents = xe_kr_input(mof, r)
        sim_name = F'simulation_{uuid4().hex}.input'
        
        with open(os.path.join(FF_OUT, sim_name), 'w') as f:
            f.writelines(simulation_contents)
        
        for n_ in range(n_repeats):
            tasks.append(F'echo "starting simulation [{count}/{n_sims}] at $(date)"')
            tasks.append(F'simulate -i {sim_name}')
            tasks.append(F'mv Output/System_0/*.data {RESULTS}/{mof}_{r}_{n_}.data')
            tasks.append(F'echo "simulation completed at $(date)"')
            count += 1
        
with open(os.path.join(FF_OUT, 'tasks.sh'), 'w') as f:
    f.writelines([t+'\n' for t in tasks])
