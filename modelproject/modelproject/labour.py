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

def solver_prog(util, par):
    """ Runs SLSQP optimizer for a parameterization for each piecewise linear part of the budget constraint,
        and evaluates the kink points aswell. 
   INPUT:
   Util: Utility function of agents.
   par: Parameters of the utility function (tuple if multipile); For cobddouglas an args=alpha (bt. 0 and 1),
                                 For CES a 2-tuple, where par[0]=a  and par[1]=r, 0<=a<=1 and r <=1.
   """
    # Optimize behaviour in no tax bracket (l_bot < l < T):
    best_notax= optimize.minimize(util,guess,args=par,
                             method='SLSQP',
                             constraints=[budget_func(wage_prog,maxlabinc_prog,leiexp_prog)],
                             options={'disp':False}, bounds=Bounds((0,l_bot), (np.inf, T)))
    # Optimize behaviour in low tax bracket ( l_top < l <l_bot):
    best_lowtax = optimize.minimize(util,guess,args=par,
                             method='SLSQP',
                             constraints=[budget_func(wage_prog,maxlabinc_prog,leiexp_prog)],
                             options={'disp':False}, bounds=Bounds((0,l_top), (np.inf, l_bot)))
    #Optimize behaviour in top tax bracket ( 0 < l < l_top):
    best_hightax = optimize.minimize(util,guess,args=par,
                             method='SLSQP',
                             constraints=[budget_func(wage_prog,maxlabinc_prog,leiexp_prog)],
                             options={'disp':False}, bounds=Bounds((0,0), (np.inf, l_top)))
    #Evaluate utility at kink point between no tax and low tax (util(l=l_bot, c=R_0-leiexp(l_bot,wage)):
    Kink_bot = util(goods_bot,l_bot) 
    kink_top= util(goods_top,l_top)
    
    # Evaluate candidates and choose optimal bundle
    candidates=np.array([[best_notax.fun, best_notax.x[0], best_notax.x[1]], [best_lowtax.fun, best_lowtax.x[0], best_lowtax.x[1]], [best_hightax.fun,best_hightax.x[0],best_hightax.x[1]], 
                        [Kink_bot, x_bot[0],x_bot[1]], [kink_top, x_top[0],x_top[1]]]) # Create array with all candidates where first element is utility
                                                                                      # 2nd is the consumption bundle as a tuple.
    best_cand=np.argmax(candidates,axis=0) # Restract row number for best bundle.
    return (candidates[best_cand[0],1],candidates[best_cand[0],2])