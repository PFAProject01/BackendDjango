from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
import pytesseract
from PIL import Image, ImageFilter


@csrf_exempt
def extract_text(request):
    if request.method == 'POST' and request.FILES.get('image'):
        # Sauvegarder temporairement l'image téléchargée
        uploaded_file = request.FILES['image']
        file_path = default_storage.save('temp_card.jpg', uploaded_file)

        # Charger l'image avec PIL
        img = Image.open(file_path)

        # Convertir l'image en noir et blanc
        img = img.convert('L')

        # Amélioration du contraste
        img = img.point(lambda x: 0 if x < 128 else 255)

        # Suppression du bruit
        img = img.filter(ImageFilter.MedianFilter(size=3))

        # Effectuer l'OCR avec Tesseract en arabe et français
        #text = pytesseract.image_to_string(img, lang='ara+fra')  # Langues : arabe et français
        text = pytesseract.image_to_string(img, lang='fra')
        # Supprimer le fichier temporaire
        default_storage.delete(file_path)

        # Diviser le texte en lignes
        lines = text.strip().split('\n')

        # Retourner les lignes sous forme de JSON
        return JsonResponse({"extracted_lines": lines})

    return JsonResponse({"error": "Invalid request"}, status=400)
