import Phaser from 'phaser';

export default class GameOverScene extends Phaser.Scene {
    constructor() {
        super('GameOverScene');
    }

    init(data) {
        this.finalScore = data.score || 0;
    }

    create() {
        // Stop all other scenes input just in case
        this.input.keyboard.removeAllListeners();

        // Show HTML UI
        const uiForm = document.getElementById('ui-card-form');
        uiForm.classList.remove('hidden');
        document.getElementById('final-score').innerText = this.finalScore;

        const generateBtn = document.getElementById('btn-generate-card');

        // Remove old listeners if they exist to prevent duplicates
        const newBtn = generateBtn.cloneNode(true);
        generateBtn.parentNode.replaceChild(newBtn, generateBtn);

        newBtn.addEventListener('click', () => {
            const name = document.getElementById('citizen-name').value || 'عريس مجهول';
            const fileInput = document.getElementById('citizen-photo');
            let photoUrl = null;

            if (fileInput.files && fileInput.files[0]) {
                photoUrl = URL.createObjectURL(fileInput.files[0]);
            }

            uiForm.classList.add('hidden');
            this.generateCard(name, this.finalScore, photoUrl);
        });

        const restartBtn = document.getElementById('btn-restart');
        const newRestartBtn = restartBtn.cloneNode(true);
        restartBtn.parentNode.replaceChild(newRestartBtn, restartBtn);

        newRestartBtn.addEventListener('click', () => {
            document.getElementById('ui-card-result').classList.add('hidden');
            this.scene.start('MainMenuScene');
        });

        const downloadBtn = document.getElementById('btn-download');
        const newDownloadBtn = downloadBtn.cloneNode(true);
        downloadBtn.parentNode.replaceChild(newDownloadBtn, downloadBtn);

        newDownloadBtn.addEventListener('click', () => {
            const canvas = document.getElementById('card-canvas');
            const link = document.createElement('a');
            link.download = 'barq_citizen_card.png';
            link.href = canvas.toDataURL();
            link.click();
        });
    }

    generateCard(name, score, photoUrl) {
        const uiResult = document.getElementById('ui-card-result');
        uiResult.classList.remove('hidden');

        const shareText = "لقد تم رفضي من الملكة في كوكب برق البرق برصيد " + score + " نقطة فقط! من يتحداني؟";
        let pText = document.getElementById('share-text');
        if (pText) {
            pText.innerText = shareText;
        }

        const canvas = document.getElementById('card-canvas');
        const ctx = canvas.getContext('2d');

        // Use template 1 as base
        const template = new Image();
        template.src = '/assets/images.jpg';
        template.onload = () => {
            canvas.width = template.width;
            canvas.height = template.height;
            ctx.drawImage(template, 0, 0);

            // Draw Texts (adjust coordinates based on the template structure)
            ctx.fillStyle = '#C71585'; // Deep Pink
            ctx.font = 'bold 30px Tahoma';
            ctx.textAlign = 'center';

            // Write Name
            ctx.fillText(name, canvas.width / 2, canvas.height - 100);

            // Write Score
            ctx.fillStyle = '#FFFFFF';
            ctx.font = 'bold 40px Tahoma';
            ctx.fillText(score.toString(), canvas.width * 0.75, canvas.height / 2);

            // Draw Photo if provided
            if (photoUrl) {
                const userImg = new Image();
                userImg.onload = () => {
                    // Draw circular image on the left side (approximate coordinates)
                    ctx.save();
                    ctx.beginPath();
                    // Assuming portrait placeholder is around x: 200, y: 250, radius: 100
                    ctx.arc(150, 250, 100, 0, Math.PI * 2, true);
                    ctx.closePath();
                    ctx.clip();
                    ctx.drawImage(userImg, 50, 150, 200, 200); // Scale to fit
                    ctx.restore();

                    // Draw border around image
                    ctx.beginPath();
                    ctx.arc(150, 250, 100, 0, Math.PI * 2, true);
                    ctx.lineWidth = 10;
                    ctx.strokeStyle = '#FFD700';
                    ctx.stroke();
                };
                userImg.src = photoUrl;
            }
        };
    }
}