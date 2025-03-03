docker-compose up --build -d
sleep 1
docker-compose -f docker-compose.yml up -d 
docker system prune -af
sleep 5