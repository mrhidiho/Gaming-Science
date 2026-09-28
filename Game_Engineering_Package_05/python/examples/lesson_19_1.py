from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from python.reference.lab_19_1 import FrameDecoder,encode_frame
wire=encode_frame(b"one")+encode_frame(b"two")
decoder=FrameDecoder();result=[]
for chunk in [wire[:2],wire[2:6],wire[6:]]:
    result.extend(decoder.feed(chunk))
decoder.finish()
print(result)
