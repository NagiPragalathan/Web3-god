module.exports = {
    apps: [
      {
        name: 'django_app',
        script: 'manage.py',
        args: 'runserver 0.0.0.0:80',
        interpreter: '/root/Web3-god/suzuka_backend/venv/bin/python',
        instances: 1,
        autorestart: true,
        watch: false,
        max_memory_restart: '1G',
        env: {
          DJANGO_SETTINGS_MODULE: 'suzuka_backend.settings',
          PYTHONUNBUFFERED: '1',
        },
      },
    ],
  };
  