# JCZQ Reverse Odds Engine V6.0
# Direction Engine V2.0
# 方向引擎 - 增强版


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


def calculate_direction_strength(probability):
    """
    计算方向强度
    最高概率 - 第二高概率
    """
    probs = list(probability.values())
    probs.sort(reverse=True)
    
    strength = round(probs[0] - probs[1], 2)
    return strength


def calculate_draw_pressure(probability):
    """
    计算平局压力
    评估平局概率的影响程度
    """
    draw_prob = probability["draw_probability"]
    
    # 平局压力指数：平局概率越高，压力越大
    if draw_prob > 30:
        pressure = "高"
    elif draw_prob > 20:
        pressure = "中"
    else:
        pressure = "低"
    
    return {
        "draw_pressure_value": draw_prob,
        "draw_pressure_level": pressure
    }


def calculate_upset_risk(probability, direction_strength):
    """
    计算冷门风险
    综合考虑：赔率接近度 + 平局压力 + 客胜概率
    """
    draw_prob = probability["draw_probability"]
    lose_prob = probability["lose_probability"]
    
    # 冷门风险 = 方向强度弱 + 平局高 + 客胜有机会
    risk_score = round(
        (100 - direction_strength) * 0.4 + 
        draw_prob * 0.3 + 
        lose_prob * 0.3,
        2
    )
    
    # 风险等级
    if risk_score > 40:
        risk_level = "高"
    elif risk_score > 25:
        risk_level = "中"
    else:
        risk_level = "低"
    
    return {
        "upset_risk_score": risk_score,
        "upset_risk_level": risk_level
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

    # 计算方向强度
    direction_strength = calculate_direction_strength(probability)
    
    # 计算平局压力
    draw_pressure = calculate_draw_pressure(probability)
    
    # 计算冷门风险
    upset_risk = calculate_upset_risk(probability, direction_strength)

    return {
        "probability": probability,
        "direction": direction,
        "direction_score": probability[max_direction],
        "direction_strength": direction_strength,
        "draw_pressure": draw_pressure,
        "upset_risk": upset_risk
    }



# 测试

if __name__ == "__main__":

    print("=" * 50)
    print("JCZQ Direction Engine V2.0")
    print("=" * 50)
    
    result = analyze_direction(
        1.80,
        3.50,
        4.20
    )

    print("\n【胜平负解析】")
    print(f"主胜概率: {result['probability']['win_probability']}%")
    print(f"平局概率: {result['probability']['draw_probability']}%")
    print(f"客胜概率: {result['probability']['lose_probability']}%")

    print(f"\n【方向判断】")
    print(f"方向: {result['direction']}")
    print(f"Direction Score: {result['direction_score']}")

    print(f"\n【方向强度】")
    print(f"方向强度: {result['direction_strength']}")

    print(f"\n【平局压力】")
    print(f"平局压力值: {result['draw_pressure']['draw_pressure_value']}%")
    print(f"平局压力等级: {result['draw_pressure']['draw_pressure_level']}")

    print(f"\n【冷门风险】")
    print(f"冷门风险值: {result['upset_risk']['upset_risk_score']}")
    print(f"冷门风险等级: {result['upset_risk']['upset_risk_level']}")
    
    print("\n" + "=" * 50)

