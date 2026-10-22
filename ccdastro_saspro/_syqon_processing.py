"""Cancellable SyQon processing with explicit candidate review afterward."""
from PyQt6.QtCore import QThread,pyqtSignal
from PyQt6.QtWidgets import QDialog,QVBoxLayout,QLabel,QPushButton,QProgressBar
from ._syqon import run_tool,StudioCancelled

class ToolWorker(QThread):
    completed=pyqtSignal(object);failed=pyqtSignal(str);cancelled=pyqtSignal(str)
    def __init__(self,data,parameters,parent=None,runner=run_tool):super().__init__(parent);self.data=data;self.parameters=parameters;self.runner=runner
    def run(self):
        try:self.completed.emit(self.runner(self.data,self.parameters,self.isInterruptionRequested))
        except InterruptedError as error:self.cancelled.emit(str(error))
        except Exception as error:self.failed.emit(str(error))

class ProcessingDialog(QDialog):
    def __init__(self,data,parameters,parent=None,runner=run_tool,title=None):
        super().__init__(parent);self.result=None;self.error='';self.was_cancelled=False;self.setWindowTitle(title or 'SyQon Studio processing');root=QVBoxLayout(self)
        self.label=QLabel('Working on a temporary copy. First use may require the provider’s model setup.');self.label.setWordWrap(True);root.addWidget(self.label)
        if parameters.get('operation')=='studio-gui':self.label.setText('Opening SyQon Studio editor on a temporary copy. Choose model, ROI and intensity there. Click Done to review the candidate here, or Cancel to keep the previous result.')
        bar=QProgressBar();bar.setRange(0,0);root.addWidget(bar);self.cancel=QPushButton('Cancel processing');self.cancel.clicked.connect(self.stop);root.addWidget(self.cancel)
        self.worker=ToolWorker(data,parameters,self,runner);self.worker.completed.connect(self.complete);self.worker.failed.connect(self.fail);self.worker.cancelled.connect(self.cancelled);self.resize(520,170)
    def stop(self):self.worker.requestInterruption();self.cancel.setEnabled(False);self.label.setText('Cancelling; waiting for the external process to stop…')
    def complete(self,result):self.result=result;super().done(QDialog.DialogCode.Accepted)
    def cancelled(self,message):self.was_cancelled=True;self.error=message;super().done(QDialog.DialogCode.Rejected)
    def fail(self,error):self.error=error;super().done(QDialog.DialogCode.Rejected)
    def done(self,code):
        if self.worker.isRunning():self.stop();return
        super().done(code)
    def execute(self):
        self.worker.start();self.exec();self.worker.wait()
        if self.was_cancelled:raise StudioCancelled(self.error)
        if self.result is None:raise RuntimeError(self.error or 'External-tool operation cancelled.')
        return self.result
