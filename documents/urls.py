from django.urls import path
from .views import documents_home, delete_document

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

]