#!/usr/bin/env python3
"""AryanBlock CLI"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter
from src.repl import start_repl

def run_file(filename):
    if not filename.endswith(".ab"):
        filename += ".ab"
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            source = f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {filename}")
        return 1
    try:
        tokens = Lexer(source, filename).tokenize()
        program = Parser(tokens).parse()
        Interpreter().interpret(program)
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def main():
    if len(sys.argv) < 2:
        print("AryanBlock v1.0.0")
        print("Usage: python src/main.py <command>")
        print("Commands:")
        print("  repl           Start interactive REPL")
        print("  run <file>     Run a .ab file")
        print("  <file.ab>      Run a .ab file")
        return
    
    cmd = sys.argv[1]
    if cmd == "repl":
        start_repl()
    elif cmd == "run" and len(sys.argv) > 2:
        sys.exit(run_file(sys.argv[2]))
    elif cmd.endswith(".ab"):
        sys.exit(run_file(cmd))
    elif cmd == "version":
        print("AryanBlock v1.0.0")
    else:
        print(f"Unknown command: {cmd}")

if __name__ == "__main__":
    main()
