# Set environment variables
export POSTGRES_HOST="localhost"
export POSTGRES_DB="trips"
export POSTGRES_USER="trips"
export POSTGRES_PASSWORD="password"
export REDIS_URL="redis://localhost:6379"


# Remove containers
docker rm -f redis-trips postgres-trips-db

# Postgresql
docker run --name postgres-trips-db \
    --env-file env \
    -p 5432:5432 \
    -d postgres

# Redis
docker run --name redis-trips \
    --env-file env \
    -p 6379:6379 \
    -d redis redis-server \
