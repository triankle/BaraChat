#!/bin/bash
# Development helper script to run server and client

case "$1" in
    server)
        echo "Starting BaraChat server..."
        cd server && python main.py
        ;;
    client)
        echo "Starting BaraChat client..."
        cd client && python main.py
        ;;
    test)
        echo "Running tests..."
        pytest tests/
        ;;
    *)
        echo "Usage: $0 {server|client|test}"
        echo ""
        echo "  server  - Start the server"
        echo "  client  - Start the client GUI"
        echo "  test    - Run tests"
        exit 1
        ;;
esac

