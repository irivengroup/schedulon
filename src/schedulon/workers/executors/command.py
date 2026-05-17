from __future__ import annotations
import subprocess
def execute(command, env=None, timeout=3600):
    p=subprocess.run(['sh','-lc',command],env=env,capture_output=True,text=True,timeout=timeout)
    return {'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
