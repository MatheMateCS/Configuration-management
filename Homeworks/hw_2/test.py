import unittest
import io
import os
from contextlib import redirect_stdout 
import main


class Tester(unittest.TestCase):
    def setUp(self):
        self.args = ['visualizer.py', 'test_repo', 'graph.mermaid', 'master']
        self.io_manager = io.StringIO() 
        with open(os.path.join("test_broken_repo", "HEAD"), "w") as h:
            h.write("empty")

    def test_alright(self):
        with redirect_stdout(self.io_manager):
            main.write_to_file(self.args[2], main.build_tree(main.get_commits_info(self.args[1], self.args[3])))
        out = self.io_manager.getvalue()
        self.assertIn(f"Mermaid code of git commits graph was successfully saved into '{self.args[2]}'", out)

    def test_wrong_pathes_1(self):
        self.args[1] = "non-exictent"
        with redirect_stdout(self.io_manager):
            main.get_commits_info(self.args[1], self.args[3])
        out = self.io_manager.getvalue()
        self.assertIn("It seems that you've entered wrong path to repo.", out)

    def test_no_git_branches(self):
        self.args[1] = "test_broken_repo"
        with redirect_stdout(self.io_manager):
            main.get_commits_info(self.args[1], self.args[3])
        out = self.io_manager.getvalue()
        self.assertIn("Well, there is no git branches in this repo at all!", out)

    def test_wrong_pathes_2(self):
        with open(os.path.join("test_broken_repo", "HEAD"), "w") as h:
            h.write("ref: refs/heads/master")
        self.args[1] = "test_broken_repo"
        with redirect_stdout(self.io_manager):
            main.get_commits_info(self.args[1], self.args[3])
        out = self.io_manager.getvalue()
        self.assertIn("It seems that you've entered wrong path to repo.", out)

    def test_non_existent_branch(self):
        self.args[3] = "non-existent-branch"
        with redirect_stdout(self.io_manager):
            main.get_commits_info(self.args[1], self.args[3])
        out = self.io_manager.getvalue()
        self.assertIn(f"There is no branch with name '{self.args[3]}' in this git tree!", out)

    def test_check_tree(self):
        output = main.build_tree(main.get_commits_info(self.args[1], self.args[3]))
        self.assertIn("flowchart TD", output)

    def test_succeed_writing(self):
        with redirect_stdout(self.io_manager):
            main.write_to_file(self.args[2], main.build_tree(main.get_commits_info(self.args[1], self.args[3])))
        out = self.io_manager.getvalue()
        self.assertIn(f"Mermaid code of git commits graph was successfully saved into '{self.args[2]}'", out)
        self.assertIn(self.args[2], os.listdir(os.path.join(".", str(os.path).join(self.args[2].split(str(os.path))[:-1]))))

    def test_fail_writing(self):
        self.args[2] = "dir/non-existent.mermaid"
        with redirect_stdout(self.io_manager):
            main.write_to_file(self.args[2], main.build_tree(main.get_commits_info(self.args[1], self.args[3])))
        out = self.io_manager.getvalue()
        self.assertIn("It seems that you've entered wrong path to result file.", out)
        
    def test_output(self):
        output = main.build_tree(main.get_commits_info(self.args[1], self.args[3]))
        with open(self.args[2], "r") as res:
            result = res.read()
        self.assertIn(output, result)

      
if __name__ == "__main__":
    unittest.main()