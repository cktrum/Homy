import os
import sys
import eyed3
import math
import traceback
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship

Base = declarative_base()

    
class Artist(Base):
    __tablename__ = "artist"
    name = Column(String(100), primary_key=True)
    
class Album(Base):
    __tablename__ = "album"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

class Song(Base):
    __tablename__ = "song"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    artist_id = Column(String(100), ForeignKey('artist.name'))
    filepath = Column(String(500), nullable=False)
    length = Column(Integer)
    album_id = Column(String(100), ForeignKey('album.id'))
    artist = relationship(Artist)
    album = relationship(Album)


class SongsLibrary():
    def __init__(self):
        self.songs = []
        self.page = 0
        self.songsPerPage = 20
        self.nSongs = 0
        self.nPages = 0
        engine = create_engine('sqlite:///SongsLibrary')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()
        
    def create_database(self):
        engine = create_engine('sqlite:///SongsLibrary')
        Base.metadata.create_all(engine)
        
    def update_database(self, path=None):
        
        if path is None:
                path = "/media/pi/Seagate Backup Plus Drive/Music/"
            
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".mp3"):
                    path = os.path.join(root, file)
                    
                    try:
                        audiofile = eyed3.load(os.path.join(root, file))
                        artist = audiofile.tag.artist
                        title = audiofile.tag.title
                        album = audiofile.tag.album
                        if title is None or artist is None or album is None:
                            continue
                        new_artist = Artist(name=artist)
                        artist_obj = session.merge(new_artist)
                        new_album = Album(name=album)
                        album_obj = session.merge(new_album)
                        session.flush()
                        new_song = Song(artist=artist_obj, title=title, album=album_obj, filepath=path)
                        session.merge(new_song)
                        print(path)
                    except:
                        tb = traceback.format_exc()
                        print(tb)
                        continue
        session.commit()
        
    def setup(self, path=None):
        self.songs = self.read_directories(path)
        self.page = 0
        self.nSongs = len(self.songs)
        self.nPages = math.ceil(self.nSongs/self.songsPerPage)
        
    def read_directories(self, path=None):
        songs = []
        if path is None:
            path = "/media/pi/Seagate Backup Plus Drive/Music/"
        
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".mp3"):
                    print(os.path.join(root, file))
                    try:
                        audiofile = eyed3.load(os.path.join(root, file))
                        artist = audiofile.tag.artist
                        title = audiofile.tag.title
                        songs.append({'title': title, 'artist': artist})
                    except:
                        continue
                    
        return songs
    
    def get_list_of_artists(self, page=None):
        if page is not None:
            self.page = page
            
        offset = self.page * self.songsPerPage
        limit = self.songsPerPage
        query = self.session.query(Artist).order_by(Artist.name.asc()).limit(limit).offset(offset)
        
        artists = []
        for row in query:
            artists.append(row.name)
            
        return artists
    
    def get_list_of_songs(self, page=None, limit=None, offset=None):
        
        if page is not None:
            self.page = page
            
        if offset is None:
            offset = self.page * self.songsPerPage
        if limit is None:
            limit = self.songsPerPage
        query = self.session.query(Song).order_by(Song.title.asc()).limit(limit).offset(offset)
        
        songs = []
        for row in query:
            songs.append({'title': row.title, 'artist': row.artist.name, 'album': row.album.name, 'path': row.filepath})
            
        return songs
        
    def go_to_next_page(self):
        self.page = min(self.nPages, self.page + 1)
        
    def go_to_prev_page(self):
        self.page = max(0, self.page - 1)