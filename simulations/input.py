
def xe_kr_input(mof_name):
    sim_details = F"""SimulationType                MonteCarlo
NumberOfCycles                1000
NumberOfInitializationCycles  1000
PrintEvery                    250
Restart File                  no
ChargeMethod                  none
CutOff                        14.0

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
