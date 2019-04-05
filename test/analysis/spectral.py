import numpy
import unittest

import harness
import symbaudio.analysis.spectral

class TestZCR(unittest.TestCase):
    """
    Tests the ZCR calculator from the spectral analysis library.
    """
    
    def test_no_points(self):
        """
        An empty array has a ZCR of 0.
        """
        result = symbaudio.analysis.spectral.zcr([])
        self.assertEqual(result, 0)
    
    def test_singleton(self):
        """
        A singleton has a ZCR of 0.
        """
        result = symbaudio.analysis.spectral.zcr([343245])
        self.assertEqual(result, 0)

    def test_strictly_positive(self):
        """
        A strictly positive array has a ZCR of 0.
        """
        result = symbaudio.analysis.spectral.zcr(numpy.arange(1, 1000))
        self.assertEqual(result, 0)

    def test_strictly_positive(self):
        """
        A strictly negative array has a ZCR of 0.
        """
        result = symbaudio.analysis.spectral.zcr(numpy.arange(-1000, -1))
        self.assertEqual(result, 0)

    def test_one_change_down(self):
        """
        Populates an array which changes sign from positive to negative once
        """
        result = symbaudio.analysis.spectral.zcr(numpy.arange(10, -10, -3))
        self.assertEqual(result, 1)

    def test_one_change_up(self):
        """
        Populates an array which changes sign once
        """
        result = symbaudio.analysis.spectral.zcr(numpy.arange(-10, 10, 3))
        self.assertEqual(result, 1)

    def test_ten_changes_with_flat(self):
        """
        Populates an array which changes sign once
        """
        arr = numpy.arange(-1, -41, -1)
        for i in range(0, 5):
            arr[i] = 1 + i
        for i in range(9, 15):
            arr[i] = 1 + i
        for i in range(18, 20):
            arr[i] = 1 + i
        for i in range(21, 22):
            arr[i] = 1 + i
        for i in range(25, 30):
            arr[i] = 1 + i
        for i in range(35, 40):
            arr[i] = 1 + i
        result = symbaudio.analysis.spectral.zcr(arr)
        self.assertEqual(result, 10)

class TestSpectralEnergy(unittest.TestCase):
    """
    Tests that spectral energy is computed properly.
    """
 
    def test_size_zero(self):
        """
        Tests the zero case is the constant 0.
        """
        result = symbaudio.analysis.spectral.spectral_energy([0])
        self.assertEqual(result, 0)
 
    def test_size_one(self):
        """
        Tests the size one case is a constant squared.
        """
        element = 3.2
        result = symbaudio.analysis.spectral.spectral_energy([element])
        expect = element * element
        self.assertEqual(result, expect)
 
    def test_size_n(self):
        """
        Tests the size five case is a sum of squares.
        """
        x1 = 3.2
        x2 = 2
        x3 = 9.2
        x4 = 0
        x5 = 32
        result = symbaudio.analysis.spectral.spectral_energy([x1, x2, x3, x4, x5])
        expect = x1 * x1 + x2 * x2 + x3 * x3 + x4 * x4 + x5 * x5
        self.assertEqual(result, expect)

class TestSpectralShape(unittest.TestCase):
    """
    Tests that spectral shape captures spread and centroid properly.
    """

    def test_size_zero(self):
        """
        Tests the empty case is a zero mean with no variance.
        """
        (mu, sigma) = symbaudio.analysis.spectral.spectral_shape([], [])
        self.assertEqual(mu, 0)
        self.assertEqual(sigma, 0)

    def test_zero_elts(self):
        """
        Tests a zero array is a zero mean with no variance.
        """
        (mu, sigma) = symbaudio.analysis.spectral.spectral_shape(numpy.zeros(5), numpy.zeros(5))
        self.assertEqual(mu, 0)
        self.assertEqual(sigma, 0)

    def test_unital_spectrum(self):
        """
        Tests a basic non-zero case with unital magnitudes.
        """
        spectrum = numpy.array([1, 1, 1, 1])
        freqs = numpy.array([0, 0, 1, 3])
        (mu, sigma) = symbaudio.analysis.spectral.spectral_shape(spectrum, freqs)
        self.assertEqual(mu, 1)
        self.assertEqual(sigma, 1.5)

    def test_dirac_spectrum(self):
        """
        Tests a one-hot spectrum.
        """
        spectrum = numpy.array([0, 0, 0, 1])
        freqs = numpy.array([50, 30, 15, 20])
        (mu, sigma) = symbaudio.analysis.spectral.spectral_shape(spectrum, freqs)
        self.assertEqual(mu, 20)
        self.assertEqual(sigma, 0)

    def test_three_hot_spectrum(self):
        """
        Tests a three-hot spectrum.
        """
        spectrum = numpy.array([1, 0, 2, 0, 1])
        freqs = numpy.array([-5, 0, 5, 0, 15])
        (mu, sigma) = symbaudio.analysis.spectral.spectral_shape(spectrum, freqs)
        self.assertEqual(mu, 5)
        self.assertEqual(sigma, 50)

class TestMakeFreqTable(unittest.TestCase):
    """
    Tests the make_freq_table function from the spectral analysis library.
    """

    def test_size_zero(self):
        """
        Tests the zero case is an empty array.
        """
        result = symbaudio.analysis.spectral.make_freq_table(0, 0)
        self.assertEqual(len(result), 0)

    def test_symmetry(self):
    	"""
    	Tests that tables are symmetric about their centres.
    	Values which produce exact frequencies are used.
    	"""
    	half_len = 25
    	result = symbaudio.analysis.spectral.make_freq_table(2 * half_len, 2 * half_len)
    	for i in range(0, half_len):
    		self.assertEqual(result[i], result[2 * half_len - 1 - i])

    def test_step_size(self):
    	"""
    	Tests that tables are symmetric about their centres.
    	Values which produce exact frequencies are used.
    	"""
    	half_len = 25
    	result = symbaudio.analysis.spectral.make_freq_table(2 * half_len, 2 * half_len)
    	for i in range(1, half_len):
    		self.assertEqual(result[i] - result[i - 1], 1)

if __name__ == '__main__':
    unittest.main()
