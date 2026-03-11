# Zemu AI — Sikkim Tourism Chatbot

Zemu AI is an intelligent tourism assistant designed to help travelers explore the beautiful state of **Sikkim, India**. The chatbot provides information about tourist destinations, culture, travel tips, and recommendations through an AI-powered conversational interface.

The project uses a **Retrieval-Augmented Generation (RAG)** architecture to provide accurate and contextual responses based on tourism-related data.

---

## 🚀 Features

* 🤖 AI-powered travel chatbot for Sikkim tourism
* 🏔️ Provides information about tourist destinations and travel tips
* 🗣️ Voice input support
* 🔊 Text-to-speech responses
* 🌐 Multi-language support (English, Hindi, Nepali, Bengali)
* 💬 Modern chat interface with thinking indicator
* 🧠 Retrieval-Augmented Generation (RAG) for better answers
* ⚡ Fast responses using Groq API
* 🎨 Custom landing page UI

---

## 🧠 How It Works

1. The user asks a travel-related question.
2. The system searches relevant documents using **vector embeddings stored in ChromaDB**.
3. Retrieved context is sent to the **LLM through the Groq API**.
4. The model generates a contextual response.
5. The response is displayed in the chat interface and can optionally be spoken using text-to-speech.

---

## 🛠 Tech Stack

### Backend

* Python
* Flask
* ChromaDB
* Sentence Transformers
* Groq API
* Deep Translator

### Frontend

* HTML
* CSS
* JavaScript
* Web Speech API

### AI / NLP

* Retrieval-Augmented Generation (RAG)
* Vector embeddings

---

## 📂 Project Structure

zemu-ai-sikkim-chatbot
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates
│   ├── landing.html
│   └── chat.html
│
├── static
│   └── images
│
└── chroma_db

---

## ⚙️ Installation

### 1. Clone the repository

git clone https://github.com/yourusername/zemu-ai-sikkim-chatbot.git
cd zemu-ai-sikkim-chatbot

### 2. Install dependencies

pip install -r requirements.txt

### 3. Add API Key

Create a `.env` file in the project root:

GROQ_API_KEY=your_api_key_here

### 4. Run the application

python app.py

### 5. Open in your browser

http://localhost:5000

---

## 💡 Example Queries

You can ask the chatbot questions like:

* Best places to visit in Sikkim
* Tell me about Nathula Pass
* Tourist attractions in Gangtok
* Best time to visit Sikkim
* Local food in Sikkim

---

## 🌍 Future Improvements

* Deploy the chatbot online
* Add more tourism datasets
* Improve UI animations and chat experience
* Add tourist destination image recommendations
* Integrate maps for travel suggestions
* Support additional languages

---

## 👨‍💻 Author

Mukul

GitHub: https://github.com/yourusername

---

## ⭐ Support

If you like this project, consider giving it a **star on GitHub**.
