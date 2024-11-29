import unittest
import io
from contextlib import redirect_stdout 
import main

class Tester(unittest.TestCase):
    def setUp(self): 
        pass

    def test(self):
        self.assertIn(..., ...)

if __name__ == "__main__":
    unittest.main()