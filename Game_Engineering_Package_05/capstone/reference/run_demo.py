from pathlib import Path
import argparse
import json
import sys
import tempfile
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from capstone.reference.service import Service
from capstone.reference.gateway import Gateway,exchange

def main():
    parser=argparse.ArgumentParser(description="Run a finite loopback ForgeQueue demonstration")
    parser.add_argument("--native",type=Path,required=True,help="path to locally built native_worker")
    args=parser.parse_args()
    request=json.dumps({"version":1,"id":"demo-1","operation":"sum_squares","values":[2,3,4]}).encode()
    with tempfile.TemporaryDirectory(prefix="forge-demo-") as folder:
        with Service(Path(folder)/"results.sqlite",args.native) as service:
            with Gateway(service) as gateway:
                first=exchange(gateway.address,request,split=True)
                second=exchange(gateway.address,request)
                print(json.dumps(first,sort_keys=True))
                print("same response:",first==second)
                print("stored rows:",service.store.count())
                if gateway.errors or first.get("result")!=29 or first!=second or service.store.count()!=1:
                    return 1
    return 0

if __name__=="__main__":
    raise SystemExit(main())
