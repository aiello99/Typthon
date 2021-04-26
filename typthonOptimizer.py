import typthonAST as ast


class Optimizer(object):

    def __init__(self, root: ast.Node):
        """
        IR_lst: list of IR code
        register_count: integer to keep track of which register to use
        label_count: similar to register_count, but with labels
        """
        self.root = root
        self.cblock = None
        self.IR_lst = []
        self.function_IR_dict = {}
        self.label_count = 0
        self.scope = 0

        self.called_functions = set()
        self.function_to_stmt_list = {}
        self.stmt_list_stack = []
        self.parse(root)

    def parse(self, node: ast.Node):
        """
        Similar to 'typecheck' method from TypeChecker object
        """
        method = "parse_" + node.__class__.__name__
        return getattr(self, method)(node)

    def generic_gen(self, node):
        pass

    def get_optimized_ir(self):
        return self.root
    ################################
    # Helper functions
    ################################

    def optimize(self):
        updated = False
        for function, (node, stmt_list) in self.function_to_stmt_list.items():
            if function not in self.called_functions:
                updated = True
                stmt_list.stmt_lst.remove(node)
        if updated:
            self.function_to_stmt_list = {}
            self.called_functions = set()
            self.stmt_list_stack = []
            self.parse(self.root)
            self.optimize()

    def inc_label(self):
        """
        Increase the label count and return its value for use
        """
        self.label_count += 1
        return self.label_count

    def add_code(self, code):
        self.cblock.add_statement(code)

    def get_IR_list(self):
        return self.IR_lst

    def get_function_IR_dict(self):
        return self.function_IR_dict

    def print_ir(self):
        """
        Loop through the generated IR code and print them out to stdout
        """
        print(self.IR_lst)
        # for ir in self.IR_lst:
        #     print(self.IR_lst[ir])

    def mark_label(self, label):
        """
        Add label mark to IR_lst
        """
        cblock = ControlFlowBlock(f"_L{label}", [])
        self.cblock = cblock
        self.IR_lst[label] = cblock

    def mark_label_while(self, cond, name, fbranch_label):
        self.cblock = WhileNode(cond, name, fbranch_label)
        self.IR_lst[name] = self.cblock

    def mark_label_function(self, node):
        """
        Add label mark to IR_lst
        """
        cblock = FunctionBlock(f"{node.name}", node.params, [])
        self.cblock = cblock
        self.IR_lst[node.name] = cblock
        self.function_IR_lst[node.name] = cblock

    def parse_File(self, node: ast.File):
        self.IR_lst.append(node)
        self.parse(node.statements)

##########################################################################

    def parse_FunctionDefn(self, node, statement=False):
        self.function_to_stmt_list[node.name] = (
            node, self.stmt_list_stack[-1])
        self.parse(node.params)
        self.parse(node.body)

    def parse_ParamList(self, node, statement=False):
        pass

    def parse_Param(self, node, statement=False):
        pass

    def parse_StmtList(self, node, statement=False):
        self.stmt_list_stack.append(node)
        for stmt in node.stmt_lst:
            self.parse(stmt)
        self.stmt_list_stack.pop()

    def parse_RetStmt(self, node, statement=False):
        self.parse(node.expr)

    def parse_Constant(self, node, statement=False):
        pass

    def parse_VarDecl(self, node, statement=False):
        self.parse(node.expr)

    def parse_UnaryOp(self, node, statement=False):
        self.parse(node.expr)

    def parse_ID(self, node, statement=False):
        pass

    def parse_VarAssign(self, node, statement=False):
        self.parse(node.expr)

    def parse_BinOp(self, node, statement=False):
        self.parse(node.left)
        self.parse(node.right)

    def parse_ArrayExprList(self, node, statement=False):
        for expr in node.exprs:
            self.parse(expr)

    def parse_ArrayIndex(self, node, statement=False):
        self.parse(node.expr)

    def parse_ArraySlice(self, node, statement=False):
        self.parse(node.expr1)
        self.parse(node.expr2)

    def parse_ArrayBuiltinCall(self, node, statement=False):
        self.parse(node.argumentExpression)

    def parse_FunctionCall(self, node, statement=False):
        self.called_functions.add(node.name)
        self.parse(node.arguments)

    def parse_Arguments(self, node, statement=False):
        for expr in node.exprs:
            self.parse(expr)

    def parse_IfStmt(self, node, statement=False):
        self.parse(node.cond)
        self.parse(node.true_body)
        if (node.false_body):
            self.parse(node.false_body)

    def parse_ElifStmt(self, node, statement=False):
        self.parse(node.cond)
        self.parse(node.true_body)
        if (node.false_body):
            self.parse(node.false_body)

    def parse_WhileStmt(self, node, statement=False):
        self.parse(node.cond)
        self.parse(node.body)

    def parse_BreakStmt(self, node, statement=False):
        pass

    def parse_DictBuiltinCall(self, node, statement=False):
        if node.builtinFunction == ".set":
            self.parse(node.argumentExpression.exprs[0])
            self.parse(node.argumentExpression.exprs[1])
        else:
            self.parse(node.argumentExpression.exprs[0])
