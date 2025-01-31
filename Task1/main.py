import sys
import json
import csv


def csv_to_json(rows):
    # 基本情報の辞書を作成
    base_type = {}
    idx_continue = 0

    # "規格" の行を見つけてヘッダーを取得
    for i, row in enumerate(rows):
        if row[0] == "規格":
            idx_continue = i
            headers = row[1:]  # 規格のレコードのインデックス1から取得
            break
        base_type[row[0]] = row[1]  # 辞書に追加

    # 詳細情報を作成
    ans = []
    for col in range(len(headers)):
        entry = {**base_type, "規格": headers[col], "詳細": {}}

        for row in rows[idx_continue + 1:]:
            key = row[0]
            # データの長さを規格の数に合わせる
            while len(row) < len(headers) + 1:
                row.append("")
            value = row[col + 1] if col + 1 < len(row) else ""
            if value and value != "-":  # 有効な値なら保存
                entry["詳細"][key] = value
            elif value == "":  # 空白の場合、左から一番後ろの有効な値を取得
                for prev_idx in range(col, 0, -1):  # col から左に探索
                    if row[prev_idx] and row[prev_idx] != "-":
                        entry["詳細"][key] = row[prev_idx]
                        break

        ans.append(entry)

    return ans


def main():
    reader = csv.reader(sys.stdin)
    rows = list(reader)
    out = csv_to_json(rows)
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()