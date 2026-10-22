"""Independent SASpro workflow. Copyright 2026 Chuck Faranda / CCDASTRO, Inc.
Support: https://ccdastro.com/ . All rights reserved.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
SCRIPT_NAME='CCDASTRO Workflow 0.4.0'
SCRIPT_GROUP='CCDASTRO'

def run(ctx):
    from ccdastro_saspro._host import Host
    from ccdastro_saspro._ui import WorkflowDialog
    from PyQt6.QtWidgets import QMessageBox
    try:
        dialog=WorkflowDialog(Host(ctx),parent=ctx.app);dialog.exec()
    except Exception as e:
        ctx.log(f'CCDASTRO workflow: {e}')
        QMessageBox.warning(ctx.app,'CCDASTRO Workflow',str(e))
        raise
