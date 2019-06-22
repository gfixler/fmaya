mapWhile = lambda p: lambda f: lambda (rs, xs): (lambda r: (mapWhile(p)(f)((rs + [(r], xs[1:])) if p(r) else (rs, xs)))(f(xs[0])) if xs else (rs, xs)

# mapWhile(lambda x: x < 10)(lambda y: y * y)(([], [1,2,3,4,5]))

