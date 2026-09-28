#!/usr/bin/env python3
"""Reproduce CPU checks from an extracted package. Does not certify GPU behavior.
Usage: python validate_all.py [--out work/validation] [--skip-cpp]
"""
from __future__ import annotations
import argparse,json,pathlib,platform,shutil,subprocess,sys,time
ROOT=pathlib.Path(__file__).resolve().parent

def main()->int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=pathlib.Path,default=ROOT/'work/validation');p.add_argument('--skip-cpp',action='store_true');a=p.parse_args()
    out=a.out.resolve();out.mkdir(parents=True,exist_ok=True)
    report={'python':sys.version,'platform':platform.platform(),'gpu_execution':'NOT PERFORMED','checks':[]}
    def run(name,command):
        start=time.perf_counter();r=subprocess.run([str(x) for x in command],cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        (out/(name+'.txt')).write_text(r.stdout,encoding='utf8');report['checks'].append({'name':name,'exit':r.returncode,'seconds':time.perf_counter()-start})
        print(f'{name}: {"PASS" if r.returncode==0 else "FAIL"}',flush=True)
        if r.returncode:raise RuntimeError(f'{name} failed; see {out/(name+".txt")}')
    try:
        run('python_exercises',[sys.executable,'tests/test_exercises.py','--track','reference'])
        run('python_pipeline',[sys.executable,'tests/test_pipeline.py'])
        run('lesson_examples',[sys.executable,'code/python/run_examples.py'])
        run('asset_cooker',[sys.executable,'code/python/cook_assets.py','--source',ROOT/'assets/source','--out',out/'cooked'])
        run('bvh_experiment',[sys.executable,'code/python/bvh_reference.py','--output',out/'bvh_report.json'])
        if not a.skip_cpp:
            if not shutil.which('cmake'):raise RuntimeError('CMake unavailable. Install CMake/compiler or use --skip-cpp; skipped work is not passed.')
            build=out/'cpp_build'
            run('cmake_configure',['cmake','-S',ROOT/'code/cpp','-B',build,'-DCMAKE_BUILD_TYPE=Release'])
            run('cmake_build',['cmake','--build',build,'--config','Release','--parallel','2'])
            run('cpp_tests',['ctest','--test-dir',build,'-C','Release','--output-on-failure'])
            suffix='.exe' if sys.platform=='win32' else ''
            exe=build/('cpu_renderer'+suffix)
            if not exe.exists():exe=build/'Release'/('cpu_renderer'+suffix)
            m=json.loads((out/'cooked/assets_manifest.json').read_text())
            run('cpp_cooked_render',[exe,'--mesh',out/'cooked'/m['assets']['scene']['path'],'--output',out/'cooked_scene.ppm'])
            run('cpp_reference_render',[exe,'--output',out/'reference.ppm'])
            run('cpp_affine_render',[exe,'--affine','--output',out/'affine.ppm'])
        else:report['cpp']='SKIPPED by request'
        if shutil.which('node'):run('webgpu_syntax',['node','--check','code/webgpu/demo.js'])
        else:report['javascript_syntax']='SKIPPED; node unavailable'
        report['status']='PASS for executed checks only'
    except (OSError,RuntimeError) as e:
        report['status']='FAIL';report['error']=str(e);print(e,file=sys.stderr)
    finally:(out/'run_report.json').write_text(json.dumps(report,indent=2)+'\n')
    return 1 if report['status']=='FAIL' else 0
if __name__=='__main__':raise SystemExit(main())
