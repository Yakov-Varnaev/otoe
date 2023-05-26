import pytest

from otoe.src.markdown import MarkdownParser
from otoe.tests import data_path


class TestMarkdownParser:
    def test_open_nonexistent_file(self):
        with pytest.raises(FileNotFoundError):
            MarkdownParser(data_path / 'nonexistent.md')

    def test_open_file(self):
        parser = MarkdownParser(data_path / 'test_open_file.md')
        text = parser.open_file()
        assert not text.endswith('\n'), 'File should not end with newline.'
        assert text == 'test'

    @pytest.mark.parametrize(
        'filename',
        ['empty', 'no_text', 'no_yaml', 'no_yaml_wrap', 'several_separators'],
    )
    def test_check_layout(self, filename):
        parser = MarkdownParser(data_path / f'{filename}.md')
        text = parser.open_file()
        with pytest.raises(ValueError):
            parser.check_layout(text)

    def test_construct_dict_from_valid_text(self):
        parser = MarkdownParser(data_path / 'valid.md')
        text = '''
        text

        ====
        ```yaml
        trigger: :keyword
        ````
        '''
        d = parser.construct_yaml(text)
        assert d == {'trigger': ':keyword', 'replace': 'text'}

    def test_construct_yaml_no_trigger(self):
        parser = MarkdownParser(data_path / 'valid.md')
        text = '''
        text

        ====
        ```yaml
        notrigger: keyword
        ```
        '''
        with pytest.raises(ValueError):
            parser.construct_yaml(text)

    def test_valid(self):
        parser = MarkdownParser(data_path / 'valid.md')
        d = parser.parse()
        assert d == {'trigger': ':test', 'replace': 'test'}

    @pytest.mark.parametrize(
        'filename',
        ['empty', 'no_text', 'no_yaml', 'no_yaml_wrap', 'several_separators'],
    )
    def test_invalid(self, filename):
        parser = MarkdownParser(data_path / f'{filename}.md')
        with pytest.raises(ValueError):
            parser.parse()
