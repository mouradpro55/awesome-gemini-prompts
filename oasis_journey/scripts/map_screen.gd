extends Node2D

@onready var caravan = $Caravan
@onready var oasis1 = $Oasis1
@onready var oasis2 = $Oasis2
@onready var oasis3 = $Oasis3

var current_oasis = "Oasis1"
var puzzle_popup_scene = preload("res://scenes/PuzzlePopup.tscn")
var puzzle_popup_instance

func _ready():
	print("تم تحميل خريطة الواحات")
	caravan.position = oasis1.position + Vector2(75, -20)

	# تهيئة نافذة الألغاز
	puzzle_popup_instance = puzzle_popup_scene.instantiate()
	add_child(puzzle_popup_instance)

func _on_oasis_pressed(target_oasis_name: String):
	if target_oasis_name == current_oasis:
		print("أنت بالفعل في هذه الواحة!")
		return

	var travel_cost_water = 20
	var travel_cost_dates = 10

	var game_manager = get_node("/root/GameManager")
	if game_manager.consume_resources(travel_cost_water, travel_cost_dates):
		print("السفر إلى ", target_oasis_name)
		current_oasis = target_oasis_name

		var target_node = get_node(target_oasis_name)
		caravan.position = target_node.position + Vector2(75, -20)

		# إظهار لغز عند الوصول
		if puzzle_popup_instance:
			puzzle_popup_instance.show_puzzle()
	else:
		print("لا تملك الموارد الكافية للسفر!")
