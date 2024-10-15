import os
import cv2
import pytesseract
import re
import numpy as np

# Set the path for Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Specify the folder containing the images
image_folder = r'C:\Users\nithy\OneDrive\Desktop\Automatic_File_Deletion\festive_images'

# Allowed image formats
allowed_formats = ('.jpg', '.jpeg', '.png', '.webp', '.avif')

# Get a list of image files in the folder with the specified formats
image_names = [f for f in os.listdir(image_folder) if f.lower().endswith(allowed_formats)]
ocr_results = []

'''# Define a function to standardize phrases
def standardize_text(text):
    replacements = {
        # Add any specific standardization rules if needed
    }
    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text.strip()'''

# Stage 1: Normal OCR without preprocessing
for image_name in image_names:
    img_path = os.path.join(image_folder, image_name)
    img = cv2.imread(img_path)
    text = pytesseract.image_to_string(img)
    combined_text = ' '.join(text.splitlines()).strip()
    ocr_results.append(combined_text)

# Save results to a text file
with open('ocr_results.txt', 'w') as file:
    for i, text in enumerate(ocr_results):
        file.write(f'Image {i + 1}: {text}\n')

# Analyze and delete images containing specific words in Stage 1
search_phrases = ['Happy Diwali', 'diwali', 'pongal', 'Happy Pongal', 'Merry', 'Merry Christmas', 'Christmas', 'Happy New Year', 'New Year']
matching_images_stage1 = []

for i, text in enumerate(ocr_results):
    standardized_text = standardize_text(text)
    for phrase in search_phrases:
        if phrase.lower() in standardized_text.lower():
            matching_images_stage1.append(image_names[i])
            break

# Delete matching images from Stage 1
for image_name in matching_images_stage1:
    image_path = os.path.join(image_folder, image_name)
    os.remove(image_path)
    print(f'Deleted image: {image_name}')

# Calculate ratio for Stage 1
matching_count_stage1 = len(matching_images_stage1)
total_images = len(image_names)
ratio_stage1 = matching_count_stage1 / total_images if total_images > 0 else 0
print(f'Stage 1 - Ratio: {ratio_stage1:.2f}')

# Remaining images for Stage 2
remaining_images_stage2 = [img for img in image_names if img not in matching_images_stage1]

# Stage 2: OCR with preprocessing (blur, threshold)
def preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY_INV)
    resized = cv2.resize(thresh, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    return resized

ocr_results_stage2 = []

for image_name in remaining_images_stage2:
    img_path = os.path.join(image_folder, image_name)
    img = cv2.imread(img_path)
    preprocessed_img = preprocess_image(img)
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(preprocessed_img, config=custom_config)
    combined_text = ' '.join(text.splitlines()).strip()
    ocr_results_stage2.append(combined_text)

# Analyze and delete images in Stage 2
matching_images_stage2 = []

for i, text in enumerate(ocr_results_stage2):
    standardized_text = standardize_text(text)
    for phrase in search_phrases:
        if phrase.lower() in standardized_text.lower():
            matching_images_stage2.append(remaining_images_stage2[i])
            break

# Delete matching images from Stage 2
for image_name in matching_images_stage2:
    image_path = os.path.join(image_folder, image_name)
    os.remove(image_path)
    print(f'Deleted image: {image_name}')

# Calculate ratio for Stage 2
matching_count_stage2 = len(matching_images_stage2)
print(f'Stage 2 - Ratio:', (matching_count_stage1 + matching_count_stage2) / total_images)

# Remaining images for Stage 3
remaining_images_stage3 = [img for img in remaining_images_stage2 if img not in matching_images_stage2]

# Stage 3: Advanced OCR with additional preprocessing techniques
def advanced_preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    adaptive_thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    denoised = cv2.medianBlur(adaptive_thresh, 3)
    kernel = np.ones((2, 2), np.uint8)
    morph = cv2.morphologyEx(denoised, cv2.MORPH_CLOSE, kernel)
    edges = cv2.Canny(morph, 100, 200)
    coords = np.column_stack(np.where(edges > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    deskewed = cv2.warpAffine(edges, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    resized = cv2.resize(deskewed, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    return resized

ocr_results_stage3 = []

# Perform OCR for Stage 3
for image_name in remaining_images_stage3:
    img_path = os.path.join(image_folder, image_name)
    img = cv2.imread(img_path)
    preprocessed_img = advanced_preprocess_image(img)
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(preprocessed_img, config=custom_config)
    combined_text = ' '.join(text.splitlines()).strip()
    ocr_results_stage3.append(combined_text)

# Analyze and delete images in Stage 3
matching_images_stage3 = []

for i, text in enumerate(ocr_results_stage3):
    standardized_text = standardize_text(text)
    for phrase in search_phrases:
        if phrase.lower() in standardized_text.lower():
            matching_images_stage3.append(remaining_images_stage3[i])
            break

# Delete matching images from Stage 3
for image_name in matching_images_stage3:
    image_path = os.path.join(image_folder, image_name)
    os.remove(image_path)
    print(f'Deleted image: {image_name}')

# Calculate ratio for Stage 3
matching_count_stage3 = len(matching_images_stage3)
print(f'Stage 3 - Ratio:', (matching_count_stage1 + matching_count_stage2 + matching_count_stage3) / total_images)

# Final summary
print(f'Total images deleted in all three stages: {matching_count_stage1 + matching_count_stage2 + matching_count_stage3}')
print(f'Final ratio after three stages of deletion:', (matching_count_stage1 + matching_count_stage2 + matching_count_stage3) / total_images)
print('Remaining images count:', len(image_names) - (matching_count_stage1 + matching_count_stage2 + matching_count_stage3))
