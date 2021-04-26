def funkyFunction(x: int, y: int) -> int: {
    return x + y
}

def funkyFunction2(z: int) -> int: {
    if (z % 2 == 0) : {
        return z + 1
    }else : {
        return z
    }
}

x : int = 5
y : int = funkyFunction2(x)
z : int = x + y