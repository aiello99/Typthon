import typthonAST as ast
import typthonIRGen as IR

TAB_LENGTH = 4


class TargetGen(object):
    """
    Translates the given IR into Python.
    """

    def __init__(self, name, IR_lst, function_IR_lst):

        self.name = name[:-4]
        self.IR_lst = IR_lst
        self.function_IR_lst = function_IR_lst
        self.i_current = 1
        self.next_i_current = None
        self.target_lst = []
        self.scope = 0
        self.in_function = False

        self.function_counts = {}

    def create_target(self):
        # for funkyfunctionKEY in self.function_IR_lst:
        #     self.translate(self.function_IR_lst[funkyfunctionKEY])

        self.translate(self.IR_lst)
        self.write_lines()

    def write_lines(self):

        with open(f"{self.name}.py", "w") as f:
            for line in self.target_lst:
                f.write(f"{line}\n")

    def translate(self, node, statement=False):
        method = "translate_" + node.__class__.__name__
        return getattr(self, method)(node, statement)

    def add_line(self, line):
        self.target_lst.append(" " * TAB_LENGTH * self.scope + line)

    def translate_FunctionDefn(self, node, statement=False):
        params = self.translate(node.params)
        self.add_line(f"def {node.name}{params}:")
        self.scope += 1
        self.in_function = True
        # for statement in node.statements:
        # self.translate(statement, True)
        self.translate(node.body)
        self.scope -= 1
        self.in_function = False

    def translate_ParamList(self, node, statement=False):
        params = []
        if not node.params:
            node.params = []
        for param in node.params:
            translation = self.translate(param)
            params.append(translation)

        return f"({','.join(params)})"

    def translate_Param(self, node, statement=False):
        return f"{node.name}"

    def translate_StmtList(self, node, statement=False):
        for stmt in node.stmt_lst:
            self.translate(stmt, statement=True)

    def translate_RetStmt(self, node, statement=False):
        expression = self.translate(node.expr)
        self.add_line(f"return {expression}")

    def translate_Constant(self, node, statement=False):
        return f"{node.value}"

    def translate_File(self, node, statement=False):
        self.translate(node.statements)

    def translate_VarDecl(self, node, statement=False):
        expression = self.translate(node.expr)
        self.add_line(f"{node.name} = {expression}")

    def translate_UnaryOp(self, node, statement=False):
        expression = self.translate(node.expr)
        return f"{node.op}{expression}"

    def translate_ID(self, node, statement=False):
        return f"{node.name}"

    def translate_VarAssign(self, node, statement=False):
        expression = self.translate(node.expr)
        self.add_line(f"{node.name} = {expression}")

    def translate_BinOp(self, node, statement=False):
        left_expresion = self.translate(node.left)
        right_expresion = self.translate(node.right)
        return f"{left_expresion} {node.op} {right_expresion}"

    def translate_ArrayExprList(self, node, statement=False):
        exprs = []
        for expr in node.exprs:
            translation = self.translate(expr)
            exprs.append(translation)

        return f"[{','.join(exprs)}]"

    def translate_ArrayIndex(self, node, statement=False):
        expression = self.translate(node.expr)
        return f"{node.name}[{expression}]"

    def translate_ArraySlice(self, node, statement=False):
        return f"{node.name}[{self.translate(node.expr1)}:{self.translate(node.expr2)}]"

    def translate_ArrayBuiltinCall(self, node, statement=False):
        expression = self.translate(node.argumentExpression)
        if(statement):
            self.add_line(
                f"{node.arrayID}{node.builtinFunction}({expression})")
        return f"{node.arrayID}{node.builtinFunction}({expression})"

    def translate_FunctionCall(self, node, statement=False):
        args = self.translate(node.arguments)
        if(statement):
            self.add_line(f"{node.name}({args})")
        return f"{node.name}({args})"

    def translate_Arguments(self, node, statement=False):
        exprs = []
        for expr in node.exprs:
            translation = self.translate(expr)
            exprs.append(translation)

        return f"{','.join(exprs)}"

    def translate_IfStmt(self, node, statement=False):
        condition = self.translate(node.cond)
        self.add_line(f"if {condition} :")
        self.scope += 1
        self.translate(node.true_body)
        self.scope -= 1
        if (node.false_body):
            self.add_line("else:")
            self.scope += 1
            self.translate(node.false_body)
            self.scope -= 1

    def translate_ElifStmt(self, node, statement=False):
        condition = self.translate(node.cond)
        self.add_line(f"if {condition} :")
        self.scope += 1
        self.translate(node.true_body)
        self.scope -= 1
        if (node.false_body):
            self.add_line("else:")
            self.scope += 1
            self.translate(node.false_body)
            self.scope -= 1

    def translate_WhileStmt(self, node, statement=False):
        cond = self.translate(node.cond)
        self.add_line(f"while {cond}:")

        self.scope += 1
        self.translate(node.body)
        self.scope -= 1

    def translate_BreakStmt(self, node, statement=False):
        self.add_line("break")

    def translate_DictBuiltinCall(self, node, statement=False):
        output = ""
        if node.builtinFunction == ".set":
            output = f"{node.dictID}[{self.translate(node.argumentExpression.exprs[0])}] = {self.translate(node.argumentExpression.exprs[1])}"
        else:
            output = f"{node.dictID}[{self.translate(node.argumentExpression.exprs[0])}]"
        if(statement):
            self.add_line(output)
        return output
