import sympy
import sympy.abc
import unittest

import harness
import symbaudio.utils.poly

class TestMaxCoeff(unittest.TestCase):
    """ Tests max_coeff with multiple cases in each domain. """

    def test_rational(self):
        """ Ensures Q works in the rational case. """
        p1 = sympy.Poly([1/100, 0, 20, 4, 9], sympy.abc.x, domain="QQ")
        p2 = sympy.Poly([0], sympy.abc.x, domain="QQ")
        p3 = sympy.Poly([2/11], sympy.abc.x, domain="QQ")
        p4 = sympy.Poly([7/2], sympy.abc.x, domain="QQ")
        self.assertEqual(symbaudio.utils.poly.max_coeff(p1), 100)
        self.assertEqual(symbaudio.utils.poly.max_coeff(p2), 1)
        self.assertEqual(symbaudio.utils.poly.max_coeff(p3), 11)
        self.assertEqual(symbaudio.utils.poly.max_coeff(p4), 7)

    def test_integer(self):
        """ Ensures Z works in the integer case. """
        p1 = sympy.Poly([1, 5, 3, 7, 3], sympy.abc.x, domain="ZZ")
        p2 = sympy.Poly([0], sympy.abc.x, domain="ZZ")
        p3 = sympy.Poly([10], sympy.abc.x, domain="ZZ")
        self.assertEqual(symbaudio.utils.poly.max_coeff(p1), 7)
        self.assertEqual(symbaudio.utils.poly.max_coeff(p2), 0)
        self.assertEqual(symbaudio.utils.poly.max_coeff(p3), 10)

    def test_finite_field(self):
        """ Ensures finite fields work in the finite field case. """
        p1 = sympy.Poly([1, 5, 3, 7, 3], sympy.abc.x, domain=sympy.GF(11))
        p2 = sympy.Poly([0], sympy.abc.x, domain=sympy.GF(11))
        p3 = sympy.Poly([10], sympy.abc.x, domain=sympy.GF(11))
        self.assertEqual(symbaudio.utils.poly.max_coeff(p1), 7)
        self.assertEqual(symbaudio.utils.poly.max_coeff(p2), 0)
        self.assertEqual(symbaudio.utils.poly.max_coeff(p3), 10)

class TestCountZeros(unittest.TestCase):
    """ Tests count_zeros in each domain. """

    def test_rational(self):
        """ Ensures Q works in the rational case. """
        p = sympy.Poly([0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0], sympy.abc.x, domain="QQ")
        self.assertEqual(symbaudio.utils.poly.count_zeros(p), 5)

    def test_integer(self):
        """ Ensures Z works in the integer case. """
        p = sympy.Poly([0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0], sympy.abc.x, domain="ZZ")
        self.assertEqual(symbaudio.utils.poly.count_zeros(p), 5)

    def test_finite_field(self):
        """ Ensures finite fields work in the finite field case. """
        p = sympy.Poly([0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0], sympy.abc.x, domain=sympy.GF(11))
        self.assertEqual(symbaudio.utils.poly.count_zeros(p), 5)

if __name__ == '__main__':
    unittest.main()
