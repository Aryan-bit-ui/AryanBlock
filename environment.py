"""Environment and runtime types"""
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
