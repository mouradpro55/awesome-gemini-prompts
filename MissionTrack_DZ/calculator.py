from datetime import datetime, time, timedelta

def calculate_allowances(departure_str, return_str, region, is_training=False):
    '''
    حساب عدد الوجبات والليالي والمبلغ الإجمالي المستحق
    مع مراعاة نسبة 25% في حال كانت المهمة من أجل تكوين.
    '''
    try:
        dep_dt = datetime.strptime(departure_str, "%d-%m-%Y %H:%M")
        ret_dt = datetime.strptime(return_str, "%d-%m-%Y %H:%M")
    except ValueError:
        return 0, 0, 0, 0  # وجبات، ليالي، مبلغ خام، مبلغ صافي

    if ret_dt <= dep_dt:
        return 0, 0, 0, 0

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

        # 1. الغداء (عتبة 13:00)
        lunch_eligible = True
        if is_first_day and dep_dt.time() > time(13, 0):
            lunch_eligible = False
        if is_last_day and ret_dt.time() < time(13, 0):
            lunch_eligible = False
        if lunch_eligible:
            total_meals += 1

        # 2. العشاء (عتبة 20:00)
        dinner_eligible = True
        if is_first_day and dep_dt.time() > time(20, 0):
            dinner_eligible = False
        if is_last_day and ret_dt.time() < time(20, 0):
            dinner_eligible = False
        if dinner_eligible:
            total_meals += 1

        # 3. المبيت
        if current_date < end_date:
            total_nights += 1

        current_date += timedelta(days=1)

    # إلغاء ليلة اليوم الأخير إذا كان الوصول قبل 06:00 صباحاً
    if total_nights > 0 and ret_dt.time() < time(6, 0):
        total_nights -= 1

    meal_rate = rates[zone]["meal"]
    night_rate = rates[zone]["night"]

    # احتساب المبلغ الخام الإجمالي
    gross_amount = (total_meals * meal_rate) + (total_nights * night_rate)

    # تطبيق نسبة 25% لمهام التكوين
    if is_training:
        net_amount = gross_amount * 0.25
    else:
        net_amount = gross_amount

    return total_meals, total_nights, gross_amount, net_amount
