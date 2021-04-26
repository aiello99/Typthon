#!/usr/bin/env python3


class ParseError(Exception):
    pass


class SymbolTable(object):
    """
    Base symbol table class.

    Features a symbol table for
    """

    def __init__(self):
        self.scope_stack = [dict()]
        self.functions_scope_stack = [dict()]
        self.dict_stack= [dict()]
        self.return_stack = []
        self.while_scope_counter = 0

    def __str__(self):
        return f"scope_stack: {self.scope_stack}, fn_stack: {self.functions_scope_stack}, ret_stack: {self.return_stack}, while_counter: {self.while_scope_counter}"

    def push_scope(self):
        self.scope_stack.append(dict())
        self.functions_scope_stack.append(dict())
        self.dict_stack.append(dict())

    def pop_scope(self):
        assert len(self.scope_stack) > 1 and len(self.functions_scope_stack) > 1
        self.scope_stack.pop()
        self.functions_scope_stack.pop()
        self.dict_stack.pop()

    def declare_variable(self, name, type, line_number):
        """
        Add a new variable.
        Need to do duplicate variable declaration error checking.
        """
        if name in self.scope_stack[-1]:
            raise ParseError('Redeclaring variable named "' + name + '"', line_number)
        self.scope_stack[-1][name] = type

    def lookup_variable(self, name, line_number):
        """
        Return the type of the variable named 'name', or throw
        a ParseError if the variable is not declared in the scope.
        """
        # You should traverse through the entire scope stack
        for scope in reversed(self.scope_stack):
            if name in scope:
                return scope[name]
        raise ParseError('Referencing undefined variable "' + name + '"', line_number)

    def declare_function(self, name, input_types, output_type, line_number):
        """
        Add a new function
        """
        if name in self.functions_scope_stack[-1]:
            raise ParseError('Redeclaring function named "' + name + '"', line_number)
        self.functions_scope_stack[-1][name] = (input_types, output_type)

    def lookup_function(self, name, line_number):
        """
        Return a tuple of (input_types, output_type)
        """
        for scope in reversed(self.functions_scope_stack):
            if name in scope:
                return scope[name]
        raise ParseError('Referencing undefined function "' + name + '"', line_number)

    def declare_dict(self, name, key_type, val_type, line_number):
        if name in self.dict_stack[-1]:
            raise ParseError('Redeclaring dictionary named "' + name + '"', line_number)
        self.dict_stack[-1][name] = (key_type, val_type)

    def lookup_dict(self, name, line_number):
        for d in reversed(self.dict_stack):
            if name in d:
                return d[name]
        raise ParseError('Referencing undefined dictionary "' + name + '"', line_number)

    def push_return_scope(self, return_type):
        self.return_stack.append(return_type)

    def get_current_return_scope(self):
        if len(self.return_stack) == 0:
            return None
        return self.return_stack[-1]

    def pop_return_scope(self):
        return self.return_stack.pop()

    def push_while_scope(self):
        self.while_scope_counter += 1

    def is_in_while_scope(self):
        return self.while_scope_counter > 0

    def pop_while_scope(self):
        assert self.while_scope_counter > 0
        self.while_scope_counter -= 1
