from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from chatbot.models import ChatMessage
from documents.models import Document


@login_required
def dashboard_home(request):

    total_chats = ChatMessage.objects.filter(
        user=request.user
    ).count()

    total_users = User.objects.count()

    total_documents = Document.objects.filter(
        user=request.user
    ).count()

    context = {
        "total_chats": total_chats,
        "total_users": total_users,
        "total_documents": total_documents,
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )