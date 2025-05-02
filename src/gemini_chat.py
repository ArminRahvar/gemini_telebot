from google import genai
from llmbot.gemini_bot.gemini_telebot.src.bot_token import gemini_api_key

# Configure your Gemini API key
client = genai.Client(api_key=gemini_api_key)

def ask_gemini(question, context=None):
    
    if context:
        prompt = f"Use the following context to answer the question.\n\nContext:\n{context}\n\nQuestion: {question}"
    else:
        prompt = question
    try:
        response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[{"text": prompt}],
)
        return response.text
    except Exception as e:
        return f"Error using Gemini API: {e}"


def voice_gemini(voice,transcript=False, voice_prompt=None):
    print(f"User {voice} sent a voice message2.")

    myfile = client.files.upload(file=voice)
    try:
        if voice_prompt:
            prompt = voice_prompt
        elif transcript:
            prompt = 'Generate a transcript of the speech'
        else:
            prompt = 'Generate a response to the speech.'

        response = client.models.generate_content(
        model="gemini-2.0-flash",
       contents=[
                {"text": prompt},
                myfile  # already a File object
            ],
)
        print(response.text)
        return response.text
    except Exception as e:
        return f"Error using Gemini API: {e}"

