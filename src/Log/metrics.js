// src/metrics.js
const parseLogs = require('./parser');

function getMetrics() {
  const result = parseLogs('./logs/game.log');

  return {
    errors: result.errorCount,
    avgLatency: result.avgLatency
  };
}

module.exports = getMetrics;