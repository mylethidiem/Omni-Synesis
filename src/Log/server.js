// src/server.js
// Express server to serve metrics and health check endpoints
const express = require('express');
const getMetrics = require('./metrics');
const port = process.env.PORT || 3000;

const app = express();

app.get('/metrics', (req, res) => {
  const metrics = getMetrics();
  res.json(metrics);
});

app.get('/health', (req, res) => {
  res.status(200).json(
    {
      status: 'UP',
      timestamp: process.uptime(),
      timestamp: Date.now()
    }
  )
});
app.get('/', (req, res) => {
  res.send(`
    <html>
      <head>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
      </head>
      <body class="container mt-5 text-center">
        <h1>Welcome to the Game Log Metrics Server!</h1>
        <div class="mt-4">
          <a href="/health" class="btn btn-success me-2">Check Health</a>
          <a href="/metrics" class="btn btn-primary">View Metrics</a>
        </div>
      </body>
    </html>
  `);
});

app.listen(port, () => {
  console.log(`Server running on port ${port}: http://localhost:${port}`);
});