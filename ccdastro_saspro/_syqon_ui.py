"""Explicit settings for separately installed SyQon Studio."""
from copy import deepcopy
from pathlib import Path
from PyQt6.QtCore import QSettings
from PyQt6.QtWidgets import (QDialog,QVBoxLayout,QHBoxLayout,QFormLayout,QLabel,
    QLineEdit,QPushButton,QFileDialog,QComboBox,QDoubleSpinBox,QCheckBox,QDialogButtonBox)
from ._syqon import discover,syqon_catalog,SYQON_MODELS,build_arguments


class SettingsDialog(QDialog):
    def __init__(self, parameters=None, parent=None):
        super().__init__(parent)
        self.parameters=deepcopy(parameters or {'provider':'syqon','operation':'prism-essential','domain':'linear','amount':1.,'stars':True})
        self.setWindowTitle('SyQon Studio settings')
        root=QVBoxLayout(self)
        note=QLabel('Uses the installed Studio CLI. Sign in and install Required Items in Studio. Model listing shows support, not installed models or license access. Processing uses a temporary FITS copy; accept the candidate explicitly afterward.')
        note.setWordWrap(True);root.addWidget(note)
        row=QHBoxLayout();root.addLayout(row)
        store=QSettings('CCDASTRO','SASproWorkflow')
        self.path=QLineEdit(discover(self.parameters.get('executable') or store.value('syqon/executable','')))
        row.addWidget(self.path,1)
        browse=QPushButton('Browse CLI…');browse.clicked.connect(self.browse);row.addWidget(browse)
        scan=QPushButton('Check CLI / models');scan.clicked.connect(self.scan);root.addWidget(scan)
        form=QFormLayout();root.addLayout(form)
        self.model=QComboBox()
        for name,label in SYQON_MODELS.items():self.model.addItem(label,name)
        self.model.setCurrentIndex(max(0,self.model.findData(self.parameters['operation'])))
        form.addRow('Model',self.model)
        self.domain=QComboBox();self.domain.addItems(['linear','nonlinear']);self.domain.setCurrentText(self.parameters.get('domain','linear'));form.addRow('Input domain',self.domain)
        self.amount=QDoubleSpinBox();self.amount.setRange(0,1);self.amount.setSingleStep(.05);self.amount.setValue(self.parameters.get('amount',1));form.addRow('Application amount',self.amount)
        self.stars=QCheckBox('Generate a separate stars candidate');self.stars.setChecked(self.parameters.get('stars',True));form.addRow(self.stars)
        self.family=QComboBox();self.family.addItems(['aesthetics','classic']);self.family.setCurrentText(self.parameters.get('family','aesthetics'));form.addRow('Premium Parallax family',self.family)
        self.stages={}
        for key in ('correction','reduction','deblur'):
            box=QCheckBox();box.setChecked(self.parameters.get(key,True));form.addRow('Parallax '+key,box);self.stages[key]=box
        self.reduction=QDoubleSpinBox();self.reduction.setRange(0,10);self.reduction.setValue(self.parameters.get('reduction_level',3));form.addRow('Parallax reduction level',self.reduction)
        self.deblur=QDoubleSpinBox();self.deblur.setRange(0,1);self.deblur.setSingleStep(.05);self.deblur.setValue(self.parameters.get('deblur_strength',.5));form.addRow('Parallax deblur strength',self.deblur)
        self.editor_note=QLabel('Studio Editor: choose the model, ROI, display-only autostretch and intensity inside Studio. Done returns a candidate for explicit acceptance; Cancel keeps the previous result. No separate stars output is requested. Requires a Studio version advertising -gui.');self.editor_note.setWordWrap(True);root.addWidget(self.editor_note)
        self.status=QLabel();self.status.setWordWrap(True);root.addWidget(self.status)
        buttons=QDialogButtonBox(QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.Cancel);buttons.accepted.connect(self.commit);buttons.rejected.connect(self.reject);root.addWidget(buttons)
        self.model.currentIndexChanged.connect(self.refresh);self.refresh();self.resize(680,580)

    def browse(self):
        path,_=QFileDialog.getOpenFileName(self,'Select installed syqon-cli',self.path.text(),'Executable (*.exe);;All files (*)')
        if path:self.path.setText(path)

    def scan(self):
        try:
            models=syqon_catalog(self.path.text().strip());self.status.setText('Supported model IDs: '+', '.join(models));return models
        except Exception as error:self.status.setText(str(error));return None

    def refresh(self):
        model=self.model.currentData();parallax=model.startswith('parallax')
        gui=model=='studio-gui';self.domain.setEnabled(not gui);self.amount.setEnabled(not gui);self.editor_note.setVisible(gui)
        self.stars.setEnabled(model.startswith('axiom'));self.family.setEnabled(model=='parallax')
        for box in self.stages.values():box.setEnabled(parallax)
        self.reduction.setEnabled(parallax);self.deblur.setEnabled(parallax)

    def commit(self):
        try:
            path=self.path.text().strip()
            if not path or not Path(path).is_file():raise ValueError('Select the installed Studio syqon-cli executable.')
            p=dict(provider='syqon',operation=self.model.currentData(),domain=self.domain.currentText(),device='auto',amount=self.amount.value(),stars=self.stars.isChecked(),family=self.family.currentText(),reduction_level=self.reduction.value(),deblur_strength=self.deblur.value())
            p.update({key:box.isChecked() for key,box in self.stages.items()})
            build_arguments(p,'input.fits','result.fits','stars.fits')
            models=self.scan()
            if models is None:return
            if p['operation'] not in models:raise ValueError('This CLI does not advertise the selected model. Update Studio or choose a supported model.')
            QSettings('CCDASTRO','SASproWorkflow').setValue('syqon/executable',path)
            self.parameters=p;self.accept()
        except Exception as error:self.status.setText(str(error))
