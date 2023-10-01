import os

from otoe.src.obsidian import ObsidianParser


def main():
    obsidian_root = os.getenv('OBSIDIAN_ROOT')
    if not obsidian_root:
        raise Exception('OBSIDIAN_ROOT is not set')
    yaml_dir = os.getenv('YAML_DIR')
    parser = ObsidianParser(obsidian_root, yaml_dir)
    parser.parse()


if __name__ == '__main__':
    main()
