from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Generator

import yaml

from otoe.src.markdown import MarkdownParser


@dataclass
class ObsidianNote:
    project: str
    path: Path

    def get_yaml(self) -> dict[str, Any]:
        return MarkdownParser(self.path).parse()


class ObsidianParser:
    def __init__(
        self, obsidian_root: str | Path, target_path: str | Path | None = None
    ):
        obsidian_root = Path(obsidian_root)
        if not obsidian_root.exists():
            raise FileNotFoundError(f'Obsidian root {obsidian_root} does not exist')
        if not obsidian_root.is_dir():
            raise NotADirectoryError(
                f'Obsidian root {obsidian_root} is not a directory'
            )
        self.obsidian_root = obsidian_root

        target_path = Path(target_path or obsidian_root / 'target')
        target_path.mkdir(exist_ok=True)
        self.target_path: Path = target_path

    def get_notes(self) -> Generator[ObsidianNote, None, None]:
        for file in self.obsidian_root.iterdir():
            if file.is_dir():
                for note in file.iterdir():
                    if note.is_file() and note.suffix == '.md':
                        yield ObsidianNote(file.name, note)
                    else:
                        print(f'Note {note} is not a markdown file')
            elif file.is_file() and file.suffix == '.md':
                yield ObsidianNote('common', file)

    def get_files_by_project(self) -> dict[str, list[ObsidianNote]]:
        d = defaultdict(list)
        for note in self.get_notes():
            d[note.project].append(note)
        return d

    def get_project_yamls(self, notes: list[ObsidianNote]) -> list[dict[str, Any]]:
        res = []
        for note in notes:
            try:
                res.append(note.get_yaml())
            except Exception as e:
                print(f'Error parsing {note.path}: {e}')
            else:
                print(f'Successfully parsed {note.path}')
        return res

    def get_yamls_by_project(self) -> dict[str, list[dict[str, Any]]]:
        d = {}
        for project, notes in self.get_files_by_project().items():
            d[project] = self.get_project_yamls(notes)
        return d

    def write_yamls(self, yamls_by_project: dict[str, list[dict[str, Any]]]):
        matches = [
            {**note, 'project': project}
            for project, notes in yamls_by_project.items()
            for note in notes
        ]
        y = {'matches': matches}
        with open(self.target_path / 'matches.yaml', 'w') as f:
            yaml.dump(y, f)

    def parse(self):
        yamls_by_project = self.get_yamls_by_project()
        self.write_yamls(yamls_by_project)
