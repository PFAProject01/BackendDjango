from PIL import Image, ImageDraw

image_path = "C:/Users/ayoub/Downloads/cindyali.jpg"  # Remplacez par votre image
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
# Taille souhaitée pour le redimensionnement
new_size = (950, 600)  # Largeur, hauteur

with Image.open(image_path) as img:
    img_resized = img.resize(new_size)
    draw = ImageDraw.Draw(img_resized)
    for coords in regions.values():
        draw.rectangle(coords, outline="red", width=2)  # Dessine des rectangles rouges
    img_resized.show()  # Affiche l'image pour ajuster les coordonnées
