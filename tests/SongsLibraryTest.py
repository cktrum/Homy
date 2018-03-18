import unittest
import pdb

from .context import bluetoothSrv

class SongsLibraryTest(unittest.TestCase):
    # execute tests with python -m tests.SongsLibraryTest
    def setUp(self):
        self.lib = bluetoothSrv.SongsLibrary()
        
    def tearDown(self):
        self.lib = None
    
    ### SONGS ###
    def test_receive_songs_correct_type(self):
        songs = self.lib.get_list_of_songs()
        self.assertIsInstance(songs, list)
        
    def test_receive_songs_correct_format(self):
        songs = self.lib.get_list_of_songs()
        self.assertIn('title', songs[0])
        self.assertIn('artist', songs[0])
        self.assertIn('album', songs[0])
        self.assertIn('path', songs[0])
        self.assertIn('length', songs[0])
        
    def test_receive_songs_limit_parameter(self):
        nSongs = 10
        songs = self.lib.get_list_of_songs(limit=nSongs)
        self.assertEqual(len(songs), nSongs)
        
    def test_receive_songs_offset_parameter(self):
        offset = 0
        songs_before = self.lib.get_list_of_songs(offset=offset)
        offset = 2
        songs_after = self.lib.get_list_of_songs(offset=offset)
        self.assertEqual(songs_before[offset], songs_after[0])
        
    def test_receive_songs_negative_parameters(self):
        offset = -1
        limit = -10
        songs = self.lib.get_list_of_songs(offset=offset, limit=limit)
        self.assertIsInstance(songs, list)
        self.assertEqual(len(songs), 0)

    def test_receive_songs_by_letter(self):
        letter = 'h'
        songs = self.lib.get_list_of_songs_by_letter(letter=letter)
        self.assertIsInstance(songs, list)
        self.assertEqual(songs[0][0], letter)
        self.assertEqual(songs[-1][0], letter)

    def test_receive_songs_of_album(self):
        album = 'Word of Mouth'
        songs = self.lib.get_list_of_songs_by_album(album=album)
        self.assertIsInstance(songs, list)
        for i in range(1, len(songs)):
            self.assertEqual(songs[i]['album'].lower(), album.lower())

    def test_receive_songs_of_album_case_sensitivity(self):
        album = 'word of mouth'
        songs = self.lib.get_list_of_songs_by_album(album=album)
        for i in range(1, len(songs)):
            self.assertEqual(songs[i]['album'].lower(), album)

    ### ARTISTS ###       
    def test_receive_artists_correct_type(self):
        artists = self.lib.get_list_of_artists()
        self.assertIsInstance(artists, list)
    
    def test_receive_artists_limit_parameter(self):
        nArtists = 15
        artists = self.lib.get_list_of_artists(limit=nArtists)
        self.assertEqual(len(artists), nArtists)
        
    def test_receive_artist_no_limit_parameter(self):
        artists = self.lib.get_list_of_artists()
        nItemsPerPage = self.lib.get_items_per_page()
        self.assertEqual(len(artists), nItemsPerPage)
        
    def test_receive_artists_offset_parameter(self):
        offset = 5
        artists_before = self.lib.get_list_of_artists()
        artists_offset = self.lib.get_list_of_artists(offset=offset)
        self.assertEqual(artists_before[offset], artists_offset[0])
        
    def test_receive_artists_higher_limit_than_artists(self):
        nArtistsInDatabase = self.lib.get_total_number_of_artists()
        limit = nArtistsInDatabase + 1
        artists = self.lib.get_list_of_artists(limit=limit)
        self.assertEqual(len(artists), nArtistsInDatabase)
    
    def test_receive_artists_higher_offset_than_artists(self):
        nArtistsInDatabase = self.lib.get_total_number_of_artists()
        offset = nArtistsInDatabase + 1
        artists = self.lib.get_list_of_artists(offset=offset)
        self.assertEqual(len(artists), 0)
        
    def test_receive_artists_out_of_bounds(self):
        nArtistsInDatabase = self.lib.get_total_number_of_artists()
        offset = nArtistsInDatabase - 5
        limit = 20
        artists = self.lib.get_list_of_artists(offset=offset, limit=limit)
        self.assertEqual(len(artists), 5)
        
if __name__ == '__main__':
    #suite = unittest.TestLoader().loadTestsFromTestCase(SongsLibraryTest)
    #suite.run()
    unittest.main()
