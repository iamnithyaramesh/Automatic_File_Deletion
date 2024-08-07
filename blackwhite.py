import cv2

# Load the color image
image_path = 'sample7.jpeg'  # Replace with the path to your image
color_image = cv2.imread(image_path)

# Check if the image was loaded properly
if color_image is None:
    print("Error: Could not load image.")
else:
    # Convert the color image to grayscale
    gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)

    # Save the grayscale image
    cv2.imwrite('gray_image.jpg', gray_image)

    # Display the original and grayscale images
    cv2.imshow('Original Image', color_image)
    cv2.imshow('Grayscale Image', gray_image)

    # Wait for a key press and close the windows
    cv2.waitKey(0)
    cv2.destroyAllWindows()
