import os
import eyed3
import math

class SongsLibrary():
    def __init__():
        self.songs = []
        self.page = 0
        self.songsPerPage = 20
        self.nSongs = 0
        self.nPages = 0
        
    def setup(self, path):
        self.songs = self.read_directories(path)
        self.page = 0
        self.nSongs = len(songs)
        self.nPages = math.ceil(self.nSongs/self.songsPerPage)
        
    def read_directories(self, path):
        songs = []
        for root, dirs, files in os.walk("/media/pi/Seagate Backup Plus Drive/Music/"):
            for file in files:
                if file.endswith(".mp3"):
                    audiofile = eyed3.load(file)
                    artist = audiofile.tag.artist
                    title = audiofile.tag.title
                    songs.append({'title': title, 'artist': artist})
                    print(os.path.join(root, file))
        
        return songs
    
    def get_list_of_songs(self, page=None):
        
        if page is not None:
            self.page = page
            
        startIdx = self.page * self.songsPerPage
        endIdx = min(self.nSongs, startIdx + self.songsPerPage)
        
        
    def go_to_next_page(self):
        self.page = min(self.nPages, self.page + 1)
        
    def go_to_prev_page(self):
        self.page = max(0, self.page - 1)