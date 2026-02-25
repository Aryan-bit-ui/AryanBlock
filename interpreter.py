"""Interpreter"""
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
