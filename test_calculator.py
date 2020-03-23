import ccc
import numpy as np


def test_find_roots():

    y = np.array([1, -1, -2, -2, 2, 4])
    x = np.array([0, 1, 2, 3, 4, 5])
    roots = ccc.find_roots(y, x)

    assert np.array_equal(roots, np.array([0.5, 3.5]))

    y = np.array([1, -1, 1, -2, -2, -4])
    x = np.array([0, 1, 2, 3, 4, 5])
    roots = ccc.find_roots(y, x)

    assert len(roots) == 3


def test_ionic_strength_coeff():

    valences = [1, -1]

    coeff = ccc.ionic_strength_coeff(valences)
    assert np.array_equal(coeff, np.array([1.0]))

    valences = [[1, -1], [1, -1], [4, -1]]

    coeff = ccc.ionic_strength_coeff(valences)
    assert np.array_equal(coeff, np.array([1.0, 1.0, 10.0]))


def test_ionic_strength():

    concentrations = [1]
    valences = [1, -1]

    strength = ccc.ionic_strength(concentrations, valences)

    assert strength == 1.0

    concentrations = [1, 2, 1]
    valences = [[1, -1], [1, -1], [1, -2]]

    strength = ccc.ionic_strength(concentrations, valences)

    assert strength == 6.0

    concentrations = [1, 2, 1]
    valences = [[1, -1], [1, -1], [4, -1]]

    strength = ccc.ionic_strength(concentrations, valences)

    assert strength == 13.0

    concentrations = [1, 0, 1]
    valences = [[1, -4], [1, -1], [4, -1]]

    strength = ccc.ionic_strength(concentrations, valences)

    assert strength == 20.0

    concentrations = [1, 0, 1]
    valences = [[2, -4], [6, -3], [4, -1]]

    strength = ccc.ionic_strength(concentrations, valences)

    assert strength == 22.0

    concentrations = [1, 1, 1]
    valences = [[2, -4], [6, -3], [4, -1]]

    strength = ccc.ionic_strength(concentrations, valences)

    assert strength == 49.0


def test_ionic_strength_and_coeff():

    concentrations = [1, 2, 1]
    valences = [[1, -1], [1, -1], [4, -1]]

    strength = ccc.ionic_strength(concentrations, valences)

    coeff = ccc.ionic_strength_coeff(valences)

    assert strength == sum(coeff * concentrations)

    concentrations = [1, 2, 10]
    valences = [[2, -8], [10, -1], [4, -1]]

    strength = ccc.ionic_strength(concentrations, valences)

    coeff = ccc.ionic_strength_coeff(valences)

    assert strength == sum(coeff * concentrations)
