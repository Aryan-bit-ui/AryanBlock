"""
Tests for the AryanBlock Interpreter
"""

import pytest
import sys
import os
from io import StringIO

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from lexer import Lexer
from parser import Parser
from interpreter import Interpreter


def run(source: str) -> any:
    """Helper to run source code."""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens, source.split('\n'))
    program = parser.parse()
    interpreter = Interpreter()
    return interpreter.interpret(program, source)


def capture_output(source: str) -> str:
    """Run code and capture stdout."""
    import sys
    from io import StringIO
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        run(source)
        output = sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout
    
    return output


class TestInterpreter:
    """Test cases for the Interpreter."""
    
    def test_integer_arithmetic(self):
        """Test integer arithmetic."""
        assert run('start { let x = 2 + 3 }') is None  # No return
    
    def test_variable_access(self):
        """Test variable declaration and access."""
        output = capture_output('start { let x = 42 \n print(x) }')
        assert "42" in output
    
    def test_string_concatenation(self):
        """Test string concatenation."""
        output = capture_output('start { print("Hello, " + "World!") }')
        assert "Hello, World!" in output
    
    def test_string_interpolation(self):
        """Test string interpolation."""
        output = capture_output('start { let name = "Alice" \n print("Hi, ${name}!") }')
        assert "Hi, Alice!" in output
    
    def test_boolean_operations(self):
        """Test boolean operations."""
        output = capture_output('start { print(true and false) }')
        assert "false" in output
        
        output = capture_output('start { print(true or false) }')
        assert "true" in output
    
    def test_comparison(self):
        """Test comparison operators."""
        output = capture_output('start { print(5 > 3) }')
        assert "true" in output
        
        output = capture_output('start { print(5 == 5) }')
        assert "true" in output
    
    def test_if_statement(self):
        """Test if statement."""
        output = capture_output('''
        start {
            let x = 10
            if x > 5 {
                print("big")
            } else {
                print("small")
            }
        }
        ''')
        assert "big" in output
    
    def test_for_loop(self):
        """Test for loop."""
        output = capture_output('''
        start {
            for i in 0..3 {
                print(i)
            }
        }
        ''')
        assert "0" in output
        assert "1" in output
        assert "2" in output
    
    def test_while_loop(self):
        """Test while loop."""
        output = capture_output('''
        start {
            mut i = 0
            while i < 3 {
                print(i)
                i += 1
            }
        }
        ''')
        assert "0" in output
        assert "1" in output
        assert "2" in output
    
    def test_loop_statement(self):
        """Test loop N times."""
        output = capture_output('''
        start {
            mut count = 0
            loop 5 {
                count += 1
            }
            print(count)
        }
        ''')
        assert "5" in output
    
    def test_function_definition_and_call(self):
        """Test function definition and calling."""
        output = capture_output('''
        func add(a: int, b: int) -> int {
            return a + b
        }
        
        start {
            print(add(2, 3))
        }
        ''')
        assert "5" in output
    
    def test_recursive_function(self):
        """Test recursive function."""
        output = capture_output('''
        func factorial(n: int) -> int {
            if n <= 1 {
                return 1
            }
            return n * factorial(n - 1)
        }
        
        start {
            print(factorial(5))
        }
        ''')
        assert "120" in output
    
    def test_lambda(self):
        """Test lambda function."""
        output = capture_output('''
        start {
            let double = (x) => x * 2
            print(double(5))
        }
        ''')
        assert "10" in output
    
    def test_class_instantiation(self):
        """Test class creation and method calls."""
        output = capture_output('''
        class Counter {
            mut value: int
            
            init(start: int) {
                self.value = start
            }
            
            func increment() {
                self.value += 1
            }
            
            func get() -> int {
                return self.value
            }
        }
        
        start {
            let c = Counter(0)
            c.increment()
            c.increment()
            print(c.get())
        }
        ''')
        assert "2" in output
    
    def test_class_inheritance(self):
        """Test class inheritance."""
        output = capture_output('''
        class Animal {
            let name: string
            
            init(name: string) {
                self.name = name
            }
            
            func speak() -> string {
                return "..."
            }
        }
        
        class Dog extends Animal {
            init(name: string) {
                super.init(name)
            }
            
            func speak() -> string {
                return "Woof!"
            }
        }
        
        start {
            let dog = Dog("Rex")
            print(dog.name)
            print(dog.speak())
        }
        ''')
        assert "Rex" in output
        assert "Woof!" in output
    
    def test_block(self):
        """Test block declaration and access."""
        output = capture_output('''
        block Math {
            func square(x: int) -> int {
                return x * x
            }
        }
        
        start {
            print(Math.square(5))
        }
        ''')
        assert "25" in output
    
    def test_array_operations(self):
        """Test array operations."""
        output = capture_output('''
        start {
            let arr = [1, 2, 3]
            print(len(arr))
            print(arr[0])
            push(arr, 4)
            print(len(arr))
        }
        ''')
        assert "3" in output
        assert "1" in output
        assert "4" in output
    
    def test_map_operations(self):
        """Test map operations."""
        output = capture_output('''
        start {
            let m = {"a": 1, "b": 2}
            print(m["a"])
            m["c"] = 3
            print(len(keys(m)))
        }
        ''')
        assert "1" in output
        assert "3" in output
    
    def test_null_coalesce(self):
        """Test null coalesce operator."""
        output = capture_output('''
        start {
            let x = null
            let y = x ?? "default"
            print(y)
        }
        ''')
        assert "default" in output
    
    def test_match_statement(self):
        """Test match statement."""
        output = capture_output('''
        start {
            let x = 2
            match x {
                1 => print("one"),
                2 => print("two"),
                _ => print("other")
            }
        }
        ''')
        assert "two" in output
    
    def test_try_catch(self):
        """Test try-catch statement."""
        output = capture_output('''
        start {
            try {
                let x = 1 / 0
            } catch e {
                print("caught error")
            }
        }
        ''')
        assert "caught" in output
    
    def test_break_continue(self):
        """Test break and continue."""
        output = capture_output('''
        start {
            for i in 0..10 {
                if i == 5 {
                    break
                }
                print(i)
            }
        }
        ''')
        assert "4" in output
        assert "5" not in output
    
    def test_range(self):
        """Test range expression."""
        output = capture_output('''
        start {
            for i in 0..3 {
                print(i)
            }
        }
        ''')
        assert "0" in output
        assert "1" in output
        assert "2" in output
        assert "3" not in output  # exclusive end
    
    def test_builtin_functions(self):
        """Test built-in functions."""
        output = capture_output('''
        start {
            print(len("hello"))
            print(type(42))
            print(str(123))
        }
        ''')
        assert "5" in output
        assert "int" in output
        assert "123" in output


if __name__ == "__main__":
    pytest.main([__file__, "-v"])