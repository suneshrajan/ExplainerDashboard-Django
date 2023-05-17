from django.urls import path
from internal_chat import views as ic_views

urlpatterns = [
    path('load-document', ic_views.load_chat_document, name='Load chat document'),
    path('train-doc-chat', ic_views.train_doc_chat_model, name='Train chat document with NLP'),
    # path('', ic_views.doc_chat, name='Display Dashboard'),
    # path('stop-explainer-dashboard', ic_views.stop_dashboard, name='Hide Dashboard')
]