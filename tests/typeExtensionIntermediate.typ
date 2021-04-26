x : dict<int, int> = {}

x.set(123, 456)
x.set(789, 101112)
x.get(123)
x.get(789)

z : dict<str, [bool]> = {}
z.set("AmIDumb", [True])
z.set("AmISmart", [False])

trousers : [bool] = z.get("AmIDumb")
pantaloons : [bool] = z.get("AmISmart")

def isThatKeyZero(x : dict<int,int>, y : int) -> bool : {
    if (x.get(y) == 0) : {
        return True
    }else : {
        return False
    }
}

liam : bool = isThatKeyZero(x, 123)