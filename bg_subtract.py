import os
import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# Specify the folder containing the images
image_folder = r'C:\Users\nithy\OneDrive\Desktop\Automatic_File_Deletion\good_morning'  # Change this to your folder path

# Get a list of image files in the folder
image_names = os.listdir(image_folder)
ocr_results = []

# Perform OCR on each image
for i, image_name in enumerate(image_names):
    # Read the image
    img_path = os.path.join(image_folder, image_name)
    img = cv2.imread(img_path)
    
    # Perform OCR
    text = pytesseract.image_to_string(img)
    ocr_results.append(text)

    print(f'Results for image {i + 1}:')
    print(text)

# Save results to a text file
with open('ocr_results.txt', 'w') as file:
    for i, text in enumerate(ocr_results):
        file.write(f'Image {i + 1}: {text}\n')

# Analyze the word extraction and find images containing "Good Morning", "morning", or "GOOD MORNING"
search_phrases = ['Good Morning', 'morning', 'GOOD MORNING']
matching_images = []

for i, text in enumerate(ocr_results):
    # Check for the presence of the search phrases in the extracted text
    for phrase in search_phrases:
        if phrase.lower() in text.lower():
            # Add the image name to the matching images list
            matching_images.append(image_names[i])
            break  # No need to check other phrases for this image

# Display the image names containing the specified words
print('Images containing "Good Morning", "morning", or "GOOD MORNING":')
print(matching_images)

# Calculate the count of matching images
matching_count = len(matching_images)
total_images = len(image_names)

# Calculate the ratio
ratio = matching_count / total_images if total_images > 0 else 0

# Display the results
print(f'Count of matching images: {matching_count}')
print(f'Total number of images: {total_images}')
print(f'Ratio of matching images to total images: {ratio:.2f}')
