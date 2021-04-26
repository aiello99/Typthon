x : int = 1
y : int = -x
y = 2

z : int = x + y
z = x - y
z = x * y
z = x / y

x += y
z -= x
y *= x
z /= x


precedenceTest : int = (x + y) - z / x * y

bools : bool = True and False
bools = bools or False
bools = bools == False
bools = bools != True
bools = x < y
bools = x > y
bools = x <= y
bools = x >= y
bools = (bools)
bools = (bools or True) and (x < y)

arr : [int] = [1,2,3,4]
x = arr[0]
slice : [int] = arr[0:2]
slice.append(1)
slice.remove(1+1)
z = slice.pop(0)

def foo(bar: str) -> int: {
    def abc(r: str) -> int: {
        if (1==1):{
            return 0
        }
        return 1
    }
    return 0
}
x = foo("random string")
