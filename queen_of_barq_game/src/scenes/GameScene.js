import Phaser from 'phaser';

export default class GameScene extends Phaser.Scene {
    constructor() {
        super('GameScene');
    }

    init(data) {
        this.selectedCharacter = data.character || 'groom';
        this.score = 0;
        this.prestige = 100;
        this.gameSpeed = 5;
        this.isQueenEvent = false;
        this.lastEventTime = 0;
    }

    create() {
        this.score = 0;
        this.prestige = 100;
        this.gameSpeed = 5;
        this.isQueenEvent = false;

        // Background
        this.bg = this.add.tileSprite(400, 300, 800, 600, 'bg_game');
        // Overlay for better visibility
        this.add.graphics().fillStyle(0x000000, 0.3).fillRect(0, 0, 800, 600);

        // Ground
        this.ground = this.add.tileSprite(400, 550, 800, 100, 'ground');
        this.physics.add.existing(this.ground, true);

        // Player
        this.player = this.physics.add.sprite(150, 450, this.selectedCharacter === 'bride' ? 'player_bride' : 'player_groom');
        this.player.setCollideWorldBounds(true);
        this.player.setGravityY(1200);
        this.physics.add.collider(this.player, this.ground);

        // Groups
        this.obstacles = this.physics.add.group();
        this.collectibles = this.physics.add.group();

        this.physics.add.collider(this.obstacles, this.ground);

        this.physics.add.overlap(this.player, this.obstacles, this.hitObstacle, null, this);
        this.physics.add.overlap(this.player, this.collectibles, this.collectItem, null, this);

        // UI Text
        this.scoreText = this.add.text(780, 20, 'النقاط: 0', { fontSize: '24px', fill: '#FFF', fontFamily: 'Tahoma' }).setOrigin(1, 0);
        this.prestigeText = this.add.text(20, 20, 'الهيبة: 100%', { fontSize: '24px', fill: '#FFF', fontFamily: 'Tahoma' });

        // Input
        this.cursors = this.input.keyboard.createCursorKeys();
        this.input.on('pointerdown', this.jump, this);
        this.input.keyboard.on('keydown-SPACE', this.jump, this);

        // Timers
        this.time.addEvent({ delay: 1500, callback: this.spawnObstacle, callbackScope: this, loop: true });
        this.time.addEvent({ delay: 2000, callback: this.spawnCollectible, callbackScope: this, loop: true });
        this.time.addEvent({ delay: 100, callback: this.updateScore, callbackScope: this, loop: true });

        // Queen Events
        this.time.addEvent({ delay: 20000, callback: this.triggerQueenGaze, callbackScope: this, loop: true });

        if (!this.bgm) {
            this.bgm = this.sound.add('bgm', { loop: true, volume: 0.5 });
        }
        if (!this.bgm.isPlaying) this.bgm.play();
        this.time.addEvent({ delay: 35000, callback: this.triggerQueenDecree, callbackScope: this, loop: true });

        // Listen to UI events
        window.GameEvents.on('answerSelected', this.handleAnswer, this);
    }

    jump() {
        if (this.player.body.touching.down && !this.isQueenEvent) {
            this.player.setVelocityY(-700);
        }
    }

    spawnObstacle() {
        if (this.isQueenEvent) return;
        if (Phaser.Math.Between(0, 10) > 7) {
            let obstacle = this.obstacles.create(850, 480, 'obstacle');
            obstacle.setVelocityX(-this.gameSpeed * 60);
        }
    }

    spawnCollectible() {
        if (this.isQueenEvent) return;
        if (Phaser.Math.Between(0, 10) > 5) {
            let item = this.collectibles.create(850, Phaser.Math.Between(300, 400), 'heart');
            item.body.allowGravity = false;
            item.setVelocityX(-this.gameSpeed * 60);
        }
    }

    updateScore() {
        if (!this.isQueenEvent) {
            this.score += 1;
            this.scoreText.setText('النقاط: ' + this.score);
            this.gameSpeed += 0.005; // Slowly increase speed
        }
    }

    hitObstacle(player, obstacle) {
        obstacle.destroy();
        this.prestige -= 20;
        this.prestigeText.setText('الهيبة: ' + this.prestige + '%');

        // Visual feedback
        this.cameras.main.shake(200, 0.01);
        player.setTint(0xff0000);
        this.time.delayedCall(200, () => player.clearTint());

        if (this.prestige <= 0) {
            this.gameOver();
        }
    }

    collectItem(player, item) {
        item.destroy();
        this.score += 50;
        this.scoreText.setText('النقاط: ' + this.score);

        // Heal prestige slightly
        if (this.prestige < 100) {
            this.prestige = Math.min(100, this.prestige + 5);
            this.prestigeText.setText('الهيبة: ' + this.prestige + '%');
        }
    }

    triggerQueenGaze() {
        if (this.isQueenEvent) return;
        // Speed up temporarily
        let oldSpeed = this.gameSpeed;
        this.gameSpeed *= 1.5;
        this.player.setTint(0xFF69B4); // Pink tint

        let overlay = document.getElementById('flash-overlay');
        overlay.classList.remove('hidden');
        overlay.classList.add('flash');

        this.time.delayedCall(3000, () => {
            this.gameSpeed = oldSpeed;
            this.player.clearTint();
            overlay.classList.remove('flash');
            setTimeout(() => overlay.classList.add('hidden'), 200);
        });
    }

    triggerQueenDecree() {
        this.isQueenEvent = true;
        this.time.delayedCall(1000, () => {
            if (this.prestige > 0) this.physics.pause();
        });
        // Delay pause so player sees flash first

        let overlay = document.getElementById('flash-overlay');
        overlay.classList.remove('hidden');
        overlay.classList.add('flash');

        setTimeout(() => {
            if (this.prestige <= 0) return;
            const ui = document.getElementById('ui-question');
            ui.classList.remove('hidden');

            const questions = [
                { q: "ما هو الشرط الأهم للزواج في كوكبنا؟", a1: "فيلا وسيارة", a2: "الحب الصادق", correct: 1 },
                { q: "ما هو المشروب الرسمي لكوكب برق البرق؟", a1: "ماء الذهب", a2: "مشروب وردي", correct: 2 },
                { q: "كم كيلو ذهب مطلوب للمهر؟", a1: "وزن العروسة", a2: "خاتم بسيط", correct: 1 }
            ];

            let q = Phaser.Utils.Array.GetRandom(questions);
            document.getElementById('q-text').innerText = q.q;

            let btnHtml = `
                <button class="btn-answer" onclick="window.GameEvents.emit('answerSelected', 1, ${q.correct})">${q.a1}</button>
                <button class="btn-answer" onclick="window.GameEvents.emit('answerSelected', 2, ${q.correct})">${q.a2}</button>
            `;
            document.getElementById('q-answers').innerHTML = btnHtml;
        }, 500);
    }

    handleAnswer(selected, correct) {
        document.getElementById('ui-question').classList.add('hidden');
        let overlay = document.getElementById('flash-overlay');
        overlay.classList.remove('flash');
        setTimeout(() => overlay.classList.add('hidden'), 200);

        if (selected === correct) {
            this.score += 200;
            this.player.setTint(0x00FF00); // Green
        } else {
            this.prestige -= 30;
            this.player.setTint(0xFF0000); // Red
        }

        this.prestigeText.setText('الهيبة: ' + this.prestige + '%');
        this.scoreText.setText('النقاط: ' + this.score);

        this.time.delayedCall(1000, () => {
            this.player.clearTint();
            if (this.prestige <= 0) {
                this.gameOver();
            } else {
                this.physics.resume();
                this.isQueenEvent = false;
            }
        });
    }

    update() {
        if (this.isQueenEvent) return;

        this.bg.tilePositionX += this.gameSpeed;
        this.ground.tilePositionX += this.gameSpeed * 2;

        this.obstacles.getChildren().forEach(obs => {
            if (obs.x < -50) obs.destroy();
            else obs.setVelocityX(-this.gameSpeed * 60);
        });

        this.collectibles.getChildren().forEach(item => {
            if (item.x < -50) item.destroy();
            else item.setVelocityX(-this.gameSpeed * 60);
        });
    }

    gameOver() {
        this.physics.pause();
        if (this.bgm) this.bgm.stop();
        this.isQueenEvent = true;
        this.player.setTint(0xff0000);
        window.GameEvents.off('answerSelected', this.handleAnswer, this);
        this.time.delayedCall(1000, () => {
            this.scene.start('GameOverScene', { score: this.score });
        });
    }
}