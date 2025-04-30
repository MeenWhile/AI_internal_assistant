# Setup
virtualvenv venv
venv\Scripts\activate
pip install -r requirements.txt
create .env file with OPENAI_API_KEY

# Run

uvicorn main:app --reload

# Docker

docker build -t internal-ai-assistant .
docker run --env-file .env -p 8000:8000 internal-ai-assistant
