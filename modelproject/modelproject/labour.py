### Preamble
import numpy as np
import scipy as sp
from scipy import linalg
from scipy import optimize
from scipy.optimize import Bounds
import scipy.integrate as integrate
### The consumer problem
# 3 ingredients: i) utility function ii) Budget constraint iii) additional constraints
#Parameters to set: T available time, w function, A non-labour income

## Utility functions

# Cobb-Douglas:
def  cobbdouglas(c,l):
    """ Cobb douglas utility function for 2 goods.
    PARAMETERS
    alpha: utility elasticity of consumption
    INPUT:
    c: consumption
    l: leisure

    OUTPUT:
    u: utility """
    u= (c**alpha)*l**(1-alpha)
    return u

# CES utility function:

def CES(c,l):
    """ CES utility function for 2 goods.
    PARAMETERS:
    r: 1/(1-r) is the elasticity of substitution, r<=1.
    a: relative preference for consumption (1 unit of consumption
     gives the same utility as 1 unit lesiure), 0<=a<=1.
    INPUT:
    c: consumption (dollars spent)
    l: leisure (hrs pr. week)

    OUTPUT:
    u: utility """
    u=(a*c**r + (1-a)*l**r)**(1/r)
    return u

## Budget constraint
# R0 is potential income if all time is spent
# working, T the time available, and A
# is non labour income
#wage function 
def wage(l):
    if l < cut1:
        return w0
    elif cut1<= l and l <= cut2:
        return w1
    else:
        return w2

maxwage = integrate.quad(wage, 0, T, args= (t1,t2))
def budget(c,l, w, T,A):
    R0=maxwage + A
    slack= R0 - w*l + - C #w is wage rate for working, C and l are
    return  slack         # consumption and lesiure respectively.
budget_con={'type':'eq', 'fun':budget}

## Additional constrains / bounds:
bounds= Bounds([0,np.inf], {0, np.inf})


 





