#!/usr/bin/env python3

import argparse
from typthonParser import typthonParser
from typthonSymbolTable import SymbolTable
from typthonTypeChecker import TypeChecker
from typthonIRGen import IRGen
from typthonTargetGen import TargetGen
from typthonOptimizer import Optimizer

import typthonAST as ast


if __name__ == "__main__":

    # Python module "argparse" allows you to easily add commandline flags
    # to your program, which can help with adding debugging options, such
    # as '--verbose' and '--print-ast' as described below.
    #
    # Of course, this is entirely optional and not necessary, as long as
    # the compiler functions correctly.
    argparser = argparse.ArgumentParser(
        description="Take in the Typthon source code and compile it"
    )
    argparser.add_argument("FILE", help="Input file")
    argparser.add_argument(
        "-p",
        "--parse-only",
        action="store_true",
        help="Stop after scanning and parsing the input",
    )
    argparser.add_argument(
        "-t", "--typecheck-only", action="store_true", help="Stop after typechecking"
    )
    argparser.add_argument(
        "-i", "--ir-only", action="store_true", help="Stop Aftering creating the IR"
    )
    argparser.add_argument(
        "-v", "--verbose", action="store_true", help="Provides additional output"
    )
    argparser.add_argument(
        "-o", "--optimize", action="store_true", help="Enables IR optimization"
    )

    args = argparser.parse_args()

    # Prints additional output if the flag is set
    if args.verbose:
        print("* Reading file " + args.FILE + "...")

    f = open(args.FILE, "r")
    data = f.read()
    f.close()

    if args.verbose:
        print("* Scanning and Parsing...")

    # Build and runs the parser to get AST
    parser = typthonParser()
    if args.parse_only:
        parser.test(data)
        quit()
    root = parser.parse(data)

    # If user asks to quit after parsing, do so.

    if args.verbose:
        print("* Typechecking...")

    typechecker = TypeChecker()
    typechecker.typecheck(root)

    if args.typecheck_only:
        quit()

    if args.verbose:
        print("* Generating IR...")

    ir_generator = IRGen()
    ir_generator.generate(root)
    ir_root = ir_generator.get_IR_list()
    ir_functions = ir_generator.get_function_IR_list()

    if args.ir_only:
        ir_generator.print_ir()
        quit()

    if args.optimize:
        optimizer = Optimizer(root)
        optimizer.optimize()
        root = optimizer.get_optimized_ir()

    target_generator = TargetGen(args.FILE, root, ir_functions)
    target_generator.create_target()
