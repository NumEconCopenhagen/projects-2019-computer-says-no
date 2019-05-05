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
# test set parameters (CB)
alpha=0.5
tax2=0.5
tax1=0.3
tax0=0
w=10
cut1=4
cut2=7
T=10
A=10
# Cobb-Douglas:
def  _cobbdouglas(c,l):
    """ Cobb douglas utility function for 2 goods.
    PARAMETERS
    alpha: income share spent on consumption
    INPUT:
    c: consumption
    l: leisure

    OUTPUT:
    u: utility (negative)"""
    u= (c**alpha)*l**(1-alpha)
    return -u
def  cobbdouglas(x):
    return _cobbdouglas(c=x[0],l=x[1])

# CES utility function:
def _CES(c,l):
    """ CES utility function for 2 goods.
    PARAMETERS:
    r: 1/(1-r) is the elasticity of substitution, r<=1.
    a: relative preference for consumption (1 unit of consumption
     gives the same utility as 1 unit lesiure), 0<=a<=1.
    INPUT:
    c: consumption (dollars spent)
    l: leisure (hrs pr. week)

    OUTPUT:
    u: utility (neg) """
    u=(a*c**r + (1-a)*l**r)**(1/r)
    return -u
def CES(x):
    """ Takes a tuple as argument:
    ARGS
    x is a 2x1
    x0= consumption
    x1= leisure
    OUTPUT
    utility from consumption
    """
    return _CES(c=x[0],l=x[1]) 

## Budget constraint (BC)
# Three elements are defined for the (BC):
#1) wage function: returning the after tax wagerate for
# for a given level of leisure consumption (the more leisure
#  the lower taxrate = higher wagerate).
#2) maxwage: returns the wage earned given all time endowed is
# spent working.
#3) The budget function: calculates the slack in budget given
#   choices of leisure and consumption (this is the contrained
#   funtion).


#Wage function 
def wage(l):
    """ Wage function for a progressive tax system with allowing for two specified kinks
        2 kinks (3 tax brackets).
        
        PARAMETERS:
        cut1, cut2: cutoff for tax brackets defined by consumption of
                    leisure.
        w0,w1,w2: wage rates in the respective tax brackets.
        
        ARGS:
        demand typle, x: x[0] cons, x[1] lesiure consumption
        
        OUTPUT:
        w0,w1,w2: the appropriate marginal after tax wage rate
    """
    if l < cut2:
        return w*(1-tax2)
    elif cut2<= l and l <= cut1:
        return w*(1-tax1)
    else:
        return w*(1-tax0)

# Return labour income if all time is spent working:
maxwage = cut2*w*(1-tax2)+(cut1-cut2)*w*(1-tax1)+(T-cut1)*w*(1-tax0)
# Budget constraint
def budget(x):
    c=x[0]
    l=x[1]
    R0= maxwage + A
    slack= R0 - wage(l)*l - c #w is wage rate for working, c and l are
    return  slack       # consumption and lesiure respectively.
budget_con={'type':'eq', 'fun':budget}
bounds= Bounds([0,np.inf], {0, T})
## Optimization:
guess=(5, 50)
result = optimize.minimize(cobbdouglas,guess,
                             method='SLSQP',
                             constraints=[budget_con],
                             options={'disp':True})
 

print('\nx = ',result.x)



