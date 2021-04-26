def funkyFunction(x: int, y: int) -> int: {
    return x + y
}

def funkyFunction2(z: int) -> int: {
    y : int = funkyFunction(z, 1)
    return y
}

funk : int = funkyFunction2(15)