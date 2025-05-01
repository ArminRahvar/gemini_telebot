# 🤖 gemini_telebot

A powerful PDF and voice assistant chatbot built with Python, Gemini AI, and FAISS. Users can upload PDFs, ask context-aware questions, or use voice messages for natural interaction.

![Python](https://img.shields.io/badge/python-3.10+-blue?style=flat-square)
![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue?style=flat-square)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## ✨ Features

- 📄 **PDF Q&A** — Upload a PDF and ask questions about its content.
- 🔊 **Voice Support** — Send voice messages and receive intelligent replies.
- 🧠 **Gemini AI Integration** — Powered by Google's Gemini API for accurate answers.
- 📚 **FAISS Embedding Indexing** — Efficient question answering using vector similarity.
- 🧩 **Modular Codebase** — Cleanly separated logic for easy maintenance and scalability.   

---
<!-- 
## 📸 Demo

| Upload PDF | Ask Questions | Voice Commands |
|------------|----------------|----------------|
| ![upload_pdf](https://user-images.githubusercontent.com/your-upload-pdf.png) | ![ask_question](https://user-images.githubusercontent.com/your-ask-question.png) | ![voice_command](https://user-images.githubusercontent.com/your-voice-command.png) |

> Replace the above demo images with real screenshots or GIFs of your bot in action.

--- -->

---
## 🛠 How to Run

1. **Set your Telegram bot token as an environment variable**:


```
export BOT_TOKEN=<your_telegram_bot_token>
```

2. **Add `src` to `PYTHONPATH`**:
```
export PYTHONPATH=${PWD}
```

3. Run:
```
python src/run.py

```
```bash
## 📁 Project Structure

gemini_telebot/
├── files/                     # Uploaded PDFs and voice files
├── src/
│   ├── bot.py                 # Main telebot instance
│   ├── run.py                # Entry point
│   ├── constant/             # Static values like buttons, states
│   ├── gemini_chat.py        # ask_gemini & voice_gemini integrations
│   └── utils/
│       ├── text_handler.py   # PDF text extraction, chunking, embedding, FAISS

```