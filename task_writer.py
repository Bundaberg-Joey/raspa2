import os
from shutil import copytree, copy


# -------------------------------------------------------------------------------------


def xe_kr_input(mof_name, cuttoff):
    sim_details = F"""SimulationType                MonteCarlo
NumberOfInitializationCycles  1000
NumberOfCycles                1000
Forcefield                    raspa
ChargeMethod                  None
CutOffVDW                     {cuttoff}

Framework 0 FrameworkName                 {mof_name}
            RemoveAtomNumberCodeFromLabel no
            Movies                        no
            UnitCells                     2 2 2
            ExternalTemperature           273
            ExternalPressure              10e5

Component 0 MoleculeName                  xenon
            MoleculeDefinition            local
            MolFraction                   0.20
            FugacityCoefficient           0.9253
            ReinsertionProbability        1.0
            SwapProbability               1.0
            TranslationProbability        1.0
            IdentityChangeProbability     1.0
                NumberOfIdentityChanges   2
                IdentityChangesList       0 1

Component 1 MoleculeName                  krypton
            MoleculeDefinition            local
            MolFraction                   0.80
            FugacityCoefficient           0.9671
            ReinsertionProbability        1.0
            SwapProbability               1.0
            TranslationProbability        1.0
            IdentityChangeProbability     1.0
                NumberOfIdentityChanges   2
                IdentityChangesList       0 1
    """
    return sim_details


# -------------------------------------------------------------------------------------
# GLOBALS
FF = 'Xe-Kr'
FF_OUT = F'output_{FF}'

if not os.path.exists(FF_OUT):
    os.mkdir(FF_OUT)


# PARAMETERS TO EVALUATE
forcefield_path = F'forcefields/{FF}'
cifs = [(c.replace('.cif', ''), os.path.join('cifs', c)) for c in os.listdir('cifs') if '.cif' in c]
cuttoff_radii = [12, 14, 16]
n_repeats = 5


# WRITING TASKS
tasks = []
for mof, mof_path in cifs:
    for r in cuttoff_radii:
        for n_ in range(n_repeats):
            dir_name = os.path.join(FF_OUT, F'{mof}_{r}_{n_}')
            
            copytree(forcefield_path, dir_name)
            copy(mof_path, dir_name)
            
            with open(os.path.join(dir_name, 'simulation.input'), 'w') as f:
                f.write(xe_kr_input(mof, r))
            
            tasks.append(F'tsp hare run --rm -it -v $PWD/{dir_name}:/app raspa simulate simulation.input')
        

# dont need the output of these so just delete them (needs to be done through the docker image because of permission)
tasks.append(F'tsp hare run --rm -it -v $PWD/{dir_name}:/app raspa rm -rf */Movies/ */VTK/ */Restart')
        
        
with open(os.path.join(FF_OUT, 'tasks.sh'), 'w') as f:
    f.writelines([t+'\n' for t in tasks])
