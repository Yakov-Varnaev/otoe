import os

from otoe.src.obsidian import ObsidianParser


def main():
    obsidian_root = os.getenv('OBSIDIAN_ROOT')
    if not obsidian_root:
        raise Exception('OBSIDIAN_ROOT is not set')
    parser = ObsidianParser(obsidian_root)
    parser.parse()


if __name__ == '__main__':
    main()
