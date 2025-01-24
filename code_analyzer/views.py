import os
import cv2
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from google.cloud import vision
from PIL import Image, ImageDraw

def extract_text_from_region(image_path, regions, extracted_text):
    """
    Extraire les informations des régions spécifiques à partir du texte extrait.
    """
    results = {}
    for field, coords in regions.items():
        x1, y1, x2, y2 = coords
        field_text = []  # Collecte de toutes les chaînes dans la région
        for text in extracted_text:
            vertices = text.bounding_poly.vertices
            x_min = min(vertex.x for vertex in vertices)
            y_min = min(vertex.y for vertex in vertices)
            x_max = max(vertex.x for vertex in vertices)
            y_max = max(vertex.y for vertex in vertices)

            # Vérifier si le texte est dans la région définie
            if x_min >= x1 and y_min >= y1 and x_max <= x2 and y_max <= y2:
                field_text.append(text.description)

        # Pour les champs "date", ne prendre que la première chaîne correspondant à une date
        if "date" in field:
            for text in field_text:
                if any(char.isdigit() for char in text):  # Vérifier s'il contient des chiffres
                    results[field] = text
                    break
        else:
            # Sinon, concaténer toutes les chaînes détectées
            results[field] = " ".join(field_text)

    return results

def crop_card(image_path):
    """
    Isoler automatiquement la carte d'identité en utilisant OpenCV.
    """
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    # Trouver les contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    for contour in contours:
        # Approximations pour les contours
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        if len(approx) == 4:  # Si un rectangle est détecté
            x, y, w, h = cv2.boundingRect(approx)
            cropped = img[y:y+h, x:x+w]
            cropped_path = image_path.replace('.jpg', '_cropped.jpg')
            cv2.imwrite(cropped_path, cropped)
            return cropped_path

    return image_path  # Retourner l'image originale si aucun recadrage n'est effectué

@csrf_exempt
def extract_text_google_visionOLD(request):
    if request.method == 'POST' and request.FILES.get('image'):
        # Définir la variable d'environnement GOOGLE_APPLICATION_CREDENTIALS
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:/Users/ayoub/Downloads/visionapi.json'

        # Sauvegarder temporairement l'image téléchargée
        uploaded_file = request.FILES['image']
        file_path = default_storage.save('uploaded_image.jpg', uploaded_file)

        # Définir les régions d'intérêt pour extraire les informations spécifiques
        regions = {
            "nom": (4, 250, 300, 310),
            "prenom": (4, 180, 390, 240),
            "prenomAr": (200, 130, 650, 195),
            "nomAr": (200, 210, 650, 290),
            "date_naissance": (150, 300, 410, 350),
            "lieu_naissanceAr": (355, 340, 600, 390),
            "lieu_naissance": (30, 370, 390, 425),
            "date_validite": (200, 410, 440, 470),
            "num_carte": (650, 460, 825, 530),
        }

        # Taille de redimensionnement pour l'image
        new_size = (950, 600)

        try:
            # Recadrer la carte d'identité
            cropped_path = crop_card(file_path)

            # Redimensionner l'image après recadrage
            with Image.open(cropped_path) as img:
                img_resized = img.resize(new_size)
                resized_path = cropped_path.replace('_cropped.jpg', '_resized.jpg')
                img_resized.save(resized_path)

            # Initialiser le client Google Vision
            client = vision.ImageAnnotatorClient()

            # Charger le contenu de l'image redimensionnée
            with open(resized_path, 'rb') as image_file:
                content = image_file.read()
            image = vision.Image(content=content)

            # Effectuer l'extraction du texte
            response = client.text_detection(image=image)
            texts = response.text_annotations

            if not texts:
                return JsonResponse({"error": "Aucun texte détecté"}, status=400)

            # Texte brut extrait
            extracted_text = texts[1:]  # Texte sans la description globale

            # Analyser les régions spécifiques
            extracted_data = extract_text_from_region(resized_path, regions, extracted_text)

            # Dessiner les régions sur l'image pour vérification
            with Image.open(resized_path) as img_resized:
                draw = ImageDraw.Draw(img_resized)
                for coords in regions.values():
                    draw.rectangle(coords, outline="red", width=2)
                img_resized.show()  # Afficher l'image avec les régions

            return JsonResponse({"extracted_data": extracted_data}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

        finally:
            # Supprimer les fichiers temporaires
            default_storage.delete(file_path)
            if 'cropped_path' in locals():
                default_storage.delete(cropped_path)
            if 'resized_path' in locals():
                default_storage.delete(resized_path)

    return JsonResponse({"error": "Invalid request"}, status=400)
