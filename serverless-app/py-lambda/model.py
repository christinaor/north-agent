def compute_stress_score(row):
    """
    Weighted heuristic model:
    - stress_level: 50%
    - inverse sleep_hours: 30%
    - inverse mood_score: 20%

    Adjusted for:
    - stress_level: 0 to 100
    - sleep_hours: 0 to 10 (ideal = 8)
    - mood_score: -3 (lowest) to 3 (highest)
    """
    try:
        stress = float(row.get("stress_level", 0))
        sleep = float(row.get("sleep_hours", 8))
        mood = float(row.get("mood_score", 0))

        # Normalize sleep: less sleep means more stress (max 8 hours baseline)
        sleep_component = max(0, (8 - sleep)) / 8

        # Normalize mood from [-3..3] to [1..0] inverse scale (lower mood → higher stress)
        mood_component = max(0, (3 - mood) / 6)  # 3 - mood scales from 6 max range

        score = (
            0.5 * (stress / 100) +
            0.3 * sleep_component +
            0.2 * mood_component
        )

        return round(score, 4)

    except Exception as e:
        print(f"[Model] Error computing score: {e}")
        return 0.0

def is_high_stress(score, threshold=0.4):
    return score >= threshold