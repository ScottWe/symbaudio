import os
import shutil
import tempfile
import unittest

import harness
import symbaudio.utils.filesystem

class CallCounter:
    """ A callable object which counts the number of times it is called. """

    def __init__(self):
        """ Sets the count to 0. """
        self.count = 0

    def __call__(self, *args):
        """ Intercepts each call with a counter increment. """
        self.count = self.count + 1

class TestApplyToFiles(unittest.TestCase):
    """ Validates the behaviour of apply_to_files over a temp dir. """

    def setUp(self):
        """ Sets up a temp dir for each test. """
        # Generates directory names
        self.tempdir = tempfile.mkdtemp()
        self.subdir = os.path.join(self.tempdir, "dir")
        self.emptydir = os.path.join(self.tempdir, "empty")
        # Populates directories
        os.makedirs(self.subdir)
        os.makedirs(self.emptydir)
        # Populates files
        self.root_fcount = 3
        self.nest_fcount = 5
        for i in range(0, self.root_fcount):
            with open(os.path.join(self.tempdir, "%i.txt" % i), "w+") as f:
                f.write("Test.")
        for i in range(0, self.nest_fcount):
            with open(os.path.join(self.subdir, "%i.txt" % i), "w+") as f:
                f.write("Test.")
        self.filename = os.path.join(self.subdir, "nontxt.mp3")
        with open(self.filename, "w+") as f:
            f.write("Test.")

    def tearDown(self):
    	""" Cleans up temporary directory. """
    	shutil.rmtree(self.tempdir)

    def run_scan(self, path, expt, ext=""):
        """ Scans a path and verifies the number of hits. """
        f = CallCounter()
        symbaudio.utils.filesystem.apply_to_files(path, ext, f, enable_logs=False)
        self.assertEqual(f.count, expt)


    def test_scan_empty_dir(self):
        """ Ensures scanning an empty directory is a no-op. """
        self.run_scan(self.emptydir, 0)

    def test_scan_file(self):
        """ Ensures scanning a file directly works. """
        self.run_scan(self.filename, 1)

    def test_scan_dir_files(self):
        """ Ensures we can scan a shallow directory of files. """
        self.run_scan(self.subdir, self.nest_fcount + 1)

    def test_scan_recursive(self):
        """ Ensures we can find files in a sub-directory. """
        self.run_scan(self.tempdir, self.root_fcount + self.nest_fcount + 1)

    def test_filtered_scan(self):
        """ Ensures filtering by extension works. """
        self.run_scan(self.tempdir, self.root_fcount + self.nest_fcount, ext=".txt")

if __name__ == '__main__':
    unittest.main()
