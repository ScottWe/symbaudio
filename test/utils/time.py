import time
import unittest

import harness
import symbaudio.utils.time

class TestPerfTimer(unittest.TestCase):
    """ Simple black and white box tests as time is a ND source of data. """

    def test_time_passage_whitebox(self):
        """ Sleep is now guaranteed to meet time, so this test is valid. """
        timer = symbaudio.utils.time.PerfTimer()
        time.sleep(0.25)
        self.assertGreater(timer.get_elapsed_ns(), 249999999)

    def test_reset_blackbox(self):
        """ Spies on internal clock time to ensure it resets. """
        timer = symbaudio.utils.time.PerfTimer()
        t1 = timer._start
        time.sleep(0.1)
        timer.reset()
        t2 = timer._start
        self.assertGreater(t2, t1)

if __name__ == '__main__':
    unittest.main()
