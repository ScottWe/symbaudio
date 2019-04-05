import sympy
import sympy.abc

def _reconstruction_impl(p_n, p_n_sub_1, n, dom):
    """
    Performs the XGCD algorithm on two polynomials, until the degree of the
    first polynomial is within a certain threshold. That polynomial, and its
    corresponding V Bezout polynomial are returned.

    Arguments
    p_n -- the polynomial of maximal degree in {p1, p2}
    p_n_sub_1 --  the polynomial of minimal degree in {p1, p2}
    n -- the termination threshold
    """
    v_n_sub_1 = sympy.Poly([0], sympy.abc.x, domain=dom)
    v_n = sympy.Poly([1], sympy.abc.x, domain=dom)
    
    while (p_n.total_degree() > n):
        (q, r) = sympy.polys.polytools.div(p_n, p_n_sub_1, domain=dom)
        (v_n_sub_1, v_n) = (v_n, v_n_sub_1 - v_n * q)
        p_n_sub_1 = p_n
        p_n = r
    
    return (p_n_sub_1, v_n_sub_1)

def reconstruct_rational(k, coefficients, dom="QQ"):
    """ Constructs a degree k rational for the given coefficients.

    Produces the numerator and denominator of a rational generating function,
    under the assumption that the provided sequence is an order k recurrence
    relation.

	Arguments
    k -- the order of the recurrence relation
    coefficients -- the coefficients from which to reconstruct
    dom -- the Euclidean domain over which to reconstruct (default: "QQ")
    """
    assert(len(coefficients) >= 2 * k)
    n = 2 * k
    a0 = sympy.Poly(sympy.abc.x ** n, sympy.abc.x, domain=dom)
    a1 = sympy.Poly(reversed(coefficients[:n]), sympy.abc.x, domain=dom)

    zero = sympy.Poly([0], sympy.abc.x, domain=dom)
    if a1 == zero:
        return (zero, zero)
    else:
        return _reconstruction_impl(a0, a1, k - 1, dom)
