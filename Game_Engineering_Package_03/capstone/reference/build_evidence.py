"""Generate synthetic/model-based reference evidence into a NEW directory.

These model outputs are separate from the actually measured benchmark. This
script does not produce a student's proof, reviewed project or original work.
"""
from pathlib import Path
import argparse
import csv
import json
import math
import random
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
import mathkit as m

def csv_write(path,rows):
    with path.open('w',newline='') as file:
        writer=csv.DictWriter(file,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)

def generate(out):
    if out.exists():raise ValueError('choose a new --out directory; existing evidence is not overwritten')
    out.mkdir(parents=True,exist_ok=False)
    world=m.matmul(m.matmul(m.translation(10,0,0),m.rotation_z(math.pi/2)),m.translation(2,0,0))
    q=(math.sqrt(.5),0,0,math.sqrt(.5))
    geom=dict(convention='column vectors, right handed, y up, scalar-first quaternion',
              parent_child_origin=m.transform4(world,(0,0,0,1)),
              translated_direction=m.transform4(m.translation(10,20,30),(1,0,0,0)),
              rotated_vector=m.quat_rotate(q,(1,0,0)),zero_vector_policy='ValueError: no unique direction')
    assert all(math.isclose(a,b,abs_tol=1e-12) for a,b in zip(geom['parent_child_origin'],(10,2,0,1)))
    (out/'geometry.json').write_text(json.dumps(geom,indent=2,allow_nan=False))
    rows=[]
    for exponent in range(1,17):
        h=10.**(-exponent)
        try:
            estimate=m.centered_difference(math.exp,1.,h)
            rows.append(dict(h=h,estimate=estimate,exact=math.e,absolute_error=abs(estimate-math.e),status='finite'))
        except ValueError:
            rows.append(dict(h=h,estimate='',exact=math.e,absolute_error='',status='unresolvable_step'))
    csv_write(out/'derivatives.csv',rows)
    rows=[]
    for method in ('left','trapezoid'):
        for n in (4,8,16,32,64):
            value=m.integrate(lambda x:x*x,0,1,n,method)
            rows.append(dict(method=method,panels=n,estimate=value,exact=1/3,absolute_error=abs(value-1/3)))
    csv_write(out/'quadrature.csv',rows)
    rows=[];summaries=[]
    for method in ('explicit','semi'):
        for h in (.1,.05,.025,.25):
            x,v=1.,0.;steps=round(2/h);errors=[];ratios=[]
            for i in range(steps+1):
                t=i*h;xr=math.cos(10*t);vr=-10*math.sin(10*t);energy=.5*v*v+50*x*x
                error=abs(x-xr);errors.append(error);ratios.append(energy/50)
                rows.append(dict(method=method,dt_s=h,index=i,time_s=t,x_m=x,v_m_per_s=v,
                                 reference_x_m=xr,reference_v_m_per_s=vr,energy_J=energy,
                                 energy_ratio=energy/50,absolute_position_error_m=error))
                if i<steps:x,v=m.spring_step(x,v,1,100,0,h,method)
            summaries.append(dict(method=method,dt_s=h,horizon_s=2,steps=steps,max_position_error_m=max(errors),
                                  final_position_error_m=errors[-1],final_energy_ratio=ratios[-1],
                                  peak_energy_ratio=max(ratios),adverse_step=h==.25))
    csv_write(out/'spring_trajectories.csv',rows)
    csv_write(out/'spring_summary.csv',summaries)
    rows=[]
    for n in range(40):
        t=n/1000
        hi=math.cos(2*math.pi*900*t);lo=math.cos(2*math.pi*100*t)
        assert abs(hi-lo)<1e-10
        rows.append(dict(index=n,time_s=t,cosine_900_Hz=hi,cosine_100_Hz=lo,
                         sine_900_Hz=math.sin(2*math.pi*900*t),negative_sine_100_Hz=-math.sin(2*math.pi*100*t)))
    csv_write(out/'sampling.csv',rows)
    filters=dict(boundary='full zero extension, causal h[0] at index 0',
                 signal=[1,2,3],kernel=[.5,.5],full=m.convolve([1,2,3],[.5,.5]),
                 checker=[0,1]*4,raw_phase0=[0,0,0,0],raw_phase1=[1,1,1,1],pair_average=[.5]*4)
    (out/'filters.json').write_text(json.dumps(filters,indent=2))
    rows=[]
    for seed in (2026,2027,2028):
        for n in (100,1000,10000):
            rng=random.Random(seed);counts=[0,0,0]
            for _ in range(n):counts[m.weighted_index((70,25,5),rng.random())]+=1
            for category,(count,p,reward) in enumerate(zip(counts,(.7,.25,.05),(0,5,20))):
                rows.append(dict(seed=seed,trials=n,category=category,reward=reward,count=count,
                                 model_probability=p,observed_frequency=count/n,
                                 model_expected_count=n*p,data_kind='synthetic_sampling_experiment'))
    csv_write(out/'loot_counts.csv',rows)
    rows=[]
    for alpha in (.25,.5,1.,1.1):
        result=m.descent_quadratic(0,alpha,32,1e-8)
        for i,x in enumerate(result['history']):
            assert math.isclose(x,3-3*(1-2*alpha)**i,rel_tol=1e-9,abs_tol=1e-9)
            rows.append(dict(alpha=alpha,iteration=i,x=x,objective=(x-3)**2,error_to_minimum=abs(x-3),
                             final_status=result['reason']))
    csv_write(out/'optimization.csv',rows)
    two=[]
    for alpha in (.1,.4):
        x,y=0.,0.
        for i in range(11):
            two.append(dict(alpha=alpha,iteration=i,x=x,y=y,objective=(x-3)**2+3*(y+1)**2))
            x,y=x-alpha*2*(x-3),y-alpha*6*(y+1)
    csv_write(out/'optimization_2d.csv',two)
    metadata=dict(data_kind='synthetic_analytic_and_numerical_reference_outputs',
                  simulation='one-dimensional undamped spring: mass=1 kg, stiffness=100 N/m, initial x=1 m, v=0, T=2 s',
                  probability='chosen weights 70/25/5; same seed across sample sizes shares prefixes and is not an independent replicate across n',
                  limitations='Not measured player, hardware or physical-system observations. No proof or student mastery is certified.',
                  reproduce='python capstone/reference/build_evidence.py --out outputs/new_reference')
    (out/'metadata.json').write_text(json.dumps(metadata,indent=2))
    print(f'Generated {len(list(out.iterdir()))} reference evidence files in {out}')

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out',required=True,type=Path)
    args=parser.parse_args()
    try:generate(args.out)
    except (ValueError,OSError) as e:parser.exit(2,f'Evidence generation stopped: {e}\n')
if __name__=='__main__':main()
