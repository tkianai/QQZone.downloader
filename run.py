

import os
import os.path as osp
import argparse
from core import BackupEngine


def parse_args():
    parser = argparse.ArgumentParser(description="Back up for QQ Zone")
    parser.add_argument('--account', type=str, help="QQ account")
    parser.add_argument('--save', type=str, default='./QQZone', help="Directory to save data")
    parser.add_argument('--visual', action='store_true', help="Not use headless mode")

    args = parser.parse_args()
    args.save = osp.join(args.save, args.account)
    if not osp.exists(args.save):
        os.makedirs(args.save)

    return args


def main():
    args = parse_args()
    engine = BackupEngine(args.account, save_dir=args.save, headless=args.visual)
    try:
        engine.download_images()
        engine.download_posts()
        engine.download_leaving_message()
        engine.download_diary()
    except Exception as e:
        print(e)
    finally:
        engine.finished()


if __name__ == "__main__":
    main()
