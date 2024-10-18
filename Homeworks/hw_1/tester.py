import unittest
import main
import time
import datetime
import tkinter as tk

class Tester(unittest.TestCase):
    def setUp(self):
        args = ['ivan', 'honsage', 'root.tar', 'main.py']
        self.shell = main.GUI(args, tk.Tk())
    
    def close(self):
        self.shell.close()
    
    def get_command_output(self, command):
        return self.shell.processer.process(command)
        
    def test_ls_bare(self):
        output = self.get_command_output("ls")
        self.close()
        self.assertIn('dir bin etc', output)

    def test_ls_parent(self):
        self.shell.processer.process("cd bin")
        output = self.get_command_output("ls ..")
        self.close()
        self.assertIn('dir bin etc', output)

    def test_ls_fullpath(self):
        self.shell.processer.process("cd bin")
        output = self.get_command_output("ls ~/etc/data")
        self.close()
        self.assertIn('table.csv inner', output)

    def test_cd_bare(self):
        self.shell.processer.process("cd")
        output = self.get_command_output("ls")
        self.close()
        self.assertIn('dir bin etc', output)
    
    def test_cd_direct(self):
        self.shell.processer.process("cd bin")
        output = self.get_command_output("ls ./")
        self.close()
        self.assertIn('text.txt code.c', output)

    def test_cd_parent(self):
        self.shell.processer.process("cd bin")
        self.shell.processer.process("cd ..")
        output = self.get_command_output("ls")
        self.shell.close()
        self.assertIn('dir bin etc', output)

    def test_cp_file_to_dir(self):
        self.shell.processer.process("cp bin/code.c ~/etc")
        output = self.get_command_output("ls ~/etc")
        self.shell.close()
        self.assertIn('code.c', output)

    def test_cp_dir_to_dir(self):
        self.shell.processer.process("cp ~/bin etc")
        output = self.get_command_output("ls ~/etc")
        self.shell.close()
        self.assertIn('bin', output)

    def test_cp_wrong(self):
        output = self.get_command_output("cp ~/bin ~/bin/data")
        self.shell.close()
        self.assertIn("There is no such file or directory with name '~/bin/data'", output)

    def test_uptime(self):
        output = self.get_command_output("uptime")
        self.shell.close()
        self.assertIn("sec", output)
    
    def test_uptime_2(self):
        output = self.get_command_output("uptime")
        cur_time = datetime.datetime.now().strftime("%H:%M")
        self.shell.close()
        self.assertIn(cur_time, output)

    def test_tree_full(self):
        output = self.get_command_output("tree")
        self.shell.close()
        self.assertIn("~\n|--dir\n|--bin\n|--|--text.txt\n|--|--code.c\n|--etc\n|--|--local\n|--|--|--script.bash\n|--|--data\n|--|--|--table.csv\n|--|--|--inner\n|--|--|--|--secret.txt", output)

    def test_tree_part(self):
        output = self.get_command_output("tree bin")
        self.shell.close()
        self.assertIn("bin\n|--text.txt\n|--code.c", output)

    def test_tree_wrong(self):
        output = self.get_command_output("tree home")
        self.shell.close()
        self.assertIn("There is no directory with name 'home'", output)

    
if __name__ == "__main__":
    unittest.main()