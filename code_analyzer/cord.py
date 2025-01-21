from PIL import Image, ImageDraw

image_path = "C:/Users/ayoub/Downloads/1245.png"  # Remplacez par votre image
regions = {
    "prenom": (300, 150, 600, 210),
    "nom": (300, 190, 590, 250),
    "date_naissance": (500, 225, 715, 295),
    "lieu_naissance": (336, 285, 680, 355),
    "date_validite": (640, 430, 780, 500),
    "num_carte":  (140, 430, 290, 500),
}
# Taille souhaitée pour le redimensionnement
new_size = (950, 600)  # Largeur, hauteur

with Image.open(image_path) as img:
    img_resized = img.resize(new_size)
    draw = ImageDraw.Draw(img_resized)
    for coords in regions.values():
        draw.rectangle(coords, outline="red", width=2)  # Dessine des rectangles rouges
    img_resized.show()  # Affiche l'image pour ajuster les coordonnées
