import argparse
import json
import subprocess
import datetime
import os

from dotenv import load_dotenv

load_dotenv()

TEMPLATE_FILES = {
    "train": "templates/kernel-metadata.train.template.json",
    "inference": "templates/kernel-metadata.inference.template.json",
}


def get_git_info():
    # ハッシュ取得
    hash_id = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode().strip()
    # 変更があるか（Dirtyか）チェック
    is_dirty = bool(subprocess.check_output(['git', 'status', '--porcelain']).decode().strip())
    return hash_id, is_dirty


def update_and_push(mode):
    hash_id, is_dirty = get_git_info()
    tag = f"{hash_id}{'-dirty' if is_dirty else ''}"
    kaggle_username = os.environ["KAGGLE_USERNAME"]
    today = datetime.date.today()

    # テンプレートの読み込み
    template_file = TEMPLATE_FILES[mode]
    with open(template_file, 'r') as f:
        template = f.read()

    # プレースホルダーを置換
    rendered = template.replace("{username}", kaggle_username)
    rendered = rendered.replace("{tag}", tag)
    rendered = rendered.replace("{date}", str(today))

    meta = json.loads(rendered)

    # kernel-metadata.json として書き出し
    with open('kernel-metadata.json', 'w') as f:
        json.dump(meta, f, indent=4)

    print(f"Mode: {mode}")
    print(f"Pushing kernel: {meta['id']}...")
    subprocess.run(['kaggle', 'kernels', 'push', '-p', './'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Push kernel to Kaggle")
    parser.add_argument("--mode", choices=list(TEMPLATE_FILES.keys()), required=True,
                        help="実行モード: train or inference")
    args = parser.parse_args()
    update_and_push(args.mode)
