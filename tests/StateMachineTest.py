import unittest
import os

from bluetoothSrv.StateMachine import *

class StateMachineTest(unittest.TestCase):
    def setUp(self):
        current_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
        config = {
            "songLibraryPath": os.path.join(current_path, "SongsLibrary.db"),
            "mediaPath": ""
        }
        self.state_machine = Runnable(config=config)

    def tearDown(self):
        self.state_machine = None

    def test_initial_state(self):
        self.assertEqual(type(self.state_machine.state), type(StartUp()))

    def test_transition_from_initial_state(self):
        self.assertEqual(type(self.state_machine.state), type(StartUp()))

        self.state_machine.step("songs")
        self.assertEqual(type(self.state_machine.state), type(BrowsingSongs()))
    