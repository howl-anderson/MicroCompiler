import unittest

from .SkeletonParser import SkeletonParser


class TestSkeletonParser(unittest.TestCase):
    def test_simple(self):
        sp = SkeletonParser("output.yaml", ['num', '/', 'num', '<EOF>'])
        self.assertTrue(sp.parse())
