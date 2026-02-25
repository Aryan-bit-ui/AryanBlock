"""AST Node definitions"""
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
