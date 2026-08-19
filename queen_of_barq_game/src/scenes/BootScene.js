import Phaser from 'phaser';

export default class BootScene extends Phaser.Scene {
    constructor() {
        super('BootScene');
    }

    preload() {
        // Create loading bar
        let progressBar = this.add.graphics();
        let progressBox = this.add.graphics();
        progressBox.fillStyle(0xFFD700, 0.8);
        progressBox.fillRect(240, 270, 320, 50);

        let width = this.cameras.main.width;
        let height = this.cameras.main.height;
        let loadingText = this.make.text({
            x: width / 2,
            y: height / 2 - 50,
            text: 'جاري التحميل...',
            style: {
                font: '20px monospace',
                fill: '#FF69B4'
            }
        });
        loadingText.setOrigin(0.5, 0.5);

        this.load.on('progress', function (value) {
            progressBar.clear();
            progressBar.fillStyle(0xFF69B4, 1);
            progressBar.fillRect(250, 280, 300 * value, 30);
        });

        this.load.on('complete', function () {
            progressBar.destroy();
            progressBox.destroy();
            loadingText.destroy();
        });

        // Load images
        this.load.image('bg_main', '/assets/images1.jpg'); // The palace/queen image
        this.load.image('bg_game', '/assets/images2.jpg'); // Passports/traveling image

        // Card templates
        this.load.image('card_template_1', '/assets/images.jpg');
        this.load.image('card_template_2', '/assets/images14.jpg');

        // Generate simple graphics for sprites if not available
        this.generateSprites();
    }

    generateSprites() {
        // Player (Groom) Placeholder
        const graphics = this.make.graphics({x: 0, y: 0, add: false});
        graphics.fillStyle(0x00BFFF, 1); // Blue suit
        graphics.fillRect(0, 0, 40, 60);
        graphics.fillStyle(0xFFDAB9, 1); // Face
        graphics.fillCircle(20, -10, 15);
        graphics.generateTexture('player', 40, 80);

        // Ground placeholder
        graphics.clear();
        graphics.fillStyle(0xFF1493, 1); // Deep pink
        graphics.fillRect(0, 0, 800, 100);
        graphics.fillStyle(0xFFD700, 1); // Gold trim
        graphics.fillRect(0, 0, 800, 10);
        graphics.generateTexture('ground', 800, 100);

        // Obstacle (Boxes/Gifts)
        graphics.clear();
        graphics.fillStyle(0xFFD700, 1); // Gold
        graphics.fillRect(0, 0, 40, 40);
        graphics.fillStyle(0xFF69B4, 1); // Pink ribbon
        graphics.fillRect(15, 0, 10, 40);
        graphics.fillRect(0, 15, 40, 10);
        graphics.generateTexture('obstacle', 40, 40);

        // Collectible (Pink Heart)
        graphics.clear();
        graphics.fillStyle(0xFF69B4, 1);
        // Simple diamond for heart placeholder
        graphics.beginPath();
        graphics.moveTo(15, 0);
        graphics.lineTo(30, 15);
        graphics.lineTo(15, 30);
        graphics.lineTo(0, 15);
        graphics.fillPath();
        graphics.generateTexture('heart', 30, 30);
    }

    create() {
        this.scene.start('MainMenuScene');
    }
}