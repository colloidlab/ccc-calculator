# Critical Coagulation Concentration Calculator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Version: 0.1.0

CCC calculator calculates critical coagulation concentration (CCC) based on the electrophoretic mobility data. The CCC is the concentration above which suspensions are not stable and rapid aggregation of colloidal particles is observed. The calculation method is based on equation (25) from Trefalt et al., Langmuir 2017, 33, 7, 1695-1704 (https://doi.org/10.1021/acs.langmuir.6b04464). For the conversion of electrophoretic mobility to electrokinetic potential Smoluchowski model is used. For the conversion between surface charge density and surface potential Debye-Huckel model is used.

## Usage

### Make a virtual environment and install dependencies
```sh
python -m venv env
pip install -r requirements.txt
```


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



