#!/bin/sh

set -e

# Parse host and port
hostport="$1"
shift

# Use POSIX-compatible parameter expansion
host="${hostport%%:*}"
port="${hostport##*:}"

if [ -z "$host" ] || [ -z "$port" ]; then
  echo "Invalid host:port - received '$hostport'"
  exit 1
fi

echo "Waiting for database at $host:$port..."

# Wait for host:port to be reachable
while ! nc -z "$host" "$port"; do
  sleep 1
done

echo "Database is up at $host:$port"
exec "$@"
