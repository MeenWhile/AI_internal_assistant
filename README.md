# Setup
1. สร้าง Virtual Environment
```bash
virtualvenv venv
```
2. เปิดใช้งาน Virtual Environment
```bash
venv\Scripts\activate
```
3. ติดตั้ง dependencies จาก requirements.txt
```bash
pip install -r requirements.txt
```
4. สร้างไฟล์ .env และใส่ OPENAI_API_KEY ของคุณลงไป:
```text
OPENAI_API_KEY=your-api-key-here
```

# Run
1. เริ่มต้นแอปพลิเคชันด้วย Uvicorn (สำหรับพัฒนา)
```bash
uvicorn main:app --reload
```

# Docker
1. สร้าง Docker image
```bash
docker build -t internal-ai-assistant .
```
2. รัน Docker container และโหลดไฟล์ .env สำหรับตัวแปร API key
```bash
docker run --env-file .env -p 8000:8000 internal-ai-assistant
```
docker run --env-file .env -p 8000:8000 internal-ai-assistant
