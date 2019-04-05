import time

class PerfTimer:
    """ A basic wrapper to Python3's performance counter interface.

    Note: timer._start is generated from perf_counter_ns(), and is therefore in
          reference to no known timeframe.
    """

    def __init__(self):
        """ Crates a new timer, from the current timepoint. """
        self.reset()

    def reset(self):
        """ Equivalent to overwriting this timer with a new timer. """
        self._start = time.perf_counter_ns()

    def get_elapsed_ns(self):
        """ Returns the number of ns from the last reset (or __init__). """
        return (time.perf_counter_ns() - self._start)
