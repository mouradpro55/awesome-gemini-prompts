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
        this.add.text(400, 100, 'ملكة كوكب برق البرق', {
            fontFamily: 'Tahoma, Arial',
            fontSize: '64px',
            color: '#FFD700',
            stroke: '#C71585',
            strokeThickness: 8,
            shadow: { offsetX: 3, offsetY: 3, color: '#000', blur: 10, fill: true }
        }).setOrigin(0.5);

        this.add.text(400, 180, 'اختر شخصيتك للانطلاق:', {
            fontFamily: 'Tahoma, Arial',
            fontSize: '28px',
            color: '#FFFFFF',
            shadow: { offsetX: 2, offsetY: 2, color: '#000', blur: 5, fill: true }
        }).setOrigin(0.5);

        // Groom Select Button
        const groomBtnBg = this.add.graphics();
        groomBtnBg.fillStyle(0xFFD700, 1);
        groomBtnBg.fillRoundedRect(200, 250, 150, 150, 16);
        this.add.image(275, 300, 'player_groom').setScale(1.5);
        this.add.text(275, 370, 'عريس', { fontFamily: 'Tahoma', fontSize: '24px', color: '#C71585', fontStyle: 'bold' }).setOrigin(0.5);

        const groomZone = this.add.zone(275, 325, 150, 150).setInteractive({ useHandCursor: true });
        groomZone.on('pointerdown', () => this.startGame('groom'));

        // Bride Select Button
        const brideBtnBg = this.add.graphics();
        brideBtnBg.fillStyle(0xFFD700, 1);
        brideBtnBg.fillRoundedRect(450, 250, 150, 150, 16);
        this.add.image(525, 300, 'player_bride').setScale(1.5);
        this.add.text(525, 370, 'عروس', { fontFamily: 'Tahoma', fontSize: '24px', color: '#C71585', fontStyle: 'bold' }).setOrigin(0.5);

        const brideZone = this.add.zone(525, 325, 150, 150).setInteractive({ useHandCursor: true });
        brideZone.on('pointerdown', () => this.startGame('bride'));

        // Hover effects
        groomZone.on('pointerover', () => { groomBtnBg.clear(); groomBtnBg.fillStyle(0xFFFFFF, 1); groomBtnBg.fillRoundedRect(200, 250, 150, 150, 16); });
        groomZone.on('pointerout', () => { groomBtnBg.clear(); groomBtnBg.fillStyle(0xFFD700, 1); groomBtnBg.fillRoundedRect(200, 250, 150, 150, 16); });

        brideZone.on('pointerover', () => { brideBtnBg.clear(); brideBtnBg.fillStyle(0xFFFFFF, 1); brideBtnBg.fillRoundedRect(450, 250, 150, 150, 16); });
        brideZone.on('pointerout', () => { brideBtnBg.clear(); brideBtnBg.fillStyle(0xFFD700, 1); brideBtnBg.fillRoundedRect(450, 250, 150, 150, 16); });
    }

    startGame(character) {
        this.scene.start('GameScene', { character: character });
    }
}
