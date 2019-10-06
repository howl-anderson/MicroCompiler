from MicroCompiler.SkeletonParser import SkeletonParser, Token


def test_simple(datadir):
    token_list = [Token("num", 6), Token("/"), Token("num", 2), Token("<EOF>")]

    sp = SkeletonParser(datadir / "output.yaml", token_list)
    assert sp.parse()
