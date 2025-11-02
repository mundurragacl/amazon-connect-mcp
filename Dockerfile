FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir .

COPY src/ src/

EXPOSE 8000

CMD ["fastmcp", "run", "src/amazon_connect_mcp/server.py", "--transport", "streamable-http", "--host", "0.0.0.0", "--port", "8000"]
