from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import re

@csrf_exempt
def extract_text(request):
    if request.method == 'POST' and request.FILES.get('image'):
        # Sauvegarder temporairement l'image téléchargée
        uploaded_file = request.FILES['image']
        file_path = default_storage.save('temp_card.jpg', uploaded_file)

        try:
            # Charger l'image avec PIL
            img = Image.open(file_path)

            # Prétraitement de l'image
            img = img.convert('L')  # Conversion en niveaux de gris
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(2)  # Améliorer le contraste
            img = img.filter(ImageFilter.MedianFilter(size=3))  # Réduction du bruit

            # OCR avec Tesseract (arabe et français)
            text = pytesseract.image_to_string(img, lang='ara+fra')

            # Diviser le texte en lignes
            lines = text.strip().split('\n')

            # Extraire les informations spécifiques
            extracted_info = {
                "nom": None,
                "prenom": None,
                "date_naissance": None,
                "lieu_naissance": None,
                "numero_identite": None,
                "date_expiration": None
            }

            # Extraction logique des données
            for line in lines:
                line = line.strip()

                # Nom et prénom
                if re.search(r'Nom|اللقب', line, re.IGNORECASE):
                    extracted_info["nom"] = line.split()[-1].strip()
                elif re.search(r'Née le|تاريخ الازدياد', line, re.IGNORECASE):
                    match = re.search(r'\d{2}/\d{2}/\d{4}', line)
                    if match:
                        extracted_info["date_naissance"] = match.group(0)
                elif re.search(r'à|ب', line):
                    if "à" in line:
                        extracted_info["lieu_naissance"] = line.split('à')[-1].strip()
                    elif "ب" in line:
                        extracted_info["lieu_naissance"] = line.split('ب')[-1].strip()
                elif re.search(r'CAN', line, re.IGNORECASE):
                    extracted_info["numero_identite"] = line.split()[-1].strip()
                elif re.search(r'Valable jusqu\'au|صالح إلى غاية', line, re.IGNORECASE):
                    match = re.search(r'\d{2}/\d{2}/\d{4}', line)
                    if match:
                        extracted_info["date_expiration"] = match.group(0)

            # Vérification des champs obligatoires
            if not any(extracted_info.values()):
                return JsonResponse({"error": "Unable to extract information. Please check the image quality."}, status=400)

            return JsonResponse({"extracted_info": extracted_info})

        finally:
            # Supprimer le fichier temporaire
            default_storage.delete(file_path)

    return JsonResponse({"error": "Invalid request"}, status=400)
