from django.urls import path
from . import views
from . import viewGemini
from . import view3lalah

urlpatterns = [
    path('extract_text_google_vision/', views.extract_text_google_vision, name='extract_text'),
    path('visionAPI/', viewGemini.extract_text_google_vision, name='visionAPI'),
    path('visionAPIig/', viewGemini.extract_text_google_visionig, name='visionAPIig'),
    path('visionAPIFR/', viewGemini.extract_text_google_visionFR, name='visionAPIFR'),
    path('extract_text4/', viewGemini.extract_text4, name='visionAPI'),
    path('extract5/', viewGemini.extract5, name='extract5'),
    path('extract_text_from_region/',view3lalah.extract_text_google_vision,name='extract_text_from_region') #hya kolchi
]
