# Instalily AI Agent 🧠🔧

This project is an AI-powered customer support agent designed for [PartSelect](https://www.partselect.com), focused on answering user queries about refrigerator and dishwasher parts — including installation instructions, compatibility, and troubleshooting.

---

## 🚀 Features

- Conversational AI assistant (powered by GPT-3.5)
- Intelligent part lookup using vector search (OpenAI Embeddings + FAISS)
- Frontend built with React
- FastAPI backend for chat handling and retrieval
- Web scraping module for extracting part information

---

## 🛠️ Project Structure

instalily-AI-agent/
├── backend/ # FastAPI server + vector search
├── frontend/ # React chat interface
├── scraping/ # Web scraper for part info
├── .env # Your local environment variables (not tracked)
├── requirements.txt # Python dependencies



---

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/LizZhangxiaoying/instalily-AI-agent.git
cd instalily-AI-agent
```

### 2. (Optional but Recommended) Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```
### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```
### 4. Setup Environment Variables
Create a .env file in the root or backend directory:
```bash
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
⚠️ Make sure .env is listed in .gitignore and never committed.

### 5. Run the Backend Server
```bash
cd backend
uvicorn main:app --reload
```
It will run on: http://127.0.0.1:8000

### 6. Start the Frontend (React)
```bash
cd ../frontend
npm install
npm start
```
This runs the frontend on: http://localhost:3000

## 💡 Example Queries
- “How can I install part number PS11752778?”
- “Is this part compatible with WDT780SAEM1?”
- “The ice maker on my Whirlpool fridge is not working.”
  
## 🧪 Demo
https://www.loom.com/share/d3355e373fee4df7b57f55f98a445083?sid=6ed56eda-7c4f-4346-ae4e-9a1554e77c3c

## 📚 Technologies Used
🧠 OpenAI GPT-3.5 + Embeddings
🔍 FAISS (vector similarity search)
⚙️ FastAPI (Python backend)
💻 React (frontend UI)
🕷️ BeautifulSoup + Selenium (web scraping)
🌐 GitHub + VS Code for development








