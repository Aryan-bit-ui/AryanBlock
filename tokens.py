"""Token definitions"""
from enum import Enum, auto
from dataclasses import dataclass
from typing import Any

class TokenType(Enum):
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    BOOLEAN = auto()
    NULL = auto()
    IDENTIFIER = auto()
    LET = auto()
    MUT = auto()
    CONST = auto()
    FUNC = auto()
    RETURN = auto()
    IF = auto()
    ELIF = auto()
    ELSE = auto()
    FOR = auto()
    WHILE = auto()
    LOOP = auto()
    IN = auto()
    MATCH = auto()
    CLASS = auto()
    TRAIT = auto()
    IMPLEMENTS = auto()
    EXTENDS = auto()
    BLOCK = auto()
    IMPORT = auto()
    EXPORT = auto()
    FROM = auto()
    AS = auto()
    START = auto()
    TRY = auto()
    CATCH = auto()
    FINALLY = auto()
    ASYNC = auto()
    AWAIT = auto()
    SELF = auto()
    SUPER = auto()
    TRUE = auto()
    FALSE = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    BREAK = auto()
    CONTINUE = auto()
    INIT = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    POWER = auto()
    EQUAL = auto()
    NOT_EQUAL = auto()
    LESS = auto()
    GREATER = auto()
    LESS_EQUAL = auto()
    GREATER_EQUAL = auto()
    ASSIGN = auto()
    PLUS_ASSIGN = auto()
    MINUS_ASSIGN = auto()
    MULT_ASSIGN = auto()
    DIV_ASSIGN = auto()
    PIPE = auto()
    ARROW = auto()
    FAT_ARROW = auto()
    RANGE = auto()
    NULL_SAFE = auto()
    NULL_COALESCE = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    COMMA = auto()
    COLON = auto()
    SEMICOLON = auto()
    DOT = auto()
    QUESTION = auto()
    NEWLINE = auto()
    EOF = auto()

@dataclass
class Token:
    type: TokenType
    value: Any
    line: int
    column: int
    length: int = 1

KEYWORDS = {
    "let": TokenType.LET, "mut": TokenType.MUT, "const": TokenType.CONST,
    "func": TokenType.FUNC, "return": TokenType.RETURN, "if": TokenType.IF,
    "elif": TokenType.ELIF, "else": TokenType.ELSE, "for": TokenType.FOR,
    "while": TokenType.WHILE, "loop": TokenType.LOOP, "in": TokenType.IN,
    "match": TokenType.MATCH, "class": TokenType.CLASS, "trait": TokenType.TRAIT,
    "implements": TokenType.IMPLEMENTS, "extends": TokenType.EXTENDS,
    "block": TokenType.BLOCK, "import": TokenType.IMPORT, "export": TokenType.EXPORT,
    "from": TokenType.FROM, "as": TokenType.AS, "start": TokenType.START,
    "try": TokenType.TRY, "catch": TokenType.CATCH, "finally": TokenType.FINALLY,
    "async": TokenType.ASYNC, "await": TokenType.AWAIT, "self": TokenType.SELF,
    "super": TokenType.SUPER, "true": TokenType.TRUE, "false": TokenType.FALSE,
    "null": TokenType.NULL, "and": TokenType.AND, "or": TokenType.OR,
    "not": TokenType.NOT, "break": TokenType.BREAK, "continue": TokenType.CONTINUE,
    "init": TokenType.INIT,
}
