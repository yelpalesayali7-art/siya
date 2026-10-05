from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .models import ChatMessage

import google.generativeai as genai


# Gemini API Configure
genai.configure(
    api_key=settings.GEMINI_API_KEY
)

# Gemini Model
model = genai.GenerativeModel(
    "gemini-3.8-flash"
)


@login_required
def chat_home(request):

    if request.method == "POST":

        user_message = request.POST.get("message")

        if user_message:

            try:

                response = model.generate_content(
                    f"""
                    You are Siya AI.

                    Rules:
                    - Always introduce yourself as Siya AI.
                    - Never say you are Gemini.
                    - Reply in a helpful and friendly way.
                    - Answer clearly and professionally.
                    - If the user greets you, greet them as Siya AI.

                    User Question:
                    {user_message}
                    """
                )

                bot_response = response.text

            except Exception as e:

                error_text = str(e)

                if "429" in error_text:
                    bot_response = (
                        "⚠ Siya AI is temporarily busy. "
                        "Please wait 1 minute and try again."
                    )

                elif "API_KEY_INVALID" in error_text:
                    bot_response = (
                        "⚠ Invalid Gemini API Key. "
                        "Please check your API configuration."
                    )

                elif "404" in error_text:
                    bot_response = (
                        "⚠ AI model not found. "
                        "Please check model configuration."
                    )

                else:
                    bot_response = (
                        f"⚠ Error: {error_text}"
                    )

            ChatMessage.objects.create(
                user=request.user,
                user_message=user_message,
                bot_response=bot_response
            )

    messages = ChatMessage.objects.filter(
        user=request.user
    ).order_by("created_at")

    return render(
        request,
        "chatbot/chat.html",
        {
            "messages": messages
        }
    )