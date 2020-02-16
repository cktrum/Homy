import unittest

from bluetoothSrv.StateMachine import StateMachine

class StateMachineTest(unittest.TestCase):
    def setUp(self):
        self.state_machine = bluetoothSrv.StateMachine()

    def tearDown(self):
        self.state_machine

    def test_initial_state(self):
        self.assertEqual(typeof(self.state_machine.state), bluetoothSrv.StartUp())
    