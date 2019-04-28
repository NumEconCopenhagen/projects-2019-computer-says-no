### Preamble
import numpy as np

### The consumer problem:
# 3 ingredients: i) utility function ii) Budget constraint iii) additional constraints

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
R0 =w*h + A     # R0 is potential income if all time is spent
                # working, h is the hrs worked in a week, and A
                # is non labour income
def budget(c,l):
    return slack=R0 - w*l + - C #, w is wage rate for working, C and l is
                # consumption and lesiure respectively.
budget_con={'type':'eq', 'fun'=budget}

## Time constraint
 




