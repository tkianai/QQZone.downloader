

import os
import os.path as osp
import argparse
from core import BackupEngine


def parse_args():
    parser = argparse.ArgumentParser(description="Back up for QQ Zone")
    parser.add_argument('--account', type=str, default="593014895", help="QQ account")
    parser.add_argument('--save', type=str, default='./results', help="Directory to save data")

    args = parser.parse_args()
    if not osp.exists(args.save):
        os.makedirs(args.save)

    return args


def main():
    args = parse_args()
    engine = BackupEngine(args.account, save_dir=args.save, headless=False)
    try:
        engine.download_images()
        engine.download_posts()
    except Exception as e:
        print(e)
    finally:
        engine.finished()


if __name__ == "__main__":
    main()
