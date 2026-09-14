from datetime import datetime, timedelta

# Rates Definition
RATES = {
    'شمال': {'meal': 800, 'night': 3200},
    'جنوب': {'meal': 1000, 'night': 4000}
}

def parse_datetime(dt_str):
    # Expected format: "DD-MM-YYYY HH:MM"
    try:
        return datetime.strptime(dt_str, "%d-%m-%Y %H:%M")
    except ValueError:
        return None

def check_intersection(day_date, target_start_hour, target_end_hour, mission_start, mission_end):
    """
    Check if the mission time intersects with a target time window on a specific day.
    """
    target_start = datetime.combine(day_date, datetime.min.time()) + timedelta(hours=target_start_hour)
    target_end = datetime.combine(day_date, datetime.min.time()) + timedelta(hours=target_end_hour)

    # Intersection occurs if max(start1, start2) < min(end1, end2)
    latest_start = max(target_start, mission_start)
    earliest_end = min(target_end, mission_end)

    return latest_start < earliest_end

def calculate_mission_allowances(departure_str, return_str, region):
    mission_start = parse_datetime(departure_str)
    mission_end = parse_datetime(return_str)

    if not mission_start or not mission_end or mission_end <= mission_start:
        return 0, 0, 0, 0

    meals_count = 0
    nights_count = 0

    current_date = mission_start.date()
    end_date = mission_end.date()

    while current_date <= end_date:
        # Check lunch: 11:00 to 14:00
        if check_intersection(current_date, 11, 14, mission_start, mission_end):
            meals_count += 1

        # Check dinner: 18:00 to 21:00
        if check_intersection(current_date, 18, 21, mission_start, mission_end):
            meals_count += 1

        # Check night: 00:00 to 06:00 (this happens on the current day 0-6am)
        # Note: If the mission starts before midnight and ends after midnight, it crosses the 00-06 boundary of the *next* day.
        # But we iterate days. So on 'current_date', 00:00 to 06:00 represents the morning of current_date.
        if check_intersection(current_date, 0, 6, mission_start, mission_end):
            # Only count night if the mission actually spanned across midnight or was entirely during the night.
            # Usually, you get a night if you are away during this period.
            nights_count += 1

        current_date += timedelta(days=1)

    rate = RATES.get(region, RATES['شمال'])
    meals_total = meals_count * rate['meal']
    nights_total = nights_count * rate['night']

    return meals_count, nights_count, meals_total, nights_total

if __name__ == "__main__":
    # Test user's example: 01-05-2023 10:00 to 03-05-2023 15:00
    m_count, n_count, m_tot, n_tot = calculate_mission_allowances("01-05-2023 10:00", "03-05-2023 15:00", "شمال")
    print(f"Meals: {m_count}, Nights: {n_count}, Meals Total: {m_tot}, Nights Total: {n_tot}")
    # Expected: 5 meals, 2 nights
