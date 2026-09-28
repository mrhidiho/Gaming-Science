"""Analytically specified checks; no imports from reference implementations."""
from dataclasses import dataclass
import math

@dataclass
class Case:
    lesson: str
    name: str
    function: str
    args: tuple
    expected: object = None
    error: type[Exception] | None = None

CASES=[]
def C(lesson,name,function,args,expected=None,error=None):
    CASES.append(Case(lesson,name,function,args,expected,error))

for args,out in [((36,6),6.),((0,2),0.),((1.5,.5),3.)]: C('06.1','valid','travel_time',args,out)
for args in [(-1,2),(1,0),(1,-2),(float('nan'),2),(True,2)]: C('06.1','invalid','travel_time',args,error=ValueError)
for p in (False,True):
 for q in (False,True): C('06.2','truth_table','implies',(p,q), not(p is True and q is False))
for args in [(1,True),(False,0)]: C('06.2','non_boolean','implies',args,error=ValueError)
for args,out in [(([],0),0),(([4,0,-1,9],0),0),(([4,0,-1,9],3),1),(([4,0,-1,9],4),2),(([-2,0,-1],3),0)]: C('06.3','prefix','count_positive_prefix',args,out)
for args in [([1],2),([1],-1),([1],True),([float('inf')],1)]: C('06.3','invalid','count_positive_prefix',args,error=ValueError)
for n,out in [(1,0),(2,1),(3,1),(1000,9),(1024,10)]: C('06.4','halving','halving_steps',(n,),out)
for n in [0,-1,1.5,True]: C('06.4','invalid','halving_steps',(n,),error=ValueError)
for args,out in [(((3,4),(1,0)),3.),(((1,0),(0,1)),0.),(((2,-3),(-1,4)),-14.)]: C('07.1','dot','dot',args,out)
for args in [((1,2),(1,)),((),()),((float('nan'),),(1,))]: C('07.1','invalid_dot','dot',args,error=ValueError)
for v,out in [((3,4),(.6,.8)),((-6,8),(-.6,.8)),((1e300,1e300),(math.sqrt(.5),math.sqrt(.5))),((1e-300,0),(1.,0.))]: C('07.1','normalize','normalize',(v,),out)
for v in [(0,0),(),(float('inf'),0)]: C('07.1','invalid_normalize','normalize',(v,),error=ValueError)
C('07.2','matrix_product','matmul',(((1,2),(3,4)),((2,0),(1,2))),((4.,4.),(10.,8.)))
C('07.2','rectangular_product','matmul',(((1,2,3),),((1,),(2,),(3,))),((14.,),))
C('07.2','matrix_dimensions','matmul',(((1,2),),((1,2),)),error=ValueError)
C('07.2','ragged','matmul',(((1,2),(3,)),((1,),(2,))),error=ValueError)
for a,b,out in [(((2,1),(1,-1)),(5,1),(2.,1.)),(((0,1),(2,1)),(3,7),(2.,3.)),(((1e-200,0),(0,1e-200)),(2e-200,3e-200),(2.,3.))]: C('07.2','solve','solve2',(a,b),out)
C('07.2','singular','solve2',(((1,2),(2,4)),(3,6)),error=ValueError)
C('07.2','small_pivot','solve2',(((1,0),(0,1e-14)),(1,1)),error=ValueError)
T=((1,0,0,10),(0,1,0,20),(0,0,1,30),(0,0,0,1))
C('07.3','point','transform4',(T,(1,2,3,1)),(11.,22.,33.,1.))
C('07.3','direction','transform4',(T,(1,2,3,0)),(1.,2.,3.,0.))
R=((0,-1,0,0),(1,0,0,0),(0,0,1,0),(0,0,0,1))
C('07.3','quarter_turn','transform4',(R,(2,0,0,1)),(0.,2.,0.,1.))
C('07.3','no_implicit_division','transform4',(((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,2)),(2,4,6,1)),(2.,4.,6.,2.))
C('07.3','bad_dimensions','transform4',(T,(1,2,3)),error=ValueError)
C('07.3','nonfinite','transform4',(T,(float('nan'),0,0,1)),error=ValueError)
for xs,ys,out in [((0,1,2),(1,3,5),(2.,1.)),((0,1,2),(5,3,1),(-2.,5.)),((0,1,2,3,4),(1.1,2.9,5.2,6.8,9.0),(1.97,1.06)),((1,2,3),(7,7,7),(0.,7.))]: C('07.4','line_fit','fit_line',(xs,ys),out)
for args in [((1,1),(2,3)),((1,),(2,)),((1,2),(3,)),((0,float('inf')),(1,2))]: C('07.4','invalid_fit','fit_line',args,error=ValueError)
for f,x,h,out in [(lambda t:t*t,3,.1,6.),(lambda t:t**3,2,.1,12.01),(lambda t:7,2,.1,0.)]: C('08.1','centered','centered_difference',(f,x,h),out)
for f,x,h in [(lambda t:t,0,0),(lambda t:t,0,-.1),(lambda t:t,1e20,1),(lambda t:float('nan'),0,.1)]: C('08.1','invalid_difference','centered_difference',(f,x,h),error=ValueError)
for f,a,b,n,method,out in [(lambda t:2*t,0,3,4,'trapezoid',9.),(lambda t:t*t,0,1,4,'trapezoid',.34375),(lambda t:t*t,0,1,4,'left',.21875),(lambda t:2*t,3,0,4,'trapezoid',-9.),(lambda t:2*t,1,1,2,'trapezoid',0.)]: C('08.2','quadrature','integrate',(f,a,b,n,method),out)
for args in [(lambda t:t,0,1,0,'left'),(lambda t:t,0,1,2,'unknown'),(lambda t:float('nan'),0,1,2,'left')]: C('08.2','invalid_quadrature','integrate',args,error=ValueError)
for args,out in [((0,4,-10,.5),(.75,-1.)),((2,3,-2,2),(4.,-1.)),((7,-2,0,3),(1.,-2.)),((2,3,7,0),(2.,3.))]: C('08.3','analytic_motion','constant_acceleration',args,out)
for args in [(0,0,1,-1),(0,0,float('inf'),1),(0,0,1,True)]: C('08.3','invalid_motion','constant_acceleration',args,error=ValueError)
for args,out in [((1,0,1,100,0,.1,'explicit'),(1.,-10.)),((1,0,1,100,0,.1,'semi'),(0.,-10.)),((.2,0,2,50,1,.01,'semi'),(.1995,-.05)),((1,2,1,3,4,0,'semi'),(1.,2.))]: C('08.4','spring_step','spring_step',args,out)
for args in [(1,0,0,100,0,.1,'semi'),(1,0,1,-1,0,.1,'semi'),(1,0,1,100,-1,.1,'semi'),(1,0,1,100,0,-.1,'semi'),(1,0,1,100,0,.1,'bogus')]: C('08.4','invalid_spring','spring_step',args,error=ValueError)
for args,out in [((.01,.9,.05),2/13),((.1,.9,.05),2/3),((0,.9,.1),0.),((1,.9,.1),1.)]: C('09.1','posterior','posterior_bug',args,out)
for args in [(0,1,0),(-.1,.9,.1),(.1,1.1,.1),(.1,.9,float('nan'))]: C('09.1','invalid_posterior','posterior_bug',args,error=ValueError)
for weights,u,out in [((70,25,5),0,0),((70,25,5),.7,1),((70,25,5),.95,2),((1,0,3),.25,2),((0,1),0,1),((1,0),.999,0)]: C('09.2','weighted_boundary','weighted_index',(weights,u),out)
for args in [((0,0),.5),((1,-1),.2),((),.2),((1,2),1),((1,2),-.1),((1,2),float('nan'))]: C('09.2','invalid_weights','weighted_index',args,error=ValueError)
for values,p,out in [(([5]*19+[100]),.95,5.),(([5]*19+[100]),.99,100.),([3,1,2],0,1.),([3,1,2],1,3.),([4],.5,4.)]: C('09.3','percentile','percentile',(values,p),out)
for args in [([],.5),([1,2],1.1)]: C('09.3','invalid_percentile','percentile',args,error=ValueError)
C('09.3','mean_interval','mean_interval',([1,2,3,4,5],1),(3.,3-math.sqrt(.5),3+math.sqrt(.5)))
C('09.3','constant_interval','mean_interval',([2,2],2),(2.,2.,2.))
C('09.3','one_sample','mean_interval',([2],2),error=ValueError)
C('09.3','critical_value','mean_interval',([1,2],0),error=ValueError)
for args,out in [(((2,4),(3,4)),math.sqrt(.5)),(((1,2),(1,2)),0.),(((0,0),(3,4)),math.sqrt(12.5))]: C('09.4','rmse','rmse',args,out)
for args in [((),()),((1,2),(1,)),((1,float('nan')),(1,2))]: C('09.4','invalid_rmse','rmse',args,error=ValueError)
for f,p,h,out in [(lambda p:p[0]**2+3*p[1]**2,(2,-1),1e-4,(4.,-6.)),(lambda p:p[0]**2-p[1]**2,(0,0),.01,(0.,0.)),(lambda p:p[0]*p[1]+p[0]**2,(2,3),1e-4,(7.,2.))]: C('10.1','gradient','gradient',(f,p,h),out)
for f,p,h in [(lambda p:0,(1,2),0),(lambda p:0,(),.1),(lambda p:0,(1e20,2),1),(lambda p:float('nan'),(1,2),.1)]: C('10.1','invalid_gradient','gradient',(f,p,h),error=ValueError)
for args,out in [((900,1000),100.),((700,1000),300.),((1100,1000),100.),((500,1000),500.),((1000,1000),0.),((0,1000),0.)]: C('10.2','alias','alias_frequency',args,out)
for args in [(-1,1000),(1,0),(float('inf'),1000)]: C('10.2','invalid_alias','alias_frequency',args,error=ValueError)
for args,out in [(([1,2,3],[.5,.5]),[.5,1.5,2.5,1.5]),(([1],[.25,.5,.25]),[.25,.5,.25]),(([1,2,3],[1,2]),[1.,4.,7.,6.]),(([],[1]),[]),(([1,1,1,1],[.5,.5]),[.5,1.,1.,1.,.5])]: C('10.3','convolution','convolve',args,out)
for args in [([1],[]),([float('nan')],[1]),([1],[float('inf')])]: C('10.3','invalid_convolution','convolve',args,error=ValueError)
for args,out in [((0,.5,10,1e-8),dict(x=3.,converged=True,iterations=1,reason='gradient_tolerance')),((3,.25,0,1e-8),dict(x=3.,converged=True,iterations=0)),((0,.25,0,1e-8),dict(x=0.,converged=False,iterations=0,reason='iteration_limit')),((0,.25,8,.03),dict(x=2.98828125,converged=True,iterations=8)),((0,1,8,1e-8),dict(x=0.,converged=False,iterations=8))]: C('10.4','descent_status','descent_quadratic',args,out)
for args in [(0,0,10,1e-8),(0,.25,-1,1e-8),(0,.25,10,0),(float('inf'),.25,10,1e-8)]: C('10.4','invalid_descent','descent_quadratic',args,error=ValueError)
