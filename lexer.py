"""Lexer/Tokenizer"""
from typing import List, Optional
from .tokens import Token, TokenType, KEYWORDS

class Lexer:
    def __init__(self, source: str, filename: str = "<stdin>"):
        self.source = source
        self.filename = filename
        self.pos = 0
        self.line = 1
        self.column = 1
    
    @property
    def current(self) -> Optional[str]:
        return self.source[self.pos] if self.pos < len(self.source) else None
    
    def peek(self, n=1) -> Optional[str]:
        pos = self.pos + n
        return self.source[pos] if pos < len(self.source) else None
    
    def advance(self) -> str:
        char = self.current
        self.pos += 1
        if char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char
    
    def skip_whitespace(self):
        while self.current and self.current in " \t\r":
            self.advance()
    
    def skip_comment(self):
        if self.current == "/" and self.peek() == "/":
            while self.current and self.current != "\n":
                self.advance()
        elif self.current == "/" and self.peek() == "*":
            self.advance()
            self.advance()
            while self.current:
                if self.current == "*" and self.peek() == "/":
                    self.advance()
                    self.advance()
                    return
                self.advance()
    
    def read_string(self) -> Token:
        line, col = self.line, self.column
        self.advance()
        value = ""
        while self.current and self.current != '"':
            if self.current == "\\":
                self.advance()
                escapes = {"n": "\n", "t": "\t", "r": "\r", "\\": "\\", '"': '"'}
                value += escapes.get(self.current, self.current)
            else:
                value += self.current
            self.advance()
        self.advance()
        return Token(TokenType.STRING, value, line, col)
    
    def read_number(self) -> Token:
        line, col = self.line, self.column
        value = ""
        while self.current and self.current.isdigit():
            value += self.advance()
        if self.current == "." and self.peek() and self.peek().isdigit():
            value += self.advance()
            while self.current and self.current.isdigit():
                value += self.advance()
            return Token(TokenType.FLOAT, float(value), line, col)
        return Token(TokenType.INTEGER, int(value), line, col)
    
    def read_identifier(self) -> Token:
        line, col = self.line, self.column
        value = ""
        while self.current and (self.current.isalnum() or self.current == "_"):
            value += self.advance()
        if value in KEYWORDS:
            tt = KEYWORDS[value]
            if tt == TokenType.TRUE:
                return Token(TokenType.BOOLEAN, True, line, col)
            if tt == TokenType.FALSE:
                return Token(TokenType.BOOLEAN, False, line, col)
            return Token(tt, value, line, col)
        return Token(TokenType.IDENTIFIER, value, line, col)
    
    def read_operator(self) -> Token:
        line, col = self.line, self.column
        c = self.current
        two = c + (self.peek() or "")
        
        two_char = {
            "==": TokenType.EQUAL, "!=": TokenType.NOT_EQUAL,
            "<=": TokenType.LESS_EQUAL, ">=": TokenType.GREATER_EQUAL,
            "**": TokenType.POWER, "+=": TokenType.PLUS_ASSIGN,
            "-=": TokenType.MINUS_ASSIGN, "*=": TokenType.MULT_ASSIGN,
            "/=": TokenType.DIV_ASSIGN, "|>": TokenType.PIPE,
            "->": TokenType.ARROW, "=>": TokenType.FAT_ARROW,
            "..": TokenType.RANGE, "?.": TokenType.NULL_SAFE,
            "??": TokenType.NULL_COALESCE,
        }
        if two in two_char:
            self.advance()
            self.advance()
            return Token(two_char[two], two, line, col, 2)
        
        one_char = {
            "+": TokenType.PLUS, "-": TokenType.MINUS, "*": TokenType.MULTIPLY,
            "/": TokenType.DIVIDE, "%": TokenType.MODULO, "<": TokenType.LESS,
            ">": TokenType.GREATER, "=": TokenType.ASSIGN, "(": TokenType.LPAREN,
            ")": TokenType.RPAREN, "{": TokenType.LBRACE, "}": TokenType.RBRACE,
            "[": TokenType.LBRACKET, "]": TokenType.RBRACKET, ",": TokenType.COMMA,
            ":": TokenType.COLON, ";": TokenType.SEMICOLON, ".": TokenType.DOT,
            "?": TokenType.QUESTION,
        }
        if c in one_char:
            self.advance()
            return Token(one_char[c], c, line, col)
        
        raise SyntaxError(f"Unknown character: {c}")
    
    def tokenize(self) -> List[Token]:
        tokens = []
        while self.current:
            self.skip_whitespace()
            if not self.current:
                break
            if self.current == "/" and self.peek() in "/*":
                self.skip_comment()
                continue
            if self.current == "\n":
                self.advance()
                continue
            if self.current == '"':
                tokens.append(self.read_string())
            elif self.current.isdigit():
                tokens.append(self.read_number())
            elif self.current.isalpha() or self.current == "_":
                tokens.append(self.read_identifier())
            else:
                tokens.append(self.read_operator())
        tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return tokens
