import numpy
import unittest

import harness
import symbaudio.analysis.audio

class TestAudioFile(unittest.TestCase):
    """ Tests basic audio loading through AudioFile. """
    
    def test_load(self):
        """
        Tests AudioFile against a manufactured wave file satisfying:
        - A sample rate of 44100
        - A sample count of 882000
        - A left channel containing a 440hz, amplitude 1 wave
        - A right channel containing silence
        """
        fn = "test/data/44100hz_2chan_440tone_stereo_88200samps.wav"
        file = symbaudio.analysis.audio.AudioFile(fn)

        # Checks generated metadata corresponds to file metadata.
        self.assertEqual(file.sample_rate_hz, 44100)
        self.assertEqual(file.sample_count, 88200)
        self.assertEqual(file.channel_count, 2)
        self.assertEqual(file.sample_count, len(file.raw))

        # The raw samples range over +/- 32767. The file contain negligible
        # artifacts wrt the maximum magnitudes. The LHS and RHS channels are
        # checked for correctness within reasonable tolerances. The error is
        # presumably due to dipher.
        for t in range(0, file.sample_count):
            # Checks for a sin wave within a tolerance of 10 discrete units.
            exp = 32767 * numpy.sin(2 * numpy.pi * 440 * t / file.sample_rate_hz)
            self.assertLessEqual(abs(file.raw[t, 0] - exp), 10)
            # Checks for silence within a tolerance of 8 discrete units.
            self.assertLessEqual(abs(file.raw[t, 1]), 8)

if __name__ == '__main__':
    unittest.main()
