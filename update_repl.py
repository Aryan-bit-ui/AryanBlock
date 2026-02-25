repl_code = r'''"""
AryanBlock REPL - Interactive Shell
"""
import os
import sys

from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter


class REPL:
    """Interactive REPL for AryanBlock."""
    
    VERSION = "1.0.0"
    
    BANNER = r"""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║     █████╗ ██████╗ ██╗   ██╗ █████╗ ███╗   ██╗           ║
║    ██╔══██╗██╔══██╗╚██╗ ██╔╝██╔══██╗████╗  ██║           ║
║    ███████║██████╔╝ ╚████╔╝ ███████║██╔██╗ ██║           ║
║    ██╔══██║██╔══██╗  ╚██╔╝  ██╔══██║██║╚██╗██║           ║
║    ██║  ██║██║  ██║   ██║   ██║  ██║██║ ╚████║           ║
║    ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝           ║
║                                                           ║
║    ██████╗ ██╗      ██████╗  ██████╗██╗  ██╗             ║
║    ██╔══██╗██║     ██╔═══██╗██╔════╝██║ ██╔╝             ║
║    ██████╔╝██║     ██║   ██║██║     █████╔╝              ║
║    ██╔══██╗██║     ██║   ██║██║     ██╔═██╗              ║
║    ██████╔╝███████╗╚██████╔╝╚██████╗██║  ██╗             ║
║    ╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝             ║
║                                                           ║
║    Version 1.0.0                                          ║
║    Type :help for commands, :quit to exit                 ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
    
    HELP_TEXT = r"""
╔══════════════════════════════════════════════════════════╗
║                  AryanBlock REPL Commands                 ║
╠══════════════════════════════════════════════════════════╣
║  :help, :h      Show this help message                   ║
║  :quit, :q      Exit the REPL                            ║
║  :clear, :c     Clear the screen                         ║
║  :reset, :r     Reset interpreter state                  ║
║  :env, :e       Show current variables                   ║
║  :load <file>   Load and run a .ab file                  ║
║  :version       Show version info                        ║
╠══════════════════════════════════════════════════════════╣
║  Tips:                                                   ║
║  • Expressions are automatically printed                 ║
║  • Use 'let' for immutable, 'mut' for mutable vars       ║
║  • End multi-line input with empty line                  ║
╚══════════════════════════════════════════════════════════╝
"""
    
    def __init__(self):
        self.interpreter = Interpreter()
        self.running = False
        self.buffer = []
        self.multiline = False
    
    def print_banner(self):
        print(self.BANNER)
    
    def run(self):
        self.running = True
        self.print_banner()
        
        while self.running:
            try:
                if self.buffer:
                    prompt = "... "
                else:
                    prompt = "ab> "
                
                try:
                    line = input(prompt)
                except EOFError:
                    print("\n★ Goodbye! ★")
                    break
                
                if line.startswith(':') and not self.buffer:
                    self.handle_command(line)
                    continue
                
                if self.is_incomplete(line) or self.buffer:
                    self.buffer.append(line)
                    if line == "" and self.buffer:
                        source = "\n".join(self.buffer[:-1])
                        self.buffer = []
                        if source.strip():
                            self.execute(source)
                    continue
                
                if line.strip():
                    self.execute(line)
                
            except KeyboardInterrupt:
                print("\n⚠ Interrupted (use :quit to exit)")
                self.buffer = []
    
    def handle_command(self, command: str):
        parts = command.split(maxsplit=1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        if cmd in [':help', ':h']:
            print(self.HELP_TEXT)
        
        elif cmd in [':quit', ':q', ':exit']:
            print("★ Goodbye! ★")
            self.running = False
        
        elif cmd in [':clear', ':c', ':cls']:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.print_banner()
        
        elif cmd in [':reset', ':r']:
            self.interpreter = Interpreter()
            print("✓ Interpreter state reset")
        
        elif cmd in [':env', ':e']:
            self.show_environment()
        
        elif cmd in [':load', ':l']:
            if args:
                self.load_file(args)
            else:
                print("✗ Usage: :load <filename>")
        
        elif cmd == ':version':
            print(f"AryanBlock v{self.VERSION}")
        
        else:
            print(f"✗ Unknown command: {cmd}")
            print("  Type :help for available commands")
    
    def execute(self, source: str):
        if not source.strip():
            return
        try:
            lexer = Lexer(source, "<repl>")
            tokens = lexer.tokenize()
            parser = Parser(tokens, source.split('\n'), "<repl>")
            program = parser.parse()
            
            if (not program.start_block and 
                len(program.statements) == 1 and 
                hasattr(program.statements[0], 'expression')):
                result = self.interpreter.execute(program.statements[0].expression)
                if result is not None:
                    self.print_result(result)
            else:
                for stmt in program.statements:
                    self.interpreter.execute(stmt)
                if program.start_block:
                    result = self.interpreter.exec_block(
                        program.start_block.body, 
                        self.interpreter.env.child()
                    )
                    if result is not None:
                        self.print_result(result)
        
        except SyntaxError as e:
            print(f"✗ Syntax Error: {e}")
        except NameError as e:
            print(f"✗ Name Error: {e}")
        except TypeError as e:
            print(f"✗ Type Error: {e}")
        except ZeroDivisionError:
            print("✗ Error: Division by zero")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    def print_result(self, value):
        formatted = self.format_value(value)
        print(f"→ {formatted}")
    
    def format_value(self, value) -> str:
        if value is None:
            return "null"
        if isinstance(value, bool):
            return "true" if value else "false"
        if isinstance(value, (int, float)):
            return str(value)
        if isinstance(value, str):
            return f'"{value}"'
        if isinstance(value, list):
            items = ", ".join(self.format_value(v) for v in value)
            return f"[{items}]"
        if isinstance(value, dict):
            pairs = ", ".join(f'"{k}": {self.format_value(v)}' for k, v in value.items())
            return "{" + pairs + "}"
        if isinstance(value, tuple):
            items = ", ".join(self.format_value(v) for v in value)
            return f"({items})"
        if hasattr(value, 'class_def'):
            return f"<{value.class_def.name} instance>"
        if hasattr(value, 'name') and hasattr(value, 'params'):
            return f"<function {value.name}>"
        return str(value)
    
    def is_incomplete(self, line: str) -> bool:
        if self.multiline:
            return True
        opens = line.count('{') + line.count('(') + line.count('[')
        closes = line.count('}') + line.count(')') + line.count(']')
        if opens > closes:
            return True
        stripped = line.rstrip()
        if stripped.endswith(('and', 'or', '+', '-', '*', '/', '|>', '=>', '->')):
            return True
        return False
    
    def show_environment(self):
        print()
        print("╔══════════════════════════════╗")
        print("║     Current Environment      ║")
        print("╠══════════════════════════════╣")
        
        if self.interpreter.env.variables:
            print("║ Variables:                   ║")
            for name, var in self.interpreter.env.variables.items():
                mut = "mut " if var.is_mutable else ("const " if var.is_constant else "")
                val = self.format_value(var.value)
                print(f"║   {mut}{name} = {val}")
        
        user_funcs = [n for n in self.interpreter.env.functions.keys() 
                      if n not in ['print', 'input', 'len', 'type', 'str', 'int', 
                                   'float', 'bool', 'range', 'abs', 'min', 'max',
                                   'sum', 'sqrt', 'pow', 'floor', 'ceil', 'round',
                                   'random', 'random_int', 'time', 'sleep', 'push',
                                   'pop', 'slice', 'reverse', 'sort', 'join', 'split',
                                   'contains', 'keys', 'values', 'upper', 'lower',
                                   'trim', 'replace', 'assert']]
        if user_funcs:
            print("║ Functions:                   ║")
            for name in user_funcs:
                print(f"║   func {name}()")
        
        if self.interpreter.env.classes:
            print("║ Classes:                     ║")
            for name in self.interpreter.env.classes:
                print(f"║   class {name}")
        
        if self.interpreter.env.blocks:
            print("║ Blocks:                      ║")
            for name in self.interpreter.env.blocks:
                print(f"║   block {name}")
        
        if not (self.interpreter.env.variables or user_funcs or 
                self.interpreter.env.classes or self.interpreter.env.blocks):
            print("║   (empty)                    ║")
        
        print("╚══════════════════════════════╝")
        print()
    
    def load_file(self, filename: str):
        if not filename.endswith('.ab'):
            filename += '.ab'
        try:
            with open(filename, 'r') as f:
                source = f.read()
            print(f"► Loading {filename}...")
            lexer = Lexer(source, filename)
            tokens = lexer.tokenize()
            parser = Parser(tokens, source.split('\n'), filename)
            program = parser.parse()
            self.interpreter.interpret(program)
            print(f"✓ Loaded {filename} successfully")
        except FileNotFoundError:
            print(f"✗ File not found: {filename}")
        except Exception as e:
            print(f"✗ Error: {e}")


def start_repl():
    repl = REPL()
    repl.run()


if __name__ == "__main__":
    start_repl()
'''

with open(r"C:\aryanblock\src\repl.py", "w", encoding="utf-8") as f:
    f.write(repl_code)

print("Updated! Now run:")
print("  cd C:\\aryanblock")
print("  python src\\main.py repl")