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
cut1=7
cut2=4
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
#1) Wage function: returning the marg. after tax wage for
# for a given level of leisure consumption (the more leisure consumed
#  the lower taxrate => higher wagerate). It is also the marg. price of
# additional leisure.
#2) Leisure expenditure function: returns the expenditure connected to
#  buying l units of leisure
#3) The budget function: calculates the slack in budget given
#   choices of leisure and consumption (this is the contrained
#   funtion).

#1) Wage function 
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
    elif cut2<= l and l < cut1:
        return w*(1-tax1)
    else:
        return w*(1-tax0)

#2) Return labour income if all time is spent working:
def leiexp(l,wage):
    """Returns labour income if T hours is spent working
    under a given tax system.
    ARGS:
    T: Time endowed (int)
    Wage: Marginal wage-function (incoperating tax system) (function)
    
    OUTPUT:
    maxwage: max labour income (int)
    """
    return sp.integrate.quad(wage,0,l)[0]
print(leiexp(5,wage))


#3) Budget constraint
maxlabinc=leiexp(T,wage) # The maximal labour income = the cost of buying
                         # T units of leisure.
def budget(x):
    c=x[0]
    l=x[1]
    R0= maxlabinc + A
    slack= R0 - leiexp(l,wage) - c #w is wage rate for working, c and l are
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



#maxwage1 = cut2*w*(1-tax2)+(cut1-cut2)*w*(1-tax1)+(T-cut1)*w*(1-tax0)
#print(maxwage1)
#3) Expenditure on leisure:
#def leisureexp(l,wage):
#    """ Calculates the expenditure used on leisure for a given
#    level of leisure demanded as the integral of the product of 
#    the wage function and leisure demanded.
#    
#    ARGS:
#    x: Leisure demandend (int)
#    wage: Marginal wage (function)
#
#    OUTPUT:
#    leiexp: Expenditure on leisure (int)
#    """
#    exp = wage*x
#    return sp.integrate.quad(exp,0,l)[0]
#print(leisureexp(3,wage))