import unittest

from .context import bluetoothSrv

class SongsLibraryTest(unittest.TestCase):
    # execute tests with python -m tests.SongsLibraryTest
    def setUp(self):
        self.lib = bluetoothSrv.SongsLibrary()
        
    def tearDown(self):
        self.lib = None
    
    def test_receiving_of_songs(self):
        songs = self.lib.get_list_of_songs()
        self.assertIsInstance(songs, dict)
        
if __name__ == '__main__':
    #suite = unittest.TestLoader().loadTestsFromTestCase(SongsLibraryTest)
    #suite.run()
    unittest.main()
