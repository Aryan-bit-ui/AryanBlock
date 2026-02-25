"""
Tests for the AryanBlock Parser
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from lexer import Lexer
from parser import Parser
from ast_nodes import *


def parse(source: str) -> Program:
    """Helper to parse source code."""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens, source.split('\n'))
    return parser.parse()


class TestParser:
    """Test cases for the Parser."""
    
    def test_empty_program(self):
        """Test parsing empty program."""
        program = parse("")
        assert isinstance(program, Program)
        assert len(program.statements) == 0
    
    def test_variable_declaration(self):
        """Test parsing variable declarations."""
        program = parse('let x = 5')
        assert len(program.statements) == 1
        stmt = program.statements[0]
        assert isinstance(stmt, VarDeclaration)
        assert stmt.name == "x"
        assert not stmt.is_mutable
        assert isinstance(stmt.initializer, IntegerLiteral)
        assert stmt.initializer.value == 5
    
    def test_mutable_variable(self):
        """Test parsing mutable variable."""
        program = parse('mut counter = 0')
        stmt = program.statements[0]
        assert isinstance(stmt, VarDeclaration)
        assert stmt.is_mutable
    
    def test_constant(self):
        """Test parsing constant."""
        program = parse('const PI = 3.14')
        stmt = program.statements[0]
        assert isinstance(stmt, VarDeclaration)
        assert stmt.is_constant
    
    def test_typed_variable(self):
        """Test parsing typed variable."""
        program = parse('let x: int = 5')
        stmt = program.statements[0]
        assert isinstance(stmt, VarDeclaration)
        assert stmt.type_annotation.name == "int"
    
    def test_function_declaration(self):
        """Test parsing function declaration."""
        program = parse('func add(a: int, b: int) -> int { return a + b }')
        stmt = program.statements[0]
        assert isinstance(stmt, FunctionDeclaration)
        assert stmt.name == "add"
        assert len(stmt.params) == 2
        assert stmt.params[0].name == "a"
        assert stmt.return_type.name == "int"
    
    def test_start_block(self):
        """Test parsing start block."""
        program = parse('start { print("hello") }')
        assert program.start_block is not None
        assert isinstance(program.start_block, StartBlock)
        assert len(program.start_block.body) == 1
    
    def test_if_statement(self):
        """Test parsing if statement."""
        program = parse('start { if x > 0 { print("positive") } }')
        stmt = program.start_block.body[0]
        assert isinstance(stmt, IfStatement)
        assert isinstance(stmt.condition, BinaryExpression)
    
    def test_if_else_statement(self):
        """Test parsing if-else statement."""
        program = parse('start { if x > 0 { print("yes") } else { print("no") } }')
        stmt = program.start_block.body[0]
        assert isinstance(stmt, IfStatement)
        assert stmt.else_branch is not None
    
    def test_if_elif_else(self):
        """Test parsing if-elif-else."""
        code = '''
        start {
            if x > 0 {
                print("positive")
            } elif x < 0 {
                print("negative")
            } else {
                print("zero")
            }
        }
        '''
        program = parse(code)
        stmt = program.start_block.body[0]
        assert isinstance(stmt, IfStatement)
        assert len(stmt.elif_branches) == 1
        assert stmt.else_branch is not None
    
    def test_for_loop(self):
        """Test parsing for loop."""
        program = parse('start { for i in 0..10 { print(i) } }')
        stmt = program.start_block.body[0]
        assert isinstance(stmt, ForLoop)
        assert stmt.variable == "i"
        assert isinstance(stmt.iterable, RangeExpression)
    
    def test_while_loop(self):
        """Test parsing while loop."""
        program = parse('start { while x > 0 { x = x - 1 } }')
        stmt = program.start_block.body[0]
        assert isinstance(stmt, WhileLoop)
    
    def test_loop_statement(self):
        """Test parsing loop statement."""
        program = parse('start { loop 5 { print("hello") } }')
        stmt = program.start_block.body[0]
        assert isinstance(stmt, LoopStatement)
    
    def test_match_statement(self):
        """Test parsing match statement."""
        code = '''
        start {
            match x {
                1 => print("one"),
                2 => print("two"),
                _ => print("other")
            }
        }
        '''
        program = parse(code)
        stmt = program.start_block.body[0]
        assert isinstance(stmt, MatchStatement)
        assert len(stmt.cases) == 3
    
    def test_class_declaration(self):
        """Test parsing class declaration."""
        code = '''
        class Person {
            let name: string
            mut age: int
            
            init(name: string, age: int) {
                self.name = name
                self.age = age
            }
            
            func greet() -> string {
                return "Hello, " + self.name
            }
        }
        '''
        program = parse(code)
        stmt = program.statements[0]
        assert isinstance(stmt, ClassDeclaration)
        assert stmt.name == "Person"
        assert stmt.init_method is not None
        assert len(stmt.members) == 3  # 2 fields + 1 method
    
    def test_class_inheritance(self):
        """Test parsing class inheritance."""
        code = 'class Student extends Person { let grade: string }'
        program = parse(code)
        stmt = program.statements[0]
        assert isinstance(stmt, ClassDeclaration)
        assert stmt.parent == "Person"
    
    def test_trait_declaration(self):
        """Test parsing trait declaration."""
        code = '''
        trait Printable {
            func display() -> string
        }
        '''
        program = parse(code)
        stmt = program.statements[0]
        assert isinstance(stmt, TraitDeclaration)
        assert stmt.name == "Printable"
    
    def test_block_declaration(self):
        """Test parsing block declaration."""
        code = '''
        block MathUtils {
            func add(a: int, b: int) -> int {
                return a + b
            }
        }
        '''
        program = parse(code)
        stmt = program.statements[0]
        assert isinstance(stmt, BlockDeclaration)
        assert stmt.name == "MathUtils"
    
    def test_binary_expression(self):
        """Test parsing binary expressions."""
        program = parse('start { let x = 1 + 2 * 3 }')
        stmt = program.start_block.body[0]
        expr = stmt.initializer
        # Should be 1 + (2 * 3) due to precedence
        assert isinstance(expr, BinaryExpression)
        assert expr.operator == '+'
    
    def test_unary_expression(self):
        """Test parsing unary expressions."""
        program = parse('start { let x = -5 }')
        stmt = program.start_block.body[0]
        expr = stmt.initializer
        assert isinstance(expr, UnaryExpression)
        assert expr.operator == '-'
    
    def test_call_expression(self):
        """Test parsing function calls."""
        program = parse('start { print("hello", 42) }')
        stmt = program.start_block.body[0]
        expr = stmt.expression
        assert isinstance(expr, CallExpression)
        assert len(expr.arguments) == 2
    
    def test_member_expression(self):
        """Test parsing member access."""
        program = parse('start { let x = obj.field }')
        stmt = program.start_block.body[0]
        expr = stmt.initializer
        assert isinstance(expr, MemberExpression)
        assert expr.member == "field"
    
    def test_index_expression(self):
        """Test parsing index access."""
        program = parse('start { let x = arr[0] }')
        stmt = program.start_block.body[0]
        expr = stmt.initializer
        assert isinstance(expr, IndexExpression)
    
    def test_array_literal(self):
        """Test parsing array literal."""
        program = parse('start { let arr = [1, 2, 3] }')
        stmt = program.start_block.body[0]
        expr = stmt.initializer
        assert isinstance(expr, ArrayLiteral)
        assert len(expr.elements) == 3
    
    def test_map_literal(self):
        """Test parsing map literal."""
        program = parse('start { let m = {"a": 1, "b": 2} }')
        stmt = program.start_block.body[0]
        expr = stmt.initializer
        assert isinstance(expr, MapLiteral)
        assert len(expr.entries) == 2
    
    def test_lambda_expression(self):
        """Test parsing lambda expression."""
        program = parse('start { let add = (a, b) => a + b }')
        stmt = program.start_block.body[0]
        expr = stmt.initializer
        assert isinstance(expr, LambdaExpression)
        assert len(expr.params) == 2
    
    def test_pipe_expression(self):
        """Test parsing pipe operator."""
        program = parse('start { let x = data |> process }')
        stmt = program.start_block.body[0]
        expr = stmt.initializer
        assert isinstance(expr, PipeExpression)
    
    def test_null_coalesce(self):
        """Test parsing null coalesce."""
        program = parse('start { let x = value ?? default }')
        stmt = program.start_block.body[0]
        expr = stmt.initializer
        assert isinstance(expr, NullCoalesceExpression)
    
    def test_string_interpolation(self):
        """Test parsing string interpolation."""
        program = parse('start { let s = "Hello, ${name}!" }')
        stmt = program.start_block.body[0]
        expr = stmt.initializer
        assert isinstance(expr, InterpolatedString)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])