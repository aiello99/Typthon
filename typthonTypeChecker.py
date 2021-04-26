# from sprint3.typthonSymbolTable import SymbolTable, ParseError
# import sprint3.typthonAST as ast

from typthonSymbolTable import SymbolTable, ParseError
import typthonAST as ast


class TypeChecker(object):
    def typecheck(self, node, st=None):
        method = "check_" + node.__class__.__name__
        return getattr(self, method)(node, st)

    def generic_typecheck(self, node, st=None):
        print(node)
        if node is None:
            return ""
        else:
            return "".join(self.typecheck(c, st) for c_name, c in node.children())

    def eq_type(self, t1, t2):
        """
        Helper function to check if two given type node is that of the
        same type. Precondition is that both t1 and t2 are that of class Type
        """
        t1_is_type = isinstance(t1, ast.Type) or isinstance(
            t1, ast.Array_Type) or isinstance(t1, ast.Dict_Type)
        t2_is_type = isinstance(t2, ast.Type) or isinstance(
            t2, ast.Array_Type) or isinstance(t2, ast.Dict_Type)

        if not (t1_is_type and t2_is_type):
            raise ParseError(
                f"eq_type invoked on non-type objects, {t1.__class__} and {t2.__class__}"
            )

        # {} <- type name dict
        # {} <- ast.dict_type(None, None)
        if isinstance(t1, ast.Type) and isinstance(t2, ast.Type):
            return t1.name == t2.name
        elif isinstance(t1, ast.Array_Type) and isinstance(t2, ast.Array_Type):
            return self.eq_type(t1.innerType, t2.innerType)
        elif isinstance(t1, ast.Dict_Type) and isinstance(t2, ast.Dict_Type):
            t2_is_empty_dict = self.eq_type(t2.key_type, ast.Type(
                "NullType")) and self.eq_type(t2.val_type, ast.Type("NullType"))
            if t2_is_empty_dict:
                return True

            return self.eq_type(t1.key_type, t2.key_type) and self.eq_type(t1.val_type, t2.val_type)
        else:
            return False

    def check_File(self, node: ast.File, st=None):

        global_st = SymbolTable()
        for (child_name, child) in node.children():
            child_st = self.typecheck(child, global_st)

        return global_st

    def check_Constant(self, node: ast.Constant, st):
        """
        Returns the type of the constant. If the constant refers to
        some kind of id, then we need to find if the id has been declared.
        """

        return node.type

    def check_BinOp(self, node: ast.BinOp, st):
        """
        NOTE
        You should also check if the type of the left and right operation
        makes sense in the context of the operator (ie., you should not be
        able to add/subtract/multiply/divide strings or booleans). In this
        example, it only checks if the left and right expressions are of the
        same type, but that won't be sufficient for your project.

        | expression "+" expression # integer or array types only
        | expression "-" expression # integer type only
        | expression "*" expression # integer type only
        | expression "/" expression # integer type only
        | expression "and" expression # boolean types only
        | expression "or" expression  # boolean types only
        | expression "==" expression
        | expression "!=" expression
        | expression "%" expression # integer type only
        | expression "<" expression # integer type only
        | expression ">" expression # integer type only
        | expression "<=" expression # integer type only
        | expression ">=" expression # integer type only

        """
        left_type = self.typecheck(node.left, st)
        right_type = self.typecheck(node.right, st)

        if node.op in {"+", "-", "*", "/", "%", "<", ">", "<=", ">="}:
            if (not self.eq_type(left_type, ast.Type("int"))) or (
                not self.eq_type(right_type, ast.Type("int"))
            ):
                raise ParseError(
                    f"Tried to call integer binary operation on {left_type.name} and {right_type.name} types",
                    node.coord,
                )
            return (
                ast.Type("bool")
                if node.op in {"<", ">", "<=", ">="}
                else ast.Type("int")
            )

        if node.op in {"and", "or"}:
            if (not self.eq_type(left_type, ast.Type("bool"))) or (
                not self.eq_type(right_type, ast.Type("bool"))
            ):
                raise ParseError(
                    f"Tried to call boolean binary operation on {left_type.name} and {right_type.name} types",
                    node.coord,
                )
            return ast.Type("bool")

        return ast.Type("bool")

    def check_UnaryOp(self, node: ast.UnaryOp, st):
        """
        | "not" expression
        | "-"expression # only for integer types
        """
        expression_type = self.typecheck(node.expr, st)
        if node.op == "not":
            if not self.eq_type(expression_type, ast.Type("bool")):
                raise ParseError(
                    f"Tried calling 'not' with non boolean variable of type {expression_type.name}"
                )
        else:
            if not self.eq_type(expression_type, ast.Type("int")):
                raise ParseError(
                    f"Tried calling '-' with non integer variable of type {expression_type.name}"
                )

        return expression_type

    def check_VarDecl(self, node: ast.VarDecl, st):
        """
        Checks if the expr declared with the variable has the same type that the
        variable was declared with.
        """
        declared_type = node.type
        expression_type = self.typecheck(node.expr, st)
        # If array Type expression Type can be [None]

        if not self.eq_type(declared_type, expression_type):
            raise ParseError(
                f"Tried to declare variable of type {declared_type.name} but with value of type {expression_type.name}",
                node.coord,
            )
        if isinstance(declared_type, ast.Dict_Type):
            st.declare_dict(node.name, node.type.key_type,
                            node.type.val_type, node.coord)
        st.declare_variable(node.name, node.type, node.coord)

        return ast.Type("NullType")

    def check_StmtList(self, node: ast.StmtList, st):
        """
        Iterates through a StmtList, and determines the type of each statement.
        Used for every scope be it if statements, while loops, etc...
        """
        retTypeFound = False
        retType = ast.Type("NullType")
        for stmt in node.stmt_lst:
            if retTypeFound:
                raise ParseError(
                    f"Found extra statement(s) after function returned", node.coord
                )
            elif isinstance(stmt, ast.RetStmt) or isinstance(stmt, ast.BreakStmt):
                retTypeFound = True
                retType = self.typecheck(stmt, st)
            elif isinstance(stmt, ast.IfStmt):
                ifStmtType = self.typecheck(stmt, st)
                if not self.eq_type(ifStmtType, ast.Type("NullType")):
                    retTypeFound = True
                    retType = ifStmtType
            else:
                stmtType = self.typecheck(stmt, st)

        return retType

    def check_ID(self, node: ast.ID, st: SymbolTable):
        """
        Checks the type of an ID in the symbol table.
        """
        return st.lookup_variable(node.name, node.coord)

    def check_VarAssign(self, node: ast.VarAssign, st: SymbolTable):
        """
        variableName "=" expression # variableName must already be declared
        """

        declaredType = st.lookup_variable(node.name, node.coord)
        expressionType = self.typecheck(node.expr, st)
        if not self.eq_type(declaredType, expressionType):
            raise ParseError(
                f"Variable {node.name} was declared as type {declaredType.name} but was assigned value of {expressionType.name} type",
                node.coord,
            )
        return ast.Type("NullType")
        # return declaredType

    def check_ArrayExprList(self, node: ast.ArrayExprList, st: SymbolTable):

        p_type = None
        for expression in node.exprs:
            expression_type = self.typecheck(expression, st)
            if not p_type:
                p_type = expression_type
            else:
                if not self.eq_type(p_type, expression_type):
                    raise ParseError(
                        f"Array has mixed types {p_type.name}, {expression_type.name}. Array can only have one type",
                        node.coord,
                    )
        return ast.Array_Type(p_type)

    def check_ArrayIndex(self, node: ast.ArrayIndex, st: SymbolTable):
        """
        | arrayName"["expression"]" # expression must be of type integer
        """
        # first check that arrayName is a valid array ID
        array_type = st.lookup_variable(node.name, node.coord)
        if not isinstance(array_type, ast.Array_Type):
            raise ParseError(
                f"Tried to index non array variable of type {array_type.name}",
                node.coord,
            )

        # then check that expression is of type int
        expr_type = self.typecheck(node.expr, st)
        if not self.eq_type(expr_type, ast.Type("int")):
            raise ParseError(
                f"Tried to index an array with non integer index of type {expr_type.name}",
                node.coord,
            )

        # return inner typer of the array
        return array_type.innerType

    def check_ArraySlice(self, node: ast.ArraySlice, st: SymbolTable):
        """
        | arrayName"["expression ":" expression "]" # expressions must be of type integer
        """
        # first check that arrayName is a valid array ID
        array_type = st.lookup_variable(node.name, node.coord)
        if not isinstance(array_type, ast.Array_Type):
            raise ParseError(
                f"Tried to slice non array variable of type {array_type.name}",
                node.coord,
            )

        # then check that expression is of type int
        expr1_type = self.typecheck(node.expr1)
        expr2_type = self.typecheck(node.expr2)
        if not self.eq_type(expr1_type, ast.Type("int")) or not self.eq_type(
            expr2_type, ast.Type("int")
        ):
            raise ParseError(
                f"Tried to slice array with non integer indices of types {expr1_type.name}, {expr2_type.name}",
                node.coord,
            )

        # return type of the array
        return array_type

    def check_ArrayBuiltinCall(self, node: ast.ArrayBuiltinCall, st: SymbolTable):
        """
        builtinFunction is one of .pop, .append, or .remove.
        """

        # first, verify that variable is an array
        array_type = st.lookup_variable(node.arrayID, node.coord)
        if not isinstance(array_type, ast.Array_Type):
            raise ParseError(
                f"Tried to call {node.builtinFunction} on non array variable of type {array_type.name}",
                node.coord,
            )

        # check if argumentExpression is of the right type.
        inner_type = array_type.innerType
        argument_expr_type = self.typecheck(node.argumentExpression)

        if node.builtinFunction == ".pop":
            if not self.eq_type(argument_expr_type, ast.Type("int")):
                raise ParseError(
                    f"Tried to pop from array with non integer index of type {argument_expr_type.name}",
                    node.coord,
                )
            else:
                return inner_type
        else:
            if not self.eq_type(argument_expr_type, inner_type):
                raise ParseError(
                    f"Mismatch of types on call of {node.builtinFunction}, expected {inner_type.name}"
                )
            else:
                return ast.Type("NullType")

    def check_FunctionDefn(self, node: ast.FunctionDefn, st: SymbolTable):
        """
        "def" functionName "(" parameters ")" "->" type ":" functionBlock
        """
        # add each param to the symboltable
        # use symbol table to type check functionblock based on return type of function
        # if type check passes, then remove params from symbol table
        # save functional type in symbol table

        st.push_scope()
        st.push_return_scope(node.ret_type)
        # pushes expected return type to symbol table

        # Go through the parameters
        param_types = []
        if node.params.params:
            for param in node.params.params:
                if isinstance(param.type, ast.Dict_Type):
                    st.declare_dict(param.name, param.type.key_type,
                                    param.type.val_type, param.coord)
                st.declare_variable(param.name, param.type, param.coord)
                param_types.append(param.type)

        body_return_type = self.typecheck(node.body, st)

        st.pop_return_scope()
        st.pop_scope()

        if not self.eq_type(node.ret_type, body_return_type):
            raise ParseError(
                f"Return type of function body {body_return_type.name} doesn't match declared return type of function {node.ret_type.name}",
                node.coord,
            )

        st.declare_function(node.name, param_types, node.ret_type, node.coord)

        return ast.Type("NullType")

    def check_RetStmt(self, node: ast.RetStmt, st: SymbolTable):
        expected_return_type = st.get_current_return_scope()
        if expected_return_type == None:
            raise ParseError(
                "Attempted to return from outside function definition", node.coord
            )

        actual_return_type = self.typecheck(node.expr, st)
        if not self.eq_type(expected_return_type, actual_return_type):
            raise ParseError(
                f"Return type of {actual_return_type.name} does not match with expected type {expected_return_type.name}",
                node.coord,
            )

        return actual_return_type

    def check_FunctionCall(self, node: ast.FunctionCall, st: SymbolTable):
        expected_input_types, output_type = st.lookup_function(
            node.name, node.coord)
        if not node.arguments.exprs:
            node.arguments.exprs = []

        given_input_types = [self.typecheck(e, st)
                             for e in node.arguments.exprs]

        types_match = len(node.arguments.exprs) == len(expected_input_types)
        if types_match:
            for input_type, given_type in zip(expected_input_types, given_input_types):
                if not self.eq_type(input_type, given_type):
                    types_match = False
                    break

        if not types_match:
            raise ParseError(
                f"Function {node.name} was expecting arguments ({', '.join([t.name for t in expected_input_types])}) but received ({', '.join([t.name for t in given_input_types])})",
                node.coord,
            )
        return output_type

    def check_IfStmt(self, node: ast.IfStmt, st: SymbolTable):
        cond_type = self.typecheck(node.cond, st)
        if not self.eq_type(cond_type, ast.Type("bool")):
            raise ParseError(
                f"Condition of If statment was type {cond_type.name}, expected bool",
                node.coord,
            )

        trueBodyType = self.typecheck(node.true_body, st)
        if node.false_body is not None:
            falseBodyType = self.typecheck(node.false_body, st)

        if not node.false_body or self.eq_type(falseBodyType, ast.Type("NullType")):
            return ast.Type("NullType")
        return trueBodyType

    def check_ElifStmt(self, node: ast.ElifStmt, st: SymbolTable):
        cond_type = self.typecheck(node.cond, st)
        if not self.eq_type(cond_type, ast.Type("bool")):
            raise ParseError("Condition in Elif not of type bool.", node.coord)

        trueBodyType = self.typecheck(node.true_body, st)
        if node.false_body is not None:
            falseBodyType = self.typecheck(node.false_body, st)

        if not node.false_body or self.eq_type(falseBodyType, ast.Type("NullType")):
            return ast.Type("NullType")
        return trueBodyType

    def check_WhileStmt(self, node: ast.WhileStmt, st: SymbolTable):
        cond_type = self.typecheck(node.cond, st)
        if not self.eq_type(cond_type, ast.Type("bool")):
            raise ParseError(
                "Condition in While Statement not of type bool.", node.coord
            )

        st.push_while_scope()
        self.typecheck(node.body, st)
        st.pop_while_scope()
        return ast.Type("NullType")

    def check_BreakStmt(self, node: ast.BreakStmt, st: SymbolTable):
        if not st.is_in_while_scope():
            raise ParseError(
                "Attempted to break from outside while loop", node.coord)

        return ast.Type("NullType")

    # def check_Dict(self, node: ast.Dict, st: SymbolTable):

    def check_DictBuiltinCall(self, node: ast.DictBuiltinCall, st: SymbolTable):
        # Check that ID is actually dict
        # idType = st.lookup_variable(node.dictID, node.coord)
        # if not self.eq_type(idType, ast.Type("dict")):
        #     raise ParseError(
        #         f"Tried to call {node.builtinFunction} on non dictionary variable of type {idType}",
        #         node.coord,
        #     )

        key_type, val_type = st.lookup_dict(node.dictID, node.coord)
        arg_type = self.typecheck(node.argumentExpression.exprs[0], st)
        if not self.eq_type(key_type, arg_type):
            raise ParseError(f"Expected Key Type: {key_type}, but recieved Type {arg_type} for dict {node.dictID}",
                             node.coord,
                             )
        if node.builtinFunction == ".get":
            return val_type
        elif node.builtinFunction == ".set":
            if len(node.argumentExpression.exprs) != 2:
                raise ParseError(
                    f"Builtin function 'set' requires 2 arguments.", node.coord)
            real_val_type = self.typecheck(
                node.argumentExpression.exprs[1], st)
            if not self.eq_type(val_type, real_val_type):
                raise ParseError(f"Expected Value Type: {val_type}, but recieved Type {real_val_type} for dict {node.dictID}",
                                 node.coord,
                                 )
            return ast.Type("NullType")
