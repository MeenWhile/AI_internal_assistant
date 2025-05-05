# Setup
1. Create Virtual Environment
```bash
virtualvenv venv
```
2. Use Virtual Environment
```bash
venv\Scripts\activate
```
3. Install dependencies from requirements.txt
```bash
pip install -r requirements.txt
```
4. Create .env file and add your OPENAI_API_KEY:
```text
OPENAI_API_KEY=your-api-key-here
```

# Run
1. Run application with Uvicorn (for development)
```bash
uvicorn main:app --reload
```

# Docker
1. Create Docker image
```bash
docker build -t internal-ai-assistant .
```
2. Run Docker container and load .env file for API key
```bash
docker run --env-file .env -p 8000:8000 internal-ai-assistant
```
