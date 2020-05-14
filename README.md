# Critical Coagulation Concentration Calculator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3725518.svg)](https://doi.org/10.5281/zenodo.3725518)

Version: 0.1.0

CCC calculator calculates critical coagulation concentration (CCC) based on the electrophoretic mobility data. The CCC is the concentration above which suspensions are not stable and rapid aggregation of colloidal particles is observed. The calculation method is based procedure published in Galli et al., Colloids Interfaces 2020, 4(2), 20 (https://doi.org/10.3390/colloids4020020). For the conversion of electrophoretic mobility to electrokinetic potential Smoluchowski model is used. For the conversion between surface charge density and surface potential Debye-Huckel model is used.

## Usage

### Make a virtual environment and install dependencies
```sh
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### Run program with
`python ccc_calculator.py`

### Input

As input a file containing electrophoretic mobility as a function of concentration has to be given. Two columns must be given. First column is the electorophoretic mobility in (1e-8 m^2/V/s) units, second column is concentration in (M).

#### Example input:
```py
# mobility(1e-8 m^2/V/s)   conc (M)
  1.9127                   0.000101309
  1.8961                   0.000106076
  1.8794                   0.000111069
  1.8624                   0.000116296
```

#### Parameters:
Parameters are input through the `parameters.yaml` file. You can define the input file name, the electrolyte valence as well as concentration and valence of 2 background electrolytes. Furthermore particle and solvent properties are defined with Hamaker constant, temperature, viscosity and dielectric constant. An example `parameters.yaml` file is given below.

```yaml
# data input file
filename: mobility.txt

# electrolyte composition
salt: # electrolyte whose concentration is in data input file
  valence: [1,-1] # valence of z:y electrolyte in format [z,-y] 
background1:  # background electrolyte 1
  valence: [1,-1]
  concentration: 1.0e-4 # concentration in M
background2:  # background electrolyte 2
  valence: [1,-1] #
  concentration: 0

# particle and solvent properties
hamaker: 1.0e-21 # Hamaker constant of particles in J
temperature: 298 # temperature in K
viscosity: 0.89e-3 # solvent viscosity in Pas
epsilon: 78.54 # solvent dielectric constant
```

### Output

Output is given as *yaml* formatted terminal output. If you wanna save it into file you can use unix tee command `python ccc_calculator.py | tee results.yaml`. Depending on the system, several critical coagulation concentrations can be observed. For every critical coagulation concentration (CCC) that is found also critical coagulation ionic strength (CCIS), surface potential (potential), surface charge density (sigma) are given. A sample output is given below.

```yaml
# Found 3 CCCs.

CCC 1:       2.80e-03 M
CCIS 1:       2.90e-03 M
Potential 1: 3.04e-03 mV
Sigma 1:     3.74e-04 mC/m^2

CCC 2:       7.04e-03 M
CCIS 2:       7.14e-03 M
Potential 2: -3.81e-03 mV
Sigma 2:     -7.35e-04 mC/m^2

CCC 3:       8.88e-01 M
CCIS 3:       8.88e-01 M
Potential 3: -1.27e-02 mV
Sigma 3:     -2.74e-02 mC/m^2

Parameters:
  Hamaker constant: 1.00e-21 J
  Viscosity: 8.90e-04 Pas
  Dielectric constant: 78.54
  Data file: mobility.txt
```


