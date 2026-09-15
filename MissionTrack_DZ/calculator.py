from datetime import datetime, timedelta, time

def calculate_allowances(departure_str, return_str, region):
    # Fallback to defaults if parsing fails
    try:
        dep_dt = datetime.strptime(departure_str, "%d-%m-%Y %H:%M")
        ret_dt = datetime.strptime(return_str, "%d-%m-%Y %H:%M")
    except ValueError:
        return 0, 0, 0

    if ret_dt <= dep_dt:
        return 0, 0, 0

    rates = {
        "شمال": {"meal": 800, "night": 3200},
        "جنوب": {"meal": 1000, "night": 4000}
    }

    zone = region if region in rates else "شمال"

    total_meals = 0
    total_nights = 0

    current_date = dep_dt.date()
    end_date = ret_dt.date()

    while current_date <= end_date:
        is_first_day = (current_date == dep_dt.date())
        is_last_day = (current_date == end_date)

        # 1. Lunch check (11:00 to 14:00, threshold 13:00)
        lunch_eligible = True
        if is_first_day and dep_dt.time() > time(13, 0):
            lunch_eligible = False
        if is_last_day and ret_dt.time() < time(13, 0):
            lunch_eligible = False

        if lunch_eligible:
            total_meals += 1

        # 2. Dinner check (18:00 to 21:00, threshold 20:00)
        dinner_eligible = True
        if is_first_day and dep_dt.time() > time(20, 0):
            dinner_eligible = False
        if is_last_day and ret_dt.time() < time(20, 0):
            dinner_eligible = False

        if dinner_eligible:
            total_meals += 1

        # 3. Night check
        if current_date < end_date:
            total_nights += 1

        current_date += timedelta(days=1)

    # If returning on the last day before 06:00, subtract the final night
    if total_nights > 0 and ret_dt.time() < time(6, 0):
        total_nights -= 1

    meal_rate = rates[zone]["meal"]
    night_rate = rates[zone]["night"]
    total_amount = (total_meals * meal_rate) + (total_nights * night_rate)

    return total_meals, total_nights, total_amount
