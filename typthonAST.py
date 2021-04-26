#!/usr/bin/env python3

import sys

# Taken from the Week 5 exercise, we will use this Node class as our AST.


class Node(object):
    """
    Abstract base class for AST nodes

    Things to implement:
        __init__: Initialize attributes / children

        children: Method to return list of children. Alternatively, you can
                  look into __iter__ method, which allow nodes to be
                  iterable.
    """

    def children(self):
        """
        A sequence of all children that are Nodes
        """
        pass

    # Set of attributes for a given node
    attr_names = ()


class NodeVisitor(object):
    """
    A base NodeVisitor class for visiting MiniJava nodes.
    Define your own visit_X methods to, where X is the class
    name you want to visit with these methods.

    Refer to visit_Program, for example
    """

    def visit(self, node, offset=0):
        """
        Your compiler can call this method to traverse through your AST
        """
        method = "visit_" + node.__class__.__name__
        return getattr(self, method, self.generic_visit)(node, offset)

    def generic_visit(self, node, offset=0):
        """
        Default visit method that simply prints out given node's attributes,
        then traverses through its children. This is called if no explicit
        visitor function exists for a node.

        NOTE: A method within Node object with similar behaviour might be
              useful when debugging your project
        """
        lead = " " * offset

        output = lead + node.__class__.__name__ + ": "

        if node.attr_names:
            vlist = [getattr(node, n) for n in node.attr_names]
            output += ", ".join("%s" % v for v in vlist)

        print(output)

        for (child_name, child) in node.children():
            self.visit(child, offset=offset + 2)

    def visit_File(self, node, offset=0):
        """
        Custom visit method for "Program" node
        """
        print("====== PROGRAM START ======")
        self.visit(node.statements, offset=2)
        print("====== PROGRAM END ======")


class File(Node):
    """
    Similar to MiniJava's program node, this is the node for the entire program.
    The entire file is essentially a list of statements.
    """

    def __init__(self, statements, coord=None):
        self.statements = statements

    def children(self):
        nodelist = []
        if self.statements is not None:
            nodelist.append(("statements", self.statements))
        return tuple(nodelist)

    attr_names = ()


class StmtList(Node):
    """
    AST Node for a list of statements.
    """

    def __init__(self, stmt_lst, coord=None):
        self.stmt_lst = stmt_lst
        self.coord = coord

    def children(self):
        nodelist = []
        for i, stmt in enumerate(self.stmt_lst or []):
            nodelist.append(("stmt[%d]" % i, stmt))
        return nodelist

    attr_names = ()


class VarDecl(Node):
    """
    AST Node for a variable declaration.
    """

    def __init__(self, name, type, expr=None, coord=None):
        self.name = name
        self.type = type
        self.expr = expr
        self.coord = coord

    def children(self):
        nodelist = []
        if self.type is not None:
            nodelist.append(("type", self.type))
        if self.expr is not None:
            nodelist.append(("expr", self.expr))
        return tuple(nodelist)

    def __str__(self):
        return f"{self.name} := {self.expr}"

    attr_names = ("name",)


class FunctionDefn(Node):
    """
    AST Node for function declaration.
    """

    def __init__(self, name, ret_type, params, body, coord=None):
        self.name = name
        self.ret_type = ret_type
        self.params = params
        self.body = body
        self.coord = coord

    def children(self):
        nodelist = []
        if self.ret_type is not None:
            nodelist.append(("ret_type", self.ret_type))
        if self.body is not None:
            nodelist.append(("body", self.body))
        if self.params is not None:
            nodelist.append(("params", self.params))
        return tuple(nodelist)

    attr_names = ("name",)


class RetStmt(Node):
    """
    AST Node for return statement.
    """

    def __init__(self, expr, coord=None):
        self.expr = expr
        self.coord = coord

    def children(self):
        nodelist = []
        if self.expr is not None:
            nodelist.append(("expr", self.expr))
        return tuple(nodelist)

    def __str__(self):
        return f"return {self.expr}"

    attr_names = ()


class WhileStmt(Node):
    """
    AST Node for a while loop.
    """

    def __init__(self, cond, body, coord=None):
        self.cond = cond
        self.body = body
        self.coord = coord

    def children(self):
        nodelist = []
        if self.cond is not None:
            nodelist.append(("cond", self.cond))
        if self.body is not None:
            nodelist.append(("body", self.body))
        return tuple(nodelist)

    attr_names = ()


class BreakStmt(Node):
    """
    AST Node for a break statement.
    """

    def __init__(self, coord=None):
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    def __str__(self):
        return "Break"

    attr_names = ()


class VarAssign(Node):
    """
    AST Node for re-assigning expr to a variable.
    """

    def __init__(
        self,
        name,
        expr=None,
        coord=None,
    ):
        self.name = name
        self.expr = expr
        self.coord = coord

    def children(self):
        nodelist = []
        if self.expr is not None:
            nodelist.append(("expr", self.expr))
        return tuple(nodelist)

    def __str__(self):
        return f"{self.name} := {self.expr}"

    attr_names = ("name",)


class ArrayExprList(Node):
    """
    AST Node for an array of expressions.

    exprs all must be of the same type.
    """

    def __init__(self, exprs, coord=None):
        self.exprs = exprs
        self.coord = coord

    def children(self):
        nodelist = []
        for i, child in enumerate(self.exprs or []):
            nodelist.append(("exprs[%d]" % i, child))
        return tuple(nodelist)

    def __str__(self):
        output = "["
        for expr in self.exprs:
            output += f"{expr},"
        output += "]"
        return output

    attr_names = ()


class ParamList(Node):
    """
    AST Node for comma separated parameters in a function declaration.
    """

    def __init__(self, params, coord=None):
        self.params = params
        self.coord = coord

    def children(self):
        nodelist = []
        for i, child in enumerate(self.params or []):
            nodelist.append(("params[%d]" % i, child))
        return tuple(nodelist)

    attr_names = ()


class Param(Node):
    """
    AST Node for a parameter.
    """

    def __init__(self, name, type, coord=None):
        self.name = name
        self.type = type
        self.coord = coord

    def children(self):
        nodelist = []
        if self.type is not None:
            nodelist.append(("type", self.type))
        return tuple(nodelist)

    attr_names = ("name",)


class FunctionCall(Node):
    """
    AST Node for a function call.
    """

    def __init__(self, name, arguments, coord=None):
        self.name = name
        self.arguments = arguments
        self.coord = coord

    def children(self):
        nodelist = []
        if self.arguments is not None:
            nodelist.append(("arguments", self.arguments))
        return tuple(nodelist)

    def __str__(self):
        return f"FuncCall {self.name} with {self.arguments}"

    attr_names = ("name",)


class Arguments(Node):
    """
    AST Node for comma separated expressions passed to a function call.
    """

    def __init__(self, exprs, coord=None):
        self.exprs = exprs
        self.coord = coord

    def children(self):
        nodelist = []
        for i, child in enumerate(self.exprs or []):
            nodelist.append(("args[%d]" % i, child))
        return tuple(nodelist)

    def __str__(self):
        output = "("
        for expr in self.exprs:
            output += f"{expr}, "
        return output + ")"

    attr_names = ()


class Constant(Node):
    """
    AST Node for a constant
    """

    def __init__(self, type, value, coord=None):
        self.type = type
        self.value = value
        self.coord = coord

    def children(self):
        nodelist = []
        nodelist.append(("type", self.type))
        return tuple(nodelist)

    def __str__(self):
        return f"{self.value}"

    attr_names = ("value",)


class ID(Node):
    """
    AST Node for a ID
    """

    def __init__(self, name, coord=None):
        self.name = name
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    def __str__(self):
        return f"{self.name}"

    attr_names = ("name",)


class Type(Node):
    """
    AST Node for a type.
    """

    def __init__(self, name, coord=None):
        self.name = name
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    def __str__(self):
        return str(self.name)

    attr_names = ("name",)


class Array_Type(Node):
    """
    AST Node for an array's type.
    """

    def __init__(self, innerType, coord=None):
        self.innerType = innerType
        self.coord = coord
        self.name = f"[{innerType.name}]"

    def children(self):
        nodelist = []
        nodelist.append(("type", self.innerType))
        return tuple(nodelist)

    def __str__(self):
        return f"[{self.innerType}]"

    attr_names = ("name",)


class FunctionalType(Node):
    """
    AST Node for storing the input and output types of a function
    """

    # (int, str) -> int

    def __init__(self, input_type_arr, returnType, coord=None):
        self.input_type_arr = input_type_arr
        self.returnType = returnType
        self.coord = coord
        self.name = str(self)

    def __str__(self):
        return f"({', '.join([t.name for t in self.input_type_arr])}) -> {self.returnType.name}"

    def children(self):
        nodelist = []
        for i, param_type in enumerate(self.input_type_arr or []):
            nodelist.append(("param_types[%d]" % i, param_type))
        nodelist.append(("return_type", self.returnType))
        return tuple(nodelist)

    attr_names = "name"


class BinOp(Node):
    """
    AST Node for binary operations on expressions.
    """

    def __init__(self, op, left, right, coord=None):
        self.op = op
        self.left = left
        self.right = right
        self.coord = coord

    def children(self):
        nodelist = []
        if self.left is not None:
            nodelist.append(("left", self.left))
        if self.right is not None:
            nodelist.append(("right", self.right))
        return tuple(nodelist)

    def __str__(self):
        return f"{self.left} {self.op} {self.right}"

    attr_names = ("op",)


class UnaryOp(Node):
    """
    AST Node for unary operations on expressions.
    """

    def __init__(self, op, expr, coord=None):
        self.op = op
        self.expr = expr

    def children(self):
        nodelist = []
        nodelist.append(("expr", self.expr))

        return tuple(nodelist)

    def __str__(self):
        if self.op == "not":
            return f"{self.op} {self.expr}"
        return f"{self.op}{self.expr}"

    attr_names = ("op",)


class IfStmt(Node):
    """
    AST Node for if statements.

    false_body is optional, as if statements do not need an else statement.
    """

    def __init__(self, cond, true_body, false_body, coord=None):
        self.cond = cond
        self.true_body = true_body
        self.false_body = false_body
        self.coord = coord

    def children(self):
        nodelist = []
        if self.cond is not None:
            nodelist.append(("cond", self.cond))
        if self.true_body is not None:
            nodelist.append(("true_body", self.true_body))
        if self.false_body is not None:
            nodelist.append(("false_body", self.false_body))
        return tuple(nodelist)

    attr_names = ()


class ElifStmt(Node):
    """
    AST Node for elif statements.
    """

    def __init__(self, cond, true_body, false_body, coord=None):
        self.cond = cond
        self.true_body = true_body
        self.false_body = false_body
        self.coord = coord

    def children(self):
        nodelist = []
        if self.cond is not None:
            nodelist.append(("cond", self.cond))
        if self.true_body is not None:
            nodelist.append(("true_body", self.true_body))
        if self.false_body is not None:
            nodelist.append(("false_body", self.false_body))
        return tuple(nodelist)

    attr_names = ()


class ArrayBuiltinCall(Node):
    """
    AST Node for array operations.

    builtinFunction is one of .pop, .append, or .remove.
    """

    def __init__(self, arrayID, builtinFunction, argumentExpression, coord=None):
        self.arrayID = arrayID
        self.builtinFunction = builtinFunction
        self.argumentExpression = argumentExpression
        self.coord = coord

    def children(self):
        nodelist = []
        nodelist.append(("expr", self.argumentExpression))

        return tuple(nodelist)

    def __str__(self):
        return f"{self.arrayID}{self.builtinFunction}({self.argumentExpression})"

    attr_names = (
        "arrayID",
        "builtinFunction",
    )


class ArraySlice(Node):
    """
    AST Node for array slicing.
    """

    def __init__(self, name, expr1, expr2, coord=None):
        self.name = name
        self.expr1 = expr1
        self.expr2 = expr2
        self.coord = coord

    def children(self):
        nodelist = []
        if self.expr1 is not None:
            nodelist.append(("expr1", self.expr1))
        if self.expr2 is not None:
            nodelist.append(("expr2", self.expr2))
        return tuple(nodelist)

    def __str__(self):
        return f"{self.name}[{self.expr1}:{self.expr2}]"

    attr_names = ("name",)


class ArrayIndex(Node):
    """
    AST Node for array slicing.
    """

    def __init__(self, name, expr, coord=None):
        self.name = name
        self.expr = expr
        self.coord = coord

    def children(self):
        nodelist = []
        if self.expr is not None:
            nodelist.append(("expr", self.expr))
        return tuple(nodelist)

    def __str__(self):
        return f"{self.name}[{self.expr}]"

    attr_names = ("name",)


class Dict_Type(Node):
    """
    AST Node for dict types
    """

    def __init__(self, key_type, val_type, coord=None):
        self.key_type = key_type
        self.val_type = val_type
        self.coord = coord
        self.name = f"{{{self.key_type.name}, {self.val_type.name}}}"

    def children(
        self,
    ):
        nodelist = []
        nodelist.append(("key_type", self.key_type))
        nodelist.append(("val_type", self.val_type))
        return tuple(nodelist)

    attr_names = ("name",)


class DictBuiltinCall(Node):
    """
    AST Node for dict operations.

    builtinFunction is one of .set or .get
    """

    def __init__(self, dictID, builtinFunction, argumentExpression, coord=None):
        self.dictID = dictID
        self.builtinFunction = builtinFunction
        self.argumentExpression = argumentExpression
        self.coord = coord

    def children(self):
        nodelist = []
        nodelist.append(("expr", self.argumentExpression))

        return tuple(nodelist)

    def __str__(self):
        return f"{self.dictID}{self.builtinFunction}{self.argumentExpression}"

    attr_names = (
        "dictID",
        "builtinFunction",
    )
