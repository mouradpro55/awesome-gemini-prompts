extends Control

func _ready():
	print("تم تحميل القائمة الرئيسية")

func _on_start_button_pressed():
	print("الزر مضغوط: ابدأ الرحلة")
	get_tree().change_scene_to_file("res://scenes/MapScreen.tscn")

func _on_quit_button_pressed():
	print("الزر مضغوط: خروج")
	get_tree().quit()
