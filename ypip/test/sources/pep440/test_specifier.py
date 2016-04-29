import unittest
from ypip.sources.pep440.version import Version
from ypip.sources.pep440.specifier import Specifier
from ypip.sources.pep440.exceptions import ParseError


class TestSpecifier(unittest.TestCase):
    def test_bad_parse(self):
        # TODO Maybe flesh this out a bit...
        bad = ['', 'version 1', 'foo bar', '== 1.2.3-xyzzy', '=> 1.2', '== 1.2, foo']

        for x in bad:
            with self.assertRaises(ParseError):
                _ = Specifier(x)

    def test_equality(self):
        s = Specifier('== 1.2.3')

        self.assertTrue(s(Version('1.2.3')))
        self.assertTrue(s(Version('1.2.3.0')))
        self.assertFalse(s(Version('1.2')))
        self.assertFalse(s(Version('1.2.3.4')))

    def test_equality_wc(self):
        s = Specifier('== 1.2.*')

        self.assertTrue(s(Version('1.2')))
        self.assertTrue(s(Version('1.2.0')))
        self.assertTrue(s(Version('1.2.3.dev4')))
        self.assertFalse(s(Version('1.3')))

    def test_arbitrary_equality(self):
        s = Specifier('=== 1.2')

        # NOTE Not Fully Implemented
        # PEP440 allows arbitrary equality to accept equal strings, but
        # this implementation only allows for comparison against Version
        # objects (which will not parse arbitrary strings). The operator
        # is "heavily discouraged", so this seems mostly reasonable.
        self.assertTrue(s(Version('1.2')))
        self.assertTrue(s(Version('1.2.0'))) # Is this true?
        self.assertFalse(s(Version('1.2+foo')))
        self.assertFalse(s(Version('1.3')))

    def test_inequality(self):
        s = Specifier('!= 1.2')

        self.assertTrue(s(Version('1.1')))
        self.assertTrue(s(Version('1.3')))
        self.assertTrue(s(Version('1.2.1')))
        self.assertFalse(s(Version('1.2')))
        self.assertFalse(s(Version('1.2.0')))

    def test_inequality_wc(self):
        s = Specifier('!= 1.2.*')

        self.assertTrue(s(Version('1.1')))
        self.assertTrue(s(Version('1.3')))
        self.assertFalse(s(Version('1.2.1')))
        self.assertFalse(s(Version('1.2')))
        self.assertFalse(s(Version('1.2.0')))
        self.assertFalse(s(Version('1.2-3')))

    def test_lt(self):
        lt = Specifier('< 1.2')
        lte = Specifier('<= 1.2')

        self.assertTrue(lt(Version('1.0')))
        self.assertTrue(lte(Version('1.0')))
        self.assertFalse(lt(Version('1.2')))
        self.assertTrue(lte(Version('1.2')))
        self.assertFalse(lt(Version('1.2.0')))
        self.assertTrue(lte(Version('1.2.0')))
        self.assertFalse(lt(Version('1.3')))
        self.assertFalse(lte(Version('1.3')))

    def test_gt(self):
        gt = Specifier('> 1.2')
        gte = Specifier('>= 1.2')

        self.assertTrue(gt(Version('1.3')))
        self.assertTrue(gte(Version('1.3')))
        self.assertFalse(gt(Version('1.2')))
        self.assertTrue(gte(Version('1.2')))
        self.assertFalse(gt(Version('1.2.0')))
        self.assertTrue(gte(Version('1.2.0')))
        self.assertFalse(gt(Version('1.0')))
        self.assertFalse(gte(Version('1.0')))

    def test_compatible(self):
        s = Specifier('~= 1.2')

        self.assertTrue(s(Version('1.2')))
        self.assertTrue(s(Version('1.2.0')))
        self.assertTrue(s(Version('1.3')))
        self.assertFalse(s(Version('1.1')))

    def test_conjunction(self):
        s = Specifier('>= 1.0, < 2.0, != 1.2.*')

        self.assertFalse(s(Version('0.9')))
        self.assertTrue(s(Version('1.0')))
        self.assertTrue(s(Version('1.1')))
        self.assertFalse(s(Version('1.2')))
        self.assertFalse(s(Version('1.2.5')))
        self.assertTrue(s(Version('1.3')))
        self.assertTrue(s(Version('1.3.1')))
        self.assertTrue(s(Version('1.9.9.9.9')))
        self.assertFalse(s(Version('2.0')))


if __name__ == '__main__':
    unittest.main()
