from pathlib import Path
import os
class SecretProvider:
    def get(self, ref):
        if ref.startswith("env://"): return os.environ[ref.removeprefix("env://")]
        if ref.startswith("file://"): return Path(ref.removeprefix("file://")).read_text().strip()
        raise NotImplementedError("Enterprise secret manager hook")
