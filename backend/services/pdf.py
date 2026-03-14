from pdf2image import convert_from_path, convert_from_bytes
import io
from PIL import Image
import tempfile
import os

def convert_pdf_to_images(file_bytes: bytes) -> list[Image.Image]:
    """
    Converts a PDF file (bytes) into a list of PIL Images.
    """
    try:
        # Convert bytes to images
        # We might need poppler installed on the system for this to work
        images = convert_from_bytes(file_bytes)
        return images
    except Exception as e:
        print(f"Error converting PDF to image: {e}")
        # If pdf2image fails (e.g. missing poppler), we might need fallback or error handling
        # For now let's raise
        raise e
