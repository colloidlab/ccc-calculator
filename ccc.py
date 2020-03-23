""" Functions used by the ccc_calculator.py """

import numpy as np


def find_roots(y, x):
    """
    Finds all roots (zeros) of the why vs ex function.

    It gets the roots by looking where the y crosses 0 and then
    linerly interpolates between these two points.

    Parameters
    ----------
    y : array of n elements
        y-values of a function
    x : array of n elements
        x-values of a function
    Returns
    -------
    roots: array
        Array which holds all the found roots.

    """
    roots = []

    previous_y = y[0]
    previous_x = x[0]

    for ex, why in zip(x, y):

        if previous_y * why < 0:

            delta_y = why - previous_y

            delta_x = ex - previous_x

            result = previous_x + delta_x / delta_y * (0 - previous_y)

            roots.append(result)

        previous_y = why
        previous_x = ex

    return np.array(roots)


def ionic_strength(concentrations, valences):
    """
    Calculates ionic strength of mixture of electrolytes defined in
    valences and concentrations.

    Parameters
    ----------
    concentrations : array of n elements
        List of electrolyte concentrations in a mixture.
        For example 0.1 M NaCl + 0.2 M CaCl2 is [0.1, 0.2]
    valences : nx2 matrix
        Matrix which holds electrolyte valences.
        For example 0.1 M NaCl + 0.2 M CaCl2 is [[1,-1],
                                                 [2,-1]]

    Returns
    -------
    float
        Value of ionic strength of all electrolytes together.

    """
    concentrations = np.array([concentrations]).transpose()

    valences = np.array(valences)
    if len(valences.shape) < 2:
        valences = np.array([valences])

    gcd = np.gcd(valences, np.flip(valences, 1))

    coeff = abs(np.flip(valences, 1)) / gcd * valences ** 2

    return 0.5 * np.sum(coeff * concentrations)


def ionic_strength_coeff(valences):
    """
    Calculates ionic strength coefficients for electrolytes.
    This coeffcient can be multiplied by concentration to get
    ionic strength.

    Parameters
    ----------
    valences : nx2 matrix
        Matrix which holds electrolyte valences.
        For example 0.1 M NaCl + 0.2 M CaCl2 is [[1,-1],
                                                 [2,-1]]

    Returns
    -------
    coeff: array
        Value of ionic strength coefficients.

    """
    valences = np.array(valences)

    if len(valences.shape) < 2:
        # if we have only one electrolyte create a matrix with one row
        valences = np.array([valences])

    coeff = []

    for valence in valences:
        z1 = valence[0]
        z2 = valence[1]

        gcd = np.gcd(z1, z2)
        c = abs(z2 / gcd) * z1 ** 2 + z1 / gcd * z2 ** 2
        coeff.append(0.5 * c)

    return np.array(coeff)
