import numpy as np
from ase.io import read


def xe_kr_input(mof_name, na, nb, nc):
    sim_details = F"""SimulationType                MonteCarlo
NumberOfCycles                1000
NumberOfInitializationCycles  1000
PrintEvery                    1000
Restart File                  no
ChargeMethod                  none
CutOff                        16.0

Framework 0
FrameworkName {mof_name}
UnitCells {na} {nb} {nc}
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


def find_minimum_image(cell, cutoff):
    ncutoff = cutoff + 1e-8 * cutoff
    V = np.abs(np.linalg.det(cell))
    a, b, c = cell
    Xa = np.cross(b, c)
    ha = V / np.linalg.norm(Xa)
    na = int(np.ceil(2 * ncutoff / ha))
    Xb = np.cross(a, c)
    hb = V / np.linalg.norm(Xb)
    nb = int(np.ceil(2 * ncutoff / hb))
    Xc = np.cross(a, b)
    hc = V / np.linalg.norm(Xc)
    nc = int(np.ceil(2 * ncutoff / hc))
    return na, nb, nc


def extract_cif_cell(cif_path):
    atoms = read(cif_path, format="cif")
    cell = np.array(atoms.cell)
    return cell

def calc_min_image_indices(cif_path, cutoff):
    cell = extract_cif_cell(cif_path)
    na, nb, nc = find_minimum_image(cell)
    return na, nb, nc
