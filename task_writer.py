import os
from uuid import uuid4

from tqdm import tqdm
import pandas as pd

# -------------------------------------------------------------------------------------


def xe_kr_input(mof_name):
    sim_details = F"""SimulationType                MonteCarlo
NumberOfCycles                1000
NumberOfInitializationCycles  1000
PrintEvery                    250
Restart File                  no
ChargeMethod                  none
CutOff                        16.0

Framework 0
FrameworkName {mof_name}
UnitCells 2 2 2
ExternalTemperature 273
ExternalPressure 1e6
RemoveAtomNumberCodeFromLabel yes

Component 0 MoleculeName        xenon
ChargeMethod                    None
IdealGasRosenbluthWeight        1.0
FugacityCoefficient             0.9253
MoleculeDefinition              local
MolFraction                     0.20
IdentityChangeProbability       1.0
  NumberOfIdentityChanges       2
  IdentityChangesList           0 1
TranslationProbability          1.0
ReinsertionProbability          1.0
SwapProbability                 1.0
CreateNumberOfMolecules         0

Component 1 MoleculeName        krypton
ChargeMethod                    None
IdealGasRosenbluthWeight        1.0
FugacityCoefficient             0.9671
MoleculeDefinition              local
MolFraction                     0.80
IdentityChangeProbability       1.0
  NumberOfIdentityChanges       2
  IdentityChangesList           0 1
TranslationProbability          1.0
ReinsertionProbability          1.0
SwapProbability                 1.0
CreateNumberOfMolecules         0
    """
    return sim_details


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
#cifs = [c.replace('.cif', '') for c in os.listdir('cifs') if '.cif' in c]
cifs = pd.read_csv('E6_07_missing.txt', header=None)[0].tolist()


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
