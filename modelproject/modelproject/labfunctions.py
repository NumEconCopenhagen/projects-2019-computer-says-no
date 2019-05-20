import numpy as np
import scipy as sp
from scipy import linalg
from scipy import optimize
from scipy.optimize import Bounds
import scipy.integrate as integrate
%matplotlib inline
import matplotlib.pyplot as plt
from matplotlib import cm

def max_u(util, wage, maxlabinc, leiexp,par):
    """Return utility for optimal consumption bundle.
    INPUT:
    Util: Utility function (CES or cobbdouglas)
    wage: wage function
    maxlabinc: max. wage income if all time is supplied as labour
    leiexp: Expenditure on leisure
    par: parameters for util function
    
    OUTPUT:
    max_U: Utility derived in optimum
    """
    if util=="cobbdouglas":
        # Call optimizer
        temp = optimize.minimize(cobbdouglas, guess_flat,args=par, method='SLSQP',                        
           constraints=[budget_func(wage, maxlabinc, leiexp)], options={'disp':False}, bounds=bounds)
        return -temp.fun
    elif util=="CES":
        temp = optimize.minimize(CES, guess_flat,args=par, method='SLSQP',                        
           constraints=[budget_func(wage, maxlabinc, leiexp)], options={'disp':False}, bounds=bounds)
        return -temp.fun
    else:
        print(f'Utility function not recognized, util can be cobbdouglas or CES')
    
def indif_opt(util,max_u,par):
    """ Function to plot indifference curve for a given utility level and function. Returns a list of goods
     consumption levels, where each element is such that it secures a fixed utility for some leisure choice.
      Leisure choices are then a linear space of between 0 and 10.
    INPUT:
    util: utility func (either CES or Cobbdouglas at present)
    max_u: utility in optimum (found from maximiation by numerical or analytical means)
    alpha: utility fucntion parameter
    
    OUTPUT:
    c: goods consumption that ensures u_bar utility given l leisure.
    """
    if util=="cobbdouglas":
        c_indif=lambda l: max_u**(1/par)*l**((par-1)/par)
        return [c_indif(x) for x in np.linspace(0.01,10,100)]
    elif util=="CES":
        a=par[0]
        r=par[1]
        c_indif=lambda l: ((max_u-(1-a)*l^r)/a)^(1/r)
        return [c_indif(x) for x in np.linspace(0.01,10,100)]
    else:
        print(f'Undefined utility function provided, util is either CES or cobbdouglas')


# Optimizer for the progressive tax system:
def solverprog(util, par):
    """ Runs SLSQP optimizer for a parameterization for each piecewise linear part of the budget constraint (3),
    and evaluates the kink points (2) aswell, then compares the utility of these 5 points, and returns the leisure consumption
    associated with the highest utility bundle.
    INPUT:
    Util: Utility function of agents.
    par: Parameters of the utility function (tuple if multipile); For cobddouglas an args=alpha (bt. 0 and 1),
    For CES a 2-tuple, where par[0]=a  and par[1]=r, 0<=a<=1 and r <=1.
    OUTPUT
    c^*: optimal leisure consumption (float)
    """
    # Optimize behaviour in no tax bracket (l_bot < l < T):
    guess_no= (goods(1/2*(T-l_bot)), 1/2*(T-l_bot))
    best_notax= optimize.minimize(util,guess_no,args=par,method='SLSQP', constraints=[budget_func(wage_prog,maxlabinc_prog,leiexp_prog)],
                                options={'disp':False}, bounds=Bounds((0,l_bot), (np.inf, T)))
    # Optimize behaviour in low tax bracket ( l_top < l <l_bot):
    guess_low= (goods(1/2*(l_bot-l_top)), 1/2*(l_bot-l_top))
    best_lowtax = optimize.minimize(util,guess_low,args=par, method='SLSQP', constraints=[budget_func(wage_prog,maxlabinc_prog,leiexp_prog)],
                                options={'disp':False}, bounds=Bounds((0,l_top), (np.inf, l_bot)))
    #Optimize behaviour in top tax bracket ( 0 < l < l_top):
    guess_high=(goods(1/2*(l_top)), 1/2*l_top)
    best_hightax = optimize.minimize(util,guess_high,args=par, method='SLSQP', constraints=[budget_func(wage_prog,maxlabinc_prog,leiexp_prog)],
                                options={'disp':False}, bounds=Bounds((0,0), (np.inf, l_top)))
    #Evaluate utility at kink point between no tax and low tax (util(l=l_bot, c=R_0-leiexp(l_bot,wage)):
    Kink_bot = util(x_bot,par) 
    kink_top= util(x_top,par)
    
    # Evaluate candidates and choose optimal bundle
    candidates=np.array([[best_notax.fun, best_notax.x[0], best_notax.x[1]], [best_lowtax.fun, best_lowtax.x[0], best_lowtax.x[1]], [best_hightax.fun,best_hightax.x[0],best_hightax.x[1]], 
                         [Kink_bot, x_bot[0],x_bot[1]], [kink_top, x_top[0],x_top[1]]]) # Create array with all candidates where first element is utility
                                                                                      # 2nd is the consumption bundle as a tuple.
    best_cand=np.argmin(candidates,axis=0) # exstract row number for best bundle.
    return candidates[best_cand[0],2] # returns only optimal leisure choice.

# Solver for lump sum tax or progressive tax
def solverdif(util, wage, maxlabinc, leiexp,par):
    """Return utility for optimal consumption bundle given a budget constraint that is continously  differentiable (class C^1).
    INPUT:
    Util: Utility function
    wage: wage function
    maxlabinc: max. wage income if all time is supplied as labour
    leiexp: Expenditure on leisure
    alpha: parameters for util function
    
    OUTPUT:
    max_U: Utility derived in optimum
    """
    # Call optimizer
    temp = optimize.minimize(util, guess_flat,args=par, method='SLSQP',                        
           constraints=[budget_func(wage, maxlabinc, leiexp)], options={'disp':False}, bounds=bounds)
    return temp.x[1]
