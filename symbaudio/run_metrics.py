"""
This script recursively scans a directory. For ever *.wav file found, the file
is passed through the feature analysis framework, and the results are logged to
stdout. A log to stderr will display the current file being analyzed.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import symbaudio.analysis.audio
import symbaudio.analysis.feature
import symbaudio.utils.filesystem

_LOG_FMT = "%s %f %i %f %f %f %f %f %f %f %f"

def analyze_file(target, rel):
    """ Aggregates metrics on an audio file, and writes to stdout.

    Conforms to the apply_to_files signature. Assumes target is a wave file.

    Arguments:
    target -- the file to scan
    rel -- the relative path of the file, in reference to the root
    """
    audio = symbaudio.analysis.audio.AudioFile(target)
    summary = symbaudio.analysis.feature.AudioSummary(audio)
    secs = summary.length_s
    rate = audio.sample_rate_hz
    c_avg = summary.second_order["centroid"].mean
    c_mod = summary.second_order["centroid"].modulation
    s_avg = summary.second_order["spread"].mean
    s_mod = summary.second_order["spread"].modulation
    p_avg = summary.second_order["energy"].mean
    p_mod = summary.second_order["energy"].modulation
    z_avg = summary.second_order["zeros"].mean
    z_mod = summary.second_order["zeros"].modulation
    print(_LOG_FMT % (rel, secs, rate, c_avg, c_mod, s_avg, s_mod, p_avg, p_mod, z_avg, z_mod))

def main():
    """ Initiates a recursive scan, using sys.argv[1] as a root. """
    symbaudio.utils.filesystem.apply_to_files(sys.argv[1], ".wav", analyze_file)

if __name__ == "__main__":
    main()
else:
    raise ImportError("run_metrics is a script and should not be imported.")
