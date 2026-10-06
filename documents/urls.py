from django.urls import path
from .views import (
    documents_home,
    delete_document,
    pdf_summary
)

urlpatterns = [

    path(
        '',
        documents_home,
        name='documents'
    ),

    path(
        'delete/<int:doc_id>/',
        delete_document,
        name='delete_document'
    ),

    path(
        'summary/<int:doc_id>/',
        pdf_summary,
        name='pdf_summary'
    ),

]