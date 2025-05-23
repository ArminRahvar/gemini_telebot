import os
import emoji
import numpy as np
from functools import partial
from src.constant import keyboards, keys, states
from sentence_transformers import SentenceTransformer
from src.gemini_chat import ask_gemini,voice_gemini
from src.utils.text_handler import extract_text_from_pdf,chunk_text,embed_chunks,build_faiss_index,model
from src.bot_token import bot



class Bot:
    user_data = {}  # Stores chunks & faiss index per user

    def __init__(self, telebot):
        self.bot = telebot
        # register handler
        self.handlers()
        self.conversation = {}
        # run Bot
        self.bot.infinity_polling(timeout=300, long_polling_timeout=120)


    def handlers(self):
    # --- TELEGRAM HANDLERS ---
        @self.bot.message_handler(commands=["start"])
        def send_welcome(message):
            print(f"User {message.from_user.username} started the bot.")
            self.bot.reply_to(message, "Hi! I'm your gemini-powered chatbot",
            reply_markup=keyboards.main)
            self.bot.send_message(message.chat.id, "Just type a message and I'll reply.",
                            reply_markup=keyboards.main_inline)

        @self.bot.message_handler(content_types=["document"])
        def handle_pdf(message):
            if message.document.mime_type != "application/pdf":
                self.bot.reply_to(message, "Please send a valid PDF file.")
                return

            file_info = self.bot.get_file(message.document.file_id)
            downloaded = self.bot.download_file(file_info.file_path)

            os.makedirs("files", exist_ok=True)
            file_path = f"files/{message.chat.id}.pdf"
            with open(file_path, "wb") as f:
                f.write(downloaded)

            self.bot.reply_to(message, "Processing your PDF...")

            # Process
            text = extract_text_from_pdf(file_path)
            chunks = chunk_text(text)
            embeddings = embed_chunks(chunks)
            index = build_faiss_index(np.array(embeddings))

            self.user_data[message.message_id] = {
                "chunks": chunks,
                "index": index
            }

            self.bot.send_message(message.chat.id, "PDF loaded! Now ask me something about it.")

        @self.bot.message_handler(func=lambda message: True)
        def handle_question(message):
            if message.reply_to_message and message.reply_to_message.message_id in self.user_data:
                # This is a reply to a PDF message
                pdf_info = self.user_data[message.reply_to_message.message_id]
                question = message.text
                q_embedding = model.encode([question])
                D, I = pdf_info["index"].search(np.array(q_embedding), k=3)
                relevant_chunks = [pdf_info["chunks"][i] for i in I[0]]
                context = "\n\n".join(relevant_chunks)

                answer = ask_gemini(question, context)
                self.send_large_message(message.chat.id, answer)
                # self.bot.send_message(message.chat.id, answer)
            else:
                # Limit context size to 10 messages
                self.conversations[message.chat.id] = self.conversations[message.chat.id][-10:]
                
                # No PDF context: fallback to regular chat
                question = message.text
                answer = ask_gemini(question, self.conversation[message.chat.id])
                self.save_conversation(chat_id=message.chat.id, question=question, answer=answer)
                self.send_large_message(message.chat.id, answer)
                # self.bot.send_message(message.chat.id, answer)

        @self.bot.message_handler(content_types=["voice"])
        def handle_voice_message(message):
            if not states.voice:
                self.bot.reply_to(message, "to send voices Please press voice butoon first.", reply_markup=keyboards.main_inline)
                return
            else:
                print(f"User {message.from_user.username} sent a voice message.")
                file_info = self.bot.get_file(message.voice.file_id)
                file_path = f"files/{message.chat.id}.ogg"
                downloaded = self.bot.download_file(file_info.file_path)
                with open(file_path, "wb") as f:
                    f.write(downloaded)

                # Process the voice message
                if states.voice_prompt:
                    self.bot.send_message(message.chat.id, "Please enter your prompt:")
                    handler = partial(self.save_prompt, file_path=file_path, transcript=states.transcript)
                    self.bot.register_next_step_handler(message, handler)
                else:
                    voice_prompt = False
                    answer = voice_gemini(voice=file_path, transcript=states.transcript, voice_prompt=states.voice_prompt)
                    self.send_large_message(message.chat.id, answer)
                # self.bot.reply_to(message, answer)



        @self.bot.callback_query_handler(func=lambda call: True)
        def handle_voice(call):
            if call.data == emoji.emojize(keys.audio):
                states.voice = True
                self.bot.answer_callback_query(call.id, "Please send a voice message.")
                self.bot.edit_message_reply_markup(
                                                chat_id=call.message.chat.id,
                                                message_id=call.message.message_id,
                                                reply_markup=keyboards.voice
                                                )


            if call.data == emoji.emojize(keys.enable_transcription):
                states.transcript = True
                self.bot.answer_callback_query(call.id, "Transcription enabled.")

            if call.data == emoji.emojize(keys.disable_transcription):
                states.transcript = False
                self.bot.answer_callback_query(call.id, "Transcription disabled.")
            if call.data == emoji.emojize(keys.enable_prompt):
                states.voice_prompt = True
                self.bot.answer_callback_query(call.id, "voice prompt enabled")
            if call.data == emoji.emojize(keys.disable_prompt):
                states.voice_prompt = False
                self.bot.answer_callback_query(call.id, "voice prompt disabled")

            if call.data == emoji.emojize(keys.back):
                self.bot.edit_message_reply_markup(
                                                chat_id=call.message.chat.id,
                                                message_id=call.message.message_id,
                                                reply_markup=keyboards.main_inline
                                            )
                self.bot.send_message(call.message.chat.id, "Cancelled.")

    def save_prompt(self, message, file_path, transcript):
        user_prompt = message.text
        answer = voice_gemini(voice=file_path, transcript=transcript, voice_prompt=user_prompt)
        self.send_large_message(message.chat.id, answer)

    def send_large_message(self, chat_id, text):
        MAX_MESSAGE_LENGTH = 4096
        for i in range(0, len(text), MAX_MESSAGE_LENGTH):
            self.bot.send_message(chat_id, text[i:i+MAX_MESSAGE_LENGTH])

    def save_conversation(self, chat_id, question, answer):
        if chat_id not in self.conversation:
            self.conversation[chat_id] = []

        self.conversations[chat_id].extend({
            "role": "user",
            "parts": [{"text": question}]
        },
        { 
            "role": "model",
            "parts": [{"text": answer}]
        })
        print(self.conversation)
# --- RUN ---
if __name__ == "__main__":
    print("Bot is running...")
    gemini_bot = Bot(telebot=bot)

