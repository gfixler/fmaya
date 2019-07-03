ident = lambda x: x
cmap = lambda f: lambda xs: map(f, xs)
strict = list

ctrlState = lambda prop: lambda ctrl: cmds.control(ctrl, query=True, **{prop: True})

"""
filter(lambda x: cmds.button(x, query=True, enable=True), cmds.lsUI(type="button"))
any(strict(cmap(ctrlState("enable"))(["button321", "button322", "button323"])))
"""

attr = lambda a: lambda x: cmds.getAttr(x + "." + a)

pair = lambda f: lambda g: lambda x: (f(x), g(x))
three = lambda f: lambda g: lambda h: lambda x: (f(x), g(x), h(x))
ident = lambda x: x
comp2 = lambda f: lambda g: lambda x: f(g(x))
txyz = three(attr("tx"))(attr("ty"))(attr("tz"))

"""
strict(cmap(pair(ident)(txyz))(["persp","top","front","side"]))
"""

