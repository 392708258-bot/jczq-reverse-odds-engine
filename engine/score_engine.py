# JCZQ Reverse Odds Engine V6.0
# Score Engine
# 比分引擎 - 核心集成模块


def filter_scores_by_direction(scores, direction):
    """
    根据方向过滤比分
    主胜：筛选主队进球多于客队的比分
    平局：筛选进球相同的比分
    客胜：筛选客队进球多于主队的比分
    """
    filtered = {}
    
    for score, odds in scores.items():
        home, away = map(int, score.split(":"))
        
        if direction == "主胜" and home > away:
            filtered[score] = odds
        elif direction == "平局" and home == away:
            filtered[score] = odds
        elif direction == "客胜" and home < away:
            filtered[score] = odds
    
    return filtered


def filter_scores_by_goal(scores, target_goal):
    """
    根据目标进球数过滤比分
    只保留进球总数等于目标进球的比分
    """
    filtered = {}
    
    for score, odds in scores.items():
        home, away = map(int, score.split(":"))
        total = home + away
        
        if total == int(target_goal):
            filtered[score] = odds
        elif abs(total - int(target_goal)) <= 1:  # 相邻进球数也保留
            filtered[score] = odds
    
    return filtered


def calculate_score_confidence(
        score,
        odds,
        direction_info,
        compression_info,
        target_goal):
    """
    计算比分的综合置信度
    综合考虑：方向强度 + 压缩等级 + 进球匹配
    """
    home, away = map(int, score.split(":"))
    total = home + away
    
    # 1. 方向强度权重（25%）
    direction_strength = direction_info.get("direction_strength", 0)
    direction_score = min(direction_strength, 100)
    
    # 2. 赔率压缩权重（25%）
    compression_level = compression_info.get("level", "弱压缩")
    if compression_level == "强压缩":
        compression_score = 100
    elif compression_level == "中压缩":
        compression_score = 70
    else:
        compression_score = 40
    
    # 3. 进球匹配权重（25%）
    if total == int(target_goal):
        goal_match_score = 100
    elif abs(total - int(target_goal)) == 1:
        goal_match_score = 70
    else:
        goal_match_score = 40
    
    # 4. 赔率热度权重（25%）
    # 赔率越低，热度越高
    odds_score = max(0, 100 - odds * 10)
    odds_score = min(odds_score, 100)
    
    # 综合评分
    total_score = (
        direction_score * 0.25 +
        compression_score * 0.25 +
        goal_match_score * 0.25 +
        odds_score * 0.25
    )
    
    return round(total_score, 2)


def analyze_best_score(
        scores,
        direction_info,
        compression_info,
        goal_info):
    """
    分析最支持的比分
    输入各个引擎的分析结果和比分赔率
    输出：最支持比分 + 置信度
    """
    direction = direction_info.get("direction", "主胜")
    target_goal = goal_info.get("best_goal", "2")
    
    # 步骤1：按方向过滤比分
    direction_filtered = filter_scores_by_direction(
        scores,
        direction
    )
    
    # 步骤2：按进球过滤
    goal_filtered = filter_scores_by_goal(
        direction_filtered,
        target_goal
    )
    
    # 步骤3：计算每个比分的置信度
    score_results = {}
    
    for score, odds in goal_filtered.items():
        confidence = calculate_score_confidence(
            score,
            odds,
            direction_info,
            compression_info,
            target_goal
        )
        score_results[score] = {
            "odds": odds,
            "confidence": confidence
        }
    
    # 步骤4：找出最高置信度的比分
    if score_results:
        best_score = max(
            score_results,
            key=lambda x: score_results[x]["confidence"]
        )
        
        return {
            "best_score": best_score,
            "odds": score_results[best_score]["odds"],
            "confidence": score_results[best_score]["confidence"],
            "candidates": score_results
        }
    else:
        return {
            "best_score": None,
            "confidence": 0,
            "candidates": {}
        }


if __name__ == "__main__":

    print("=" * 60)
    print("JCZQ Score Engine V1.0 - 比分引擎")
    print("=" * 60)
    
    # 模拟数据
    direction_info = {
        "direction": "主胜",
        "direction_strength": 25.0,
        "direction_score": 51.47
    }
    
    compression_info = {
        "compression_ratio": 8.0,
        "level": "强压缩"
    }
    
    goal_info = {
        "best_goal": "2"
    }
    
    scores = {
        "1:0": 8.5,
        "2:0": 8.0,
        "2:1": 7.5,
        "3:0": 10.0,
        "3:1": 9.5,
        "3:2": 15.0
    }
    
    # 分析最支持的比分
    result = analyze_best_score(
        scores,
        direction_info,
        compression_info,
        goal_info
    )
    
    print("\n【输入信息】")
    print(f"方向: {direction_info['direction']}")
    print(f"方向强度: {direction_info['direction_strength']}")
    print(f"压缩等级: {compression_info['level']}")
    print(f"目标进球: {goal_info['best_goal']}球")
    
    print("\n【比分池】")
    for score, odds in scores.items():
        print(f"{score}: {odds}")
    
    print("\n【分析结果】")
    if result["best_score"]:
        print(f"最支持比分: {result['best_score']}")
        print(f"比分赔率: {result['odds']}")
        print(f"置信度: {result['confidence']}%")
        
        print(f"\n【候选比分排序】")
        sorted_candidates = sorted(
            result["candidates"].items(),
            key=lambda x: x[1]["confidence"],
            reverse=True
        )
        for score, data in sorted_candidates:
            print(f"{score} (赔率{data['odds']}) - 置信度{data['confidence']}%")
    else:
        print("未找到符合条件的比分")
    
    print("\n" + "=" * 60)
