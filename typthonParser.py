#!/usr/bin/env python3

import argparse
from ply import yacc
import typthonLexer as lexer
import typthonAST as ast


class typthonParser:

    precedence = (
        ("left", "WITHOUT_NEWLINE"),
        ("left", "NEWLINE"),
        ("left", "EQ"),
        ("left", "AND", "OR"),
        ("left", "EQOP", "NEQ"),
        ("left", "LESS", "LESSEQ", "GREATER", "GREATEREQ"),
        ("left", "PLUS", "MINUS"),
        ("left", "TIMES", "DIVIDE", "MOD"),
        ("right", "UNARY"),
    )

    def __init__(self, **kwargs):
        """
        Builds the Lexer and Parser
        """
        self.tokens = lexer.tokens
        self.lexer = lexer.typthonLexer()
        self.lexer.build()
        self.parser = yacc.yacc(module=self, **kwargs)

    # =======================#
    #       # Misc #        #
    # =======================#
    def p_empty(self, p):
        "empty :"
        pass

    def p_error(self, p):
        raise SyntaxError(f"Syntax error at token {p}")

    def parse(self, data):
        self.build()
        return self.parser.parse(data)

    def build(self, **kwargs):
        self.tokens = lexer.tokens
        self.lexer = lexer.typthonLexer()
        self.lexer.build()
        self.parser = yacc.yacc(module=self, **kwargs)

    def test(self, data):
        result = self.parser.parse(data)
        visitor = ast.NodeVisitor()
        visitor.visit(result)

    start = "file"

    # =======================#
    # File (starting point) #
    # =======================#

    def p_file(self, p):
        """
        file : statements
        """
        p[0] = ast.File(p[1])

    # =======================#
    # Statements            #
    # =======================#
    def p_statements(self, p):
        """
        statements : statements_list
        """
        p[0] = ast.StmtList(p[1], p.lineno(1))

    def p_statements_list(self, p):
        """
        statements_list : statements_list statement
                        | statement
                        | NEWLINE statement
        """
        if p[1] == "\n":
            p[0] = [p[2]]
        elif len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_statement(self, p):
        """
        statement : statement NEWLINE
                  | var_modify
                  | var_assign
                  | var_decl
                  | function_call
                  | array_builtin_call
                  | if_statement
                  | ret_statement
                  | break_statement
                  | while_statement
                  | function_defn
                  | dict_builtin_call
        """
        if p[1] == "\n":
            p[0] = p[2]
        else:
            p[0] = p[1]

    def p_block(self, p):
        """
        block : LBRACE statements RBRACE %prec WITHOUT_NEWLINE
              | LBRACE statements RBRACE NEWLINE
        """
        p[0] = p[2]

    def p_if_statement(self, p):
        """
        if_statement : IF expression COLON block
                     | IF expression COLON block elif_statement
        """
        if len(p) == 5:
            p[0] = ast.IfStmt(p[2], p[4], None, p.lineno(1))
        else:
            p[0] = ast.IfStmt(p[2], p[4], p[5], p.lineno(1))

    def p_if_statement_else(self, p):
        """
        if_statement : IF expression COLON block else_statement
        """
        p[0] = ast.IfStmt(p[2], p[4], p[5])

    def p_elif_statement(self, p):
        """
        elif_statement : ELIF expression COLON block
                     | ELIF expression COLON block elif_statement
        """
        if len(p) == 5:
            p[0] = ast.ElifStmt(p[2], p[4], None, p.lineno(1))
        else:
            p[0] = ast.ElifStmt(p[2], p[4], p[5], p.lineno(1))

    def p_elif_statement_else(self, p):
        """
        elif_statement : ELIF expression COLON block else_statement
        """
        p[0] = ast.ElifStmt(p[2], p[4], p[5], p.lineno(1))

    def p_else_statement(self, p):
        """
        else_statement : ELSE COLON block
        """
        p[0] = p[3]

    def p_while_statement(self, p):
        """
        while_statement : WHILE expression COLON block
        """
        p[0] = ast.WhileStmt(p[2], p[4], p.lineno(1))

    def p_break_statement_or_empty(self, p):
        """
        break_statement : BREAK
        """
        p[0] = ast.BreakStmt(p.lineno(1))

    def p_return_statement(self, p):
        """
        ret_statement : RETURN expression
        """
        p[0] = ast.RetStmt(p[2], p.lineno(1))

    def p_function_defn(self, p):
        # Enforces that functions must have a return statement in their block. Can ease this requirement.
        """
        function_defn : DEFINITION ID parameters RARROW type COLON block
        """
        p[0] = ast.FunctionDefn(p[2], p[5], p[3], p[7], p.lineno(2))

    # =======================#
    # Arguments and Params  #
    # =======================#

    def p_parameters(self, p):
        """
        parameters : LPAREN parameters_or_empty RPAREN
        """
        p[0] = ast.ParamList(p[2], p.lineno(2))

    def p_parameters_or_empty(self, p):
        """
        parameters_or_empty : param_lst
                            | empty
        """
        if len(p) == 1:
            p[0] = []
        else:
            p[0] = p[1]

    def p_param_lst(self, p):
        """
        param_lst : param_lst COMMA param
                  | param
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_param(self, p):
        """
        param : ID COLON type
        """
        p[0] = ast.Param(p[1], p[3], p.lineno(1))

    def p_arguments(self, p):
        """
        arguments : LPAREN exprs_or_empty RPAREN
        """
        p[0] = ast.Arguments(p[2], p.lineno(2))

    # =======================#
    #     Variables          #
    # =======================#
    def p_var_decl(self, p):
        """
        var_decl : ID COLON type EQ expression
        """ 
        p[0] = ast.VarDecl(p[1], p[3], p[5], p.lineno(1))

    # def p_dict_declaration(self, p):
    #     """
    #     dict_declaration : ID COLON DICT EQ LBRACE RBRACE
    #     """
    #     p[0] = ast.DictDecl()

    def p_var_assign(self, p):
        """
        var_assign : ID EQ expression
        """
        p[0] = ast.VarAssign(p[1], p[3], p.lineno(1))

    def p_var_modify(self, p):
        """
        var_modify : ID PLUSEQ expression
                   | ID MINUSEQ expression
                   | ID TIMESEQ expression
                   | ID DIVIDEEQ expression
                   | ID MODEQ expression
        """
        if p[2] == "+=":
            p[0] = ast.VarAssign(
                p[1], ast.BinOp("+", ast.ID(p[1], p.lineno(1)), p[3]), p.lineno(1)
            )
        elif p[2] == "-=":
            p[0] = ast.VarAssign(
                p[1], ast.BinOp("-", ast.ID(p[1], p.lineno(1)), p[3]), p.lineno(1)
            )
        elif p[2] == "*=":
            p[0] = ast.VarAssign(
                p[1], ast.BinOp("*", ast.ID(p[1], p.lineno(1)), p[3]), p.lineno(1)
            )
        elif p[2] == "/=":
            p[0] = ast.VarAssign(
                p[1], ast.BinOp("/", ast.ID(p[1], p.lineno(1)), p[3]), p.lineno(1)
            )
        elif p[2] == "%=":
            p[0] = ast.VarAssign(
                p[1], ast.BinOp("%", ast.ID(p[1], p.lineno(1)), p[3]), p.lineno(1)
            )

    # =======================#
    #     Expression        #
    # =======================#

    def p_expression(self, p):
        """
        expression : literal
                   | binops_expr
                   | unary_op_expr
                   | brackets_expr
                   | function_call
                   | array_builtin_call
                   | dict_builtin_call
                   | array_slice
                   | array_exprs
                   | array_index
                   | empty_dict
        """
        p[0] = p[1]

    def p_function_call(self, p):
        """
        function_call : ID arguments
        """
        p[0] = ast.FunctionCall(p[1], p[2], p.lineno(1))

    def p_expr_id(self, p):
        """
        expression : ID
        """
        p[0] = ast.ID(p[1], p.lineno(1))

    def p_array_exprs(self, p):
        """
        array_exprs : LBRACK exprs_or_empty RBRACK
        """
        p[0] = ast.ArrayExprList(p[2], p.lineno(2))

    def p_exprs_or_empty(self, p):
        """
        exprs_or_empty : expr_lst
                       | empty
        """
        if len(p) == 1:
            p[0] = []
        else:
            p[0] = p[1]

    def p_expr_lst(self, p):
        """
        expr_lst : expr_lst COMMA expression
                 | expression
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_binops_expr(self, p):
        """
        binops_expr : expression PLUS expression
                   | expression MINUS expression
                   | expression TIMES expression
                   | expression DIVIDE expression
                   | expression AND expression
                   | expression OR expression
                   | expression EQOP expression
                   | expression NEQ expression
                   | expression MOD expression
                   | expression LESS expression
                   | expression GREATER expression
                   | expression LESSEQ expression
                   | expression GREATEREQ expression
        """
        p[0] = ast.BinOp(p[2], p[1], p[3], p.lineno(2))

    def p_unary_op_expr(self, p):
        """
        unary_op_expr : MINUS expression %prec UNARY
                      | NOT expression %prec UNARY

        """
        p[0] = ast.UnaryOp(p[1], p[2], p.lineno(1))

    def p_brackets_expr(self, p):
        """
        brackets_expr : LPAREN expression RPAREN
        """
        p[0] = p[2]

    # =======================#
    #     Array Operations   #
    # =======================#

    def p_array_builtin_call(self, p):
        """
        array_builtin_call : ID ARRAPPEND brackets_expr
                           | ID ARRREMOVE brackets_expr
                           | ID ARRPOP brackets_expr
        """
        p[0] = ast.ArrayBuiltinCall(p[1], p[2], p[3], p.lineno(1))

    def p_array_slice(self, p):
        """
        array_slice : ID LBRACK expression COLON expression RBRACK
        """

        p[0] = ast.ArraySlice(p[1], p[3], p[5], p.lineno(5))

    def p_array_index(self, p):
        """
        array_index : ID LBRACK expression RBRACK
        """

        p[0] = ast.ArrayIndex(p[1], p[3], p.lineno(3))


    # =======================#
    #     Dict  Operations   #
    # =======================#

    def p_dict_builtin_call(self, p):
        """
        dict_builtin_call : dict_builtin_get
                           | dict_builtin_set
        """
        p[0] =  p[1]


    def p_dict_builtin_get(self, p):
        """
        dict_builtin_get : ID DICTGET LPAREN expression RPAREN
        """
        p[0] = ast.DictBuiltinCall(p[1], p[2], ast.Arguments([p[4]], p.lineno(1)), p.lineno(1))

    def p_dict_builtin_set(self, p):
        """
        dict_builtin_set : ID DICTSET LPAREN expression COMMA expression RPAREN
        """
        p[0] = ast.DictBuiltinCall(p[1], p[2], ast.Arguments([p[4], p[6]], p.lineno(1)), p.lineno(1))


    def p_empty_dict(self, p):
        """
        empty_dict : EMPTYDICT
        """
        p[0] = ast.Constant(ast.Dict_Type(ast.Type("NullType"), ast.Type("NullType")), p[1], p.lineno(1))
        # p[0] = ast.Dict(p.lineno(1))
    # =======================#
    #     Literals           #
    # =======================#

    def p_literal_number(self, p):
        """
        literal : NUMBER
        """
        p[0] = ast.Constant(ast.Type("int"), p[1], p.lineno(1))

    def p_literal_string(self, p):
        """
        literal : STRINGLITERAL
        """
        p[0] = ast.Constant(ast.Type("str"), p[1], p.lineno(1))

    def p_literal_boolean(self, p):
        """
        literal : TRUE
                | FALSE
        """
        p[0] = ast.Constant(ast.Type("bool"), p[1], p.lineno(1))

    # =======================#
    #         Types          #
    # =======================#
    # =======================#
    # =======================#
    # =======================#
    # =======================#
    # =======================#

    def p_type(self, p):
        """
        type : primitive_type
             | array_type
             | dict_type
        """
        p[0] = p[1]

    def p_array_type(self, p):
        """
        array_type : LBRACK array_type RBRACK
        """
        p[0] = ast.Array_Type(p[2], p.lineno(2))

    def p_array_type_primitive(self, p):
        """
        array_type : LBRACK primitive_type RBRACK
        """
        p[0] = ast.Array_Type(p[2], p.lineno(2))

    def p_array_type_dict(self, p):
        """
        array_type : LBRACK dict_type RBRACK
        """
        p[0] = ast.Array_Type(p[2], p.lineno(2))

    def p_dict_type(self, p):
        """
        dict_type : DICT LESS type COMMA type GREATER
        """
        p[0] = ast.Dict_Type(p[3], p[5], p.lineno(2))

    def p_primitive_type(self, p):
        """
        primitive_type : INT
                        | STRING
                        | BOOLEAN
                        | NULLTYPE
        """
        p[0] = ast.Type(p[1], p.lineno(1))



if __name__ == "__main__":

    argparser = argparse.ArgumentParser(
        description="Take in the miniJava source code and parses it"
    )
    argparser.add_argument("FILE", help="Input file with miniJava source code")
    args = argparser.parse_args()

    f = open(args.FILE, "r")
    data = f.read()
    f.close()

    m = typthonParser()
    m.build()
    m.test(data)