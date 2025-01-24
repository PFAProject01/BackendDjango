from django.urls import path
from . import views
from . import viewGemini
from . import view3lalah

urlpatterns = [

    path('extract_text_from_region/',view3lalah.extract_text_google_vision,name='extract_text_from_region'), #hya kolchi
    path('extract_text_from_regionOLD/',views.extract_text_google_visionOLD,name='extract_text_from_regionOLD') #hya kolchi
]
