# JCZQ Reverse Odds Engine V6.0
# Direction Engine
# 方向引擎


def calculate_probability(win, draw, lose):

    # 赔率转换概率
    win_p = 1 / win
    draw_p = 1 / draw
    lose_p = 1 / lose

    total = win_p + draw_p + lose_p

    # 归一化
    return {
        "win_probability": round(win_p / total * 100, 2),
        "draw_probability": round(draw_p / total * 100, 2),
        "lose_probability": round(lose_p / total * 100, 2)
    }



def analyze_direction(win, draw, lose):

    probability = calculate_probability(
        win,
        draw,
        lose
    )

    max_direction = max(
        probability,
        key=probability.get
    )


    if max_direction == "win_probability":
        direction = "主胜"

    elif max_direction == "draw_probability":
        direction = "平局"

    else:
        direction = "客胜"


    return {

        "probability": probability,

        "direction": direction,

        "direction_score":
            probability[max_direction]

    }



# 测试

if __name__ == "__main__":

    result = analyze_direction(
        1.80,
        3.50,
        4.20
    )

    print(result)
