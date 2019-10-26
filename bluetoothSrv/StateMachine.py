from SongsLibrary import *

class State:
    def __init__(self):
        self.library = SongsLibrary()
        self.library.setup()

    def run(self, command):
        assert 0, "run not implemented"

    def transition(self, event):
        assert 0, "run not implemented"

class StartUp(State):
    def run(self, command):
        switcher = {
            "songs": (self.library.get_list_of_songs, 'selected_songs'),
            "artists": (self.library.get_list_of_artists, 'selected_artists')
        }
        
        (command, event) = switcher.get(data, lambda: ("nothing", None))
        response = command()

        if event:
            self.transition(event)

    def transition(self, event):
        if event == 'selected_songs':
            self.state = BrowsingSongs()

class BrowsingSongs(State):
    def run(self, command):
        print('BrowsingSongs')

    def transition(self, event):
        if event == 'play_song':
            self.state = Playing()

class Playing(State):
    def run(self, command):
        print('Playing')

    def transition(self, event):
        assert 0, "not implemented"

class Runnable:
    def __init__(self):
        self.state = StartUp()

    def step(self, command):
        response = self.state.run(command)
        self.state.transition()
        return response