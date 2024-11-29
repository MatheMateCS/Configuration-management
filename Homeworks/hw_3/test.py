import unittest
import io
from contextlib import redirect_stdout 
import main

test_simple = '''
    (def cnt 2)
    (def str 'Hello, World!')
    (def lst [3, -7, 2])
    (def map { name=> 'Ivan', age=>19 })
    '''
test_access = '''
    (def cnt 2)
    (def new $(cnt))
    (def arr [$(cnt), $(new)])
    '''

test_nesting = '''
    (def arr [2, 3])
    // There will be nesting!
    (def submap { val=>7, info=>'tomorrow' })
    (def map {
        arr => $(arr),
        son => $(submap)
    })
    '''

test_complex = '''
    // Kids in kindergarden
    (def age 6)
    (def Fedor { age=> 5, height=>125 })
    (def Anna { age=> 7, height => 140 })
    (def Boris { age => $(age), surname=>'Popov'})
    (def kids [$(Anna), $(Fedor), 'Yulia', $(Boris)])
    '''

translated_complex = '''
<number name='age'>6.0</number>
<dictionary name='Fedor'>
  <entry key='age'>
    <number>5.0</number>
  </entry>
  <entry key='height'>
    <number>125.0</number>
  </entry>
</dictionary>
<dictionary name='Anna'>
  <entry key='age'>
    <number>7.0</number>
  </entry>
  <entry key='height'>
    <number>140.0</number>
  </entry>
</dictionary>
<dictionary name='Boris'>
  <entry key='age'>
    <number>6.0</number>
  </entry>
  <entry key='surname'>
    <string>Popov</string>
  </entry>
</dictionary>
<array name='kids'>
  <dictionary>
    <entry key='age'>
      <number>7.0</number>
    </entry>
    <entry key='height'>
      <number>140.0</number>
    </entry>
  </dictionary>
  <dictionary>
    <entry key='age'>
      <number>5.0</number>
    </entry>
    <entry key='height'>
      <number>125.0</number>
    </entry>
  </dictionary>
  <string>Yulia</string>
  <dictionary>
    <entry key='age'>
      <number>6.0</number>
    </entry>
    <entry key='surname'>
      <string>Popov</string>
    </entry>
  </dictionary>
</array>
'''

test_name_not_declared = '''
    (def a $(b))
'''

test_comment_err = '''
    / There is a comment
'''

test_name_err = '''
    // Comment
    (def 2cnt 4)
'''

test_operator_err = '''
    (def map { val = 3, cnt=>5 })
'''

class Tester(unittest.TestCase):
    # Initial settings
    def setUp(self): 
        self.io_manager = io.StringIO() 
        self.converter = main.Converter()

    # Tests declaration of different types
    def test_simple(self):
        test_simple
        self.converter.load(test_simple)
        with redirect_stdout(self.io_manager):
            self.converter.convert()
        out = self.io_manager.getvalue()
        obj = ({'cnt': 2.0, 'str': "'Hello, World!'", 'lst': [3.0, -7.0, 2.0], 'map': {'name': "'Ivan'", 'age': 19.0}})
        self.assertDictEqual(obj, self.converter._constants)
        self.assertIn('Source code is syntactically correct', out)

    # Tests access to constant by '$(<name>)'
    def test_access(self):
        self.converter.load(test_access)
        with redirect_stdout(self.io_manager):
            self.converter.convert()
        out = self.io_manager.getvalue()
        obj = ({'cnt': 2.0, 'new': 'cnt', 'arr': ['cnt', 'new']})
        self.assertDictEqual(obj, self.converter._constants)
        self.assertIn('Source code is syntactically correct', out)

    # Tests nesting of arrays and dictionaries
    def test_nesting(self):
        self.converter.load(test_nesting)
        with redirect_stdout(self.io_manager):
            self.converter.convert()
        out = self.io_manager.getvalue()
        obj = ({'arr': [2.0, 3.0], 'submap': {'val': 7.0, 'info': "'tomorrow'"}, 'map': {'arr': 'arr', 'son': 'submap'}})
        self.assertDictEqual(obj, self.converter._constants)
        self.assertIn('Source code is syntactically correct', out)

    # Tests nesting and accessibility
    def test_complex(self):
        self.converter.load(test_complex)
        with redirect_stdout(self.io_manager):
            xml = self.converter.convert()
        out = self.io_manager.getvalue()
        obj = ({'age': 6.0, 'Fedor': {'age': 5.0, 'height': 125.0}, 'Anna': {'age': 7.0, 'height': 140.0}, 'Boris': {'age': 'age', 'surname': "'Popov'"}, 'kids': ['Anna', 'Fedor', "'Yulia'", 'Boris']})
        self.assertDictEqual(obj, self.converter._constants)
        self.assertIn('Source code is syntactically correct', out)
        self.assertIn(xml, translated_complex)

    # Tests error of non-declared constant name
    def test_name_not_declared(self):
        self.converter.load(test_name_not_declared)
        with redirect_stdout(self.io_manager):
            self.converter.convert()
        out = self.io_manager.getvalue()
        self.assertIn("There is no constant 'b' declared in this scope!", out)

    # Tests error of incorrect comment declaration
    def test_comment_err(self):
        self.converter.load(test_comment_err)
        with redirect_stdout(self.io_manager):
            self.converter.convert()
        out = self.io_manager.getvalue()
        self.assertIn("There is syntax error in 1 line", out)

    # Tests error of incorrect naming
    def test_name_err(self):
        self.converter.load(test_name_err)
        with redirect_stdout(self.io_manager):
            self.converter.convert()
        out = self.io_manager.getvalue()
        self.assertIn("There is syntax error in 2 line", out)

    # Tests error of incorrect assignment sign
    def test_operator_err(self):
        self.converter.load(test_operator_err)
        with redirect_stdout(self.io_manager):
            self.converter.convert()
        out = self.io_manager.getvalue()
        self.assertIn("There is syntax error in 1 line", out)

    # Tests output of failed converting
    def test_failure(self):
        self.converter.load(test_operator_err)
        with redirect_stdout(self.io_manager):
            xml = self.converter.convert()
        out = self.io_manager.getvalue()
        self.assertIn("There is syntax error in 1 line", out)
        self.assertIn("<!-- Parse error -->", xml)

if __name__ == "__main__":
    unittest.main()


