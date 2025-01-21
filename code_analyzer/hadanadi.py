import os
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
        for text in extracted_text:
            vertices = text.bounding_poly.vertices
            x_min = min(vertex.x for vertex in vertices)
            y_min = min(vertex.y for vertex in vertices)
            x_max = max(vertex.x for vertex in vertices)
            y_max = max(vertex.y for vertex in vertices)

            # Vérifier si le texte est dans la région définie
            if x_min >= x1 and y_min >= y1 and x_max <= x2 and y_max <= y2:
                results[field] = text.description
                break
    return results

@csrf_exempt
def extract_text_google_vision(request):
    if request.method == 'POST' and request.FILES.get('image'):
        # Définir la variable d'environnement GOOGLE_APPLICATION_CREDENTIALS
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:/Users/ayoub/Downloads/visionapi.json'

        # Sauvegarder temporairement l'image téléchargée
        uploaded_file = request.FILES['image']
        file_path = default_storage.save('uploaded_image.jpg', uploaded_file)

        # Définir les régions d'intérêt pour extraire les informations spécifiques
        regions = {
            "prenom": (250, 120, 600, 210),
            "nom": (280, 190, 590, 250),
            "date_naissance": (510, 225, 715, 295),
            "lieu_naissance": (366, 285, 700, 385),
            "date_validite": (665, 500, 815, 580),
            "num_carte":  (98, 500, 290, 590),
        }

        # Taille de redimensionnement pour l'image
        new_size = (950, 600)

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

            if not texts:
                return JsonResponse({"error": "Aucun texte détecté"}, status=400)

            # Texte brut extrait
            extracted_text = texts[1:]  # Texte sans la description globale

            # Analyser les régions spécifiques
            extracted_data = extract_text_from_region(file_path, regions, extracted_text)

            # Dessiner les régions sur l'image pour vérification
            with Image.open(file_path) as img:
                img_resized = img.resize(new_size)
                draw = ImageDraw.Draw(img_resized)
                for coords in regions.values():
                    draw.rectangle(coords, outline="red", width=2)
                img_resized.show()  # Afficher l'image avec les régions

            return JsonResponse({"extracted_data": extracted_data}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

        finally:
            # Supprimer le fichier temporaire
            default_storage.delete(file_path)

    return JsonResponse({"error": "Invalid request"}, status=400)
