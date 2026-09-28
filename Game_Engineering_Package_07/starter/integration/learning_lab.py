"""Synthetic episode-split classifier experiment, not game-AI effectiveness proof."""
from __future__ import annotations
import json
import math
import random


def sigmoid(z):
    if z>=0:return 1/(1+math.exp(-z))
    e=math.exp(z);return e/(1+e)

def dataset():
    rows=[]
    for episode in range(150):
        rng=random.Random(episode+280400);bias=rng.uniform(-.4,.4)
        for _ in range(8):
            x=[rng.uniform(-1,1),rng.uniform(-1,1)]
            y=int(1.5*x[0]-.8*x[1]+bias+rng.uniform(-.2,.2)>0)
            rows.append((episode,x,y))
    return rows

def train(rows,epochs):
    w=[0.,0.];b=0.
    for _ in range(epochs):
        for _,x,y in rows:
            error=sigmoid(sum(a*v for a,v in zip(w,x))+b)-y
            w=[a-.02*error*v for a,v in zip(w,x)];b-=.02*error
    return w,b

def confusion(rows,w,b):
    result={'tp':0,'tn':0,'fp':0,'fn':0}
    for _,x,y in rows:
        prediction=int(sigmoid(sum(a*v for a,v in zip(w,x))+b)>=.5)
        result['tp' if prediction and y else 'tn' if not prediction and not y else 'fp' if prediction else 'fn']+=1
    return result

def accuracy(c):return (c['tp']+c['tn'])/sum(c.values())

def experiment():
    rows=dataset();train_rows=[r for r in rows if r[0]<90];val=[r for r in rows if 90<=r[0]<120];test=[r for r in rows if r[0]>=120]
    sets=[{r[0] for r in split} for split in (train_rows,val,test)]
    assert not sets[0]&sets[1] and not sets[0]&sets[2] and not sets[1]&sets[2]
    trials=[]
    for epochs in (5,20,60):
        w,b=train(train_rows,epochs);trials.append((accuracy(confusion(val,w,b)), -epochs,w,b))
    score,negative_epochs,w,b=max(trials,key=lambda row:(row[0],row[1]))
    final=confusion(test,w,b)
    baseline=int(sum(r[2] for r in train_rows)>=len(train_rows)/2)
    baseline_accuracy=sum(r[2]==baseline for r in test)/len(test)
    assert sum(final.values())==240 and all(math.isfinite(z) for z in w+[b])
    return {'data':'synthetic; 150 independent episode seeds; 8 correlated samples per episode',
            'split_episode_counts':[90,30,30],'split_sample_counts':[720,240,240],
            'selected_epochs':-negative_epochs,'validation_accuracy':score,
            'frozen_weights':w,'frozen_bias':b,'heldout_confusion':final,
            'heldout_accuracy':accuracy(final),'majority_training_baseline_heldout_accuracy':baseline_accuracy,
            'limits':'No player data; no latency, generalization to real games, or superiority claim.'}

if __name__=='__main__':print(json.dumps(experiment(),indent=2))
