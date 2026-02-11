import pydicom
import numpy as np
from PIL import Image
import sys
import os

def extract_dicom_preview(dicom_path, output_path):
    try:
        # Load the DICOM file
        ds = pydicom.dcmread(dicom_path)
        
        # Get pixel data
        if 'PixelData' not in ds:
            print("Error: DICOM file does not contain pixel data.")
            return False
            
        # Use pixel_array directly
        image_array = ds.pixel_array.astype(float)
        
        # Squeeze the array but keep meaningful dimensions
        # (20, 1024, 1024) -> Multi-frame
        if image_array.ndim > 2:
            # If it's something like (20, 1024, 1024), it's multi-frame
            # We take the middle slice or first slice
            image_array = image_array[image_array.shape[0] // 2]
            
        # Rescale Slope/Intercept
        slope = getattr(ds, 'RescaleSlope', 1.0)
        intercept = getattr(ds, 'RescaleIntercept', 0.0)
        image_array = image_array * float(slope) + float(intercept)
        
        # Windowing (VOI LUT)
        if hasattr(ds, 'WindowCenter') and hasattr(ds, 'WindowWidth'):
            window_center = ds.WindowCenter
            window_width = ds.WindowWidth
            
            # Handle multiple values (using index 0)
            if hasattr(window_center, '__getitem__'):
                window_center = window_center[0]
            if hasattr(window_width, '__getitem__'):
                window_width = window_width[0]
                
            window_center = float(window_center)
            window_width = float(window_width)
            
            img_min = window_center - window_width / 2
            img_max = window_center + window_width / 2
            
            image_array = np.clip(image_array, img_min, img_max)
            
            # Normalization
            normalized_image = ((image_array - img_min) / window_width * 255).astype(np.uint8)
        else:
            # Fallback to full range
            img_min = np.min(image_array)
            img_max = np.max(image_array)
            if img_max == img_min:
                normalized_image = np.zeros(image_array.shape, dtype=np.uint8)
            else:
                normalized_image = ((image_array - img_min) / (img_max - img_min) * 255).astype(np.uint8)

        # Photometric Interpretation
        if getattr(ds, 'PhotometricInterpretation', '') == 'MONOCHROME1':
            normalized_image = 255 - normalized_image

        # Convert to PIL Image
        img = Image.fromarray(normalized_image)
        img.save(output_path)
        print(f"Preview saved to {output_path}")
        return True
        
    except Exception as e:
        print(f"Error processing DICOM: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python dicom_preview.py <input_dicom> <output_preview>")
    else:
        extract_dicom_preview(sys.argv[1], sys.argv[2])
