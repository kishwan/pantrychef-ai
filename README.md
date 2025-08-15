# PantryChef: Your Smart Recipe Assistant

Ever stare into your fridge and wonder what to cook? **PantryChef** has you covered! This full-stack web app takes the ingredients you have on hand and serves up delicious recipe ideas. But it’s more than just a search tool—it’s your personal kitchen assistant, ready to answer all your cooking questions.

## Features

- **Find Recipes by Ingredients**  
  Enter the ingredients you have, and PantryChef will suggest recipes you can make.

- **Detailed Recipe Guides**  
  Get step-by-step instructions, along with recipe category and origin information.

- **Ask the AI Chef**  
  Have questions about substitutions, dietary tweaks, or cooking tips? Ask, and get personalized advice.


## Tech Stack

### Backend (Python + FastAPI)
- **Python 3.9+**
- **FastAPI**
- **Uvicorn**
- **httpx**
- **Pydantic**
- **python-dotenv**

### AI Integration
- **Hugging Face Inference API**
  - [**HuggingFaceTB/SmolLM2-1-1.7B-Instruct**](https://huggingface.co/HuggingFaceTB/SmolLM2-1.7B-Instruct)

### Recipe Data
- [**TheMealDB API**](https://www.themealdb.com/api.php) – source of recipe data.

### Frontend (React)
- **React**
- **HTML & CSS**
- **JavaScript**

---

## Getting Started

Here’s how to run PantryChef locally:

### Prerequisites
- **Python 3.9+**: [Download](https://www.python.org/)
- **Node.js & npm**  
  - Windows: Use [nvm-windows](https://github.com/coreybutler/nvm-windows/releases)  
  - macOS/Linux: Use [nvm](https://github.com/nvm-sh/nvm)  
- **Hugging Face API Token**
- **TheMealDB API Token**

---

### 1. Backend Setup

```bash
cd pantrychef-ai/backend
python -m venv .venv

# Windows PowerShell
.\.venv\Scripts\activate.ps1
# Windows CMD
.\.venv\Scripts\activate.bat
# macOS/Linux or Git Bash
source .venv/bin/activate
```

Create a .env file in backend/ with your keys:

```
# backend/.env
THEMEALDB_API_KEY="YOUR_MEALDB_TOKEN"
HF_API_TOKEN="hf_YOUR_HUGGING_FACE_TOKEN_HERE"
```

Install dependencies:

```
pip install -r requirements.txt
```

Run the backend:

**From the top-level project folder**
```
uvicorn backend.main:app --reload
```

Your backend will now run at http://127.0.0.1:8000.

### 2. Frontend Setup
Open a new terminal and go to the frontend folder
```
cd pantrychef-ai/frontend
npm install 
npm start
```

Your browser should open http://localhost:3000.

### How to Use

1. Open your browser to http://localhost:3000.

2. Enter ingredients (e.g., chicken, rice, onions) and click Find Recipes.

3. Browse recipes from TheMealDB.

4. Got a question about a recipe? Type it in the Ask about this recipe… box and hit Ask AI to get instant advice.