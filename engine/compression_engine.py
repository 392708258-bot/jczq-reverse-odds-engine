# JCZQ Reverse Odds Engine V6.0
# Compression Engine
# 赔率压缩引擎


def compression_ratio(original, compressed):
    """
    计算压缩比例
    CR = 初始赔率 ÷ 当前赔率
    """
    return round(
        original / compressed,
        2
    )


def compression_level(ratio):
    """
    判断压缩等级
    弱压缩: CR < 2
    中压缩: 2 <= CR < 5
    强压缩: CR >= 5
    """
    if ratio < 2:
        return "弱压缩"

    elif ratio < 5:
        return "中压缩"

    else:
        return "强压缩"


def analyze_compression(
        win_other,
        final_value):
    """
    分析赔率压缩情况
    输入：胜其他的初始赔率和当前赔率
    """
    ratio = compression_ratio(
        win_other,
        final_value
    )

    return {
        "original": win_other,
        "current": final_value,
        "compression_ratio": ratio,
        "level": compression_level(ratio)
    }


if __name__ == "__main__":

    print("=" * 50)
    print("JCZQ Compression Engine V1.0")
    print("=" * 50)

    result = analyze_compression(
        80,
        10
    )

    print("\n【赔率压缩分析】")
    print(f"初始赔率: {result['original']}")
    print(f"当前赔率: {result['current']}")
    print(f"压缩比例: {result['compression_ratio']}")
    print(f"压缩等级: {result['level']}")
    
    print("\n" + "=" * 50)
