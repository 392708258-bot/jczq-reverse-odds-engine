# Direction Engine - V6.0
from typing import Dict, Tuple
def determine_direction(match_data: Dict) -> Tuple[str, float]:
    home_win = match_data.get('win', 5.0)
    away_win = match_data.get('lose', 1.8)
    if away_win < 2.0:
        return '客胜', 0.65
    return '主胜', 0.60