import os
import cv2
import numpy as np
from pdf2image import convert_from_path
from pyzxing import BarCodeReader
from PIL import Image

# ---------- CONFIG ----------
PDF_PATH = "input.pdf"
OUTPUT_DIR = "output_pages"
DPI = 300
# ----------------------------

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def pdf_to_images(pdf_path, dpi=300):
    print(f"[INFO] Converting PDF to images at {dpi} DPI...")
    pages = convert_from_path(pdf_path, dpi=dpi)
    ensure_dir(OUTPUT_DIR)
    image_paths = []
    for i, page in enumerate(pages):
        img_path = os.path.join(OUTPUT_DIR, f"page_{i+1}.png")
        page.save(img_path, "PNG")
        image_paths.append(img_path)
    print(f"[INFO] Extracted {len(image_paths)} page(s).")
    return image_paths

def preprocess_image(path):
    """Preprocess image for better barcode readability."""
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Equalize histogram for better contrast
    gray = cv2.equalizeHist(gray)

    # Adaptive threshold for variable lighting / faded ink
    binary = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 51, 10
    )

    # Morphological closing to fill gaps in dotted bars
    kernel = np.ones((3, 3), np.uint8)
    closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    processed_path = path.replace(".png", "_processed.png")
    cv2.imwrite(processed_path, closed)
    return processed_path

def decode_with_zxing(image_path):
    reader = BarCodeReader()
    results = reader.decode(image_path)
    return results

def main():
    image_paths = pdf_to_images(PDF_PATH, DPI)
    reader = BarCodeReader()

    for img_path in image_paths:
        print(f"\n[INFO] Processing {img_path} ...")
        processed_path = preprocess_image(img_path)
        results = decode_with_zxing(processed_path)

        if not results:
            print("⚠️  No barcode found.")
            continue

        for res in results:
            if "parsed" in res and res["parsed"]:
                print(f"✅ Type: {res['format']}")
                print(f"   Data: {res['parsed']}")
            elif "raw" in res:
                print(f"✅ Type: {res.get('format', 'Unknown')}")
                print(f"   Raw data: {res['raw']}")
            else:
                print("⚠️  Unrecognized barcode result:", res)

    print("\n[DONE] Barcode extraction complete.")

if __name__ == "__main__":
    main()