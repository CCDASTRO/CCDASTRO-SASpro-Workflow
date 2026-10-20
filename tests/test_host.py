import unittest
from copy import deepcopy
from types import SimpleNamespace
import numpy as np
from ccdastro_saspro._host import Host

class HostTests(unittest.TestCase):
    def test_native_targets_copy_and_restores_selection(self):
        class Context:
            def __init__(self):
                self.original=SimpleNamespace(image=np.full((4,5,3),.2,np.float32),metadata={'OBJECT':'test'})
                self.current=self.original;self.previous=object();self.app=SimpleNamespace(mdi=SimpleNamespace(setActiveSubWindow=lambda w:setattr(self,'restored',w)))
            def get_image(self):return self.current.image
            def active_document(self):return self.current
            def active_subwindow(self):return self.previous
            def list_image_views(self):return [('source',self.original)]
            def open_new_document(self,a,metadata,name):self.current=SimpleNamespace(image=a.copy(),metadata=deepcopy(metadata));return self.current
            def run_command(self,command,preset,**kwargs):
                self.assert_target=kwargs['target_doc'] is self.current
                self.current.image*=2
        ctx=Context();host=Host(ctx);a,meta=host.read();out,_=host.native(a,meta,{'command':'stat_stretch','preset':{}})
        self.assertTrue(ctx.assert_target);self.assertIs(ctx.restored,ctx.previous)
        np.testing.assert_allclose(out,.4);np.testing.assert_allclose(ctx.original.image,.2)
        with self.assertRaises(ValueError):host.native(a,meta,{'command':'export','preset':{}})
    def test_publish_metadata_is_copy(self):
        calls=[];ctx=SimpleNamespace(open_new_document=lambda a,metadata,name:calls.append((a,metadata,name)))
        host=Host(ctx);a=np.ones((3,4),np.float32);meta={'history':['source']};host.publish(a,meta)
        calls[0][1]['history'].append('new');self.assertEqual(meta['history'],['source'])

if __name__=='__main__':unittest.main()
