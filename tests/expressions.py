x = 1
y = -x
y = 2
z = x + y
z = x - y
z = x * y
z = x / y
x = x + y
z = z - x
y = y * x
z = z / x
precedenceTest = x + y - z / x * y
bools = True and False
bools = bools or False
bools = bools == False
bools = bools != True
bools = x < y
bools = x > y
bools = x <= y
bools = x >= y
bools = bools
bools = bools or True and x < y
arr = [1,2,3,4]
x = arr[0]
slice = arr[0:2]
slice.append(1)
slice.remove(1 + 1)
z = slice.pop(0)
def foo(bar):
    def abc(r):
        if 1 == 1 :
            return 0
        return 1
    return 0
x = foo("random string")
