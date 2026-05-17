from pathlib import Path
from schedulon.workers.executors.command import execute
def execute_file(path): return execute(Path(path).read_text())
