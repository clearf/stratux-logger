import unittest

import emulator


class EmulatorTestCase(unittest.TestCase):

    def setUp(self):
        self.app = emulator.app.test_client()

    def test_index(self):
        rv = self.app.get('/')
        self.assertIn('Welcome to Stratux Emulator', rv.data.decode())


if __name__ == '__main__':
    unittest.main()
