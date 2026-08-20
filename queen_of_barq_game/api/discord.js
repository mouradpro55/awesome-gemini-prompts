export const config = {
  api: {
    bodyParser: false, // Disallow body parsing, consume as stream
  },
};

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  try {
    // Forward the raw request to Discord webhook
    const discordWebhookUrl = 'https://discordapp.com/api/webhooks/1503536005402329148/xyNGmOqvEWRyrKSO2mLx1Kk-A2ZwEo4RxZfOubwhh1EeaWUzGQaMwpUvFXIka-2DTUw4';

    // We need to consume the incoming stream and send it to Discord
    // Since we disabled the body parser, req is an incoming stream
    const response = await fetch(discordWebhookUrl, {
      method: 'POST',
      headers: {
        'Content-Type': req.headers['content-type'],
        'Content-Length': req.headers['content-length'],
      },
      body: req,
      duplex: 'half'
    });

    if (response.ok) {
      return res.status(200).json({ success: true });
    } else {
      const errorText = await response.text();
      return res.status(response.status).json({ error: 'Discord API error', details: errorText });
    }
  } catch (error) {
    console.error('Error forwarding to Discord:', error);
    return res.status(500).json({ error: 'Internal Server Error' });
  }
}
