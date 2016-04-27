import unittest
from ypip.sources.pep440.version import Version, ParseError


class TestVersionParsing(unittest.TestCase):
    def test_bad_parse(self):
        # TODO Maybe flesh this out a bit...
        bad = ['', 'version 1', 'foo bar', '1.2.3-xyzzy']

        for x in bad:
            with self.assertRaises(ParseError):
                _ = Version(x)

    def test_initial_v(self):
        with_v = 'v1.2.3'
        without_v = '1.2.3'

        self.assertEqual(Version(with_v), Version(without_v))

    def test_epoch(self):
        versions = {
            '1':     None,
            '1!1':   1,
            '123!1': 123
        }

        for s, t in versions.items():
            v = Version(s)
            self.assertEqual(v.epoch, t)

        with self.assertRaises(ParseError):
            _ = Version('foo!1')

    def test_release(self):
        versions = {
            '3':          (3,),
            '3.1':        (3, 1),
            '3.1.41':     (3, 1, 41),
            '3.141.59.2': (3, 141, 59, 2)
        }

        for s, t in versions.items():
            v = Version(s)
            self.assertEqual(v.release, t)

    def test_pre(self):
        versions = {
            '1':        None,
            '1a':       ('a', 0),
            '1alpha':   ('a', 0),
            '1-a1':     ('a', 1),
            '1_a12':    ('a', 12),
            '1.a123':   ('a', 123),
            '1AlPhA':   ('a', 0),
            '1b':       ('b', 0),
            '1beta':    ('b', 0),
            '1rc':      ('rc', 0),
            '1pre':     ('rc', 0),
            '1preview': ('rc', 0)
        }

        for s, t in versions.items():
            v = Version(s)
            self.assertEqual(v.pre, t)

    def test_post(self):
        versions = {
            '1':         None,
            '1post':     0,
            '1post1':    1,
            '1r':        0,
            '1r1':       1,
            '1rev':      0,
            '1rev1':     1,
            '1.post1':   1,
            '1-post12':  12,
            '1_post123': 123,
            '1-1':       1
        }

        for s, t in versions.items():
            v = Version(s)
            self.assertEqual(v.post, t)

        with self.assertRaises(ParseError):
            _ = Version('1-')

    def test_dev(self):
        versions = {
            '1':      None,
            '1dev':   0,
            '1dev1':  1,
            '1.dev1': 1,
            '1-dev1': 1,
            '1_dev1': 1
        }

        for s, t in versions.items():
            v = Version(s)
            self.assertEqual(v.dev, t)

    def test_local(self):
        versions = {
            '1':         None,
            '1+foo':     ('foo',),
            '1+foo.bar': ('foo', 'bar'),
            '1+foo.123': ('foo', 123),
            '1+a.b.c':   ('a', 'b', 'c'),
            '1+a-b_c':   ('a', 'b', 'c')
        }

        for s, t in versions.items():
            v = Version(s)
            self.assertEqual(v.local, t)

        bad_versions = ['1+', '1+.', '1+a.', '1+-a']

        for v in bad_versions:
            with self.assertRaises(ParseError):
                _ = Version(v)

    def test_complex_normalise(self):
        # A version string has one compulsory part and five optional
        # parts. Thus, there are 2^5 (32) possible combinations...
        for epoch in ['', '1!']:
            for pre in ['', 'a0']:
                for post in ['', '.post0']:
                    for dev in ['', '.dev0']:
                        for local in ['', '+foo']:
                            version = '{}1{}{}{}{}'.format(epoch, pre, post, dev, local)
                            self.assertEqual(str(Version(version)), version)


class TestVersionOrdering(unittest.TestCase):
    def test_epoch(self):
        self.assertTrue(Version('1!1') == Version('1!1'))
        self.assertTrue(Version('2!1') > Version('1!1') > Version('1'))
        self.assertTrue(Version('1') < Version('1!1') < Version('2!1'))

    def test_release(self):
        self.assertTrue(Version('1') == Version('1'))
        self.assertTrue(Version('2') > Version('1'))
        self.assertTrue(Version('1') < Version('2'))

        self.assertTrue(Version('1.1') == Version('1.1'))
        self.assertTrue(Version('1') < Version('1.1') < Version('1.2'))
        self.assertTrue(Version('1.2') > Version('1.1') > Version('1'))

        self.assertTrue(Version('1.1.1') == Version('1.1.1'))
        self.assertTrue(Version('1.1') < Version('1.1.1') < Version('1.1.2'))
        self.assertTrue(Version('1.1.2') > Version('1.1.1') > Version('1.1'))

if __name__ == '__main__':
    unittest.main()
