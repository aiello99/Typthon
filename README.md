# Typthon
Statically typed minimal Python compiler using PLY. Inspired by TypeScript, this project aims to statically type 
Python by adding a robust typechecker and adapt existing python types to obey typical type-checking rules.

# Statements
If, else, elif, and while statements are supported. Some examples of their syntax are provided below.

```py
x : int = 1

if (x > 0): {
    return 1
} elif (x < 0): {
    return -1
} else: {
    return 0
}


while(y) : {
    x += 1
}
```
# Types
Current supported types are integer, boolean, strings, dictionaries, and lists. 

```py
integerVariable : int = 5
stringVariable : str = "abc"
booleanVariable : bool = True

integerList : [int] = [ 1, 2, 3 ]
nestedList : [[int]] = [ integerArray ]
nestedList = [[1,2,3], [4,5,6]]
anotherList : [str] = ["a", "b", "c"]

x : dict<int, int> = {} # Specifies that key value pairs in this dictionary must be integer to integer.
y : dict<str, bool> = {} # Specifies that key value pairs in this dictionary must be string to a boolean.
z : dict<str, [str]> = {} # Specifies that key value pairs in this dictionary must be string to a list of strings.
```

# Functions
Functions have also been typed. An example function may look like:

```py

def foo(x : dict<int, int>, y : str, z : [str]) -> int : {
  #code here
}
```
The type of each parameter must be specified, with standard type-checking rules applying if there's a 
type mismatch.

# How to run the Compiler
The compiler can be run by simply executing `typthonCompiler.py` on a `.typ` file that uses the syntax
laid out above. Some possible flag options are:

`-t` for typechecking only.
`-i` to see the IR only.
`-o` to enable optimizations.

An example command may look like:
`./typthonCompiler.py -o test.typ`

# Authors
Liam Aiello, Shahmeer Shahid, Erik Holmes
