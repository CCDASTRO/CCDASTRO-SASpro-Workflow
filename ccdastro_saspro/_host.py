"""Seti Astro Suite Pro adapter using the documented ScriptContext API."""
from copy import deepcopy
from pathlib import Path
import numpy as np
from ._core import image_array

class Host:
    title='Seti Astro Suite Pro'
    native_commands={'stat_stretch','remove_green','abe','graxpert','background_neutral',
        'white_balance','remove_stars','cosmic_clarity','syqontools','rcastro','texture_clarity',
        'wavescale_hdr','clahe','convo','satchroma','curves','ghs','levels','sfcc','crop'}
    def __init__(self,ctx): self.api=ctx
    def read(self):
        a=self.api.get_image()
        if a is None: raise ValueError('Open an image first.')
        doc=self.api.active_document()
        return image_array(a),deepcopy(getattr(doc,'metadata',{}) or {})
    def publish(self,data,metadata,name='CCDASTRO result'):
        return self.api.open_new_document(image_array(data),metadata=deepcopy(metadata),name=name)
    def save(self,data,metadata,path):
        from ._io import save_fits
        return save_fits(path,data,metadata)
    def native(self,data,metadata,parameters):
        command=parameters.get('command'); preset=parameters.get('preset',{})
        if command not in self.native_commands or not isinstance(preset,dict):
            raise ValueError('Choose a supported SASpro image-processing command with a JSON preset object.')
        previous=self.api.active_subwindow()
        before={id(doc) for _,doc in self.api.list_image_views()}
        self.api.open_new_document(image_array(data),metadata=deepcopy(metadata),name='CCDASTRO native working copy')
        scratch=self.api.active_subwindow()
        try:
            doc=self.api.active_document()
            if doc is None or id(doc) in before: raise RuntimeError('SASpro did not activate a separate working copy.')
            self.api.run_command(command,preset,target_doc=doc)
            result=image_array(doc.image);meta=deepcopy(getattr(doc,'metadata',{}) or {})
            return result,meta
        finally:
            # Leave only our temporary working document open on an error if the host
            # cannot close it without a save prompt. Never close a pre-existing view.
            if previous is not None:
                mdi=getattr(self.api.app,'mdi',None)
                if mdi is not None and hasattr(mdi,'setActiveSubWindow'): mdi.setActiveSubWindow(previous)
    def log(self,message): self.api.log(message)
