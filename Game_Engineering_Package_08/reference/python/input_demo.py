"""Write ideal sampled-input examples to CSV, with no plotting dependency."""
import argparse,csv,math
from pathlib import Path
from reference.python.circuits import lowpass,quantize

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path('evidence/input_samples.csv'))
    args=parser.parse_args();args.output.parent.mkdir(parents=True,exist_ok=True)
    fs=1000; signal=[1.65+.8*math.cos(2*math.pi*300*n/fs) for n in range(100)]
    filtered=lowpass(signal,.25,1.65)
    with args.output.open('w',newline='') as f:
        writer=csv.writer(f);writer.writerow(['sample','seconds','cos_300','cos_700','voltage','code_12bit','filtered_voltage'])
        for n,(v,y) in enumerate(zip(signal,filtered)):
            writer.writerow([n,n/fs,math.cos(2*math.pi*300*n/fs),math.cos(2*math.pi*700*n/fs),v,quantize(v),y])
    print(f'Wrote analytical samples: {args.output}')
if __name__=='__main__':main()
