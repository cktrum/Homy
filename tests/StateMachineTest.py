import unittest

from bluetoothSrv.StateMachine import *

class StateMachineTest(unittest.TestCase):
    def setUp(self):
        self.state_machine = Runnable()

    def tearDown(self):
        self.state_machine = None

    def test_initial_state(self):
        self.assertEqual(type(self.state_machine.state), type(StartUp()))

    def test_transition_from_initial_state(self):
        self.assertEqual(type(self.state_machine.state), type(StartUp()))

        self.state_machine.step("songs")
        self.assertEqual(type(self.state_machine.state), type(BrowsingSongs()))
    