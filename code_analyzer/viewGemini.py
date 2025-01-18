import os
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from google.cloud import vision

@csrf_exempt
def extract_text_google_vision(request):
    if request.method == 'POST' and request.FILES.get('image'):
        # Définir la variable d'environnement GOOGLE_APPLICATION_CREDENTIALS
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:/Users/ayoub\Downloads/visionapi.json'  # Remplacez par le chemin de votre fichier JSON

        # Sauvegarder temporairement l'image téléchargée
        uploaded_file = request.FILES['image']
        file_path = default_storage.save('uploaded_image.jpg', uploaded_file)

        try:
            # Initialiser le client Google Vision
            client = vision.ImageAnnotatorClient()

            # Charger le contenu de l'image
            with open(file_path, 'rb') as image_file:
                content = image_file.read()
            image = vision.Image(content=content)

            # Effectuer l'extraction du texte
            response = client.text_detection(image=image)
            texts = response.text_annotations

            if texts:
                extracted_text = texts[0].description  # Texte principal
                lines = extracted_text.strip().split('\n')  # Diviser en lignes

                # Retourner les lignes extraites sous forme de JSON
                return JsonResponse({"extracted_lines": lines}, status=200)
            else:
                return JsonResponse({"error": "Aucun texte détecté"}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

        finally:
            # Supprimer le fichier temporaire
            default_storage.delete(file_path)

    return JsonResponse({"error": "Invalid request"}, status=400)
@csrf_exempt
def extract_text4(request):
    if request.method == 'POST' and request.FILES.get('image'):
        # Définir la variable d'environnement GOOGLE_APPLICATION_CREDENTIALS
        os.environ[
            'GOOGLE_APPLICATION_CREDENTIALS'] = 'C:/Users/ayoub/Downloads/visionapi.json'  # Remplacez par le chemin de votre fichier JSON

        # Sauvegarder temporairement l'image téléchargée
        uploaded_file = request.FILES['image']
        file_path = default_storage.save('uploaded_image.jpg', uploaded_file)

        try:
            # Initialiser le client Google Vision
            client = vision.ImageAnnotatorClient()

            # Charger le contenu de l'image
            with open(file_path, 'rb') as image_file:
                content = image_file.read()
            image = vision.Image(content=content)

            # Effectuer l'extraction du texte
            response = client.text_detection(image=image)
            texts = response.text_annotations

            if texts:
                extracted_text = texts[0].description  # Texte principal
                return JsonResponse({"extracted_text": extracted_text}, status=200)
            else:
                return JsonResponse({"error": "Aucun texte détecté"}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

        finally:
            # Supprimer le fichier temporaire
            default_storage.delete(file_path)

    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def extract5(request):
    if request.method == 'POST' and request.FILES.get('image'):
        # Définir la variable d'environnement GOOGLE_APPLICATION_CREDENTIALS
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:/Users/ayoub/Downloads/visionapi.json'  # Remplacez par le chemin de votre fichier JSON

        # Sauvegarder temporairement l'image téléchargée
        uploaded_file = request.FILES['image']
        file_path = default_storage.save('uploaded_image.jpg', uploaded_file)

        try:
            # Initialiser le client Google Vision
            client = vision.ImageAnnotatorClient()

            # Charger le contenu de l'image
            with open(file_path, 'rb') as image_file:
                content = image_file.read()
            image = vision.Image(content=content)

            # Effectuer l'extraction du texte
            response = client.text_detection(image=image)
            texts = response.text_annotations

            if texts:
                extracted_text = texts[0].description  # Texte principal extrait

                # Diviser le texte en lignes pour traitement
                lines = extracted_text.strip().split('\n')

                # Extraire les informations spécifiques
                extracted_info = {
                    "nom": None,
                    "prenom": None,
                    "date_naissance": None,
                    "lieu_naissance": None,
                    "numero_identite": None,
                    "date_expiration": None
                }

                # Extraction logique des données (comme avec Tesseract)
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

            else:
                return JsonResponse({"error": "No text detected in the image."}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

        finally:
            # Supprimer le fichier temporaire
            default_storage.delete(file_path)

    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def extract_text_google_visionFR(request):
    if request.method == 'POST' and request.FILES.get('image'):
        # Définir la variable d'environnement GOOGLE_APPLICATION_CREDENTIALS
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:/Users/ayoub/Downloads/visionapi.json'  # Remplacez par le chemin de votre fichier JSON

        # Sauvegarder temporairement l'image téléchargée
        uploaded_file = request.FILES['image']
        file_path = default_storage.save('uploaded_image.jpg', uploaded_file)

        try:
            # Initialiser le client Google Vision
            client = vision.ImageAnnotatorClient()

            # Charger le contenu de l'image
            with open(file_path, 'rb') as image_file:
                content = image_file.read()
            image = vision.Image(content=content)

            # Effectuer l'extraction du texte en français uniquement
            response = client.text_detection(image=image, image_context={"language_hints": ["fr"]})
            texts = response.text_annotations

            if texts:
                extracted_text = texts[0].description  # Texte principal extrait
                lines = extracted_text.strip().split('\n')  # Diviser en lignes

                # Retourner les lignes extraites sous forme de JSON
                return JsonResponse({"extracted_lines": lines}, status=200)
            else:
                return JsonResponse({"error": "Aucun texte détecté"}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

        finally:
            # Supprimer le fichier temporaire
            default_storage.delete(file_path)

    return JsonResponse({"error": "Invalid request"}, status=400)


# Liste des mots ou phrases à ignorer
ignored_phrases = [
    "ROYAUME DU MAROC",
    "CARTE NATIONALE D'IDENTITE",
    "المملكة المغربية",
    "البطاقة الوطنية للتعريف",
    "المدير العام للأمن الوطني",
    "عبد اللطيف حموشي"
]

@csrf_exempt
def extract_text_google_visionig(request):
    if request.method == 'POST' and request.FILES.get('image'):
        # Définir la variable d'environnement GOOGLE_APPLICATION_CREDENTIALS
        os.environ[
            'GOOGLE_APPLICATION_CREDENTIALS'] = 'C:/Users/ayoub/Downloads/visionapi.json'  # Remplacez par le chemin de votre fichier JSON

        # Sauvegarder temporairement l'image téléchargée
        uploaded_file = request.FILES['image']
        file_path = default_storage.save('uploaded_image.jpg', uploaded_file)

        try:
            # Initialiser le client Google Vision
            client = vision.ImageAnnotatorClient()

            # Charger le contenu de l'image
            with open(file_path, 'rb') as image_file:
                content = image_file.read()
            image = vision.Image(content=content)

            # Effectuer l'extraction du texte avec la langue française et orientation de texte spécifique
            response = client.text_detection(
                image=image,
                image_context={'language_hints': ['fr']}  # Spécifier la langue française
            )
            texts = response.text_annotations

            if texts:
                extracted_text = texts[0].description  # Texte principal
                lines = extracted_text.strip().split('\n')  # Diviser en lignes

                # Filtrer les lignes contenant les phrases à ignorer
                filtered_lines = [line for line in lines if not any(phrase in line for phrase in ignored_phrases)]

                # Retourner les lignes extraites sous forme de JSON
                return JsonResponse({"extracted_lines": filtered_lines}, status=200)
            else:
                return JsonResponse({"error": "Aucun texte détecté"}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

        finally:
            # Supprimer le fichier temporaire
            default_storage.delete(file_path)

    return JsonResponse({"error": "Invalid request"}, status=400)