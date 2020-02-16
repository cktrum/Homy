from SongsLibrary import SongsLibrary

class State:
    def __init__(self):
        self.library = SongsLibrary()

    def run(self):
        assert 0, "run not implemented"

    def transition(self, event):
        assert 0, "transition not implemented"

class StartUp(State):
    def run(self):
        # Send command to show welcome screen
        print("Welcome")

    def transition(self, event):
        if event == 'songs':
            return BrowsingSongs()

class BrowsingSongs(State):
    def run(self):
        response = self.library.get_list_of_songs()
        # Display all songs in response - send command

    def transition(self, event):
        if event == 'play_song':
            self.state = Playing()

class Playing(State):
    def run(self):
        print('Playing')

    def transition(self, event):
        assert 0, "not implemented"

class Runnable:
    def __init__(self):
        self.state = StartUp()
        self.state.run()

    def step(self, command):
        self.state = self.state.transition(command)
        self.state.run()