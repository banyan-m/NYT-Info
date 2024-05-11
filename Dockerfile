# Start from the Python 3.8 image
FROM mcr.microsoft.com/vscode/devcontainers/python:0-3.8

# Install SQLite3
RUN apt-get update && apt-get install -y sqlite3