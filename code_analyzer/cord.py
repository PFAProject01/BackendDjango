from PIL import Image, ImageDraw

image_path = "C:/Users/ayoub/Downloads/cinMama2.jpg"  # Remplacez par votre image
regions = {
    "prenom": (250, 120, 600, 210),
    "nom": (280, 190, 590, 250),
    "prenomAr": (800, 105, 950, 170),
    "nomAr": (800, 160, 950, 230),
    "date_naissance": (510, 225, 715, 295),
    "lieu_naissance": (360, 285, 700, 385),
    "lieu_naissanceAr": (680, 264, 950, 320),
    "date_validite": (665, 500, 815, 580),
    "num_carte": (98, 500, 290, 590),
}
# Taille souhaitée pour le redimensionnement
new_size = (950, 600)  # Largeur, hauteur

with Image.open(image_path) as img:
    img_resized = img.resize(new_size)
    draw = ImageDraw.Draw(img_resized)
    for coords in regions.values():
        draw.rectangle(coords, outline="red", width=2)  # Dessine des rectangles rouges
    img_resized.show()  # Affiche l'image pour ajuster les coordonnées
