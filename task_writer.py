import os
from shutil import copytree, copy

from tqdm import tqdm

# -------------------------------------------------------------------------------------


def xe_kr_input(mof_name, cuttoff):
    sim_details = F"""SimulationType                MonteCarlo
NumberOfCycles                1000
NumberOfInitializationCycles  1000
PrintEvery                    250
Restart File                  no
ChargeMethod                  none
CutOff                        {cuttoff}

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
FF_OUT = F'output_{FF}'
IMAGE = 'crh53/raspa2'

if not os.path.exists(FF_OUT):
    os.mkdir(FF_OUT)


# PARAMETERS TO EVALUATE
forcefield_path = F'forcefields/{FF}'
cifs = [(c.replace('.cif', ''), os.path.join('cifs', c)) for c in os.listdir('cifs') if '.cif' in c]
cuttoff_radii = [12.0, 14.0, 16.0]
n_repeats = 5


# WRITING TASKS
tasks = []
count = 1
for mof, mof_path in tqdm(cifs):
    for r in cuttoff_radii:
        for n_ in range(n_repeats):
            dir_name = os.path.join(FF_OUT, F'{mof}_{r}_{n_}')
            
            copytree(forcefield_path, dir_name)
            copy(mof_path, dir_name)
            
            with open(os.path.join(dir_name, 'simulation.input'), 'w') as f:
                f.write(xe_kr_input(mof, r))
            
            tasks.append(F'echo "starting simulation [{count}/165] at $(date)"')
            tasks.append(F'hare run --rm -it -v $PWD/{dir_name}:/app {IMAGE} simulate simulation.input')
            tasks.append(F'echo "simulation completed at $(date)"')
            count += 1
        
        
with open('tasks.sh', 'w') as f:
    f.writelines([t+'\n' for t in tasks])
