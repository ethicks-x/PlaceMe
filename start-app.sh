#!/usr/bin/bash 

ESC=$(printf '\033')

# Color Mapping ANSI
NC="${ESC}[0m"
WHITE="${ESC}[0;37m"
RED="${ESC}[0;31m"
GREEN="${ESC}[0;32m"
YELLOW="${ESC}[0;33m"
CYAN="${ESC}[0;36m"
BOLD_CYAN="${ESC}[1;36m"
BOLD_RED="${ESC}[1;31m"
BOLD_GREEN="${ESC}[1;32m"
DIM_WHITE="${ESC}[2;37m"

cleanup() {
    echo -e "\n Shutting down all services..."
    kill $(jobs -p) 2>/dev/null
    docker stop redis-celery > /dev/null
    docker container rm redis-celery > /dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

echo "${BOLD_CYAN}Starting Project..${NC}"
sleep 2

echo "${WHITE}---------------------------------------------------${NC}"
echo "${DIM_WHITE}Installing backend dependencies..${NC}"
cd backend
uv sync
cd ..

echo "${WHITE}---------------------------------------------------${NC}"
echo "${DIM_WHITE}Installing frontend dependencies..${NC}"
cd frontend
bun install
cd ..

echo "${WHITE}---------------------------------------------------${NC}"
echo "${DIM_WHITE}Starting Redis..${NC}"
if redis-cli ping &>/dev/null; then
    echo "${DIM_WHITE}Redis already running.${NC}"
else
    docker run --name redis-celery -p 6379:6379 -d redis:8-alpine > /dev/null &
    REDIS_PID=$!
    sleep 2
fi 

echo "${WHITE}---------------------------------------------------${NC}"
echo "${DIM_WHITE}Starting Celery worker..${NC}"
cd backend
uv run celery -A utils.celery_app.celery worker --loglevel=info &>/dev/null &
WORKER_PID=$!
cd ..
sleep 2

echo "${WHITE}---------------------------------------------------${NC}"
echo "${DIM_WHITE}Firing up backend..${NC}"
cd backend 
uv run app.py &>/dev/null &
BACKEND_PID=$!
cd ..
sleep 2

echo "${WHITE}---------------------------------------------------${NC}"
echo "${DIM_WHITE}Populating Database...${NC}"
cd backend
uv run utils/seed.py
cd ..
sleep 2

clear
echo "${WHITE}---------------------------------------------------${NC}"
echo "${DIM_WHITE}Starting Frontend...${NC}"
cd frontend 
bun run dev &>/dev/null &
FRONTEND_PID=$!
cd ..

sleep 5

# Health Check
BACKEND_RUNNING=$(ps -p $BACKEND_PID -o state= 2>/dev/null)
FRONTEND_RUNNING=$(ps -p $FRONTEND_PID -o state= 2>/dev/null)
WORKER_RUNNING=$(ps -p $WORKER_PID -o state= 2>/dev/null)

if [ -z "$WORKER_RUNNING" ]; then 
    echo "${BOLD_RED}Celery Worker failed to start!${NC}"
    cleanup
fi

if [ -z "$BACKEND_RUNNING" ]; then 
    echo "${BOLD_RED}Backend failed to start!${NC}"
    cleanup
fi

if [ -z "$FRONTEND_RUNNING" ]; then 
    echo "${BOLD_RED}Frontend failed to start!${NC}"
    cleanup
fi

clear
echo "${BOLD_CYAN}---------------------------------------------------${NC}"
echo "${BOLD_CYAN}All services have been started succesfully!${NC}"
echo "${BOLD_GREEN}Check http://localhost:5173 in your browser.${NC}"
echo "${BOLD_CYAN}---------------------------------------------------${NC}"

while true; do
    sleep 1
done
