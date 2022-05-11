set -e

if [ -f /src/app/main.py ]; then
    DEFAULT_MODULE_NAME=app.main
elif [ -f /app/main.py ]; then
    DEFAULT_MODULE_NAME=main
fi
MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
VARIABLE_NAME=${VARIABLE_NAME:-app}
export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}

HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8001}
LOG_LEVEL=${LOG_LEVEL:-info}


exec uvicorn --reload --debug --host $HOST --port $PORT --use-colors --log-level debug "$APP_MODULE" --proxy-headers --forwarded-allow-ips='127.0.0.1,[::1]'