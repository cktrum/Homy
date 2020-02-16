import os
import sys
import eyed3
import math
import traceback
import json
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
    def __init__(self, config=None):
        self.songs = []
        self.SongPage = 0
        self.ArtistPage = 0
        self.itemsPerPage = 20
        self.nSongs = 0
        self.nArtists = 0
        self.config = config    
        if not config:
            try:
                self.config = self.read_config()
            except Exception as e:
                print("Error reading config", e)
                self.session = None
                return

        try:
            engine = create_engine('sqlite:///' + self.config['songLibraryPath'])
            Base.metadata.bind = engine
            DBSession = sessionmaker(bind=engine)
            self.session = DBSession()
            
            self.nArtists = self.session.query(Artist).count()
            self.nSongs = self.session.query(Song).count()
        except Exception as e:
            print("Error creating database engine", e)
            self.session = None
    
    def read_config(self):
        data = dict()
        current_path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(current_path, 'config.json')) as config_file:
            data = json.load(config_file)
        return data

    def get_items_per_page(self):
        return self.itemsPerPage
    
    def create_database(self):
        engine = create_engine('sqlite:///' + self.config['songLibraryPath'])
        Base.metadata.create_all(engine)
        
    def update_database(self, path=None):
        
        if path is None:
            path = self.config['mediaPath']
            
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".mp3"):
                    path = os.path.join(root, file)
                    
                    try:
                        audiofile = eyed3.load(os.path.join(root, file))
                        artist = audiofile.tag.artist
                        title = audiofile.tag.title
                        album = audiofile.tag.album
                        length = audiofile.info.time_secs
                        if title is None or artist is None or album is None:
                            continue
                        new_artist = Artist(name=artist)
                        artist_obj = self.session.merge(new_artist)
                        new_album = Album(name=album)
                        album_obj = self.session.merge(new_album)
                        self.session.flush()
                        new_song = Song(artist=artist_obj, title=title, album=album_obj, filepath=path, length=length)
                        self.session.merge(new_song)
                        print(path)
                    except:
                        tb = traceback.format_exc()
                        print(tb)
                        continue
        self.session.commit()     
    
    def get_total_number_of_artists(self):
        return self.nArtists
    
    def get_total_number_of_songs(self):
        return self.nSongs
    
    def get_number_of_pages(self, item=None):
        if item == 'Song':
            return math.ceil(self.nSongs / self.itemsPerPage)
        elif item == 'Artist':
            return math.ceil(self.nArtists / self.itemsPerPage)
        return 0
    
    def get_list_of_artists(self, limit=None, offset=None):
        offset,limit = self.validate_offset_and_limit(offset, limit, 'Artist')
            
        query = self.session.query(Artist).order_by(Artist.name.asc()).limit(limit).offset(offset)
        
        artists = []
        for row in query:
            artists.append(row.name)
            
        return artists
    
    def get_list_of_songs(self, limit=None, offset=None):
        offset,limit = self.validate_offset_and_limit(offset, limit, 'Song')
        
        query = self.session.query(Song).order_by(Song.title.asc()).limit(limit).offset(offset)
        return self.format_songs_from_query(query)

    def get_list_of_songs_by_letter(self, letter, limit=None, offset=None):
        offset,limit = self.validate_offset_and_limit(offset, limit, 'Song')

        if letter is None:
            return []

        query = self.session.query(Song).filter(Song.title.like(letter + '%')).limit(limit).offset(offset)
        return self.format_songs_from_query(query)

    def get_list_of_songs_by_album(self, album, limit=None, offset=None):
        offset,limit = self.validate_offset_and_limit(offset, limit, 'Song')

        if album is None:
            return []

        album = album.lower()
        query = self.session.query(Song).join(Song.album).filter(Album.name.like(album)).limit(limit).offset(offset)
        return self.format_songs_from_query(query)
        
    def reset_page(self, item=None):
        if item == 'Song':
            self.SongPage = 0
        elif item == 'Artist':
            self.ArtistPage = 0
        
    def go_to_next_page(self, item=None):
        nPages = self.get_number_of_pages(item)
        if item == 'Song':
            self.SongPage = min(nPages, self.SongPage + 1)
        elif item == 'Artist':
            self.ArtistPage = min(nPages, self.ArtistPage + 1)
        
    def go_to_prev_page(self, item=None):
        if item == 'Song':
            self.SongPage = max(0, self.SongPage - 1)
        elif item == 'Artist':
            self.ArtistPage = min(0, self.ArtistPage - 1)

    def validate_offset_and_limit(self, offset, limit, item=None):
        page = 0
        if item == 'Song':
            page = self.SongPage
        elif item == 'Artist':
            page = self.ArtistPage
        if offset is None:
            offset = page * self.itemsPerPage
        if limit is None:
            limit = self.itemsPerPage
            
        if limit < 0:
            limit = 0
        if offset < 0:
            offset = 0

        return (offset, limit)

    def format_songs_from_query(self, query_result):
        songs = []
        for row in query_result:
            songs.append({
                'title': row.title,
                'artist': row.artist.name,
                'album': row.album.name,
                'path': row.filepath,
                'length': row.length
            })
            
        return songs