import unittest

from MicroCompiler.SkeletonParser import SkeletonParser, Token


class TestSkeletonParser(unittest.TestCase):
    def test_simple(self):
        token_list = [Token("num", 6), Token("/"), Token("num", 2), Token("<EOF>")]

        sp = SkeletonParser("output.yaml", token_list)
        self.assertTrue(sp.parse())
