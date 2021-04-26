#!/usr/bin/env python3

import argparse
from ply import lex

# List of token names.
tokens = [
    "NUMBER",
    "ID",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "LESS",
    "LESSEQ",
    "GREATER",
    "GREATEREQ",
    "MOD",
    "EQOP",
    "NEQ",
    "COMMA",
    "EQ",
    "LPAREN",  # (
    "RPAREN",  # )
    "LBRACK",
    "RBRACK",
    "LBRACE",
    "RBRACE",
    "COLON",
    "RARROW",
    "NEWLINE",
    "PLUSEQ",
    "MINUSEQ",
    "TIMESEQ",
    "DIVIDEEQ",
    "MODEQ",
    "STRINGLITERAL",
    "ARRAPPEND",
    "ARRREMOVE",
    "ARRPOP",
    "DICTGET",
    "DICTSET",
    "EMPTYDICT"
]

# Reserved words which should not match any IDs
reserved = {
    "int": "INT",
    "str": "STRING",
    "bool": "BOOLEAN",
    "NullType": "NULLTYPE",
    "True": "TRUE",
    "False": "FALSE",
    "if": "IF",
    "else": "ELSE",
    "elif": "ELIF",
    "while": "WHILE",
    "return": "RETURN",
    "break": "BREAK",
    "def": "DEFINITION",
    "not": "NOT",
    "or": "OR",
    "and": "AND",
    "dict": "DICT"
}

# Add reserved names to list of tokens
tokens += list(reserved.values())


class typthonLexer:

    # A string containing ignored characters (spaces and tabs)
    t_ignore = " \t"

    # Regular expression rule with some action code
    t_PLUS = r"\+"
    t_MINUS = r"-"
    t_TIMES = r"\*"
    t_DIVIDE = r"/"
    t_PLUSEQ = r"\+="
    t_MINUSEQ = r"\-="
    t_TIMESEQ = r"\*="
    t_DIVIDEEQ = r"\/="
    t_LESS = r"\<"
    t_LESSEQ = r"\<="
    t_GREATER = r"\>"
    t_GREATEREQ = r"\>="
    t_EQOP = r"\=="
    t_NEQ = r"\!="
    t_COMMA = r","
    t_EQ = r"\="
    t_LPAREN = r"\("
    t_RPAREN = r"\)"
    t_LBRACE = r"\{"
    t_RBRACE = r"\}"
    t_LBRACK = r"\["
    t_RBRACK = r"\]"
    t_COLON = r"\:"
    t_RARROW = r"\->"
    t_MOD = r"\%"
    t_MODEQ = r"\%="

    # A regular expression rule with some action code
    def t_NUMBER(self, t):
        r"\d+"
        t.value = int(t.value)
        return t

    def t_ID(self, t):
        r"[a-zA-Z_][a-zA-Z_0-9]*"
        t.type = reserved.get(t.value, "ID")  # Check for reserved words
        return t

    def t_NEWLINE(self, t):
        r"\n+"
        # Helps with tracking line numbers for debugging.
        t.lexer.lineno += len(t.value)
        return t

    def t_STRINGLITERAL(self, t):
        r'"(.*?)"'

        t.value = str(t.value)
        return t

    def t_ARRAPPEND(self, t):
        r".append"
        return t

    def t_ARRREMOVE(self, t):
        r".remove"
        return t

    def t_ARRPOP(self, t):
        r".pop"
        return t

    def t_DICTGET(self, t):
        r".get"
        return t

    def t_DICTSET(self, t):
        r".set"
        return t

    def t_EMPTYDICT(self, t):
        r"{}"
        return t

    # Error handling rule. DO NOT MODIFY
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer. DO NOT MODIFY
    def build(self, **kwargs):
        self.tokens = tokens
        self.lexer = lex.lex(module=self, **kwargs)

    # Test the output. DO NOT MODIFY
    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)


# Main function. DO NOT MODIFY
if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Take in the miniJava source code and perform lexical analysis."
    )
    parser.add_argument("FILE", help="Input file with miniJava source code")
    args = parser.parse_args()

    f = open(args.FILE, "r")
    data = f.read()
    f.close()

    m = typthonLexer()
    m.build()
    m.test(data)
