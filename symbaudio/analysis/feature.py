import numpy
import symbaudio.analysis.spectral

class FeatureAggregation:
    """ Describes the mean and modulation of a first-order statistic. """

    def __init__(self, x, fs):
        """ Generates second-order statitics.

        Arguments:
        x -- the time series's first-order statistics
        fs -- the downsampling rate for the first-order statistics
        """
        freqs = symbaudio.analysis.spectral.make_freq_table(fs, len(x))
        spectrum = numpy.fft.fft(x)
        mu, _ = symbaudio.analysis.spectral.spectral_shape(spectrum, freqs)
        self.mean = numpy.mean(x)
        self.modulation = mu

class FeatureSeries:
    """ Provides a structure for managing series of audio features. """

    FIELDS = ["centroid", "spread", "energy", "zeros"]

    def __init__(self, samps, size, fs):
        """ Creates a fixed length mapping of frames to features.

        Arguments:
        samps -- the number of samples being analyzed
        size -- the width of each frame
        fs -- the sample rate

        Note: this will truncate a partial window.
        """
        self.downsample_hz = fs / size
        self.count = int(samps / size)
        self.features = numpy.ndarray((self.count, len(FeatureSeries.FIELDS)))

    def record(self, n, centroid, spread, energy, zeros):
        """ Records a set of metrics to a given data frame.

        Arguments:
        n -- sthe index of the frame
        centroid -- the spectral centroid of the frame
        spread -- the spectral spread of the frame
        energy -- the total energy across the frame
        zeros -- the zero-crossing rate for the frame
        """
        self.features[n] = [centroid, spread, energy, zeros]

    def aggregate(self):
        """ Calculates statistics over this feature set.

        The result is a mapping from field name to FeatureAggregation. If there
        is an odd number of frames, the final frame is dropped.
        """
        agg = {}

        feature_count = (len(self.features) // 2) * 2
        for i in range(0, len(FeatureSeries.FIELDS)):
            field = FeatureSeries.FIELDS[i]
            seq = self.features[:feature_count,i]
            agg[field] = FeatureAggregation(seq, self.downsample_hz)

        return agg

class AudioSummary:
    """ Produces first and second order statistics about the audio. """

    def __init__(self, audio, framesize=1024, chan=0):
        """ Processes the audio across adjacent, fixed witdth windows.

        All analysis is performed in mono.

        Arguments:
        audio -- the file to analyze
        framesize -- keyword argument to adjust the window width (default: 1024)
        chan -- keyword argument to select analysis channel (default: 0)

        Note: A trailing, odd sample will be truncated in the analysis.
        """
        assert(framesize > 0)
        assert(framesize % 2 == 0)
        assert(0 <= chan and chan < audio.channel_count)

        freqs = symbaudio.analysis.spectral.make_freq_table(audio.sample_rate_hz, framesize)

        self.length_s = audio.sample_count / audio.sample_rate_hz

        frames = FeatureSeries(audio.sample_count, framesize, audio.sample_rate_hz)
        for n in range(0, frames.count):
            framestart = n * framesize
            temporal_frame = audio.raw[framestart:framestart+framesize, chan]
            if len(temporal_frame) % 2 == 1:
                temporal_frame = temporal_frame[:-1]
            spectral_frame = numpy.absolute(numpy.fft.fft(temporal_frame))

            (mu, sigma) = symbaudio.analysis.spectral.spectral_shape(spectral_frame, freqs)
            eng = symbaudio.analysis.spectral.spectral_energy(spectral_frame)
            zc = symbaudio.analysis.spectral.zcr(temporal_frame)
            frames.record(n, mu, sigma, eng, zc)
        self.second_order = frames.aggregate()
