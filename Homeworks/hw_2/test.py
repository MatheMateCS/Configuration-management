import unittest
import io
from contextlib import redirect_stdout 
import main


class Tester(unittest.TestCase):
    def setUp(self):
        self.args = ['visualizer.py', 'test_repo', 'graph.mermaid', 'main']

    def test_wrong_pathes_1(self):
        f = io.StringIO()
        with redirect_stdout(f):
            main.get_commits_info(self.args[1], self.args[3])
        out = f.getvalue()
        print(out)
        pass

    def test_wrong_pathes_2(self):
        pass

    def test_non_existent_branch():
        pass

    def test_check_tree(self):
        # output = main.build_tree(main.get_commits_info(self.args[1], self.args[3]))
        # print(output)
        pass

    def test_succeed_writing(self):
        pass

    def test_fail_writing(self):
        pass

    def test_output(self):
        self.assertIn()
        pass

    def test_alright(self):
        pass
  
    
if __name__ == "__main__":
    unittest.main()