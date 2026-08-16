extends CanvasLayer

@onready var question_label = $Panel/VBoxContainer/QuestionLabel
@onready var options_container = $Panel/VBoxContainer/OptionsContainer
@onready var feedback_label = $Panel/VBoxContainer/FeedbackLabel
@onready var close_button = $Panel/VBoxContainer/CloseButton

var current_puzzle: Dictionary
var puzzles: Array = []

func _ready():
	hide() # إخفاء النافذة مبدئياً
	load_puzzles()

func load_puzzles():
	var file = FileAccess.open("res://data/puzzles.json", FileAccess.READ)
	if file:
		var json_text = file.get_as_text()
		var json = JSON.new()
		var error = json.parse(json_text)
		if error == OK:
			puzzles = json.data
		file.close()

func show_puzzle():
	if puzzles.size() == 0:
		return

	# اختيار لغز عشوائي
	current_puzzle = puzzles[randi() % puzzles.size()]

	question_label.text = current_puzzle["question"]
	feedback_label.text = ""
	close_button.hide()

	# مسح الأزرار القديمة
	for child in options_container.get_children():
		child.queue_free()

	# إنشاء أزرار الخيارات
	var index = 0
	for option_text in current_puzzle["options"]:
		var btn = Button.new()
		btn.text = option_text
		btn.add_theme_font_size_override("font_size", 20)
		btn.pressed.connect(_on_option_pressed.bind(index))
		options_container.add_child(btn)
		index += 1

	get_tree().paused = true # إيقاف اللعبة مؤقتاً أثناء اللغز
	show()

func _on_option_pressed(index: int):
	# تعطيل الأزرار بعد الاختيار
	for child in options_container.get_children():
		child.disabled = true

	if index == current_puzzle["correct_index"]:
		feedback_label.text = "إجابة صحيحة! حصلت على موارد."
		feedback_label.add_theme_color_override("font_color", Color(0, 1, 0))
		var game_manager = get_node("/root/GameManager")
		game_manager.add_resources(current_puzzle["reward_water"], current_puzzle["reward_dates"])
	else:
		feedback_label.text = "إجابة خاطئة! حظاً أوفر في المرة القادمة."
		feedback_label.add_theme_color_override("font_color", Color(1, 0, 0))

	close_button.show()

func _on_close_button_pressed():
	hide()
	get_tree().paused = false
