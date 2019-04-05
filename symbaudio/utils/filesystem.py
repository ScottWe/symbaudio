import os
import sys

def _scan_dir(f, ext, path, rel, logs):
    """ Recursive implemntation of apply_to_files.

    Argument
    f -- a function to apply to each matching file
    ext -- the extension to match
    path -- the directory/file to start the scan from
    rel -- the relative path of the file, in reference to the root
    """
    target = path
    if len(rel) > 0:
        target = os.path.join(path, rel)
    if os.path.isfile(target):
        if len(ext) == 0 or target[-len(ext):] == ext:
            if logs: sys.stderr.write("%s\n" % rel)
            f(target, rel)
    elif os.path.isdir(target):
        for fn in os.listdir(target):
            _scan_dir(f, ext, path, os.path.join(rel, fn), logs)

def apply_to_files(path, ext, f, enable_logs=True):
    """ Runs a recursive directory scan from a given directory.

    The extension of the file may be specified. A lambda will be applied to each
    file which matches.

    Arguments:
    path -- the directory/file to start the scan from
    ext -- the extension to match
    f -- a function to apply to each matching file
    enable_logs -- logs each file to stderr (default: True)
    """
    _scan_dir(f, ext, path, "", enable_logs)
