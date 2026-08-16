extends CanvasLayer

@onready var water_label = $MarginContainer/HBoxContainer/WaterLabel
@onready var dates_label = $MarginContainer/HBoxContainer/DatesLabel

func _ready():
	# محاولة ربط الإشارة إذا كان GameManager موجوداً كـ Autoload
	if name == "HUD": # Just a safe check
		var game_manager = get_node_or_null("/root/GameManager")
		if game_manager:
			game_manager.resources_updated.connect(_on_resources_updated)
			# تحديث أولي
			_on_resources_updated(game_manager.water, game_manager.dates)

func _on_resources_updated(water: int, dates: int):
	water_label.text = "الماء: " + str(water)
	dates_label.text = "التمور: " + str(dates)
