import numpy

def zcr(series):
    """ Estimates the ZCR of a signal.
    
    This uses the formula often seen in the literature. That is, adjacent
    elements are multiplied, and then summed with an indicator function R<0.
    This is a crude estimate, as [1, 0, -1] results in a ZCR of 0, whereas
    applying IVT to [1, 0, -1](0) and [1, 0, -1](2) clearly indicates a root.
    Attempts to filter zeros proved too costly, while less local approaches
    proved too complex to write without native loops.
    
    Arguments:
    series -- the points to analyze
    """
    if len(series) > 1:
        return numpy.sum((series[:-1] * series[1:]) < 0)
    else:
        return 0

def spectral_energy(spectrum):
    """ Computes the total energy (sum of squares) in a series.
    
    Arguments:
    spectrum -- the points to analyze
    """
    return numpy.sum(numpy.square(spectrum))

def spectral_shape(spectrum, freqs):
    """ Calculates the spread and centroid of a spectrum.
    
    Arguments:
    spectrum -- a length (n) sequence of frequency bins
    freqs -- a length (n) mapping from frequency bin to central frequency
    """
    mu = 0
    sigma = 0
    spectrum = numpy.abs(spectrum)

    density = numpy.sum(spectrum)
    if (density > 0):
        mu = numpy.sum(spectrum * freqs) / density
        sigma = numpy.sum(spectrum * numpy.square(freqs - mu)) / density

    return (mu, sigma)

def make_freq_table(fs, N):
    """ Produces a mapping from DFT bins to central frequencies.
    
    The mapping will take the form of a numpy vector.
    
    Arguments:
    fs -- the sampling rate
    N -- the number of bins in the DFT
    
    Assumes: the DFT is non-hemitian
    Requires: N is even
    """
    assert(N % 2 == 0)
    
    if N == 0:
        return numpy.array([])
    else:
        delta_f = fs / float(N)
        f = lambda i: delta_f * (min(i, N - 1 - i) + 0.5)
        
        return numpy.fromfunction(numpy.vectorize(f), [N], dtype=numpy.int32)
