import cv2
import numpy as np


def detect_and_crop_card(image_path):
    # Read the image
    image = cv2.imread(image_path)

    if image is None:
        print(f"Erreur: Impossible de lire l'image à {image_path}")
        return False

    # Get image dimensions
    height, width = image.shape[:2]

    # Resize if image is too large while maintaining aspect ratio
    max_dimension = 1000
    if max(height, width) > max_dimension:
        scale = max_dimension / max(height, width)
        image = cv2.resize(image, None, fx=scale, fy=scale)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply bilateral filter to reduce noise while preserving edges
    denoised = cv2.bilateralFilter(gray, 9, 75, 75)

    # Apply adaptive thresholding to handle varying lighting conditions
    thresh = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 115, 4)

    # Apply morphological operations to remove noise and strengthen edges
    kernel = np.ones((3, 3), np.uint8)
    morphed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # Find contours
    contours, _ = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter and process contours
    card_contour = None
    max_area = 0

    for contour in contours:
        area = cv2.contourArea(contour)
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)

        # Filter based on area and shape (should be roughly rectangular)
        if len(approx) >= 4 and len(approx) <= 6:
            # Check if contour is roughly rectangular by comparing area ratios
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box_area = cv2.contourArea(box.astype(np.float32))

            if area > max_area and area > 0.1 * image.shape[0] * image.shape[1]:
                aspect_ratio = float(rect[1][0]) / rect[1][1] if rect[1][1] != 0 else 0
                # ID cards typically have an aspect ratio between 1.4 and 1.7
                if 1.4 <= aspect_ratio <= 1.7 or 1.4 <= (1 / aspect_ratio) <= 1.7:
                    card_contour = contour
                    max_area = area

    if card_contour is not None:
        # Get the minimum area rectangle
        rect = cv2.minAreaRect(card_contour)
        box = cv2.boxPoints(rect)
        box = box.astype(np.int32)

        # Sort points to ensure consistent ordering
        box = order_points(box)

        # Get width and height for the output image
        width = int(max(np.linalg.norm(box[0] - box[1]),
                        np.linalg.norm(box[2] - box[3])))
        height = int(max(np.linalg.norm(box[0] - box[3]),
                         np.linalg.norm(box[1] - box[2])))

        # Create destination points
        dst_pts = np.array([
            [0, 0],
            [width - 1, 0],
            [width - 1, height - 1],
            [0, height - 1]
        ], dtype="float32")

        # Get perspective transform matrix
        M = cv2.getPerspectiveTransform(box.astype(np.float32), dst_pts)

        # Apply perspective transform
        warped = cv2.warpPerspective(image, M, (width, height))

        # Save the cropped card
        cv2.imwrite('cropped_card.jpg', warped)

        # Show images
        cv2.drawContours(image, [box], 0, (0, 255, 0), 2)
        cv2.imshow('Detected Card', image)
        cv2.imshow('Cropped Card', warped)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return True

    return False


def order_points(pts):
    """Order points in clockwise order starting from top-left"""
    rect = np.zeros((4, 2), dtype=np.float32)

    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect


# Usage
image_path = 'C:/Users/ayoub/Downloads/mama3.jpg'  # Remplacez par le chemin de votre image
success = detect_and_crop_card(image_path)

if success:
    print("Card successfully detected and cropped!")
else:
    print("No card detected in the image.")

