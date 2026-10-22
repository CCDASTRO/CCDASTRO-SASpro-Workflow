"""Local process and scientific FITS interchange helpers; no vendor assets."""
from pathlib import Path
import os,subprocess
import numpy as np
from ._core import image_array

def process_args(executable,args,cancel=lambda:False,timeout=None):
    flags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0
    process=subprocess.Popen([str(executable),*args],cwd=str(Path(executable).parent),stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=False,text=True,encoding='utf-8',errors='replace',creationflags=flags)
    import time
    started=time.monotonic()
    try:
        while True:
            if cancel():raise InterruptedError('External-tool operation cancelled. Candidate was not accepted.')
            if timeout is not None and time.monotonic()-started>timeout:raise TimeoutError('The external tool did not respond to the query.')
            try:
                stdout,stderr=process.communicate(timeout=.2)
                return process.returncode,stdout,stderr
            except subprocess.TimeoutExpired:pass
    finally:
        if process.poll() is None:
            process.terminate()
            try:process.communicate(timeout=5)
            except subprocess.TimeoutExpired:process.kill();process.communicate()

def read_result(path,expected_shape):
    from astropy.io import fits
    with fits.open(path,memmap=False) as hdus:
        data=np.asarray(hdus[0].data,dtype=np.float32)
        if str(hdus[0].header.get('ROWORDER','BOTTOM-UP')).upper()=='TOP-DOWN':data=np.flip(data,axis=-2)
        if data.ndim==3 and data.shape[0] in (1,3):data=data[0] if data.shape[0]==1 else np.moveaxis(data,0,-1)
        result=image_array(data)
    if result.shape!=expected_shape:raise ValueError('External-tool output dimensions do not match the input.')
    return result

