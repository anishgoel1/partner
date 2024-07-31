const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();
const PORT = 3000;

app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'templates')));

// Proxy middleware configuration
const pythonApiProxy = createProxyMiddleware('/send_message', {
    target: 'http://localhost:5000',
    changeOrigin: true,
});

// Use the proxy middleware for /send_message route
app.use('/send_message', pythonApiProxy);

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates', 'index.html'));
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
    console.log(`Proxying /send_message requests to Python server at http://localhost:5000`);
});