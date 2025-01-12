import sympy

x = sympy.symbols('x')
zeropoly = x - x
onepoly = zeropoly + 1


def lagrangepoly(yseq, xseq=None):
    """Build a Lagrange polynomial from a sequence of `y` values.
    If no sequence of `x`s is given, use x = 1, 2, ..."""
    if xseq is None:
        xseq = list(range(1, len(yseq) + 1))
    assert len(yseq) == len(xseq)

    result = zeropoly
    for j, (xj, yj) in enumerate(zip(xseq, yseq)):
        # Build the j'th base polynomial
        polyj = onepoly
        for m, xm in enumerate(xseq):
            if m != j:
                polyj *= (x - xm) / (xj - xm)
        # Add in the j'th polynomial
        result += yj * polyj
    return sympy.expand(result)


print(lagrangepoly([28, 68, 164, 404, 998, 2482, 6166]))

