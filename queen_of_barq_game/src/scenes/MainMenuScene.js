import Phaser from 'phaser';

export default class MainMenuScene extends Phaser.Scene {
    constructor() {
        super('MainMenuScene');
    }

    create() {
        // Background
        const bg = this.add.image(400, 300, 'bg_main');

        // Scale to fit
        const scaleX = 800 / bg.width;
        const scaleY = 600 / bg.height;
        const scale = Math.max(scaleX, scaleY);
        bg.setScale(scale);

        // Dark overlay for text readability
        const overlay = this.add.graphics();
        overlay.fillStyle(0x000000, 0.4);
        overlay.fillRect(0, 0, 800, 600);

        // Title text
        this.add.text(400, 150, 'ملكة كوكب برق البرق', {
            fontFamily: 'Tahoma, Arial',
            fontSize: '64px',
            color: '#FFD700',
            stroke: '#C71585',
            strokeThickness: 8,
            shadow: { offsetX: 3, offsetY: 3, color: '#000', blur: 10, fill: true }
        }).setOrigin(0.5);

        this.add.text(400, 220, 'هل أنت جاهز لتلبية الشروط يا عريس؟', {
            fontFamily: 'Tahoma, Arial',
            fontSize: '28px',
            color: '#FFFFFF',
            shadow: { offsetX: 2, offsetY: 2, color: '#000', blur: 5, fill: true }
        }).setOrigin(0.5);

        // Start Button
        const startBtnBg = this.add.graphics();
        startBtnBg.fillStyle(0xFFD700, 1);
        startBtnBg.fillRoundedRect(300, 350, 200, 60, 16);

        const startText = this.add.text(400, 380, 'ابدأ الرحلة', {
            fontFamily: 'Tahoma, Arial',
            fontSize: '32px',
            color: '#C71585',
            fontStyle: 'bold'
        }).setOrigin(0.5);

        // Make button interactive
        const startBtnZone = this.add.zone(400, 380, 200, 60).setInteractive({ useHandCursor: true });

        startBtnZone.on('pointerover', () => {
            startBtnBg.clear();
            startBtnBg.fillStyle(0xFFFFFF, 1);
            startBtnBg.fillRoundedRect(300, 350, 200, 60, 16);
        });

        startBtnZone.on('pointerout', () => {
            startBtnBg.clear();
            startBtnBg.fillStyle(0xFFD700, 1);
            startBtnBg.fillRoundedRect(300, 350, 200, 60, 16);
        });

        startBtnZone.on('pointerdown', () => {
            this.scene.start('GameScene');
        });
    }
}