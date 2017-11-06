"""
Author: Esteban Jiménez Rodríguez
Institution: ITESO - Universidad Jesuita de Guadalajara
Date: 01/11/2017
Description: This script contains an abstract model definition for linear 
programming problems. The model considered is 
            min f'*x    subject to: A x  <= b 
              x                     Aeq x = beq
"""

from __future__ import division
from pyomo.environ import *
from pyomo.opt import SolverFactory

model = AbstractModel()
opt = SolverFactory('glpk')

model.m1 = Param(within=NonNegativeIntegers)
model.m2 = Param(within=NonNegativeIntegers)
model.n = Param(within=NonNegativeIntegers)

model.I = RangeSet(1, model.m1)
model.J = RangeSet(1, model.m2)
model.K = RangeSet(1, model.n)

model.A = Param(model.I, model.K)
model.b = Param(model.I)
model.Aeq = Param(model.J, model.K)
model.beq = Param(model.J)
model.f = Param(model.K)

# the next line declares a variable indexed by the set J
model.x = Var(model.K, domain = NonNegativeReals)

def obj_expression(model):
    return summation(model.f, model.x)

model.OBJ = Objective(rule=obj_expression)

def ax_ineq_constraint(model, i):
    # return the expression for the inequality constraint for i
    return sum(model.A[i,k] * model.x[k] for k in model.K) <= model.b[i]

def ax_eq_constraint(model, j):
    # return the expression for the equality constraint for j
    if sum(model.Aeq[j,k] * model.x[k] for k in model.K) == model.beq[j]:
        return Constraint.Feasible
    else:
        return sum(model.Aeq[j,k] * model.x[k] for k in model.K) == model.beq[j]

# the next line creates one ineq constraint for each member of the set model.I
model.AxleqbConstraint = Constraint(model.I, rule=ax_ineq_constraint)
# the next line creates one equality constraint for each member of the set model.J
model.AxeqbConstraint = Constraint(model.J, rule=ax_eq_constraint)