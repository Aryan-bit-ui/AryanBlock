import os

BASE = r"C:\aryanblock"
SRC = os.path.join(BASE, "src")
EXAMPLES = os.path.join(BASE, "examples")

os.makedirs(SRC, exist_ok=True)
os.makedirs(EXAMPLES, exist_ok=True)

# ==================== __init__.py ====================
open(os.path.join(SRC, "__init__.py"), "w").write('''"""AryanBlock Programming Language"""
__version__ = "1.0.0"
''')

# ==================== tokens.py ====================
open(os.path.join(SRC, "tokens.py"), "w").write('''"""Token definitions"""
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
''')

# ==================== errors.py ====================
open(os.path.join(SRC, "errors.py"), "w").write('''"""Error handling"""

class AryanBlockError(Exception):
    def __init__(self, message, line=None, column=None):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(self.format())
    
    def format(self):
        if self.line:
            return f"Error at line {self.line}, column {self.column}: {self.message}"
        return f"Error: {self.message}"

class LexerError(AryanBlockError):
    pass

class ParseError(AryanBlockError):
    pass

class RuntimeError(AryanBlockError):
    pass
''')

# ==================== lexer.py ====================
open(os.path.join(SRC, "lexer.py"), "w").write('''"""Lexer/Tokenizer"""
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
        if char == "\\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char
    
    def skip_whitespace(self):
        while self.current and self.current in " \\t\\r":
            self.advance()
    
    def skip_comment(self):
        if self.current == "/" and self.peek() == "/":
            while self.current and self.current != "\\n":
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
            if self.current == "\\\\":
                self.advance()
                escapes = {"n": "\\n", "t": "\\t", "r": "\\r", "\\\\": "\\\\", '"': '"'}
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
            if self.current == "\\n":
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
''')

# ==================== ast_nodes.py ====================
open(os.path.join(SRC, "ast_nodes.py"), "w").write('''"""AST Node definitions"""
from dataclasses import dataclass, field
from typing import List, Optional, Any, Union

@dataclass
class Program:
    statements: List[Any] = field(default_factory=list)
    start_block: Optional[Any] = None

@dataclass
class StartBlock:
    body: List[Any] = field(default_factory=list)

@dataclass
class VarDeclaration:
    name: str
    initializer: Any = None
    type_annotation: Any = None
    is_mutable: bool = False
    is_constant: bool = False

@dataclass
class FunctionDeclaration:
    name: str
    params: List[Any] = field(default_factory=list)
    body: List[Any] = field(default_factory=list)
    return_type: Any = None

@dataclass
class Parameter:
    name: str
    type_annotation: Any = None
    default_value: Any = None

@dataclass
class ClassDeclaration:
    name: str
    parent: Optional[str] = None
    traits: List[str] = field(default_factory=list)
    members: List[Any] = field(default_factory=list)
    init_method: Any = None

@dataclass
class InitMethod:
    params: List[Any] = field(default_factory=list)
    body: List[Any] = field(default_factory=list)

@dataclass
class BlockDeclaration:
    name: str
    members: List[Any] = field(default_factory=list)

@dataclass
class TraitDeclaration:
    name: str
    methods: List[Any] = field(default_factory=list)

@dataclass
class ReturnStatement:
    value: Any = None

@dataclass
class BreakStatement:
    pass

@dataclass
class ContinueStatement:
    pass

@dataclass
class ExpressionStatement:
    expression: Any

@dataclass
class IfStatement:
    condition: Any
    then_branch: List[Any] = field(default_factory=list)
    elif_branches: List[tuple] = field(default_factory=list)
    else_branch: Optional[List[Any]] = None

@dataclass
class MatchStatement:
    value: Any
    cases: List[Any] = field(default_factory=list)

@dataclass
class MatchCase:
    pattern: Any
    body: Any
    is_default: bool = False

@dataclass
class ForLoop:
    variable: str
    iterable: Any
    body: List[Any] = field(default_factory=list)

@dataclass
class WhileLoop:
    condition: Any
    body: List[Any] = field(default_factory=list)

@dataclass
class LoopStatement:
    count: Any
    body: List[Any] = field(default_factory=list)

@dataclass
class TryStatement:
    try_body: List[Any] = field(default_factory=list)
    catch_var: Optional[str] = None
    catch_body: Optional[List[Any]] = None
    finally_body: Optional[List[Any]] = None

@dataclass
class BinaryExpression:
    left: Any
    operator: str
    right: Any

@dataclass
class UnaryExpression:
    operator: str
    operand: Any

@dataclass
class CallExpression:
    callee: Any
    arguments: List[Any] = field(default_factory=list)

@dataclass
class MemberExpression:
    object: Any
    member: str
    null_safe: bool = False

@dataclass
class IndexExpression:
    object: Any
    index: Any

@dataclass
class AssignmentExpression:
    target: Any
    value: Any
    operator: str = "="

@dataclass
class LambdaExpression:
    params: List[Any] = field(default_factory=list)
    body: Any = None

@dataclass
class PipeExpression:
    value: Any
    function: Any

@dataclass
class NullCoalesceExpression:
    value: Any
    default: Any

@dataclass
class RangeExpression:
    start: Any
    end: Any

@dataclass
class IntegerLiteral:
    value: int

@dataclass
class FloatLiteral:
    value: float

@dataclass
class StringLiteral:
    value: str

@dataclass
class InterpolatedString:
    parts: List[Any] = field(default_factory=list)

@dataclass
class BooleanLiteral:
    value: bool

@dataclass
class NullLiteral:
    pass

@dataclass
class Identifier:
    name: str

@dataclass
class ArrayLiteral:
    elements: List[Any] = field(default_factory=list)

@dataclass
class MapLiteral:
    entries: List[tuple] = field(default_factory=list)

@dataclass
class TypeAnnotation:
    name: str
    nullable: bool = False

@dataclass
class SelfExpression:
    pass

@dataclass
class SuperExpression:
    member: Optional[str] = None
''')

# ==================== parser.py ====================
open(os.path.join(SRC, "parser.py"), "w").write('''"""Parser"""
from typing import List, Optional
from .tokens import Token, TokenType
from .ast_nodes import *

class Parser:
    def __init__(self, tokens: List[Token], source_lines=None, filename="<stdin>"):
        self.tokens = tokens
        self.pos = 0
        self.source_lines = source_lines or []
    
    @property
    def current(self) -> Token:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else self.tokens[-1]
    
    def advance(self) -> Token:
        token = self.current
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return token
    
    def match(self, *types) -> bool:
        return self.current.type in types
    
    def consume(self, tt, msg=""):
        if self.current.type == tt:
            return self.advance()
        raise SyntaxError(f"{msg} at line {self.current.line}")
    
    def parse(self) -> Program:
        program = Program()
        while not self.match(TokenType.EOF):
            stmt = self.parse_declaration()
            if isinstance(stmt, StartBlock):
                program.start_block = stmt
            elif stmt:
                program.statements.append(stmt)
        return program
    
    def parse_declaration(self):
        if self.match(TokenType.START):
            return self.parse_start()
        if self.match(TokenType.FUNC):
            return self.parse_function()
        if self.match(TokenType.CLASS):
            return self.parse_class()
        if self.match(TokenType.BLOCK):
            return self.parse_block_decl()
        if self.match(TokenType.TRAIT):
            return self.parse_trait()
        if self.match(TokenType.LET, TokenType.MUT, TokenType.CONST):
            return self.parse_var()
        return self.parse_statement()
    
    def parse_start(self) -> StartBlock:
        self.consume(TokenType.START)
        self.consume(TokenType.LBRACE)
        body = self.parse_block_body()
        self.consume(TokenType.RBRACE)
        return StartBlock(body=body)
    
    def parse_function(self) -> FunctionDeclaration:
        self.consume(TokenType.FUNC)
        name = self.consume(TokenType.IDENTIFIER).value
        self.consume(TokenType.LPAREN)
        params = self.parse_params()
        self.consume(TokenType.RPAREN)
        ret = None
        if self.match(TokenType.ARROW):
            self.advance()
            ret = self.parse_type()
        self.consume(TokenType.LBRACE)
        body = self.parse_block_body()
        self.consume(TokenType.RBRACE)
        return FunctionDeclaration(name=name, params=params, body=body, return_type=ret)
    
    def parse_params(self) -> List[Parameter]:
        params = []
        while not self.match(TokenType.RPAREN):
            name = self.consume(TokenType.IDENTIFIER).value
            ta = None
            if self.match(TokenType.COLON):
                self.advance()
                ta = self.parse_type()
            default = None
            if self.match(TokenType.ASSIGN):
                self.advance()
                default = self.parse_expression()
            params.append(Parameter(name=name, type_annotation=ta, default_value=default))
            if not self.match(TokenType.RPAREN):
                self.consume(TokenType.COMMA)
        return params
    
    def parse_type(self) -> TypeAnnotation:
        name = self.consume(TokenType.IDENTIFIER).value
        nullable = self.match(TokenType.QUESTION)
        if nullable:
            self.advance()
        return TypeAnnotation(name=name, nullable=nullable)
    
    def parse_class(self) -> ClassDeclaration:
        self.consume(TokenType.CLASS)
        name = self.consume(TokenType.IDENTIFIER).value
        parent = None
        if self.match(TokenType.EXTENDS):
            self.advance()
            parent = self.consume(TokenType.IDENTIFIER).value
        traits = []
        if self.match(TokenType.IMPLEMENTS):
            self.advance()
            while True:
                traits.append(self.consume(TokenType.IDENTIFIER).value)
                if not self.match(TokenType.COMMA):
                    break
                self.advance()
        self.consume(TokenType.LBRACE)
        members = []
        init = None
        while not self.match(TokenType.RBRACE, TokenType.EOF):
            if self.match(TokenType.INIT):
                init = self.parse_init()
            elif self.match(TokenType.FUNC):
                members.append(self.parse_function())
            elif self.match(TokenType.LET, TokenType.MUT):
                members.append(self.parse_var())
            else:
                break
        self.consume(TokenType.RBRACE)
        return ClassDeclaration(name=name, parent=parent, traits=traits, members=members, init_method=init)
    
    def parse_init(self) -> InitMethod:
        self.consume(TokenType.INIT)
        self.consume(TokenType.LPAREN)
        params = self.parse_params()
        self.consume(TokenType.RPAREN)
        self.consume(TokenType.LBRACE)
        body = self.parse_block_body()
        self.consume(TokenType.RBRACE)
        return InitMethod(params=params, body=body)
    
    def parse_block_decl(self) -> BlockDeclaration:
        self.consume(TokenType.BLOCK)
        name = self.consume(TokenType.IDENTIFIER).value
        self.consume(TokenType.LBRACE)
        members = []
        while not self.match(TokenType.RBRACE, TokenType.EOF):
            if self.match(TokenType.FUNC):
                members.append(self.parse_function())
            elif self.match(TokenType.LET, TokenType.MUT, TokenType.CONST):
                members.append(self.parse_var())
            else:
                break
        self.consume(TokenType.RBRACE)
        return BlockDeclaration(name=name, members=members)
    
    def parse_trait(self) -> TraitDeclaration:
        self.consume(TokenType.TRAIT)
        name = self.consume(TokenType.IDENTIFIER).value
        self.consume(TokenType.LBRACE)
        methods = []
        while not self.match(TokenType.RBRACE, TokenType.EOF):
            methods.append(self.parse_function())
        self.consume(TokenType.RBRACE)
        return TraitDeclaration(name=name, methods=methods)
    
    def parse_var(self) -> VarDeclaration:
        is_mut = self.match(TokenType.MUT)
        is_const = self.match(TokenType.CONST)
        self.advance()
        name = self.consume(TokenType.IDENTIFIER).value
        ta = None
        if self.match(TokenType.COLON):
            self.advance()
            ta = self.parse_type()
        init = None
        if self.match(TokenType.ASSIGN):
            self.advance()
            init = self.parse_expression()
        return VarDeclaration(name=name, initializer=init, type_annotation=ta, is_mutable=is_mut, is_constant=is_const)
    
    def parse_statement(self):
        if self.match(TokenType.IF):
            return self.parse_if()
        if self.match(TokenType.MATCH):
            return self.parse_match()
        if self.match(TokenType.FOR):
            return self.parse_for()
        if self.match(TokenType.WHILE):
            return self.parse_while()
        if self.match(TokenType.LOOP):
            return self.parse_loop()
        if self.match(TokenType.TRY):
            return self.parse_try()
        if self.match(TokenType.RETURN):
            self.advance()
            val = None if self.match(TokenType.RBRACE) else self.parse_expression()
            return ReturnStatement(value=val)
        if self.match(TokenType.BREAK):
            self.advance()
            return BreakStatement()
        if self.match(TokenType.CONTINUE):
            self.advance()
            return ContinueStatement()
        if self.match(TokenType.LET, TokenType.MUT, TokenType.CONST):
            return self.parse_var()
        return ExpressionStatement(expression=self.parse_expression())
    
    def parse_if(self) -> IfStatement:
        self.consume(TokenType.IF)
        cond = self.parse_expression()
        self.consume(TokenType.LBRACE)
        then = self.parse_block_body()
        self.consume(TokenType.RBRACE)
        elifs = []
        while self.match(TokenType.ELIF):
            self.advance()
            ec = self.parse_expression()
            self.consume(TokenType.LBRACE)
            eb = self.parse_block_body()
            self.consume(TokenType.RBRACE)
            elifs.append((ec, eb))
        els = None
        if self.match(TokenType.ELSE):
            self.advance()
            self.consume(TokenType.LBRACE)
            els = self.parse_block_body()
            self.consume(TokenType.RBRACE)
        return IfStatement(condition=cond, then_branch=then, elif_branches=elifs, else_branch=els)
    
    def parse_match(self) -> MatchStatement:
        self.consume(TokenType.MATCH)
        val = self.parse_expression()
        self.consume(TokenType.LBRACE)
        cases = []
        while not self.match(TokenType.RBRACE, TokenType.EOF):
            is_def = self.match(TokenType.IDENTIFIER) and self.current.value == "_"
            pat = Identifier(name="_") if is_def else self.parse_expression()
            if is_def:
                self.advance()
            self.consume(TokenType.FAT_ARROW)
            body = self.parse_expression()
            cases.append(MatchCase(pattern=pat, body=body, is_default=is_def))
            if self.match(TokenType.COMMA):
                self.advance()
        self.consume(TokenType.RBRACE)
        return MatchStatement(value=val, cases=cases)
    
    def parse_for(self) -> ForLoop:
        self.consume(TokenType.FOR)
        var = self.consume(TokenType.IDENTIFIER).value
        self.consume(TokenType.IN)
        it = self.parse_expression()
        self.consume(TokenType.LBRACE)
        body = self.parse_block_body()
        self.consume(TokenType.RBRACE)
        return ForLoop(variable=var, iterable=it, body=body)
    
    def parse_while(self) -> WhileLoop:
        self.consume(TokenType.WHILE)
        cond = self.parse_expression()
        self.consume(TokenType.LBRACE)
        body = self.parse_block_body()
        self.consume(TokenType.RBRACE)
        return WhileLoop(condition=cond, body=body)
    
    def parse_loop(self) -> LoopStatement:
        self.consume(TokenType.LOOP)
        cnt = self.parse_expression()
        self.consume(TokenType.LBRACE)
        body = self.parse_block_body()
        self.consume(TokenType.RBRACE)
        return LoopStatement(count=cnt, body=body)
    
    def parse_try(self) -> TryStatement:
        self.consume(TokenType.TRY)
        self.consume(TokenType.LBRACE)
        tb = self.parse_block_body()
        self.consume(TokenType.RBRACE)
        cv, cb = None, None
        if self.match(TokenType.CATCH):
            self.advance()
            cv = self.consume(TokenType.IDENTIFIER).value
            self.consume(TokenType.LBRACE)
            cb = self.parse_block_body()
            self.consume(TokenType.RBRACE)
        fb = None
        if self.match(TokenType.FINALLY):
            self.advance()
            self.consume(TokenType.LBRACE)
            fb = self.parse_block_body()
            self.consume(TokenType.RBRACE)
        return TryStatement(try_body=tb, catch_var=cv, catch_body=cb, finally_body=fb)
    
    def parse_block_body(self) -> List:
        stmts = []
        while not self.match(TokenType.RBRACE, TokenType.EOF):
            stmts.append(self.parse_statement())
        return stmts
    
    def parse_expression(self):
        return self.parse_assignment()
    
    def parse_assignment(self):
        expr = self.parse_or()
        if self.match(TokenType.ASSIGN, TokenType.PLUS_ASSIGN, TokenType.MINUS_ASSIGN, TokenType.MULT_ASSIGN, TokenType.DIV_ASSIGN):
            op = self.advance().value
            val = self.parse_assignment()
            return AssignmentExpression(target=expr, value=val, operator=op)
        return expr
    
    def parse_or(self):
        expr = self.parse_and()
        while self.match(TokenType.OR):
            op = self.advance().value
            expr = BinaryExpression(left=expr, operator=op, right=self.parse_and())
        return expr
    
    def parse_and(self):
        expr = self.parse_equality()
        while self.match(TokenType.AND):
            op = self.advance().value
            expr = BinaryExpression(left=expr, operator=op, right=self.parse_equality())
        return expr
    
    def parse_equality(self):
        expr = self.parse_comparison()
        while self.match(TokenType.EQUAL, TokenType.NOT_EQUAL):
            op = self.advance().value
            expr = BinaryExpression(left=expr, operator=op, right=self.parse_comparison())
        return expr
    
    def parse_comparison(self):
        expr = self.parse_pipe()
        while self.match(TokenType.LESS, TokenType.GREATER, TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL):
            op = self.advance().value
            expr = BinaryExpression(left=expr, operator=op, right=self.parse_pipe())
        return expr
    
    def parse_pipe(self):
        expr = self.parse_additive()
        while self.match(TokenType.PIPE):
            self.advance()
            expr = PipeExpression(value=expr, function=self.parse_additive())
        return expr
    
    def parse_additive(self):
        expr = self.parse_multiplicative()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = self.advance().value
            expr = BinaryExpression(left=expr, operator=op, right=self.parse_multiplicative())
        return expr
    
    def parse_multiplicative(self):
        expr = self.parse_power()
        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            op = self.advance().value
            expr = BinaryExpression(left=expr, operator=op, right=self.parse_power())
        return expr
    
    def parse_power(self):
        expr = self.parse_unary()
        if self.match(TokenType.POWER):
            self.advance()
            expr = BinaryExpression(left=expr, operator="**", right=self.parse_power())
        return expr
    
    def parse_unary(self):
        if self.match(TokenType.MINUS, TokenType.NOT):
            op = self.advance().value
            return UnaryExpression(operator=op, operand=self.parse_unary())
        return self.parse_call()
    
    def parse_call(self):
        expr = self.parse_primary()
        while True:
            if self.match(TokenType.LPAREN):
                self.advance()
                args = []
                while not self.match(TokenType.RPAREN):
                    args.append(self.parse_expression())
                    if not self.match(TokenType.RPAREN):
                        self.consume(TokenType.COMMA)
                self.consume(TokenType.RPAREN)
                expr = CallExpression(callee=expr, arguments=args)
            elif self.match(TokenType.DOT):
                self.advance()
                member = self.consume(TokenType.IDENTIFIER).value
                expr = MemberExpression(object=expr, member=member)
            elif self.match(TokenType.LBRACKET):
                self.advance()
                idx = self.parse_expression()
                self.consume(TokenType.RBRACKET)
                expr = IndexExpression(object=expr, index=idx)
            else:
                break
        return expr
    
    def parse_primary(self):
        if self.match(TokenType.INTEGER):
            return IntegerLiteral(value=self.advance().value)
        if self.match(TokenType.FLOAT):
            return FloatLiteral(value=self.advance().value)
        if self.match(TokenType.STRING):
            return self.parse_string(self.advance().value)
        if self.match(TokenType.BOOLEAN):
            return BooleanLiteral(value=self.advance().value)
        if self.match(TokenType.NULL):
            self.advance()
            return NullLiteral()
        if self.match(TokenType.SELF):
            self.advance()
            return SelfExpression()
        if self.match(TokenType.SUPER):
            self.advance()
            member = None
            if self.match(TokenType.DOT):
                self.advance()
                member = self.consume(TokenType.IDENTIFIER).value
            return SuperExpression(member=member)
        if self.match(TokenType.LBRACKET):
            return self.parse_array()
        if self.match(TokenType.LBRACE):
            return self.parse_map()
        if self.match(TokenType.LPAREN):
            return self.parse_paren()
        if self.match(TokenType.IDENTIFIER):
            return Identifier(name=self.advance().value)
        raise SyntaxError(f"Unexpected token: {self.current.type}")
    
    def parse_string(self, value):
        if "${" not in value:
            return StringLiteral(value=value)
        parts = []
        i = 0
        text = ""
        while i < len(value):
            if value[i:i+2] == "${":
                if text:
                    parts.append(text)
                    text = ""
                i += 2
                start = i
                depth = 1
                while i < len(value) and depth > 0:
                    if value[i] == "{":
                        depth += 1
                    elif value[i] == "}":
                        depth -= 1
                    i += 1
                expr_str = value[start:i-1]
                from .lexer import Lexer
                toks = Lexer(expr_str).tokenize()
                parts.append(Parser(toks).parse_expression())
            else:
                text += value[i]
                i += 1
        if text:
            parts.append(text)
        return InterpolatedString(parts=parts)
    
    def parse_array(self):
        self.consume(TokenType.LBRACKET)
        elems = []
        while not self.match(TokenType.RBRACKET):
            elems.append(self.parse_expression())
            if not self.match(TokenType.RBRACKET):
                self.consume(TokenType.COMMA)
        self.consume(TokenType.RBRACKET)
        return ArrayLiteral(elements=elems)
    
    def parse_map(self):
        self.consume(TokenType.LBRACE)
        entries = []
        while not self.match(TokenType.RBRACE):
            key = StringLiteral(value=self.advance().value)
            self.consume(TokenType.COLON)
            val = self.parse_expression()
            entries.append((key, val))
            if not self.match(TokenType.RBRACE):
                self.consume(TokenType.COMMA)
        self.consume(TokenType.RBRACE)
        return MapLiteral(entries=entries)
    
    def parse_paren(self):
        self.consume(TokenType.LPAREN)
        if self.match(TokenType.RPAREN):
            self.advance()
            if self.match(TokenType.FAT_ARROW):
                self.advance()
                return LambdaExpression(params=[], body=self.parse_expression())
            return IntegerLiteral(value=0)
        expr = self.parse_expression()
        if self.match(TokenType.COMMA):
            elems = [expr]
            while self.match(TokenType.COMMA):
                self.advance()
                elems.append(self.parse_expression())
            self.consume(TokenType.RPAREN)
            if self.match(TokenType.FAT_ARROW):
                self.advance()
                params = [Parameter(name=e.name) for e in elems if isinstance(e, Identifier)]
                return LambdaExpression(params=params, body=self.parse_expression())
            return ArrayLiteral(elements=elems)
        self.consume(TokenType.RPAREN)
        if self.match(TokenType.FAT_ARROW):
            self.advance()
            params = [Parameter(name=expr.name)] if isinstance(expr, Identifier) else []
            return LambdaExpression(params=params, body=self.parse_expression())
        return expr
''')

# ==================== environment.py ====================
open(os.path.join(SRC, "environment.py"), "w").write('''"""Environment and runtime types"""
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class Variable:
    name: str
    value: Any
    is_mutable: bool = True
    is_constant: bool = False

class Environment:
    def __init__(self, parent=None):
        self.parent = parent
        self.variables: Dict[str, Variable] = {}
        self.functions: Dict[str, Any] = {}
        self.classes: Dict[str, Any] = {}
        self.blocks: Dict[str, Any] = {}
    
    def define(self, name, value, is_mutable=True, is_constant=False):
        self.variables[name] = Variable(name, value, is_mutable, is_constant)
    
    def define_function(self, name, func):
        self.functions[name] = func
    
    def define_class(self, name, cls):
        self.classes[name] = cls
    
    def define_block(self, name, block):
        self.blocks[name] = block
    
    def get(self, name):
        if name in self.variables:
            return self.variables[name].value
        if self.parent:
            return self.parent.get(name)
        raise NameError(f"Undefined: {name}")
    
    def get_function(self, name):
        if name in self.functions:
            return self.functions[name]
        if self.parent:
            return self.parent.get_function(name)
        return None
    
    def get_class(self, name):
        if name in self.classes:
            return self.classes[name]
        if self.parent:
            return self.parent.get_class(name)
        return None
    
    def get_block(self, name):
        if name in self.blocks:
            return self.blocks[name]
        if self.parent:
            return self.parent.get_block(name)
        return None
    
    def set(self, name, value):
        if name in self.variables:
            v = self.variables[name]
            if v.is_constant:
                raise TypeError(f"Cannot reassign constant: {name}")
            if not v.is_mutable:
                raise TypeError(f"Cannot reassign immutable: {name}")
            v.value = value
            return
        if self.parent:
            self.parent.set(name, value)
            return
        raise NameError(f"Undefined: {name}")
    
    def child(self):
        return Environment(parent=self)

class ABObject:
    def __init__(self, cls):
        self.class_def = cls
        self.fields: Dict[str, Any] = {}
    
    def get_field(self, name):
        return self.fields.get(name)
    
    def set_field(self, name, value):
        self.fields[name] = value
    
    def has_field(self, name):
        return name in self.fields

class ABClass:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.methods: Dict[str, Any] = {}
        self.fields: Dict[str, Any] = {}
        self.init_method = None
    
    def get_method(self, name):
        if name in self.methods:
            return self.methods[name]
        if self.parent:
            return self.parent.get_method(name)
        return None

class ABBlock:
    def __init__(self, name):
        self.name = name
        self.members: Dict[str, Any] = {}
    
    def get_member(self, name):
        return self.members.get(name)

class ABFunction:
    def __init__(self, name, params, body, closure):
        self.name = name
        self.params = params
        self.body = body
        self.closure = closure

class ABLambda:
    def __init__(self, params, body, closure):
        self.params = params
        self.body = body
        self.closure = closure

class ReturnException(Exception):
    def __init__(self, value=None):
        self.value = value

class BreakException(Exception):
    pass

class ContinueException(Exception):
    pass
''')

# ==================== builtins.py ====================
open(os.path.join(SRC, "builtins.py"), "w").write('''"""Built-in functions"""
import math
import random
import time

def _fmt(v):
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, list):
        return "[" + ", ".join(_fmt(x) for x in v) + "]"
    if isinstance(v, dict):
        return "{" + ", ".join(f\'"{k}": {_fmt(v)}\' for k, v in v.items()) + "}"
    return str(v)

BUILTINS = {
    "print": lambda *args: print(*[_fmt(a) for a in args]),
    "input": input,
    "len": len,
    "type": lambda x: type(x).__name__,
    "str": str,
    "int": int,
    "float": float,
    "bool": bool,
    "range": lambda *a: list(range(*a)),
    "abs": abs,
    "min": min,
    "max": max,
    "sum": sum,
    "sqrt": math.sqrt,
    "pow": pow,
    "floor": math.floor,
    "ceil": math.ceil,
    "round": round,
    "random": random.random,
    "random_int": random.randint,
    "time": time.time,
    "sleep": time.sleep,
    "push": lambda arr, x: arr.append(x) or arr,
    "pop": lambda arr: arr.pop(),
    "slice": lambda arr, *a: arr[slice(*a)],
    "reverse": lambda arr: arr.reverse() or arr,
    "sort": lambda arr: arr.sort() or arr,
    "join": lambda arr, sep="": sep.join(str(x) for x in arr),
    "split": lambda s, sep=" ": s.split(sep),
    "contains": lambda col, x: x in col,
    "keys": lambda d: list(d.keys()),
    "values": lambda d: list(d.values()),
    "upper": lambda s: s.upper(),
    "lower": lambda s: s.lower(),
    "trim": lambda s: s.strip(),
    "replace": lambda s, a, b: s.replace(a, b),
    "assert": lambda c, m="Assertion failed": None if c else (_ for _ in ()).throw(AssertionError(m)),
}

CONSTANTS = {"PI": math.pi, "E": math.e, "TAU": math.tau}
''')

# ==================== interpreter.py ====================
open(os.path.join(SRC, "interpreter.py"), "w").write('''"""Interpreter"""
from typing import Any, List
from .ast_nodes import *
from .environment import *
from .builtins import BUILTINS, CONSTANTS

class Interpreter:
    def __init__(self):
        self.env = Environment()
        for name, func in BUILTINS.items():
            self.env.define_function(name, func)
        for name, val in CONSTANTS.items():
            self.env.define(name, val, is_constant=True)
    
    def interpret(self, program, source="", filename=""):
        for stmt in program.statements:
            self.execute(stmt)
        if program.start_block:
            self.exec_block(program.start_block.body, self.env.child())
    
    def execute(self, node):
        method = f"exec_{type(node).__name__}"
        return getattr(self, method, self.exec_generic)(node)
    
    def exec_generic(self, node):
        raise RuntimeError(f"Unknown node: {type(node).__name__}")
    
    def exec_block(self, stmts, env):
        prev = self.env
        self.env = env
        result = None
        try:
            for stmt in stmts:
                result = self.execute(stmt)
        finally:
            self.env = prev
        return result
    
    def exec_VarDeclaration(self, node):
        val = self.execute(node.initializer) if node.initializer else None
        self.env.define(node.name, val, node.is_mutable, node.is_constant)
    
    def exec_FunctionDeclaration(self, node):
        func = ABFunction(node.name, node.params, node.body, self.env)
        self.env.define_function(node.name, func)
    
    def exec_ClassDeclaration(self, node):
        parent = self.env.get_class(node.parent) if node.parent else None
        cls = ABClass(node.name, parent)
        for m in node.members:
            if isinstance(m, FunctionDeclaration):
                cls.methods[m.name] = ABFunction(m.name, m.params, m.body, self.env)
            elif isinstance(m, VarDeclaration):
                cls.fields[m.name] = self.execute(m.initializer) if m.initializer else None
        if node.init_method:
            cls.init_method = ABFunction("init", node.init_method.params, node.init_method.body, self.env)
        self.env.define_class(node.name, cls)
    
    def exec_BlockDeclaration(self, node):
        block = ABBlock(node.name)
        for m in node.members:
            if isinstance(m, FunctionDeclaration):
                block.members[m.name] = ABFunction(m.name, m.params, m.body, self.env)
            elif isinstance(m, VarDeclaration):
                block.members[m.name] = self.execute(m.initializer) if m.initializer else None
        self.env.define_block(node.name, block)
    
    def exec_TraitDeclaration(self, node):
        pass
    
    def exec_ExpressionStatement(self, node):
        return self.execute(node.expression)
    
    def exec_ReturnStatement(self, node):
        raise ReturnException(self.execute(node.value) if node.value else None)
    
    def exec_BreakStatement(self, node):
        raise BreakException()
    
    def exec_ContinueStatement(self, node):
        raise ContinueException()
    
    def exec_IfStatement(self, node):
        if self.truthy(self.execute(node.condition)):
            return self.exec_block(node.then_branch, self.env.child())
        for cond, body in node.elif_branches:
            if self.truthy(self.execute(cond)):
                return self.exec_block(body, self.env.child())
        if node.else_branch:
            return self.exec_block(node.else_branch, self.env.child())
    
    def exec_MatchStatement(self, node):
        val = self.execute(node.value)
        for case in node.cases:
            if case.is_default or val == self.execute(case.pattern):
                if isinstance(case.body, list):
                    return self.exec_block(case.body, self.env.child())
                return self.execute(case.body)
    
    def exec_ForLoop(self, node):
        iterable = self.execute(node.iterable)
        for item in iterable:
            env = self.env.child()
            env.define(node.variable, item, is_mutable=False)
            try:
                self.exec_block(node.body, env)
            except BreakException:
                break
            except ContinueException:
                continue
    
    def exec_WhileLoop(self, node):
        while self.truthy(self.execute(node.condition)):
            try:
                self.exec_block(node.body, self.env.child())
            except BreakException:
                break
            except ContinueException:
                continue
    
    def exec_LoopStatement(self, node):
        count = int(self.execute(node.count))
        for _ in range(count):
            try:
                self.exec_block(node.body, self.env.child())
            except BreakException:
                break
            except ContinueException:
                continue
    
    def exec_TryStatement(self, node):
        try:
            self.exec_block(node.try_body, self.env.child())
        except Exception as e:
            if node.catch_body:
                env = self.env.child()
                if node.catch_var:
                    env.define(node.catch_var, {"message": str(e), "type": type(e).__name__})
                self.exec_block(node.catch_body, env)
        finally:
            if node.finally_body:
                self.exec_block(node.finally_body, self.env.child())
    
    def exec_BinaryExpression(self, node):
        if node.operator == "and":
            l = self.execute(node.left)
            return l if not self.truthy(l) else self.execute(node.right)
        if node.operator == "or":
            l = self.execute(node.left)
            return l if self.truthy(l) else self.execute(node.right)
        l, r = self.execute(node.left), self.execute(node.right)
        ops = {
            "+": lambda: str(l) + str(r) if isinstance(l, str) or isinstance(r, str) else l + r,
            "-": lambda: l - r, "*": lambda: l * r, "/": lambda: l / r,
            "%": lambda: l % r, "**": lambda: l ** r,
            "==": lambda: l == r, "!=": lambda: l != r,
            "<": lambda: l < r, ">": lambda: l > r,
            "<=": lambda: l <= r, ">=": lambda: l >= r,
        }
        return ops[node.operator]()
    
    def exec_UnaryExpression(self, node):
        val = self.execute(node.operand)
        if node.operator == "-":
            return -val
        if node.operator == "not":
            return not self.truthy(val)
    
    def exec_CallExpression(self, node):
        callee = self.execute(node.callee)
        args = [self.execute(a) for a in node.arguments]
        if callable(callee) and not isinstance(callee, (ABFunction, ABLambda, ABClass)):
            return callee(*args)
        if isinstance(callee, ABFunction):
            return self.call_func(callee, args)
        if isinstance(callee, ABLambda):
            return self.call_lambda(callee, args)
        if isinstance(callee, ABClass):
            return self.instantiate(callee, args)
        if isinstance(node.callee, Identifier):
            cls = self.env.get_class(node.callee.name)
            if cls:
                return self.instantiate(cls, args)
        raise TypeError(f"Not callable: {type(callee)}")
    
    def call_func(self, func, args):
        env = func.closure.child()
        for i, p in enumerate(func.params):
            val = args[i] if i < len(args) else (self.execute(p.default_value) if p.default_value else None)
            env.define(p.name, val)
        try:
            return self.exec_block(func.body, env)
        except ReturnException as e:
            return e.value
    
    def call_lambda(self, lam, args):
        env = lam.closure.child()
        for i, p in enumerate(lam.params):
            env.define(p.name, args[i] if i < len(args) else None)
        prev = self.env
        self.env = env
        try:
            if isinstance(lam.body, list):
                for s in lam.body:
                    r = self.execute(s)
                return r
            return self.execute(lam.body)
        except ReturnException as e:
            return e.value
        finally:
            self.env = prev
    
    def instantiate(self, cls, args):
        obj = ABObject(cls)
        for name, val in cls.fields.items():
            obj.fields[name] = val
        if cls.init_method:
            env = cls.init_method.closure.child()
            env.define("self", obj)
            for i, p in enumerate(cls.init_method.params):
                env.define(p.name, args[i] if i < len(args) else None)
            try:
                self.exec_block(cls.init_method.body, env)
            except ReturnException:
                pass
        return obj
    
    def exec_MemberExpression(self, node):
        obj = self.execute(node.object)
        if node.null_safe and obj is None:
            return None
        if isinstance(obj, ABObject):
            if obj.has_field(node.member):
                return obj.get_field(node.member)
            method = obj.class_def.get_method(node.member)
            if method:
                return BoundMethod(obj, method, self)
        if isinstance(obj, ABBlock):
            return obj.get_member(node.member)
        if isinstance(obj, dict):
            return obj.get(node.member)
        if isinstance(obj, list) and node.member == "length":
            return len(obj)
        if isinstance(obj, str) and node.member == "length":
            return len(obj)
        raise AttributeError(f"No attribute: {node.member}")
    
    def exec_IndexExpression(self, node):
        obj = self.execute(node.object)
        idx = self.execute(node.index)
        return obj[idx]
    
    def exec_AssignmentExpression(self, node):
        val = self.execute(node.value)
        if node.operator != "=":
            old = self.execute(node.target)
            ops = {"+=": lambda a, b: a + b, "-=": lambda a, b: a - b, "*=": lambda a, b: a * b, "/=": lambda a, b: a / b}
            val = ops[node.operator](old, val)
        if isinstance(node.target, Identifier):
            self.env.set(node.target.name, val)
        elif isinstance(node.target, MemberExpression):
            obj = self.execute(node.target.object)
            if isinstance(obj, ABObject):
                obj.set_field(node.target.member, val)
            elif isinstance(obj, dict):
                obj[node.target.member] = val
        elif isinstance(node.target, IndexExpression):
            obj = self.execute(node.target.object)
            idx = self.execute(node.target.index)
            obj[idx] = val
        return val
    
    def exec_LambdaExpression(self, node):
        return ABLambda(node.params, node.body, self.env)
    
    def exec_PipeExpression(self, node):
        val = self.execute(node.value)
        if isinstance(node.function, CallExpression):
            callee = self.execute(node.function.callee)
            args = [val] + [self.execute(a) for a in node.function.arguments]
            if callable(callee):
                return callee(*args)
            if isinstance(callee, ABFunction):
                return self.call_func(callee, args)
            if isinstance(callee, ABLambda):
                return self.call_lambda(callee, args)
        func = self.execute(node.function)
        if callable(func):
            return func(val)
        if isinstance(func, ABFunction):
            return self.call_func(func, [val])
        if isinstance(func, ABLambda):
            return self.call_lambda(func, [val])
    
    def exec_NullCoalesceExpression(self, node):
        val = self.execute(node.value)
        return val if val is not None else self.execute(node.default)
    
    def exec_RangeExpression(self, node):
        return list(range(self.execute(node.start), self.execute(node.end)))
    
    def exec_IntegerLiteral(self, node):
        return node.value
    
    def exec_FloatLiteral(self, node):
        return node.value
    
    def exec_StringLiteral(self, node):
        return node.value
    
    def exec_InterpolatedString(self, node):
        result = ""
        for p in node.parts:
            if isinstance(p, str):
                result += p
            else:
                val = self.execute(p)
                result += "null" if val is None else ("true" if val is True else ("false" if val is False else str(val)))
        return result
    
    def exec_BooleanLiteral(self, node):
        return node.value
    
    def exec_NullLiteral(self, node):
        return None
    
    def exec_Identifier(self, node):
        if node.name == "_":
            return None
        try:
            return self.env.get(node.name)
        except:
            pass
        f = self.env.get_function(node.name)
        if f:
            return f
        c = self.env.get_class(node.name)
        if c:
            return c
        b = self.env.get_block(node.name)
        if b:
            return b
        raise NameError(f"Undefined: {node.name}")
    
    def exec_ArrayLiteral(self, node):
        return [self.execute(e) for e in node.elements]
    
    def exec_MapLiteral(self, node):
        return {self.execute(k).value if hasattr(self.execute(k), "value") else self.execute(k): self.execute(v) for k, v in node.entries}
    
    def exec_SelfExpression(self, node):
        return self.env.get("self")
    
    def exec_SuperExpression(self, node):
        obj = self.env.get("self")
        parent = obj.class_def.parent
        if node.member:
            method = parent.get_method(node.member)
            if method:
                return BoundMethod(obj, method, self)
        return parent
    
    def truthy(self, val):
        if val is None:
            return False
        if isinstance(val, bool):
            return val
        if isinstance(val, (int, float)):
            return val != 0
        if isinstance(val, (str, list, dict)):
            return len(val) > 0
        return True

class BoundMethod:
    def __init__(self, instance, method, interpreter):
        self.instance = instance
        self.method = method
        self.interpreter = interpreter
    
    def __call__(self, *args):
        env = self.method.closure.child()
        env.define("self", self.instance)
        for i, p in enumerate(self.method.params):
            env.define(p.name, args[i] if i < len(args) else None)
        try:
            return self.interpreter.exec_block(self.method.body, env)
        except ReturnException as e:
            return e.value
''')

# ==================== repl.py ====================
open(os.path.join(SRC, "repl.py"), "w").write('''"""REPL"""
import os
from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter

class REPL:
    def __init__(self):
        self.interpreter = Interpreter()
    
    def run(self):
        print()
        print("=" * 40)
        print("  AryanBlock v1.0.0")
        print("  Type :help for commands, :quit to exit")
        print("=" * 40)
        print()
        
        while True:
            try:
                line = input("ab> ")
                if line.startswith(":"):
                    if line in [":quit", ":q", ":exit"]:
                        print("Goodbye!")
                        break
                    elif line in [":help", ":h"]:
                        print("Commands: :help, :quit, :clear, :reset")
                    elif line in [":clear", ":c"]:
                        os.system("cls" if os.name == "nt" else "clear")
                    elif line in [":reset", ":r"]:
                        self.interpreter = Interpreter()
                        print("Reset.")
                    else:
                        print(f"Unknown: {line}")
                    continue
                
                if not line.strip():
                    continue
                
                tokens = Lexer(line).tokenize()
                program = Parser(tokens).parse()
                
                if not program.start_block and len(program.statements) == 1:
                    stmt = program.statements[0]
                    if hasattr(stmt, "expression"):
                        result = self.interpreter.execute(stmt.expression)
                        if result is not None:
                            print(f"=> {self.fmt(result)}")
                        continue
                
                self.interpreter.interpret(program)
            
            except KeyboardInterrupt:
                print("\\n^C")
            except EOFError:
                print("\\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def fmt(self, val):
        if val is None:
            return "null"
        if isinstance(val, bool):
            return "true" if val else "false"
        if isinstance(val, str):
            return f\'"{val}"\'
        if isinstance(val, list):
            return "[" + ", ".join(self.fmt(v) for v in val) + "]"
        if isinstance(val, dict):
            return "{" + ", ".join(f\'"{k}": {self.fmt(v)}\' for k, v in val.items()) + "}"
        return str(val)

def start_repl():
    REPL().run()

if __name__ == "__main__":
    start_repl()
''')

# ==================== main.py ====================
open(os.path.join(SRC, "main.py"), "w").write('''#!/usr/bin/env python3
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
        with open(filename) as f:
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
''')

# ==================== examples/hello.ab ====================
open(os.path.join(EXAMPLES, "hello.ab"), "w").write('''// Hello World in AryanBlock

start {
    print("Hello, AryanBlock!")
    
    let name = "World"
    print("Hello, ${name}!")
    
    mut counter = 0
    loop 5 {
        counter += 1
        print("Count: ${counter}")
    }
}
''')

# ==================== setup.py ====================
open(os.path.join(BASE, "setup.py"), "w").write('''from setuptools import setup, find_packages
setup(
    name="aryanblock",
    version="1.0.0",
    packages=find_packages(),
    entry_points={"console_scripts": ["ab=src.main:main"]},
)
''')

print("All files created successfully!")
print()
print("Now run:")
print("  cd C:\\aryanblock")
print("  python src\\main.py repl")