#General tests showing the compiler compiling to the target language.
python ./typthonCompiler.py tests/expressions.typ > tests/out/expressionsTest.out
python ./typthonCompiler.py tests/statements.typ > tests/out/statementsTest.out
python ./typthonCompiler.py tests/declaration.typ > tests/out/declaration.out
python ./typthonCompiler.py tests/testIRGen2.typ > tests/out/testIRGen2.out
python ./typthonCompiler.py tests/testIRGen.typ > tests/out/testIRGen.out
python ./typthonCompiler.py tests/testIRGen.typ > tests/out/testIRGen.out

#These tests are to show the optimization working.
python ./typthonCompiler.py -o tests/optimizationTestBasic.typ > tests/out/optimizationTestBasic.out
python ./typthonCompiler.py -o tests/optimizationTestIntermediate.typ > tests/out/optimizationTestIntermediate.out
python ./typthonCompiler.py -o tests/optimizationTestAdvanced.typ > tests/out/optimizationTestAdvanced.out

#Note that because neither function is called, the compiler optimizes both functions out of the source.
python ./typthonCompiler.py -o tests/optimizationTestNest.typ > tests/out/optimizationTestNest.out

#These tests are to show the type extension working, and it failing type checking. Last 4 tests are meant to fail.
python ./typthonCompiler.py tests/typeExtensionBasic.typ > tests/out/typeExtensionBasic.out
python ./typthonCompiler.py tests/typeExtensionIntermediate.typ > tests/out/typeExtensionIntermediate.out
python ./typthonCompiler.py tests/typeExtensionAdvanced.typ > tests/out/typeExtensionAdvanced.out
python ./typthonCompiler.py tests/failTests/dictFailDeclType.typ &> tests/failTestsOut/dictFailDeclType.out
python ./typthonCompiler.py tests/failTests/dictFailGetMismatch.typ &> tests/failTestsOut/dictFailGetMismatch.out
python ./typthonCompiler.py tests/failTests/dictFailSetKeyValMismatch.typ &> tests/failTestsOut/dictFailSetKeyValMismatch.out
python ./typthonCompiler.py tests/failTests/dictFailSetValMismatch.typ &> tests/failTestsOut/dictFailSetValMismatch.out

#These tests are to show the ifElse extension working, Last two tests are meant to fail.
python ./typthonCompiler.py tests/ifElseExtensionBasic.typ > tests/out/ifElseExtensionBasic.out
python ./typthonCompiler.py tests/ifElseExtensionElif.typ > tests/out/ifElseExtensionElif.out
python ./typthonCompiler.py tests/failTests/ifElseExtensionNoReturn.typ &> tests/failTestsOut/ifElseExtensionNoReturn.out
python ./typthonCompiler.py tests/failTests/ifElseExtensionNoElifReturn.typ &> tests/failTestsOut/ifElseExtensionNoElifReturn.out

# #These tests are meant to fail, they are to show the typechecker working.

# These two tests deal with type mismatches of binary operations.
python ./typthonCompiler.py tests/failTests/binOpFail1.typ &> tests/failTestsOut/binOpFail1.out
python ./typthonCompiler.py tests/failTests/binOpFail2.typ &> tests/failTestsOut/binOpFail2.out

#These two tests deal with type mismatches of unary operations.
python ./typthonCompiler.py tests/failTests/unOpFail1.typ &> tests/failTestsOut/unOpFail1.out
python ./typthonCompiler.py tests/failTests/unOpFail2.typ &> tests/failTestsOut/unOpFail2.out

#Type mismatch of declared variable and variable assignment.
python ./typthonCompiler.py tests/failTests/varDeclFail.typ &> tests/failTestsOut/varDeclFail.out
python ./typthonCompiler.py tests/failTests/varAssFail.typ &> tests/failTestsOut/varAssFail.out

#Type mismatches related to arrays.
python ./typthonCompiler.py tests/failTests/arrayMultiFail.typ &> tests/failTestsOut/arrayMultiFail.out
python ./typthonCompiler.py tests/failTests/arrayIndexFail.typ &> tests/failTestsOut/arrayIndexFail.out
python ./typthonCompiler.py tests/failTests/arrayIndexFail2.typ &> tests/failTestsOut/arrayIndexFail2.out
python ./typthonCompiler.py tests/failTests/arraySliceFail.typ &> tests/failTestsOut/arraySliceFail.out
python ./typthonCompiler.py tests/failTests/arrayBuiltinFail.typ &> tests/failTestsOut/arrayBuiltinFail.out
python ./typthonCompiler.py tests/failTests/arrayBuiltinFail2.typ &> tests/failTestsOut/arrayBuiltinFail2.out

#Type mistmatches related to function calls and their definitions.
python ./typthonCompiler.py tests/failTests/functionCallFail.typ &> tests/failTestsOut/functionCallFail.out
python ./typthonCompiler.py tests/failTests/functionCallFail2.typ &> tests/failTestsOut/functionCallFail2.out
python ./typthonCompiler.py tests/failTests/functionParamFail.typ &> tests/failTestsOut/functionParamFail.out

#Type checks related to statements.
python ./typthonCompiler.py tests/failTests/ifStmtFail.typ &> tests/failTestsOut/ifStmtFail.out
python ./typthonCompiler.py tests/failTests/elifStmtFail.typ &> tests/failTestsOut/elifStmtFail.out
python ./typthonCompiler.py tests/failTests/whileFail.typ &> tests/failTestsOut/whileFail.out
python ./typthonCompiler.py tests/failTests/returnFail.typ &> tests/failTestsOut/returnFail.out
python ./typthonCompiler.py tests/failTests/breakFail.typ &> tests/failTestsOut/breakFail.out