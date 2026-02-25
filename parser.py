"""Parser"""
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
