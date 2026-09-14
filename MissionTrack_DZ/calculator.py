from datetime import datetime, timedelta

RATES = {
    'شمال': {'meal': 800, 'night': 3200},
    'جنوب': {'meal': 1000, 'night': 4000}
}

def parse_datetime(dt_str):
    try:
        return datetime.strptime(dt_str, "%d-%m-%Y %H:%M")
    except ValueError:
        return None

def check_intersection(day_date, target_start_hour, target_end_hour, mission_start, mission_end):
    target_start = datetime.combine(day_date, datetime.min.time()) + timedelta(hours=target_start_hour)
    target_end = datetime.combine(day_date, datetime.min.time()) + timedelta(hours=target_end_hour)
    latest_start = max(target_start, mission_start)
    earliest_end = min(target_end, mission_end)
    return latest_start < earliest_end

def calculate_allowances(departure_str, return_str, region):
    mission_start = parse_datetime(departure_str)
    mission_end = parse_datetime(return_str)

    if not mission_start or not mission_end or mission_end <= mission_start:
        return 0, 0, 0

    meals = 0
    nights = 0
    current_date = mission_start.date()
    end_date = mission_end.date()

    while current_date <= end_date:
        if check_intersection(current_date, 11, 14, mission_start, mission_end):
            meals += 1
        if check_intersection(current_date, 18, 21, mission_start, mission_end):
            meals += 1
        if check_intersection(current_date, 0, 6, mission_start, mission_end):
            nights += 1
        current_date += timedelta(days=1)

    rate = RATES.get(region, RATES['شمال'])
    total_amount = (meals * rate['meal']) + (nights * rate['night'])
    return meals, nights, total_amount
