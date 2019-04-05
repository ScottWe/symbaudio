import numpy
import numpy.fft
import unittest

import harness
import symbaudio.analysis.feature
import symbaudio.analysis.spectral

def _calc_mod(x, fs):
    """ Helper function to produce modulation values. """
    freqs = symbaudio.analysis.spectral.make_freq_table(fs, len(x))
    mu, _ = symbaudio.analysis.spectral.spectral_shape(numpy.fft.fft(x), freqs)
    return mu

class FakeAudioFile:
    """ A mock class for testing AudioFile clients. """
    
    def __init__(self, fs, raw):
        """ Treats (fs, raw) as the return from scipy.io.wavfile. """
        self.sample_rate_hz = fs
        self.raw = raw
        self.sample_count, self.channel_count = self.raw.shape

class TestFeatureAggregation(unittest.TestCase):
    """ Tests basic feature aggregation, with mocked data. """

    def test_two_points(self):
        """ Edge casess of 2 points. The mean and centroid are tivial. """
        a = symbaudio.analysis.feature.FeatureAggregation([1, 1], 1)
        b = symbaudio.analysis.feature.FeatureAggregation([2, 2], 1)
        c = symbaudio.analysis.feature.FeatureAggregation([3, 3], 1)
        self.assertEqual(a.mean, 1)
        self.assertEqual(a.modulation, 0.25)
        self.assertEqual(b.mean, 2)
        self.assertEqual(a.modulation, 0.25)
        self.assertEqual(c.mean, 3)
        self.assertEqual(a.modulation, 0.25)

    def test_many_points(self):
        """ Verifies that a set of points is also handled. """
        a = symbaudio.analysis.feature.FeatureAggregation([1, 2, 3, 4, 5, 6, 7, 8], 1)
        self.assertEqual(a.mean, 4.5)
        self.assertAlmostEqual(a.modulation, 0.15688756)

    def test_fs(self):
        """ Verifies that frequencies only impact the centroid. """
        a = symbaudio.analysis.feature.FeatureAggregation([1, 2, 3, 4, 5, 6, 7, 8], 100)
        self.assertEqual(a.mean, 4.5)
        self.assertAlmostEqual(a.modulation, 15.68875668)

class TestFeatureSeries(unittest.TestCase):
    """ Tests basic feature tracking, as both  awhite and black box. """

    def test_ctor(self):
        """ White box test to ensure the constructor works. """
        feat = symbaudio.analysis.feature.FeatureSeries(101, 2, 1024)
        self.assertEqual(feat.downsample_hz, 512)
        self.assertEqual(feat.count, 50)
        self.assertEqual(feat.features.shape, (50, 4))

    def test_record(self):
        """ Black-box test to ensure records are set. """
        feat = symbaudio.analysis.feature.FeatureSeries(100, 2, 1024)
        feat.record(4, 1, 2, 3, 4)
        self.assertEqual(feat.features[4, 0], 1)
        self.assertEqual(feat.features[4, 1], 2)
        self.assertEqual(feat.features[4, 2], 3)
        self.assertEqual(feat.features[4, 3], 4)

    def test_aggregation(self):
        """ Grey box test to see if the correct metrics are aggregated. """
        feat = symbaudio.analysis.feature.FeatureSeries(512 * 8, 512, 1024)
        centroid = [1, 1, 1, 1, 1, 1, 1, 1]
        spread = [1, 5, 1, -3, 1, 5, 1, -3]
        energy = [1, 2, 3, 4, 5, 6, 7, 8]
        zeros = [1, 2, 3, 4, 4, 3, 2, 1]
        for i in range(0, 8):
            feat.record(i, centroid[i], spread[i], energy[i], zeros[i])
        aggregation = feat.aggregate()
        self.assertEqual(aggregation["centroid"].mean, 1)
        self.assertEqual(aggregation["spread"].mean, 1)
        self.assertEqual(aggregation["energy"].mean, 4.5)
        self.assertEqual(aggregation["zeros"].mean, 2.5)
        self.assertEqual(aggregation["centroid"].modulation, _calc_mod(centroid, 2))
        self.assertEqual(aggregation["spread"].modulation, _calc_mod(spread, 2))
        self.assertEqual(aggregation["energy"].modulation, _calc_mod(energy, 2))
        self.assertAlmostEqual(aggregation["zeros"].modulation, _calc_mod(zeros, 2))

    def test_odd_points(self):
        """ An odd number of features would previously result in a failure. """
        symbaudio.analysis.feature.FeatureSeries(512 * 3, 512, 1).aggregate()

class TestAudioSummary(unittest.TestCase):
    """ Performs test on the audio summary function, using mocked files. """

    def test_global_summary(self):
        """ Checks global statistics, such as sample length. """
        a = FakeAudioFile(1024, numpy.random.random((2048, 2)))
        s = symbaudio.analysis.feature.AudioSummary(a)
        self.assertEqual(s.length_s, 2)

    def test_mean_statistics(self):
        """ Ensures windowed means are correct. """
        raw = numpy.ones((2048, 2))
        a = FakeAudioFile(1024, raw)
        s = symbaudio.analysis.feature.AudioSummary(a)
        self.assertEqual(s.second_order["centroid"].mean, 0.5)
        self.assertEqual(s.second_order["spread"].mean, 0)
        self.assertEqual(s.second_order["energy"].mean, 1024 * 1024)
        self.assertEqual(s.second_order["zeros"].mean, 0)

    def test_modulation_statistics(self):
        """ Ensures windowed modulations are correct. """
        raw = numpy.ones((2048, 2))
        a = FakeAudioFile(1024, raw)
        s = symbaudio.analysis.feature.AudioSummary(a)
        self.assertEqual(s.second_order["centroid"].modulation, 0.25)
        self.assertEqual(s.second_order["spread"].modulation, 0)
        self.assertEqual(s.second_order["energy"].modulation, 0.25)
        self.assertEqual(s.second_order["zeros"].modulation, 0)

if __name__ == '__main__':
    unittest.main()
