from aliasupdater.login import authenticate
import unittest



class TestStringMethods(unittest.TestCase):

    def test_login(self):
        self.assertEqual('foo'.upper(), 'FOO')
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

        """
        with self.assertRaises(TypeError):
            pass
        """
        


if __name__ == '__main__':
    unittest.main()