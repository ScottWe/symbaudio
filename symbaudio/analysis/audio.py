import scipy.io.wavfile

class AudioFile:
    """ Wrapper class for raw scipy wave files. """
    
    def __init__(self, fn):
        """ Opens and mem-maps an audio file into Python.

        By mem-mapping the audio file, a file may be accessed in terms of
        frames, with negligible memory overhead.

        The resulting class will expose fields:
        sample_rate_hz -- the rate at which the wave is sampled, in Hertz
        sample_count -- the number of samples taken to produce the wave file
        channel_count -- the number of channels encoded in each sample
        raw -- the time-series of nd samples, given as a numpy matrix

        Arguments:
        fn -- a relative or absolute path to the wave file
        """
        self.sample_rate_hz, self.raw = scipy.io.wavfile.read(fn, mmap = True)
        self.sample_count, self.channel_count = self.raw.shape
