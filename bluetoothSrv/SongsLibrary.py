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

import pdb

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
        self.itemsPerPage = 20
        self.nSongs = 0
        self.nPages = 0
        try:
            engine = create_engine('sqlite:////home/pi/Documents/SongsLibrary.db')
            Base.metadata.bind = engine
            DBSession = sessionmaker(bind=engine)
            self.session = DBSession()
        except:
            self.session = None
        
    def create_database(self):
        engine = create_engine('sqlite:////home/pi/Documents/SongsLibrary.db')
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
                        artist_obj = self.session.merge(new_artist)
                        new_album = Album(name=album)
                        album_obj = self.session.merge(new_album)
                        self.session.flush()
                        new_song = Song(artist=artist_obj, title=title, album=album_obj, filepath=path)
                        self.session.merge(new_song)
                        print(path)
                    except:
                        tb = traceback.format_exc()
                        print(tb)
                        continue
        self.session.commit()
    
    def get_list_of_artists(self, page=None):
        if page is not None:
            self.page = page
            
        offset = self.page * self.itemsPerPage
        limit = self.itemsPerPage
        query = self.session.query(Artist).order_by(Artist.name.asc()).limit(limit).offset(offset)
        
        artists = []
        for row in query:
            artists.append(row.name)
            
        return artists
    
    def get_list_of_songs(self, page=None, limit=None, offset=None):
        
        if page is not None:
            self.page = page
            
        if offset is None:
            offset = self.page * self.itemsPerPage
        if limit is None:
            limit = self.itemsPerPage
        pdb.set_trace()
        query = self.session.query(Song).order_by(Song.title.asc()).limit(limit).offset(offset)
        
        songs = []
        for row in query:
            songs.append({'title': row.title, 'artist': row.artist.name, 'album': row.album.name, 'path': row.filepath})
            
        return songs
        
    def go_to_next_page(self):
        self.page = min(self.nPages, self.page + 1)
        
    def go_to_prev_page(self):
        self.page = max(0, self.page - 1)