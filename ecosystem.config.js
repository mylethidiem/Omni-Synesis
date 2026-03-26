module.exports = {
  apps: [{
    name: 'speech-api',
    script: 'npm',
    args: 'start',
    exec_mode: 'fork', // need explicitly declare mode otherwise it will fallback to cluster mode and cause infinite reload
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G'
  }],
}