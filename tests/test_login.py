from aliasupdater.login import authenticate
import os
import unittest



class TestStringMethods(unittest.TestCase):

    def test_login(self):
        login = authenticate(os.environ.get("arcgis_portal_url"), os.environ.get("arcgis_user_name"), os.environ.get("arcgis_user_password"))
        self.assertIsNotNone(login, "The returned instance must not be None!")
        
        self.assertIsNotNone(login.users.me, "The authenticated user must not be None!")
        """
        with self.assertRaises(TypeError):
            pass
        """
        


if __name__ == "__main__":
    unittest.main()