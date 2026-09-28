"""Deterministic teaching traces; no sensors, devices or downloaded telemetry."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent

def main():
    power={'times_s':list(range(121)), 'power_w':[60]*60+[50]*60,
           'completed_frames':[60]*60+[45]*60}
    inputs=[round(i*1000/60,9) for i in range(180)]
    presents=[round(t+1000/30+(i//60)*(1000/60),9) for i,t in enumerate(inputs)]
    latency={'input_ms':inputs,'present_ms':presents,'timestamp_kind':'synthetic_present'}
    for name,value in [('synthetic_power_trace.json',power),('synthetic_latency_trace.json',latency)]:
        (ROOT/name).write_text(json.dumps(value,indent=2)+'\n')
    provenance={'kind':'synthetic teaching data','randomness':'none; deterministic formulas',
        'power':'120 one-second intervals. First 60: 60 W and 60 accepted frames each. Last 60: 50 W and 45 frames each. Power is interval-average.',
        'latency':'180 inputs at 60 Hz. Software markers start two intervals behind input; an extra interval of queue age is added at inputs 60 and 120. One synthetic clock, no panel model.',
        'limits':'Not measurements, not battery-life predictions, not input-to-photon observations.'}
    (ROOT/'SYNTHETIC_PROVENANCE.json').write_text(json.dumps(provenance,indent=2)+'\n')
    print('Wrote two synthetic traces and provenance.')

if __name__=='__main__': main()
