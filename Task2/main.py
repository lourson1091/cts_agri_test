import sys
import numpy as np

# 野菜の重量の正規分布 (平均, 標準偏差)
WEIGHT_DISTRIBUTION = {
    "c": (100, 20),  # きゅうり
    "t": (150, 15),  # トマト
    "e": (180, 18)  # なすび
}

# 規格表 (下限, 上限)
STANDARDS = {
    "c": [(51, 80, "S"), (81, 120, "M"), (121, 150, "L")],
    "t": [(101, 135, "S"), (136, 165, "M"), (166, 200, "L")],
    "e": [(161, 200, "M"), (201, 240, "L")]
}

# 価格表
PRICES = {
    "c": {"S": 30, "M": 60, "L": 60, "規格外": 0},
    "t": {"S": 50, "M": 100, "L": 150, "規格外": 10},
    "e": {"M": 120, "L": 180, "規格外": 0}
}


def classify_and_price(vegetable: str, count: int):
    """
    野菜の個数に対して重さを正規分布からランダムに生成し、
    規格を決定して価格を計算する。
    """
    mean, std = WEIGHT_DISTRIBUTION[vegetable]
    weights = np.random.normal(mean, std, count).astype(int)  # 正規分布で発生させて重さを整数化
    total_price = 0

    for w in weights:
        size = "規格外"
        for min_w, max_w, label in STANDARDS.get(vegetable, []):
            if min_w <= w <= max_w:
                size = label
                break
        total_price += PRICES[vegetable][size]

    return total_price


def randomized_price(c: int, t: int, e: int) -> int:
    """
    500円以上5000円以下の価格を生成する。

    :param c: きゅうりの個数
    :param t: トマトの個数
    :param e: なすびの個数
    :return: 制約を満たした価格
    """
    while True:
        total_price = classify_and_price("c", c) + classify_and_price("t", t) + classify_and_price("e", e)
        if 500 <= total_price <= 5000:
            return total_price


def main():
    inputs = [list(map(int, line.split())) for line in sys.stdin.read().strip().split("\n")]

    # 各袋の合計価格を計算
    bag_prices = [randomized_price(c, t, e) for c, t, e in inputs]
    # 金額上限を出力（最大価格）
    print(max(bag_prices))


if __name__ == "__main__":
    main()
