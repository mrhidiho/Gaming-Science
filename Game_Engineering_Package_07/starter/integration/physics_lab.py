"""Free-fall convergence, chain residuals and off-center contact impulse.

Original numerical demonstrations. Not a Box2D adapter or rigid-body engine.
"""
import json


def free_fall(steps):
    h=1/steps;x=v=0.
    for _ in range(steps):v-=10*h;x+=v*h
    return {'steps':steps,'position':x,'analytic':-5.,'absolute_error':abs(x+5)}

def chain(iterations):
    x=[0.,1.4,2.8,4.2]
    for _ in range(iterations):
        for i in range(3):
            error=x[i+1]-x[i]-1
            if i==0:x[i+1]-=error
            else:x[i]+=error/2;x[i+1]-=error/2
    return {'iterations':iterations,'max_distance_error':max(abs(x[i+1]-x[i]-1) for i in range(3)),'positions':x}

def angular_contact():
    # Static B; A mass 2, inertia .25; +x normal; r_A=(0,.5).
    wa=.5;inv_i=4.;ra_cross_n=-.5;vn=-3.;e=.5
    effective=wa+ra_cross_n**2*inv_i
    impulse=-(1+e)*vn/effective
    va=3-impulse*wa
    # A receives -J*n; angular change = -I^-1*(r_A cross n)*J.
    omega=-inv_i*ra_cross_n*impulse
    after_vn=-(va-omega*.5)
    assert abs(after_vn-(-e*vn))<1e-12
    return {'effective_inverse_mass':effective,'impulse':impulse,'va_after':va,'omega_after':omega,'relative_normal_speed_after':after_vn}

if __name__=='__main__':
    falls=[free_fall(n) for n in (30,60,120)]
    residuals=[chain(n) for n in (1,2,4,8,16,32)]
    assert falls[-1]['absolute_error']<falls[0]['absolute_error']
    assert residuals[-1]['max_distance_error']<residuals[0]['max_distance_error']
    print(json.dumps({'free_fall':falls,'chain_position_projection':residuals,'off_center_contact':angular_contact(),
      'limits':'Projection is not an energy-conserving constraint solver. No maintained-library comparison performed.'},indent=2))
