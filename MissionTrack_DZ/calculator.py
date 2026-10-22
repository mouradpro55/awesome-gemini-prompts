from datetime import datetime, timedelta, time
from allowance_rules import ALLOWANCE_TABLE

def calculate_allowances(departure_str, return_str, region, category, distance_km):
    try:
        distance = float(distance_km)
    except (ValueError, TypeError):
        distance = 0.0

    if distance <= 50:
        return 0, 0, 0

    try:
        dep_dt = datetime.strptime(departure_str, "%d-%m-%Y %H:%M")
        ret_dt = datetime.strptime(return_str, "%d-%m-%Y %H:%M")
    except ValueError:
        return 0, 0, 0

    if ret_dt <= dep_dt:
        return 0, 0, 0

    cat_rates = ALLOWANCE_TABLE.get(category)
    if not cat_rates:
        cat_rates = ALLOWANCE_TABLE["1-10"]

    rates = cat_rates.get(region)
    if not rates:
        rates = cat_rates["شمال"]

    meal_rate = rates["meal"]
    night_rate = rates["night"]

    total_meals = 0
    total_nights = 0

    current_date = dep_dt.date()
    end_date = ret_dt.date()

    while current_date <= end_date:
        day_start = datetime.combine(current_date, time(0, 0))
        day_end = datetime.combine(current_date, time(23, 59, 59))

        presence_start = max(day_start, dep_dt)
        presence_end = min(day_end, ret_dt)

        if presence_start < presence_end:
            # 1. Lunch overlap (11:00 -> 14:00)
            lunch_start = datetime.combine(current_date, time(11, 0))
            lunch_end = datetime.combine(current_date, time(14, 0))
            if presence_start < lunch_end and presence_end > lunch_start:
                total_meals += 1

            # 2. Dinner overlap (18:00 -> 21:00)
            dinner_start = datetime.combine(current_date, time(18, 0))
            dinner_end = datetime.combine(current_date, time(21, 0))
            if presence_start < dinner_end and presence_end > dinner_start:
                total_meals += 1

            # 3. Night overlap (00:00 -> 06:00)
            night_start = datetime.combine(current_date, time(0, 0))
            night_end = datetime.combine(current_date, time(6, 0))
            if presence_start < night_end and presence_end > night_start:
                total_nights += 1

        current_date += timedelta(days=1)

    total_amount = (total_meals * meal_rate) + (total_nights * night_rate)

    return total_meals, total_nights, total_amount
