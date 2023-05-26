from collections import defaultdict

import pytest
import yaml

from otoe.src.obsidian import ObsidianNote, ObsidianParser
from otoe.tests import data_path, obsidian_root


@pytest.fixture
def obsidian_notes():
    return [
        ObsidianNote(project='project1', path=obsidian_root / 'project1' / 'valid2.md'),
        ObsidianNote(project='project1', path=obsidian_root / 'project1' / 'valid.md'),
        ObsidianNote(project='common', path=obsidian_root / 'valid.md'),
        ObsidianNote(project='project2', path=obsidian_root / 'project2' / 'note.md'),
    ]


@pytest.fixture
def notes_by_project(obsidian_notes):
    d = defaultdict(list)
    for note in obsidian_notes:
        d[note.project].append(note)
    return {**d}


@pytest.fixture
def project1_notes(notes_by_project):
    return notes_by_project['project1']


class TestObsidian:
    def test_invalid_obsidian_root(self):
        with pytest.raises(FileNotFoundError):
            ObsidianParser(data_path / 'non_existing_path')

    def test_non_directory_obsidian_root(self):
        with pytest.raises(NotADirectoryError):
            ObsidianParser(data_path / 'empty.md')

    def test_get_notes(self, obsidian_notes):
        parser = ObsidianParser(obsidian_root)
        assert list(parser.get_notes()) == obsidian_notes

    def test_get_file_by_project(self, notes_by_project):
        parser = ObsidianParser(obsidian_root)
        assert parser.get_files_by_project() == notes_by_project

    def test_get_project_yamls(self, project1_notes):
        parser = ObsidianParser(obsidian_root)
        expected = [
            {'trigger': ':test', 'replace': 'test'},
            {'trigger': ':test', 'replace': 'test'},
        ]
        assert parser.get_project_yamls(project1_notes) == expected

    def test_get_yamls_by_project(self):
        parser = ObsidianParser(obsidian_root)
        expected = {
            'project1': [
                {'trigger': ':test', 'replace': 'test'},
                {'trigger': ':test', 'replace': 'test'},
            ],
            'project2': [{'trigger': ':test', 'replace': 'test'},],
            'common': [{'trigger': ':test', 'replace': 'test'},],
        }
        assert parser.get_yamls_by_project() == expected

    def test_write_yamls(self):
        parser = ObsidianParser(obsidian_root)
        parser.write_yamls(parser.get_yamls_by_project())
        match_path = obsidian_root / 'target' / 'matches.yml'
        assert match_path.exists()
        assert match_path.is_file()
        with open(match_path, 'r') as f:
            assert yaml.safe_load(f) == {
                'matches': [
                    {'trigger': ':test', 'replace': 'test', 'project': 'project1'},
                    {'trigger': ':test', 'replace': 'test', 'project': 'project1'},
                    {'trigger': ':test', 'replace': 'test', 'project': 'common'},
                    {'trigger': ':test', 'replace': 'test', 'project': 'project2'},
                ]
            }
