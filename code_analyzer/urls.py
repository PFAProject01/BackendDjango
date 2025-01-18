from django.urls import path
from . import views
from . import viewGemini

urlpatterns = [
    path('extract_text/', views.extract_text, name='extract_text'),
    path('visionAPI/', viewGemini.extract_text_google_vision, name='visionAPI'),
    path('visionAPIig/', viewGemini.extract_text_google_visionig, name='visionAPIig'),
    path('visionAPIFR/', viewGemini.extract_text_google_visionFR, name='visionAPIFR'),
    path('extract_text4/', viewGemini.extract_text4, name='visionAPI'),
    path('extract5/', viewGemini.extract5, name='extract5'),
]
