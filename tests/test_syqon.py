import os
os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
import unittest,tempfile,json
from pathlib import Path
from unittest.mock import patch
import numpy as np
from astropy.io import fits
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication
from ccdastro_saspro._syqon import build_arguments,syqon_catalog,run_tool,SYQON_MODELS
from ccdastro_saspro._ui import WorkflowDialog
from ccdastro_saspro._core import Step
from ccdastro_saspro._syqon_ui import SettingsDialog
from ccdastro_saspro._syqon_processing import ProcessingDialog

class Host:
    title='Seti Astro Suite Pro'
    def read(self):return np.full((4,5,3),.3,np.float32),{'original':'retained'}

class SyQonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.app=QApplication.instance() or QApplication([])
    def test_model_domains_stages_and_no_weight_paths(self):
        self.assertEqual(len(SYQON_MODELS),12)
        for model in ['deep-gradient','prism-essential','prism-advanced','prism-legacy-v2']:
            with self.assertRaises(ValueError):build_arguments({'provider':'syqon','operation':model,'domain':'nonlinear'},'i','o')
        for settings in [dict(operation='unknown'),dict(operation='parallax-nano',correction=False,reduction=False,deblur=False),dict(operation='prism-max',amount=float('nan')),dict(operation='prism-max',device='cpu')]:
            with self.assertRaises(ValueError):build_arguments(dict(provider='syqon',**settings),'i','o')
        args=build_arguments({'provider':'syqon','operation':'axiom-mini','domain':'linear'},'in','out','stars')
        self.assertIn('--stars-output',args);self.assertIn('auto',args);self.assertNotIn('--gui',args);self.assertNotIn('--model-path',args)
        args=build_arguments({'provider':'syqon','operation':'parallax-nano'},'i','o');self.assertNotIn('--family',args)
    def test_catalog_filters_and_verifies_cli(self):
        with patch('ccdastro_saspro._syqon.process_args',side_effect=[(0,'SyQon Studio 1.1.9',''),(0,'axiom-mini free\nunknown paid\ndeep-gradient free',''),(0,'headless help','')]):
            self.assertEqual(syqon_catalog('cli'),['axiom-mini','deep-gradient'])
        with patch('ccdastro_saspro._syqon.process_args',return_value=(0,'different application','')):
            with self.assertRaises(RuntimeError):syqon_catalog('cli')
    def test_entitlement_and_cancellation_preserve_source(self):
        data=Host().read()[0];before=data.copy()
        with patch('ccdastro_saspro._syqon.syqon_catalog',return_value=['axiom-mini']),patch('ccdastro_saspro._syqon.process_args',return_value=(4,'','denied')):
            with self.assertRaisesRegex(RuntimeError,'Sign in'):run_tool(data,{'provider':'syqon','operation':'axiom-mini','executable':__file__})
        with patch('ccdastro_saspro._syqon.syqon_catalog',side_effect=InterruptedError('Cancelled')):
            with self.assertRaises(InterruptedError):run_tool(data,{'provider':'syqon','operation':'axiom-mini','executable':__file__})
        np.testing.assert_array_equal(data,before)
    def test_output_orientation_and_metadata_independent_pixels(self):
        data=np.arange(60,dtype=np.float32).reshape(4,5,3)/100;before=data.copy()
        def process(exe,args,cancel):
            output=Path(args[-1]);header=fits.Header();header['ROWORDER']='TOP-DOWN'
            fits.PrimaryHDU(np.flip(np.moveaxis(data,-1,0),axis=-2),header).writeto(output)
            return 0,str(output),''
        with patch('ccdastro_saspro._syqon.syqon_catalog',return_value=['prism-essential']),patch('ccdastro_saspro._syqon.process_args',side_effect=process):
            result=run_tool(data,{'provider':'syqon','operation':'prism-essential','executable':__file__})
        np.testing.assert_array_equal(result['image'],before);np.testing.assert_array_equal(data,before)
    def test_missing_stars_never_returns_candidate(self):
        data=Host().read()[0]
        def process(exe,args,cancel):
            fits.PrimaryHDU(np.zeros((3,4,5),np.float32)).writeto(args[-1]);return 0,args[-1],''
        with patch('ccdastro_saspro._syqon.syqon_catalog',return_value=['axiom-mini']),patch('ccdastro_saspro._syqon.process_args',side_effect=process):
            with self.assertRaisesRegex(RuntimeError,'stars output'):run_tool(data,{'provider':'syqon','operation':'axiom-mini','executable':__file__})
    def test_bad_geometry_never_returns_candidate(self):
        data=Host().read()[0];before=data.copy()
        def process(exe,args,cancel):
            fits.PrimaryHDU(np.zeros((3,2,2),np.float32)).writeto(args[-1]);return 0,args[-1],''
        with patch('ccdastro_saspro._syqon.syqon_catalog',return_value=['prism-essential']),patch('ccdastro_saspro._syqon.process_args',side_effect=process):
            with self.assertRaisesRegex(ValueError,'dimensions'):run_tool(data,{'provider':'syqon','operation':'prism-essential','executable':__file__})
        np.testing.assert_array_equal(data,before)
    def test_pending_stars_only_kept_on_acceptance(self):
        w=WorkflowDialog(Host());w.steps=[Step('syqon',{'provider':'syqon','operation':'axiom-mini'})];w.refresh();w.list.setCurrentRow(0)
        result={'image':np.full((4,5,3),.2,np.float32),'stars':np.full((4,5,3),.1,np.float32),'method':'add'}
        with patch('ccdastro_saspro._syqon_processing.ProcessingDialog.execute',return_value=result):w.preview_step()
        self.assertIsNone(w.generated_stars);np.testing.assert_array_equal(w.session.current,Host().read()[0])
        w.discard();self.assertIsNone(w.pending_stars);self.assertIsNone(w.generated_stars)
        w.list.setCurrentRow(0)
        with patch('ccdastro_saspro._syqon_processing.ProcessingDialog.execute',return_value=result):w.preview_step()
        w.accept_candidate();self.assertTrue(w.use_stars.isEnabled());self.assertEqual(w.session.metadata['original'],'retained')
        self.assertEqual(w.session.audit[0]['kind'],'syqon');np.testing.assert_array_equal(w.session.source,Host().read()[0])
        w.update_controller.shutdown();w.close()
    def test_presets_do_not_store_executable(self):
        w=WorkflowDialog(Host());w.steps=[Step('syqon',{'provider':'syqon','operation':'prism-essential','executable':'private-local-path.exe'})]
        with tempfile.TemporaryDirectory() as td:
            path=str(Path(td)/'preset.json')
            with patch('ccdastro_saspro._ui.QFileDialog.getSaveFileName',return_value=(path,'')):w.save_preset()
            saved=json.loads(Path(path).read_text());self.assertNotIn('executable',saved['steps'][0]['parameters'])
            with patch('ccdastro_saspro._ui.QFileDialog.getOpenFileName',return_value=(path,'')):w.load_preset()
            self.assertEqual(w.steps[0].kind,'syqon')
        w.update_controller.shutdown();w.close()
    def test_settings_validation_and_model_catalog(self):
        with patch('ccdastro_saspro._syqon_ui.QSettings') as store,patch('ccdastro_saspro._syqon_ui.syqon_catalog',return_value=['prism-essential']):
            store.return_value.value.return_value=__file__
            d=SettingsDialog();d.domain.setCurrentText('nonlinear');d.commit();self.assertIn('linear',d.status.text())
            d.domain.setCurrentText('linear');d.commit();self.assertEqual(d.parameters['operation'],'prism-essential');self.assertNotIn('executable',d.parameters);d.close()
    def test_processing_cancel_stops_worker(self):
        import time
        def runner(data,parameters,cancel):
            deadline=time.monotonic()+2
            while time.monotonic()<deadline:
                if cancel():raise InterruptedError('Cancelled without acceptance')
                time.sleep(.002)
            raise RuntimeError('Cancellation did not arrive')
        d=ProcessingDialog(Host().read()[0],{},runner=runner)
        QTimer.singleShot(10,d.stop)
        with self.assertRaisesRegex(InterruptedError,'Cancelled'):d.execute()
        self.assertFalse(d.worker.isRunning())

    def test_editor_arguments_and_controls(self):
        args=build_arguments(dict(provider='syqon',operation='studio-gui',amount=float('nan'),stars=True),'in.fits','out.fits','stars.fits')
        self.assertEqual(args,['-gui','in.fits','out.fits'])
        with self.assertRaises(ValueError):build_arguments(dict(provider='syqon',operation='studio-gui'),'i.fits','o.tif')
        d=SettingsDialog(dict(provider='syqon',operation='studio-gui'))
        self.assertFalse(d.amount.isEnabled());self.assertFalse(d.domain.isEnabled());self.assertFalse(d.stars.isEnabled());d.close()
    def test_editor_discovery_requires_advertised_support(self):
        for helptext,available in [('usage: -gui [options] INPUT OUTPUT',True),('headless only',False),('--gui is not supported',False)]:
            with patch('ccdastro_saspro._syqon.process_args',side_effect=[(0,'SyQon Studio 1.2',''),(0,'prism-essential included',''),(0,helptext,'')]):
                self.assertEqual('studio-gui' in syqon_catalog('cli'),available)
    def test_editor_cancel_and_done_candidate(self):
        data=Host().read()[0];before=data.copy();settings=dict(provider='syqon',operation='studio-gui',executable=__file__)
        with patch('ccdastro_saspro._syqon.syqon_catalog',return_value=['studio-gui']),patch('ccdastro_saspro._syqon.process_args',return_value=(20,'','')):
            with self.assertRaises(InterruptedError):run_tool(data,settings)
        def done(exe,args,cancel):
            self.assertEqual(args[0],'-gui');fits.PrimaryHDU(np.moveaxis(data*.5,-1,0)).writeto(args[-1]);return 0,args[-1],''
        with patch('ccdastro_saspro._syqon.syqon_catalog',return_value=['studio-gui']),patch('ccdastro_saspro._syqon.process_args',side_effect=done):result=run_tool(data,settings)
        np.testing.assert_array_equal(data,before);np.testing.assert_allclose(result['image'],data*.5);self.assertIsNone(result['stars']);self.assertEqual(result['provenance']['domain'],'editor-managed')
    def test_editor_workflow_cancel_is_quiet(self):
        w=WorkflowDialog(Host());w.update_controller.shutdown();w.steps=[Step('syqon',dict(provider='syqon',operation='studio-gui'))];w.refresh();w.list.setCurrentRow(0)
        with patch.object(w,'error') as error,patch('ccdastro_saspro._syqon_processing.ProcessingDialog.execute',side_effect=InterruptedError('Editor cancelled')):w.preview_step()
        error.assert_not_called();self.assertIsNone(w.pending);self.assertFalse(w.accept_button.isEnabled());np.testing.assert_array_equal(w.session.current,Host().read()[0]);w.close()

    def test_editor_done_requires_acceptance_without_second_blend(self):
        w=WorkflowDialog(Host());w.update_controller.shutdown();w.steps=[Step('syqon',dict(provider='syqon',operation='studio-gui',amount=.1))];w.refresh();w.list.setCurrentRow(0)
        output=Host().read()[0]*.4
        result=dict(image=output,stars=None,method='add',provenance=dict(mode='gui',domain='editor-managed'))
        with patch('ccdastro_saspro._syqon_processing.ProcessingDialog.execute',return_value=result):w.preview_step()
        np.testing.assert_array_equal(w.session.current,Host().read()[0]);np.testing.assert_array_equal(w.pending,output)
        w.accept_candidate();np.testing.assert_array_equal(w.session.current,output);np.testing.assert_array_equal(w.session.source,Host().read()[0]);self.assertEqual(w.session.metadata['original'],'retained');self.assertEqual(w.session.audit[-1]['parameters']['studio_run']['mode'],'gui');w.close()
    def test_editor_probe_timeout_keeps_headless_models(self):
        with patch('ccdastro_saspro._syqon.process_args',side_effect=[(0,'SyQon Studio 1.1.9',''),(0,'prism-essential included',''),TimeoutError('query timed out')]):
            self.assertEqual(syqon_catalog('cli'),['prism-essential'])
