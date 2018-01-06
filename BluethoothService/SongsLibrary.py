import os

class SongsLibrary():
    def __init__():
        self.page = 0
        self.songsPerPage = 0
        self.nSongs = 0
        
    def setup(self, path):
        files = self.read_directories(path)
        self.page = 1
        self.nSongs = len(files)
        
    def read_directories(self, path):
        songs = []
        for root, dirs, files in os.walk("/media/"):
            for file in files:
                if file.endswith(".mp3"):
                     songs.append(file)
                     print(os.path.join(root, file))
