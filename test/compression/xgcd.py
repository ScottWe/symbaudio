import sympy
import unittest

import harness
import symbaudio.compression.xgcd

class TestReconstructRational(unittest.TestCase):
    """ Reconstructs known recurrence relations to ensure some correctness. """

    def test_order_1_constant(self):
        """ Reconstructs a{0} = 1, a{i} = a{i-1}. """
        (n, d) = symbaudio.compression.xgcd.reconstruct_rational(1, [1,1])
        self.assertEqual(n.all_coeffs(), [1])
        self.assertEqual(d.all_coeffs(), [-1,1])

    def test_order_2_fib(self):
        """ Reconstructs a{0} = 1, a{1} = 1, a{i} = a{i-1} + a{i-2}. """
        (n, d) = symbaudio.compression.xgcd.reconstruct_rational(2, [1,1,2,3])
        self.assertEqual(n.all_coeffs(), [-9])
        self.assertEqual(d.all_coeffs(), [9,9,-9])

    def test_higher_order_2_fib(self):
        """ Reconstructs a{0} = 1, a{1} = 1, a{i} = a{i-1} + a{i-2}. """
        (n, d) = symbaudio.compression.xgcd.reconstruct_rational(3, [1,1,2,3,5,8])
        self.assertEqual(n.all_coeffs(), [-64])
        self.assertEqual(d.all_coeffs(), [64,64,-64])

    def test_finite_field(self):
        """ Reconstructs a simple recurrence over the finite field GF(5). """
        (n, d) = symbaudio.compression.xgcd.reconstruct_rational(1, [3,1], dom=sympy.GF(5))
        self.assertEqual(n.all_coeffs(), [-1])
        self.assertEqual(d.all_coeffs(), [-1,-2])

if __name__ == '__main__':
    unittest.main()
