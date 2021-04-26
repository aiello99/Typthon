a : int = 1 % 1
b : int = a
a = 3
d : [int] = [1, 2, 3]
e : [int] = d[0:1]
d.append(1)
x : int = d.pop(1)
d.remove(2)

def funkyfunction(x : int, z: int) -> int : {
    y : int = x + 1
    return y
}

funkyfunction(1, 2)