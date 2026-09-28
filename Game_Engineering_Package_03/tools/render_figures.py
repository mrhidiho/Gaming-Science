"""Optional Matplotlib figure renderer; all required labs work without it.

Uses supplied numerical CSVs. Install/use Matplotlib only in an appropriate local
environment; this tool never installs packages automatically.
"""
from pathlib import Path
import csv
import math
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
except ImportError:
    raise SystemExit('Optional plotting requires Matplotlib. The PDFs already include rendered figures; required labs and CSV generation use only the standard library.')
DATA=ROOT/'capstone/reference_evidence/numerics'
OUT=ROOT/'figures';OUT.mkdir(exist_ok=True)

def rows(name):
    with (DATA/name).open() as file:return list(csv.DictReader(file))
def finish(fig,name):
    fig.tight_layout();fig.savefig(OUT/name,dpi=170);plt.close(fig)

fig,ax=plt.subplots(figsize=(6.5,3.7))
ax.plot([0,3],[0,4],marker='o',label='v = (3, 4)')
ax.plot([0,3],[0,0],marker='o',label='projection onto x')
ax.plot([3,3],[0,4],linestyle='--',label='perpendicular residual')
ax.set(xlim=(-.3,4.5),ylim=(-.3,4.5),xlabel='x component',ylabel='y component',title='Vector and projection in a y-up plane')
ax.set_aspect('equal');ax.legend(loc='upper left',fontsize=8);ax.grid(True,alpha=.25)
finish(fig,'vector_projection.png')

fig,ax=plt.subplots(figsize=(6.5,3.7))
d=[r for r in rows('derivatives.csv') if r['status']=='finite' and float(r['absolute_error'])>0]
ax.loglog([float(r['h']) for r in d],[float(r['absolute_error']) for r in d],marker='o')
ax.set(xlabel='Centered-difference step h',ylabel='Absolute derivative error',title='Derivative of exp(x) at x = 1: smaller is not always better')
ax.grid(True,which='both',alpha=.25)
finish(fig,'derivative_error.png')

fig,ax=plt.subplots(figsize=(6.5,3.7))
d=rows('spring_trajectories.csv')
for method in ('explicit','semi'):
 a=[r for r in d if r['method']==method and float(r['dt_s'])==.05]
 ax.semilogy([float(r['time_s']) for r in a],[float(r['energy_ratio']) for r in a],label=method)
ax.set(xlabel='Simulated time (s)',ylabel='E / E0 (log scale)',title='Same undamped spring, same 0.05 s step, different methods')
ax.legend();ax.grid(True,alpha=.25)
finish(fig,'spring_energy.png')

fig,ax=plt.subplots(figsize=(6.5,3.7))
t=[i/100000 for i in range(901)]
ax.plot(t,[math.cos(2*math.pi*900*x) for x in t],label='continuous 900 Hz cosine')
ax.plot(t,[math.cos(2*math.pi*100*x) for x in t],linestyle='--',label='continuous 100 Hz cosine')
st=[i/1000 for i in range(10)]
ax.plot(st,[math.cos(2*math.pi*100*x) for x in st],linestyle='none',marker='o',label='shared samples at 1000 Hz')
ax.set(xlabel='Time (s)',ylabel='Amplitude (unitless)',title='Different continuous signals, identical sampled cosines')
ax.legend(fontsize=8,loc='upper right');ax.grid(True,alpha=.25)
finish(fig,'aliasing.png')

fig,ax=plt.subplots(figsize=(6.5,3.7))
d=rows('optimization.csv')
for alpha in (.25,1.,1.1):
 a=[r for r in d if float(r['alpha'])==alpha]
 ax.semilogy([int(r['iteration']) for r in a],[float(r['error_to_minimum']) for r in a],marker='.',label=f'alpha = {alpha:g}')
ax.set(xlabel='Update count',ylabel='Absolute error |x - 3| (log scale)',title='The same correct gradient with three step sizes')
ax.legend();ax.grid(True,alpha=.25)
finish(fig,'optimization.png')
print('Rendered 5 figures with Matplotlib',matplotlib.__version__)
