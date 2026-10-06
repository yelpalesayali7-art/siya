from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required

from .models import Document
from .utils import extract_pdf_text

from chatbot.views import model


@login_required
def documents_home(request):

    if request.method == "POST":

        pdf = request.FILES.get("pdf")

        if pdf:

            Document.objects.create(
                user=request.user,
                file=pdf
            )

            return redirect("/documents/")

    documents = Document.objects.filter(
        user=request.user
    ).order_by("-uploaded_at")

    return render(
        request,
        "documents/home.html",
        {
            "documents": documents
        }
    )


@login_required
def delete_document(request, doc_id):

    document = get_object_or_404(
        Document,
        id=doc_id,
        user=request.user
    )

    document.delete()

    return redirect("/documents/")


@login_required
def pdf_summary(request, doc_id):

    document = get_object_or_404(
        Document,
        id=doc_id,
        user=request.user
    )

    pdf_text = extract_pdf_text(
        document.file.path
    )

    prompt = f"""
    You are Siya AI.

    Summarize the following PDF:

    {pdf_text}
    """

    try:

        response = model.generate_content(
            prompt
        )

        summary = response.text

    except Exception as e:

        summary = f"Error: {str(e)}"

    return render(
        request,
        "documents/summary.html",
        {
            "document": document,
            "summary": summary
        }
    )