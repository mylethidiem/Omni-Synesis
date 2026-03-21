// src/server.js
// Express server to serve metrics and health check endpoints
const express = require('express');
const getMetrics = require('./metrics');

const app = express();

app.get('/metrics', (req, res) => {
  const metrics = getMetrics();
  res.json(metrics);
});

app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});