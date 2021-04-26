x : dict<str, int> = {}

x.set("abc", 123)
y : int = x.get("abc")
z : int = y + 1

new_thing : [dict<str, int>] = [x,x,x]