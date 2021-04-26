import typthonAST as ast

class ControlFlowBlock(ast.Node):
    def __init__(self, name, statements):
        self.name = name
        self.statements = statements

    def add_statement(self, statement):
        self.statements.append(statement)

    def __str__(self):
        output = f"{self.name}:"
        for statement in self.statements:
            output += f"\n    {statement}"
        return output
    
    def children(self):
        nodelist = []
        for i, stmt in enumerate(self.statements or []):
            nodelist.append(("stmt[%d]" % i, stmt))
        return nodelist
    attr_names = ("name",)

class FunctionBlock(ast.Node):
    def __init__(self, name, param, statements):
        self.name = name
        self.param = param
        self.statements = statements

    def add_statement(self, statement):
        self.statements.append(statement)

    def __str__(self):
        output = f"{self.name}:\n    BeginFunc"
        for statement in self.statements:
            output += f"\n    {statement}"
        return output + "\n    EndFunc"

    def children(self):
        nodelist = []
        for i, stmt in enumerate(self.statements or []):
            nodelist.append(("stmt[%d]" % i, stmt))
        return nodelist
    attr_names = ("name",)

class ElseNode(ast.Node):
    def __init__(self):
        pass
    def __str__(self):
        return ""
    def children(self):
        nodelist = []
        return nodelist
    attr_names = ()

class GOTONode(ast.Node):
    def __init__(self, goto):
        self.goto = goto
    
    def children(self):
        nodelist = []
        return nodelist

    def __str__(self):
        return f"GOTO _L{self.goto}"
    attr_names = ("goto",)

class IfNode(ast.Node):
    def __init__(self, cond, gotoTrue, gotoFalse):
        self.cond = cond
        self.gotoTrue = gotoTrue
        self.gotoFalse = gotoFalse
        
    def children(self):
        nodelist = []
        nodelist.append(("cond", self.cond))
        nodelist.append(("gotoTrue", self.gotoTrue))
        nodelist.append(("gotoFalse", self.gotoFalse))
        
    def __str__(self):
        return f"IF NOT {self.cond} GOTO _L{self.gotoFalse}"
    
    attr_names = ("name",)

class ElifNode(ast.Node):
    def __init__(self, cond, gotoTrue, gotoFalse):
        self.cond = cond
        self.gotoTrue = gotoTrue
        self.gotoFalse = gotoFalse
        
    def children(self):
        nodelist = []
        nodelist.append(("cond", self.cond))
        nodelist.append(("gotoTrue", self.gotoTrue))
        nodelist.append(("gotoFalse", self.gotoFalse))
        return nodelist

    def __str__(self):
        return f"IF NOT {self.cond} GOTO _L{self.gotoFalse}"

    attr_names = ("name",)
    
class WhileNode(ast.Node):
    def __init__(self, cond, name, gotoFalse):
        self.cond = cond
        self.name = name
        self.gotoFalse = gotoFalse
        self.statements = []

    def add_statement(self, statement):
        self.statements.append(statement)
        
    def children(self):
        nodelist = []
        nodelist.append(("cond", self.cond))
        nodelist.append(("name", self.gotoTrue))
        nodelist.append(("gotoFalse", self.gotoFalse))
        return nodelist

    def __str__(self):
        output = f"_L{self.name}:\n"
        output += f"    IF NOT {self.cond} GOTO _L{self.gotoFalse}"
        for statement in self.statements:
            output += f"\n    {statement}"
        return output + f"\n    GOTO _L{self.name}"


class IRGen(object):

    def __init__(self):
        """
        IR_lst: list of IR code
        register_count: integer to keep track of which register to use
        label_count: similar to register_count, but with labels
        """
        self.cblock = None
        self.IR_lst = {}
        self.function_IR_lst = {}
        self.label_count = 0

    def generate(self, node: ast.Node):
        """
        Similar to 'typecheck' method from TypeChecker object
        """
        method = "gen_" + node.__class__.__name__
        return getattr(self, method, self.generic_gen)(node)

    def generic_gen(self, node):
        pass
    ################################
    ## Helper functions
    ################################

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
    def get_function_IR_list(self):
        return self.function_IR_lst
    def print_ir(self):
        """
        Loop through the generated IR code and print them out to stdout
        """
        for ir in self.IR_lst:
            print(self.IR_lst[ir])

    def mark_label(self, label):
        """
        Add label mark to IR_lst
        """
        cblock =ControlFlowBlock(f"_L{label}", [])
        self.cblock = cblock
        self.IR_lst[label] = cblock
    
    def mark_label_while(self, cond, name, fbranch_label):
        self.cblock = WhileNode(cond, name, fbranch_label)
        self.IR_lst[name] = self.cblock

    def mark_label_function(self, node):
        """
        Add label mark to IR_lst
        """
        cblock =FunctionBlock(f"{node.name}",node.params, [])
        self.cblock = cblock
        self.IR_lst[node.name]= cblock
        self.function_IR_lst[node.name]= cblock

    def gen_File(self, node: ast.File):
        branch_label = self.inc_label()
        self.mark_label(branch_label)
        self.generate(node.statements)
    
    def gen_VarDecl(self, node: ast.VarDecl):
        self.add_code(node)

    def gen_BreakStmt(self, node: ast.BreakStmt):
        self.add_code(node)

    def gen_FunctionDefn(self, node: ast.FunctionDefn):
        skip_decl = self.inc_label()
        self.add_code(GOTONode(skip_decl))
        self.mark_label_function(node)
        self.generate(node.body)
        self.mark_label(skip_decl)

    def gen_DictBuiltinCall(self, node: ast.DictBuiltinCall):
        self.add_code(node)

    def gen_ArrayBuiltinCall(self, node: ast.ArrayBuiltinCall):
        self.add_code(node)
    
    def gen_VarAssign(self, node: ast.VarAssign):
        self.add_code(node)

    def gen_StmtList(self, node: ast.StmtList):
        if node:
            for (child_name, child) in node.children():
                self.generate(child)

    def gen_FunctionCall(self, node: ast.FunctionCall):
        self.add_code(node)

    def gen_IfStmt(self, node: ast.IfStmt):
        fbranch_label = self.inc_label()
        tbranch_label = self.inc_label()

        # Skip to the false_body if the condition is not met
        self.add_code(IfNode(node.cond, tbranch_label, fbranch_label))
        self.generate(node.true_body)
        # Make sure the statements from false_body is skipped
        self.add_code(GOTONode(tbranch_label))

        self.mark_label(fbranch_label)
        if(node.false_body):
            if(type(node.false_body) != ast.ElifStmt):
                self.add_code(ElseNode())
            self.generate(node.false_body)
        self.mark_label(tbranch_label)

    def gen_ElifStmt(self, node: ast.ElifStmt):
        fbranch_label = self.inc_label()
        tbranch_label = self.inc_label()

        # Skip to the false_body if the condition is not met
        self.add_code(ElifNode(node.cond, tbranch_label, fbranch_label))
        self.generate(node.true_body)
        # Make sure the statements from false_body is skipped
        self.add_code(GOTONode(tbranch_label))

        self.mark_label(fbranch_label)
        if(node.false_body):
            if(type(node.false_body) != ast.ElifStmt):
                self.add_code(ElseNode())
            self.generate(node.false_body)
        self.mark_label(tbranch_label)
    
    def gen_RetStmt(self, node: ast.RetStmt):
        self.add_code(node)

    def gen_WhileStmt(self, node: ast.WhileStmt):
        branch_label = self.inc_label()
        fbranch_label = self.inc_label()

        # self.add_code(GOTONode(branch_label))

        # self.mark_label_while(node.cond, branch_label, fbranch_label)
        # self.generate(node.body)
        # # self.add_code(GOTONode(branch_label))
        # self.mark_label(fbranch_label)

        # skip_decl = self.inc_label()
        self.add_code(GOTONode(branch_label))
        self.mark_label_while(node.cond, branch_label, fbranch_label)
        self.generate(node.body)
        self.mark_label(fbranch_label)