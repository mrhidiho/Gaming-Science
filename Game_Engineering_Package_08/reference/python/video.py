"""Educational raster model and PPM reference capture; NOT a standard display mode."""
import argparse
from pathlib import Path
from dataclasses import dataclass
@dataclass(frozen=True)
class Pixel:
    x:int;y:int;active:bool;frame_start:bool
class Raster:
    def __init__(self,hactive:int=64,htotal:int=80,vactive:int=48,vtotal:int=60):
        if not 0<hactive<=htotal or not 0<vactive<=vtotal:raise ValueError('invalid raster geometry')
        self.hactive,self.htotal,self.vactive,self.vtotal=hactive,htotal,vactive,vtotal
        self.x=self.y=0
    def step(self,reset:bool=False)->Pixel:
        if reset:self.x=self.y=0;return Pixel(0,0,False,False)
        p=Pixel(self.x,self.y,self.x<self.hactive and self.y<self.vactive,self.x==0 and self.y==0)
        self.x+=1
        if self.x==self.htotal:self.x=0;self.y=(self.y+1)%self.vtotal
        return p

def rgb(x:int,y:int,width:int=64)->tuple[int,int,int]:
    bars=((255,255,255),(255,255,0),(0,255,255),(0,255,0),(255,0,255),(255,0,0),(0,0,255),(0,0,0))
    if 20<=x<32 and 16<=y<28:return (255,128,0) # simple overlay
    return bars[min(7,8*x//width)]

def write_ppm(path:Path,width:int=64,height:int=48)->None:
    if width<1 or height<1:raise ValueError('positive image size required')
    path.parent.mkdir(parents=True,exist_ok=True)
    payload=bytes(channel for y in range(height) for x in range(width) for channel in rgb(x,y,width))
    path.write_bytes(f'P6\n{width} {height}\n255\n'.encode()+payload)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=Path('evidence/reference_frame.ppm'))
    a=p.parse_args();write_ppm(a.output);print(f'Wrote software reference, not RTL capture: {a.output}')
if __name__=='__main__':main()
