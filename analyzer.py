"""
AryanBlock Semantic Analyzer
Performs type checking, scope resolution, and validation.
"""

from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass, field
from .ast_nodes import *
from .errors import TypeError, NameError, AryanBlockError, SourceLocation, ErrorType


@dataclass
class Symbol:
    """Represents a symbol in the symbol table."""
    name: str
    symbol_type: str  # 'variable', 'function', 'class', 'block', 'trait'
    data_type: Optional[str] = None
    is_mutable: bool = True
    is_constant: bool = False
    params: List = field(default_factory=list)
    return_type: Optional[str] = None
    defined_at: Optional[Position] = None


class SymbolTable:
    """Symbol table for tracking declarations."""
    
    def __init__(self, parent: Optional['SymbolTable'] = None, name: str = "global"):
        self.parent = parent
        self.name = name
        self.symbols: Dict[str, Symbol] = {}
    
    def define(self, symbol: Symbol) -> None:
        """Define a symbol in the current scope."""
        self.symbols[symbol.name] = symbol
    
    def resolve(self, name: str) -> Optional[Symbol]:
        """Resolve a symbol, searching up the scope chain."""
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.resolve(name)
        return None
    
    def resolve_local(self, name: str) -> Optional[Symbol]:
        """Resolve a symbol in the current scope only."""
        return self.symbols.get(name)
    
    def create_child(self, name: str) -> 'SymbolTable':
        """Create a child scope."""
        return SymbolTable(parent=self, name=name)


class SemanticAnalyzer(ASTVisitor):
    """
    Performs semantic analysis on the AST.
    
    - Type checking
    - Scope resolution
    - Variable declaration validation
    - Function signature verification
    """
    
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.current_function: Optional[str] = None
        self.current_class: Optional[str] = None
        self.errors: List[AryanBlockError] = []
        self.warnings: List[str] = []
        
        # Register built-in functions
        self._register_builtins()
    
    def _register_builtins(self):
        """Register built-in functions in the symbol table."""
        builtins = [
            ("print", ["any"], "null"),
            ("input", ["string"], "string"),
            ("len", ["any"], "int"),
            ("type", ["any"], "string"),
            ("str", ["any"], "string"),
            ("int", ["any"], "int"),
            ("float", ["any"], "float"),
            ("bool", ["any"], "bool"),
            ("array", [], "array"),
            ("map", [], "map"),
            ("range", ["int", "int?", "int?"], "array"),
            ("abs", ["float"], "float"),
            ("min", ["any"], "any"),
            ("max", ["any"], "any"),
            ("sum", ["array"], "float"),
            ("sqrt", ["float"], "float"),
            ("push", ["array", "any"], "array"),
            ("pop", ["array"], "any"),
            ("join", ["array", "string?"], "string"),
            ("split", ["string", "string?"], "array"),
            ("upper", ["string"], "string"),
            ("lower", ["string"], "string"),
            ("trim", ["string"], "string"),
            ("contains", ["any", "any"], "bool"),
            ("keys", ["map"], "array"),
            ("values", ["map"], "array"),
        ]
        
        for name, params, return_type in builtins:
            self.symbol_table.define(Symbol(
                name=name,
                symbol_type="function",
                params=params,
                return_type=return_type
            ))
    
    def analyze(self, program: Program) -> List[AryanBlockError]:
        """
        Analyze a program AST.
        
        Returns:
            List of errors found during analysis
        """
        self.errors = []
        self.visit(program)
        return self.errors
    
    def error(self, message: str, position: Position = None, 
              error_type: ErrorType = ErrorType.TYPE_ERROR):
        """Record an error."""
        location = None
        if position:
            location = SourceLocation(position.line, position.column, position.length)
        
        self.errors.append(AryanBlockError(
            error_type=error_type,
            message=message,
            location=location
        ))
    
    def warning(self, message: str):
        """Record a warning."""
        self.warnings.append(message)
    
    # ============== VISITOR METHODS ==============
    
    def visit_program(self, node: Program):
        """Visit the program root."""
        # First pass: collect all top-level declarations
        for stmt in node.statements:
            if isinstance(stmt, FunctionDeclaration):
                self.symbol_table.define(Symbol(
                    name=stmt.name,
                    symbol_type="function",
                    params=[p.name for p in stmt.params],
                    return_type=stmt.return_type.name if stmt.return_type else None
                ))
            elif isinstance(stmt, ClassDeclaration):
                self.symbol_table.define(Symbol(
                    name=stmt.name,
                    symbol_type="class"
                ))
            elif isinstance(stmt, BlockDeclaration):
                self.symbol_table.define(Symbol(
                    name=stmt.name,
                    symbol_type="block"
                ))
            elif isinstance(stmt, TraitDeclaration):
                self.symbol_table.define(Symbol(
                    name=stmt.name,
                    symbol_type="trait"
                ))
        
        # Second pass: analyze all statements
        for stmt in node.statements:
            self.visit(stmt)
        
        # Analyze start block
        if node.start_block:
            self.visit(node.start_block)
    
    def visit_start_block(self, node: StartBlock):
        """Visit the start block."""
        child_scope = self.symbol_table.create_child("start")
        old_table = self.symbol_table
        self.symbol_table = child_scope
        
        for stmt in node.body:
            self.visit(stmt)
        
        self.symbol_table = old_table
    
    def visit_var_declaration(self, node: VarDeclaration):
        """Visit a variable declaration."""
        # Check for redeclaration in current scope
        existing = self.symbol_table.resolve_local(node.name)
        if existing:
            self.error(
                f"Variable '{node.name}' is already declared in this scope",
                node.position,
                ErrorType.NAME_ERROR
            )
            return
        
        # Determine type
        declared_type = None
        if node.type_annotation:
            declared_type = node.type_annotation.name
        
        inferred_type = None
        if node.initializer:
            inferred_type = self._infer_type(node.initializer)
        
        # Type check
        if declared_type and inferred_type:
            if not self._types_compatible(declared_type, inferred_type):
                self.error(
                    f"Type mismatch: declared '{declared_type}', got '{inferred_type}'",
                    node.position,
                    ErrorType.TYPE_ERROR
                )
        
        final_type = declared_type or inferred_type or "any"
        
        self.symbol_table.define(Symbol(
            name=node.name,
            symbol_type="variable",
            data_type=final_type,
            is_mutable=node.is_mutable,
            is_constant=node.is_constant,
            defined_at=node.position
        ))
        
        if node.initializer:
            self.visit(node.initializer)
    
    def visit_function_declaration(self, node: FunctionDeclaration):
        """Visit a function declaration."""
        # Create function scope
        func_scope = self.symbol_table.create_child(f"function:{node.name}")
        old_table = self.symbol_table
        old_function = self.current_function
        
        self.symbol_table = func_scope
        self.current_function = node.name
        
        # Add parameters to scope
        for param in node.params:
            param_type = param.type_annotation.name if param.type_annotation else "any"
            self.symbol_table.define(Symbol(
                name=param.name,
                symbol_type="variable",
                data_type=param_type,
                is_mutable=True
            ))
        
        # Analyze body
        for stmt in node.body:
            self.visit(stmt)
        
        self.symbol_table = old_table
        self.current_function = old_function
    
    def visit_parameter(self, node: Parameter):
        """Visit a parameter."""
        pass
    
    def visit_class_declaration(self, node: ClassDeclaration):
        """Visit a class declaration."""
        # Verify parent class exists
        if node.parent:
            parent_symbol = self.symbol_table.resolve(node.parent)
            if not parent_symbol or parent_symbol.symbol_type != "class":
                self.error(
                    f"Parent class '{node.parent}' is not defined",
                    node.position,
                    ErrorType.NAME_ERROR
                )
        
        # Verify traits exist
        for trait_name in node.traits:
            trait_symbol = self.symbol_table.resolve(trait_name)
            if not trait_symbol or trait_symbol.symbol_type != "trait":
                self.error(
                    f"Trait '{trait_name}' is not defined",
                    node.position,
                    ErrorType.NAME_ERROR
                )
        
        # Create class scope
        class_scope = self.symbol_table.create_child(f"class:{node.name}")
        old_table = self.symbol_table
        old_class = self.current_class
        
        self.symbol_table = class_scope
        self.current_class = node.name
        
        # Add 'self' to scope
        self.symbol_table.define(Symbol(
            name="self",
            symbol_type="variable",
            data_type=node.name
        ))
        
        # Analyze members
        for member in node.members:
            self.visit(member)
        
        if node.init_method:
            self.visit(node.init_method)
        
        self.symbol_table = old_table
        self.current_class = old_class
    
    def visit_init_method(self, node: InitMethod):
        """Visit an init method."""
        init_scope = self.symbol_table.create_child("init")
        old_table = self.symbol_table
        self.symbol_table = init_scope
        
        # Add parameters
        for param in node.params:
            param_type = param.type_annotation.name if param.type_annotation else "any"
            self.symbol_table.define(Symbol(
                name=param.name,
                symbol_type="variable",
                data_type=param_type
            ))
        
        # Analyze body
        for stmt in node.body:
            self.visit(stmt)
        
        self.symbol_table = old_table
    
    def visit_trait_declaration(self, node: TraitDeclaration):
        """Visit a trait declaration."""
        for method in node.methods:
            self.visit(method)
    
    def visit_block_declaration(self, node: BlockDeclaration):
        """Visit a block declaration."""
        block_scope = self.symbol_table.create_child(f"block:{node.name}")
        old_table = self.symbol_table
        self.symbol_table = block_scope
        
        for member in node.members:
            self.visit(member)
        
        self.symbol_table = old_table
    
    def visit_import_statement(self, node: ImportStatement):
        """Visit an import statement."""
        # Just register the imports
        for item in node.items:
            self.symbol_table.define(Symbol(
                name=item,
                symbol_type="import",
                data_type="any"
            ))
    
    def visit_export_statement(self, node: ExportStatement):
        """Visit an export statement."""
        if node.declaration:
            self.visit(node.declaration)
    
    def visit_return_statement(self, node: ReturnStatement):
        """Visit a return statement."""
        if not self.current_function:
            self.error(
                "'return' outside of function",
                node.position,
                ErrorType.SYNTAX_ERROR
            )
        
        if node.value:
            self.visit(node.value)
    
    def visit_break_statement(self, node: BreakStatement):
        """Visit a break statement."""
        pass  # Loop context checking could be added
    
    def visit_continue_statement(self, node: ContinueStatement):
        """Visit a continue statement."""
        pass
    
    def visit_expression_statement(self, node: ExpressionStatement):
        """Visit an expression statement."""
        self.visit(node.expression)
    
    def visit_if_statement(self, node: IfStatement):
        """Visit an if statement."""
        self.visit(node.condition)
        
        # Analyze then branch
        then_scope = self.symbol_table.create_child("if-then")
        old_table = self.symbol_table
        self.symbol_table = then_scope
        
        for stmt in node.then_branch:
            self.visit(stmt)
        
        self.symbol_table = old_table
        
        # Analyze elif branches
        for condition, body in node.elif_branches:
            self.visit(condition)
            
            elif_scope = self.symbol_table.create_child("elif")
            self.symbol_table = elif_scope
            
            for stmt in body:
                self.visit(stmt)
            
            self.symbol_table = old_table
        
        # Analyze else branch
        if node.else_branch:
            else_scope = self.symbol_table.create_child("else")
            self.symbol_table = else_scope
            
            for stmt in node.else_branch:
                self.visit(stmt)
            
            self.symbol_table = old_table
    
    def visit_match_statement(self, node: MatchStatement):
        """Visit a match statement."""
        self.visit(node.value)
        
        for case in node.cases:
            self.visit(case)
    
    def visit_match_case(self, node: MatchCase):
        """Visit a match case."""
        self.visit(node.pattern)
        
        if isinstance(node.body, list):
            for stmt in node.body:
                self.visit(stmt)
        else:
            self.visit(node.body)
    
    def visit_for_loop(self, node: ForLoop):
        """Visit a for loop."""
        self.visit(node.iterable)
        
        # Create loop scope
        loop_scope = self.symbol_table.create_child("for")
        old_table = self.symbol_table
        self.symbol_table = loop_scope
        
        # Add loop variable
        self.symbol_table.define(Symbol(
            name=node.variable,
            symbol_type="variable",
            data_type="any",
            is_mutable=False
        ))
        
        for stmt in node.body:
            self.visit(stmt)
        
        self.symbol_table = old_table
    
    def visit_while_loop(self, node: WhileLoop):
        """Visit a while loop."""
        self.visit(node.condition)
        
        loop_scope = self.symbol_table.create_child("while")
        old_table = self.symbol_table
        self.symbol_table = loop_scope
        
        for stmt in node.body:
            self.visit(stmt)
        
        self.symbol_table = old_table
    
    def visit_loop_statement(self, node: LoopStatement):
        """Visit a loop statement."""
        self.visit(node.count)
        
        loop_scope = self.symbol_table.create_child("loop")
        old_table = self.symbol_table
        self.symbol_table = loop_scope
        
        for stmt in node.body:
            self.visit(stmt)
        
        self.symbol_table = old_table
    
    def visit_try_statement(self, node: TryStatement):
        """Visit a try statement."""
        try_scope = self.symbol_table.create_child("try")
        old_table = self.symbol_table
        self.symbol_table = try_scope
        
        for stmt in node.try_body:
            self.visit(stmt)
        
        self.symbol_table = old_table
        
        if node.catch_body:
            catch_scope = self.symbol_table.create_child("catch")
            self.symbol_table = catch_scope
            
            if node.catch_var:
                self.symbol_table.define(Symbol(
                    name=node.catch_var,
                    symbol_type="variable",
                    data_type="Error"
                ))
            
            for stmt in node.catch_body:
                self.visit(stmt)
            
            self.symbol_table = old_table
        
        if node.finally_body:
            finally_scope = self.symbol_table.create_child("finally")
            self.symbol_table = finally_scope
            
            for stmt in node.finally_body:
                self.visit(stmt)
            
            self.symbol_table = old_table
    
    def visit_binary_expression(self, node: BinaryExpression):
        """Visit a binary expression."""
        self.visit(node.left)
        self.visit(node.right)
    
    def visit_unary_expression(self, node: UnaryExpression):
        """Visit a unary expression."""
        self.visit(node.operand)
    
    def visit_call_expression(self, node: CallExpression):
        """Visit a call expression."""
        self.visit(node.callee)
        
        # Check if function exists (if it's a simple identifier)
        if isinstance(node.callee, Identifier):
            symbol = self.symbol_table.resolve(node.callee.name)
            if not symbol:
                # Could be a class constructor or imported function
                pass
        
        for arg in node.arguments:
            self.visit(arg)
    
    def visit_member_expression(self, node: MemberExpression):
        """Visit a member expression."""
        self.visit(node.object)
    
    def visit_index_expression(self, node: IndexExpression):
        """Visit an index expression."""
        self.visit(node.object)
        self.visit(node.index)
    
    def visit_assignment_expression(self, node: AssignmentExpression):
        """Visit an assignment expression."""
        # Check if target is mutable
        if isinstance(node.target, Identifier):
            symbol = self.symbol_table.resolve(node.target.name)
            if symbol:
                if symbol.is_constant:
                    self.error(
                        f"Cannot reassign constant '{node.target.name}'",
                        n                        node.position,
                        ErrorType.TYPE_ERROR
                    )
                elif not symbol.is_mutable:
                    self.error(
                        f"Cannot reassign immutable variable '{node.target.name}'",
                        node.position,
                        ErrorType.TYPE_ERROR
                    )
        
        self.visit(node.target)
        self.visit(node.value)
    
    def visit_lambda_expression(self, node: LambdaExpression):
        """Visit a lambda expression."""
        lambda_scope = self.symbol_table.create_child("lambda")
        old_table = self.symbol_table
        self.symbol_table = lambda_scope
        
        for param in node.params:
            param_type = param.type_annotation.name if param.type_annotation else "any"
            self.symbol_table.define(Symbol(
                name=param.name,
                symbol_type="variable",
                data_type=param_type
            ))
        
        self.visit(node.body)
        
        self.symbol_table = old_table
    
    def visit_pipe_expression(self, node: PipeExpression):
        """Visit a pipe expression."""
        self.visit(node.value)
        self.visit(node.function)
    
    def visit_null_coalesce_expression(self, node: NullCoalesceExpression):
        """Visit a null coalesce expression."""
        self.visit(node.value)
        self.visit(node.default)
    
    def visit_await_expression(self, node: AwaitExpression):
        """Visit an await expression."""
        self.visit(node.expression)
    
    def visit_range_expression(self, node: RangeExpression):
        """Visit a range expression."""
        self.visit(node.start)
        self.visit(node.end)
    
    def visit_integer_literal(self, node: IntegerLiteral):
        """Visit an integer literal."""
        pass
    
    def visit_float_literal(self, node: FloatLiteral):
        """Visit a float literal."""
        pass
    
    def visit_string_literal(self, node: StringLiteral):
        """Visit a string literal."""
        pass
    
    def visit_interpolated_string(self, node: InterpolatedString):
        """Visit an interpolated string."""
        for part in node.parts:
            if isinstance(part, ASTNode):
                self.visit(part)
    
    def visit_char_literal(self, node: CharLiteral):
        """Visit a char literal."""
        pass
    
    def visit_boolean_literal(self, node: BooleanLiteral):
        """Visit a boolean literal."""
        pass
    
    def visit_null_literal(self, node: NullLiteral):
        """Visit a null literal."""
        pass
    
    def visit_identifier(self, node: Identifier):
        """Visit an identifier."""
        if node.name == '_':
            return  # Wildcard pattern
        
        symbol = self.symbol_table.resolve(node.name)
        if not symbol:
            # Could be a class name or built-in
            pass
    
    def visit_array_literal(self, node: ArrayLiteral):
        """Visit an array literal."""
        for element in node.elements:
            self.visit(element)
    
    def visit_map_literal(self, node: MapLiteral):
        """Visit a map literal."""
        for key, value in node.entries:
            self.visit(key)
            self.visit(value)
    
    def visit_tuple_literal(self, node: TupleLiteral):
        """Visit a tuple literal."""
        for element in node.elements:
            self.visit(element)
    
    def visit_type_annotation(self, node: TypeAnnotation):
        """Visit a type annotation."""
        pass
    
    def visit_new_expression(self, node: NewExpression):
        """Visit a new expression."""
        # Check if class exists
        symbol = self.symbol_table.resolve(node.class_name)
        if not symbol or symbol.symbol_type != "class":
            self.error(
                f"Class '{node.class_name}' is not defined",
                node.position,
                ErrorType.NAME_ERROR
            )
        
        for arg in node.arguments:
            self.visit(arg)
    
    def visit_super_expression(self, node: SuperExpression):
        """Visit a super expression."""
        if not self.current_class:
            self.error(
                "'super' outside of class",
                node.position,
                ErrorType.SYNTAX_ERROR
            )
    
    def visit_self_expression(self, node: SelfExpression):
        """Visit a self expression."""
        if not self.current_class:
            self.error(
                "'self' outside of class",
                node.position,
                ErrorType.SYNTAX_ERROR
            )
    
    # ============== HELPER METHODS ==============
    
    def _infer_type(self, node: ASTNode) -> str:
        """Infer the type of an expression."""
        if isinstance(node, IntegerLiteral):
            return "int"
        elif isinstance(node, FloatLiteral):
            return "float"
        elif isinstance(node, StringLiteral):
            return "string"
        elif isinstance(node, InterpolatedString):
            return "string"
        elif isinstance(node, CharLiteral):
            return "char"
        elif isinstance(node, BooleanLiteral):
            return "bool"
        elif isinstance(node, NullLiteral):
            return "null"
        elif isinstance(node, ArrayLiteral):
            return "array"
        elif isinstance(node, MapLiteral):
            return "map"
        elif isinstance(node, TupleLiteral):
            return "tuple"
        elif isinstance(node, Identifier):
            symbol = self.symbol_table.resolve(node.name)
            if symbol:
                return symbol.data_type or "any"
            return "any"
        elif isinstance(node, BinaryExpression):
            left_type = self._infer_type(node.left)
            right_type = self._infer_type(node.right)
            
            # Comparison operators return bool
            if node.operator in ['==', '!=', '<', '>', '<=', '>=', 'and', 'or']:
                return "bool"
            
            # Numeric operations
            if node.operator in ['+', '-', '*', '/', '%', '**']:
                if left_type == "float" or right_type == "float":
                    return "float"
                if left_type == "int" and right_type == "int":
                    return "int"
                if left_type == "string" and node.operator == '+':
                    return "string"
            
            return "any"
        elif isinstance(node, UnaryExpression):
            if node.operator == 'not':
                return "bool"
            return self._infer_type(node.operand)
        elif isinstance(node, CallExpression):
            if isinstance(node.callee, Identifier):
                symbol = self.symbol_table.resolve(node.callee.name)
                if symbol and symbol.return_type:
                    return symbol.return_type
            return "any"
        
        return "any"
    
    def _types_compatible(self, expected: str, actual: str) -> bool:
        """Check if two types are compatible."""
        if expected == "any" or actual == "any":
            return True
        if expected == actual:
            return True
        
        # Numeric compatibility
        if expected in ["int", "float"] and actual in ["int", "float"]:
            return True
        
        # Nullable types
        if expected.endswith("?"):
            base_type = expected[:-1]
            return actual == "null" or self._types_compatible(base_type, actual)
        
        return False


def analyze(source: str, filename: str = "<stdin>") -> List[AryanBlockError]:
    """
    Convenience function to analyze source code.
    
    Args:
        source: Source code string
        filename: Name of the source file
        
    Returns:
        List of semantic errors
    """
    from .parser import parse
    
    program = parse(source, filename)
    analyzer = SemanticAnalyzer()
    return analyzer.analyze(program)