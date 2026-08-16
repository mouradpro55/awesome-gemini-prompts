extends Node

# الموارد الأساسية
var water: int = 100
var dates: int = 50

# إشارة (Signal) لتحديث واجهة المستخدم عند تغير الموارد
signal resources_updated(water_amount, dates_amount)

func _ready():
	print("مدير اللعبة جاهز: الماء = ", water, " التمور = ", dates)

# دالة لاستهلاك الموارد (تُستدعى عند التحرك)
func consume_resources(water_cost: int, dates_cost: int) -> bool:
	if water >= water_cost and dates >= dates_cost:
		water -= water_cost
		dates -= dates_cost
		emit_signal("resources_updated", water, dates)
		print("تم استهلاك الموارد. المتبقي - الماء: ", water, " التمور: ", dates)
		return true
	else:
		print("الموارد غير كافية!")
		return false

# دالة لإضافة موارد (تُستدعى عند حل لغز أو شراء موارد)
func add_resources(water_amount: int, dates_amount: int):
	water += water_amount
	dates += dates_amount
	emit_signal("resources_updated", water, dates)
	print("تمت إضافة موارد. المتبقي - الماء: ", water, " التمور: ", dates)
