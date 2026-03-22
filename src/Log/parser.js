const fs = require('fs');

function parseLogs(filePath) {
  if (!fs.existsSync(filePath)) {
    return {
      errorCount: 0,
      avgLatency: 0
    };
  }

  const data = fs.readFileSync(filePath, 'utf-8');
  const lines = data.split('\n');

  let errorCount = 0;
  let latencySum = 0;
  let latencyCount = 0;

  lines.forEach(line => {
    if (line.includes('ERROR')) errorCount++;

    const match = line.match(/Latency=(\d+)ms/);
    if (match) {
      latencySum += parseInt(match[1]);
      latencyCount++;
    }
  });

  return {
    errorCount,
    avgLatency: latencyCount ? latencySum / latencyCount : 0
  };
}