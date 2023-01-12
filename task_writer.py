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


# CREATING TASKS
tasks = []
for mof in tqdm(cifs):
        
    sim_name = F'simulation_{uuid4().hex}.input'
        
    with open(os.path.join(FF_OUT, sim_name), 'w') as f:
        f.writelines(xe_kr_input(mof))
    
    tasks.append(F'tsp hare run --rm -d -v $PWD:/app crh53/raspa2 simulate -i {sim_name}')   
   

# WRITING TASKS  
with open(os.path.join(FF_OUT, 'tasks.sh'), 'w') as f:
    f.writelines([t+'\n' for t in tasks])
