### Preamble
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from scipy import linalg
from scipy import optimize
import sympy as sm

###  Solve consumer problem:
# Sympyify equation
l = sm.symbols('l') # leisure in hrs. pr. week
c = sm.symbols('c') # consumption in dollars pr. week
alpha = sm.symbols('alpha') # Elasticity of utility wrt. leisure
beta = sm.symbols('beta') # Elasticity of utility wrt. consumption
w =sm.symbols('w') # wage rate
R0 = sm.symbols('R_0') # Maximum potential income (no leisure).
A = sm.symobols('A') # Non labour income

# objective function
util= l**alpha *c**beta

# budget constraint:
bc=sm.Eq(w*l+c, 24*7*w +A)

##



