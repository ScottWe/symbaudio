import numpy
import sympy

def max_coeff(poly):
    """ Computes the maximum width of a polynomial's coefficients.

    Arguments:
    poly -- the rational polynomial to analyze
    """
    dom = poly.domain
    if isinstance(dom, sympy.polys.domains.IntegerRing):
        # Finds maximal element.
        return numpy.max(poly.all_coeffs())
    elif isinstance(dom, sympy.polys.domains.FiniteField):
        # Finds maximal element modulo the field order (handles negatives).
        return numpy.max(numpy.mod(poly.all_coeffs(), dom.characteristic()))
    elif isinstance(dom, sympy.polys.domains.RationalField):
        # Considers both numerator and denominator (coeff=p/q).
        max_coeff = 0
        for coeff in poly.all_coeffs():
            max_coeff = max(max_coeff, abs(coeff.p), coeff.q)
        return max_coeff

def count_zeros(poly):
    """ Computes the number of zero coefficients in a polynomial.

    Arguments:
    poly -- the rational polynomial to analyze
    """
    dom = poly.domain
    if isinstance(dom, sympy.polys.domains.IntegerRing) or isinstance(dom, sympy.polys.domains.FiniteField):
        # Finds all zero elements.
        return len(poly.all_coeffs()) - numpy.count_nonzero(poly.all_coeffs())
    elif isinstance(dom, sympy.polys.domains.RationalField):
        # Considers both numerator and denominator (coeff=p/q).
        zeros = 0
        for coeff in poly.all_coeffs():
            if coeff.p == 0:
                zeros = zeros + 1
        return zeros

