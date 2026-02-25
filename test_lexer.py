"""
Tests for the AryanBlock Lexer
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from lexer import Lexer
from tokens import TokenType


class TestLexer:
    """Test cases for the Lexer."""
    
    def test_empty_source(self):
        """Test lexing empty source."""
        lexer = Lexer("")
        tokens = lexer.tokenize()
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.EOF
    
    def test_integer_literal(self):
        """Test lexing integers."""
        lexer = Lexer("42 0 123456")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.INTEGER
        assert tokens[0].value == 42
        assert tokens[1].type == TokenType.INTEGER
        assert tokens[1].value == 0
        assert tokens[2].type == TokenType.INTEGER
        assert tokens[2].value == 123456
    
    def test_float_literal(self):
        """Test lexing floats."""
        lexer = Lexer("3.14 0.5 123.456")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.FLOAT
        assert tokens[0].value == 3.14
        assert tokens[1].type == TokenType.FLOAT
        assert tokens[2].type == TokenType.FLOAT
    
    def test_string_literal(self):
        """Test lexing strings."""
        lexer = Lexer('"hello" "world"')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.STRING
        assert tokens[0].value == "hello"
        assert tokens[1].type == TokenType.STRING
        assert tokens[1].value == "world"
    
    def test_string_escape_sequences(self):
        """Test escape sequences in strings."""
        lexer = Lexer(r'"hello\nworld" "tab\there"')
        tokens = lexer.tokenize()
        assert tokens[0].value == "hello\nworld"
        assert tokens[1].value == "tab\there"
    
    def test_keywords(self):
        """Test lexing keywords."""
        lexer = Lexer("let mut const func if else for while")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.LET
        assert tokens[1].type == TokenType.MUT
        assert tokens[2].type == TokenType.CONST
        assert tokens[3].type == TokenType.FUNC
        assert tokens[4].type == TokenType.IF
        assert tokens[5].type == TokenType.ELSE
        assert tokens[6].type == TokenType.FOR
        assert tokens[7].type == TokenType.WHILE
    
    def test_identifiers(self):
        """Test lexing identifiers."""
        lexer = Lexer("foo bar _private camelCase snake_case")
        tokens = lexer.tokenize()
        for i in range(5):
            assert tokens[i].type == TokenType.IDENTIFIER
        assert tokens[0].value == "foo"
        assert tokens[1].value == "bar"
        assert tokens[2].value == "_private"
    
    def test_operators(self):
        """Test lexing operators."""
        lexer = Lexer("+ - * / % ** == != < > <= >= = += -= |> -> =>")
        tokens = lexer.tokenize()
        expected = [
            TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, TokenType.DIVIDE,
            TokenType.MODULO, TokenType.POWER, TokenType.EQUAL, TokenType.NOT_EQUAL,
            TokenType.LESS, TokenType.GREATER, TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL,
            TokenType.ASSIGN, TokenType.PLUS_ASSIGN, TokenType.MINUS_ASSIGN,
            TokenType.PIPE, TokenType.ARROW, TokenType.FAT_ARROW
        ]
        for i, expected_type in enumerate(expected):
            assert tokens[i].type == expected_type
    
    def test_delimiters(self):
        """Test lexing delimiters."""
        lexer = Lexer("( ) { } [ ] , : ; .")
        tokens = lexer.tokenize()
        expected = [
            TokenType.LPAREN, TokenType.RPAREN, TokenType.LBRACE, TokenType.RBRACE,
            TokenType.LBRACKET, TokenType.RBRACKET, TokenType.COMMA, TokenType.COLON,
            TokenType.SEMICOLON, TokenType.DOT
        ]
        for i, expected_type in enumerate(expected):
            assert tokens[i].type == expected_type
    
    def test_boolean_literals(self):
        """Test lexing boolean literals."""
        lexer = Lexer("true false")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.BOOLEAN
        assert tokens[0].value == True
        assert tokens[1].type == TokenType.BOOLEAN
        assert tokens[1].value == False
    
    def test_null_literal(self):
        """Test lexing null."""
        lexer = Lexer("null")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.NULL
    
    def test_comments(self):
        """Test that comments are skipped."""
        lexer = Lexer("let x = 5 // this is a comment\nlet y = 10")
        tokens = lexer.tokenize()
        # Comments should not produce tokens
        assert TokenType.COMMENT not in [t.type for t in tokens]
        # But the code around them should be tokenized
        assert tokens[0].type == TokenType.LET
    
    def test_multiline_comment(self):
        """Test multi-line comments."""
        lexer = Lexer("let x /* this is\na multi-line\ncomment */ = 5")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.LET
        assert tokens[1].type == TokenType.IDENTIFIER
        assert tokens[2].type == TokenType.ASSIGN
        assert tokens[3].type == TokenType.INTEGER
    
    def test_range_operator(self):
        """Test range operator."""
        lexer = Lexer("0..10")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.INTEGER
        assert tokens[1].type == TokenType.RANGE
        assert tokens[2].type == TokenType.INTEGER
    
    def test_token_positions(self):
        """Test that token positions are correct."""
        lexer = Lexer("let x = 5")
        tokens = lexer.tokenize()
        assert tokens[0].line == 1
        assert tokens[0].column == 1
    
    def test_complete_statement(self):
        """Test lexing a complete statement."""
        code = 'let name: string = "hello"'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        expected = [
            (TokenType.LET, "let"),
            (TokenType.IDENTIFIER, "name"),
            (TokenType.COLON, ":"),
            (TokenType.IDENTIFIER, "string"),
            (TokenType.ASSIGN, "="),
            (TokenType.STRING, "hello"),
            (TokenType.EOF, None)
        ]
        
        for i, (expected_type, expected_value) in enumerate(expected):
            assert tokens[i].type == expected_type
            if expected_value is not None:
                assert tokens[i].value == expected_value


if __name__ == "__main__":
    pytest.main([__file__, "-v"])