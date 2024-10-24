from google.cloud import vision
import os
import io

def perform_ocr(credentials_path: str, image_path: str) -> dict:

    # Set credentials
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

    # Initialize the client
    client = vision.ImageAnnotatorClient()

    # Read the image file
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    # Create image object
    image = vision.Image(content=content)

    try:
        # Perform OCR
        response = client.text_detection(image=image)
        texts = response.text_annotations

        # Check if any text was detected
        if not texts:
            return {
                'success': False,
                'error': 'No text detected in the image',
                'text': '',
                'locale': None
            }

        # Extract the full text and locale
        result = {
            'success': True,
            'error': None,
            'text': texts[0].description,  # Complete text
            'locale': texts[0].locale,     # Detected language
            'blocks': []
        }

        # Extract individual text blocks with their locations
        for text in texts[1:]:  # Skip the first one as it contains complete text
            vertices = [(vertex.x, vertex.y) for vertex in text.bounding_poly.vertices]
            result['blocks'].append({
                'text': text.description,
                'confidence': text.confidence if hasattr(text, 'confidence') else None,
                'bounds': vertices
            })

        return result

    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'text': '',
            'locale': None
        }

def main(credentials_path: str = "./gcpVision.json", image_path: str = "./test.png"):
    """
    Main function to run OCR process

    Args:
        credentials_path (str): Path to GCP credentials file
        image_path (str): Path to image file
    """
    # Validate file existence
    if not os.path.exists(credentials_path):
        print(f"Error: Credentials file not found at {credentials_path}")
        return

    if not os.path.exists(image_path):
        print(f"Error: Image file not found at {image_path}")
        return

    # Perform OCR
    result = perform_ocr(credentials_path, image_path)

    # Print results
    if result['success']:
        print("OCR Completed Successfully!")
        print("\nDetected Text:")
        print("--------------")
        print(result['text'])
        print("--------------")
        print("\nLanguage:", result['locale'])
        print("\nText Blocks:", len(result['blocks']))
    else:
        print("OCR Failed!")
        print("Error:", result['error'])

if __name__ == "__main__":
    main()
