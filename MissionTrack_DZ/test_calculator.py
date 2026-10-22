from calculator import calculate_allowances

def test_distance_constraint():
    m, n, t = calculate_allowances('01-01-2023 08:00', '01-01-2023 20:00', 'شمال', '1-10', 40)
    assert m == 0 and n == 0 and t == 0

def test_lunch_allowance():
    m, n, t = calculate_allowances('01-01-2023 10:00', '01-01-2023 15:00', 'شمال', '1-10', 100)
    assert m == 1 and n == 0
    assert t == 600

def test_overnight():
    m, n, t = calculate_allowances('01-01-2023 23:00', '02-01-2023 07:00', 'شمال', '1-10', 100)
    assert m == 0 and n == 1
    assert t == 2400
