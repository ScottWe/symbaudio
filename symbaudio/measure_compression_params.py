"""
This script recursively scans a directory. For ever *.wav file found, the file
is passed through the XGCD compression procedure, and the coefficient size is
analyzed. A log to stderr will display the current file being analyzed.

An additional parameter may be passed to define the coefficient domain used in
compression.
"""

import os
import numpy
import random
import scipy.stats
import sympy
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import symbaudio.analysis.audio
import symbaudio.compression.xgcd
import symbaudio.utils.filesystem
import symbaudio.utils.poly
import symbaudio.utils.time

def analyze_file(file, framewidth, use_finite, samps):
    """ Runs compression tests on file, and logs results to stdout.

    Arguments:
    file -- the file to analyze (assumed to be a .wav)
    framewidth -- the number of points in each compression frame
    use_finite -- constructs coefficients over a finite field

    Requires: an even number of samples per frame.
    """
    assert(framewidth % 2 == 0)
    audio = symbaudio.analysis.audio.AudioFile(file)

    framecount = audio.sample_count // framewidth

    timer = symbaudio.utils.time.PerfTimer()
    k = framewidth // 2
    dom = "QQ"
    if use_finite:
        dom = sympy.GF(65537)
    for i in random.sample(range(0, framecount), samps):
        window = audio.raw[i*framewidth:(i+1)*framewidth,0]

        timer.reset()
        (num, dom) = symbaudio.compression.xgcd.reconstruct_rational(k, window)

        ts        = timer.get_elapsed_ns()
        max_coeff = max(symbaudio.utils.poly.max_coeff(num), symbaudio.utils.poly.max_coeff(dom))
        zero_cnt  = symbaudio.utils.poly.count_zeros(num) + symbaudio.utils.poly.count_zeros(dom)
        zero_orig = framecount - numpy.count_nonzero(window)
        coeff_cnt = num.degree() + dom.degree()

        try:
            print("%i,%i,%i,%i,%i,%i" % (i, ts, max_coeff, zero_cnt, zero_orig, coeff_cnt))
        except Exception:
            sys.stderr.write("Unexpected value in frame %s\n" % str(i))

class Analyzer:
    """ Wrapper class to analyze function. Passes fixed arguments to analyze_file. """

    def __init__(self, framewidth, use_finite, samps):
        """ Sets the parameters for analyze_function. See analyze_function. """
        self._framewidth = framewidth
        self._use_finite = use_finite
        self._samps = samps

    def __call__(self, path, rel):
        """ Runs analyze_function against the file found at path. """
        if rel is not "":
            print(rel)
        analyze_file(path, self._framewidth, self._use_finite, self._samps)

def main():
    """ Analyzes compression performance against a specific file.

	Params:
	arg1 -- path to file
	arg2 -- size of each frame
	arg3 -- compression domain ("rational" or "finite")
    """
    file = sys.argv[1]
    framewidth = int(sys.argv[2])
    use_finite = (sys.argv[3] == "finite")
    analyzer = Analyzer(framewidth, use_finite, 300)
    symbaudio.utils.filesystem.apply_to_files(sys.argv[1], ".wav", analyzer)

if __name__ == "__main__":
    main()
else:
    raise ImportError("measure_compression_params is a script and should not be imported.")
