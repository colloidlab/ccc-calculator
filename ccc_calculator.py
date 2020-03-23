#!/usr/bin/env python3
import numpy as np
import yaml
import ccc

# load parameters from the YAML file
with open("parameters.yaml", "r") as file:
    parameters = yaml.load(file, Loader=yaml.FullLoader)

viscosity = float(parameters["viscosity"])
eps0 = ccc.constants["eps0"]
epsilon = float(parameters["epsilon"]) * eps0
e0 = ccc.constants["e0"]
Na = ccc.constants["Na"]
kT = ccc.constants["kb"] * float(parameters["temperature"])
hamaker = float(parameters["hamaker"])

# load data
data_file = parameters["filename"]
data = np.loadtxt(data_file)

# sort data, so that concentration is ascending
data = data[data[:, 1].argsort()]

mobility = data[:, 0] * 1e-8  # in m^2/V/s
concentration = data[:, 1]  # in molar

# load electrolyte properties
valences = []
valences.append(np.array(parameters["salt"]["valence"], dtype=int))
valences.append(np.array(parameters["background1"]["valence"], dtype=int))
valences.append(np.array(parameters["background2"]["valence"], dtype=int))

# matrix of valences for salt and background electrolytes
valences = np.array(valences)
# background electrolyte valences
valences_back = valences[1:]

conc_back1 = float(parameters["background1"]["concentration"])
conc_back2 = float(parameters["background2"]["concentration"])

# background electrolytes
conc_back = np.array([conc_back1, conc_back2])

# calculate ionic strengths
is_salt = ccc.ionic_strength_coeff(valences[0]) * concentration
is_back = sum(ccc.ionic_strength_coeff(valences_back) * conc_back)

# calculate total ionic strength
ionic_strength = is_salt + is_back

# mobility to electrokinetic potential via Smoluchowski model
potential = mobility * viscosity / epsilon


# calculate inverse Debye length from ionic strength
lb = e0 ** 2 / 4.0 / np.pi / epsilon / kT  # Bjerrum length
kappa = np.sqrt(8 * np.pi * lb * Na * ionic_strength * 1000)

# potential to surface charge density via Debye-Huckel model
sigma = abs(epsilon * kappa * potential)


# calculate CCIS from from surface charge density for all concentrations
# equation (25) from Trefalt et al., Langmuir 2017, 33, 7, 1695-1704
# https://doi.org/10.1021/acs.langmuir.6b04464
ccis = (
    (
        1
        / 8.0
        / np.pi
        / lb
        * (24 * np.pi / hamaker / np.e / epsilon) ** 0.6666
        * sigma ** 1.3333
    )
    / Na
    / 1000
)

# find where calculated ccis is equal to experimental ioinc strength
roots = ccc.find_roots(ccis - ionic_strength, ccis)

cccs = (roots - is_back) / (ccc.ionic_strength_coeff(valences[0]))


# write out the results

results = "\n# Found %i CCCs.\n" % (len(cccs))

i = 0

for _ccc, _ccis in zip(cccs, roots):
    i += 1

    pot = np.interp(_ccc, concentration, potential)
    ionic_strength = _ccis
    sig = epsilon * np.sqrt(8 * np.pi * lb * Na * ionic_strength * 1000) * pot

    results += "\nCCC %i:       %3.2e M" % (i, _ccc)
    results += "\nCCIS %i:       %3.2e M" % (i, _ccis)
    results += "\nPotential %i: %3.2e mV" % (i, pot)
    results += "\nSigma %i:     %3.2e mC/m^2" % (i, sig)
    results += "\n"

results += "\nParameters:\n"
results += "  Hamaker constant: %3.2e J\n" % hamaker
results += "  Viscosity: %3.2e Pas\n" % viscosity
results += "  Dielectric constant: %3.2f\n" % (epsilon / eps0)
results += "  Data file: %s\n" % data_file

print(results)
