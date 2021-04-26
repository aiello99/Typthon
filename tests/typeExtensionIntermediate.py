x = {}
x[123] = 456
x[789] = 101112
x[123]
x[789]
z = {}
z["AmIDumb"] = [True]
z["AmISmart"] = [False]
trousers = z["AmIDumb"]
pantaloons = z["AmISmart"]
def isThatKeyZero(x,y):
    if x[y] == 0 :
        return True
    else:
        return False
liam = isThatKeyZero(x,123)
