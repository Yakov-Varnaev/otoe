import os
from pathlib import Path


def main():
    obsidian_root = os.getenv('OBSIDIAN_ROOT')
    if not obsidian_root:
        raise ValueError
    obsidian_root = Path(obsidian_root)

    # get all md files from obsidian root

    # for each file, parse it to a new obsidian file
    # which wraps yaml part in a code block

    for file in obsidian_root.glob('**/*.md'):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()

        text, yaml = content.split('====')
        yaml = yaml.strip()
        if yaml.startswith('```yaml'):
            continue
        yaml = f'```yaml\n{yaml}\n```'
        content = f'{text}====\n{yaml}'

        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)


if __name__ == '__main__':
    main()
