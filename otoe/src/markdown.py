from pathlib import Path
from typing import Any

import yaml

from otoe.src.constants import SEPARATOR


class MarkdownParser:
    """
    This class is responsible for parsing markdown files into espanso yamls.

    It also checks that the markdown has expected layout:

    Text of note
    ====
    ```yaml
    trigger: :keyword
    vars:
        ...
    ```
    """

    def __init__(self, path: str | Path):
        self.path = Path(path)
        if not self.path.exists():
            raise FileNotFoundError(f'File {self.path} does not exist.')

    def open_file(self):
        with open(self.path, 'r', encoding='utf-8') as file:
            return file.read().strip()

    def check_layout(self, text: str):
        """
        Check that the markdown file has expected layout.

        Expected layout:

        Text of note
        ====
        ```yaml
        trigger: :keyword
        vars:
            ...
        ```
        """
        split_text = text.split(SEPARATOR)
        if len(split_text) < 2:
            raise ValueError(
                f'Markdown file {self.path} either does not have separator '
                f'or does not have yaml or text block. Separator: {SEPARATOR}'
            )
        if len(split_text) > 2:
            raise ValueError(
                'Markdown file has more than one separator. '
                'Please avoid use of separator in the text of the note.'
            )
        note_text = split_text[0].strip()
        if not note_text:
            raise ValueError('Markdown file does not have text block.')
        yaml_text = split_text[1].strip()
        if not yaml_text.startswith('```yaml'):
            raise ValueError(
                'Markdown file does not have yaml block or it does not start with "```yaml".'
            )
        if not yaml_text.endswith('```'):
            raise ValueError(
                'Markdown file does not have yaml block or it does not end with "```".'
            )

    def construct_yaml(self, text) -> dict:
        """
        Construct yaml from markdown yaml block.

        This method is responsible for adding the `name` field to the yaml block.
        """

        split_text = text.split(SEPARATOR)
        note_text, yaml_text = split_text[0].strip(), split_text[1].strip()
        yaml_text = yaml_text.replace('\t', '    ').strip('```yaml').strip('```')
        yaml_data = yaml.load(yaml_text, Loader=yaml.FullLoader)
        if 'trigger' not in yaml_data:
            raise ValueError('Make sure you have a `trigger` field in your yaml block.')
        yaml_data['replace'] = note_text

        return yaml_data

    def parse(self) -> dict[str, Any]:
        """
        Parse markdown file into espanso yaml.
        """

        text = self.open_file()
        self.check_layout(text)
        yaml_data = self.construct_yaml(text)

        return yaml_data
