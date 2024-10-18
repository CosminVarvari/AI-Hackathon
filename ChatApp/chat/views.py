from django.shortcuts import render, redirect
from openai import OpenAI

from django.http import JsonResponse
from django.conf import settings
from django.http import JsonResponse
import json
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def chatPage(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login-user")
    context = {}
    return render(request, "chat/chatPage.html", context)


def translate_messages(messages, target_language):
    """
    Funcția care traduce o listă de mesaje în limba dorită folosind OpenAI API.
    """
    translated_messages = []

    for message in messages:
        print(f"Original message: {message['message']}")  
        try:
           
            response = client.chat.completions.create(model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": f"Translate all messages and don`t add anything to them, to {target_language}."},
                {"role": "user", "content": message['message']}
            ])
            translated_text = response.choices[0].message.content.strip()
            print(f"Translated message: {translated_text}") 
            translated_messages.append({
                'username': message['username'],
                'message': translated_text
            })
        except Exception as e:
            print(f"Error translating message: {str(e)}")

    return translated_messages

def translate_chat_view(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            messages = body.get('messages', [])
            target_language = body.get('language', 'en')  
            print(f"Received messages: {messages}")  
            if not messages:
                return JsonResponse({'error': 'No messages provided'}, status=400)


            translated_messages = translate_messages(messages, target_language)

            return JsonResponse({'translated_messages': translated_messages}, status=200)
        except Exception as e:
            print(f"Error in translation: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)