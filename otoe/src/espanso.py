import yaml
from pathlib import Path


class EspansoParser:

    def __init__(self, espanso_root: str | Path, target_path: str | Path | None = None):
        espanso_root = Path(espanso_root)
        if not espanso_root.exists():
            raise FileNotFoundError(f'Espanso root {espanso_root} does not exist')
        if not espanso_root.is_dir():
            raise NotADirectoryError(
                f'Espanso root {espanso_root} is not a directory'
            )
        self.espanso_root = espanso_root
        target_path = Path(target_path or espanso_root / 'target')

    def read_files(self):
        pass
        
