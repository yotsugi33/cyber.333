import os
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

def add_grain(image, grain_intensity=0.1):
    """Add grain to the image."""
    # Convert image to a NumPy array
    image_array = np.array(image)
    
    # Generate noise based on the shape of the image
    noise = np.random.normal(0, grain_intensity * 155, image_array.shape).astype(np.uint8)
    
    # Add noise to the image and clip to ensure values are in the valid range
    noisy_image = np.clip(image_array + noise, 0, 255).astype(np.uint8)
    
    return Image.fromarray(noisy_image)

def apply_vcr_effect(image):
    """Apply an icy blue VCR distortion effect to the image."""
    # Convert to RGB if not already
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Create a blue tint
    icy_blue = Image.new('RGB', image.size, (173, 216, 230))  # Light blue color
    distorted_image = Image.blend(image, icy_blue, alpha=0.3)  # Blend with blue tint

    # Add some blur to simulate distortion
    distorted_image = distorted_image.filter(ImageFilter.GaussianBlur(radius=2))
    
    return distorted_image

def process_images(input_folder, output_folder):
    """Process all .jpg images in the specified folder."""
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith('.jpg'):
            file_path = os.path.join(input_folder, filename)
            print(f"Processing {file_path}...")

            # Load image
            image = Image.open(file_path)

            # Apply effects
            image_with_vcr = apply_vcr_effect(image)
            final_image = add_grain(image_with_vcr, grain_intensity=0.1)

            # Save the processed image in the output folder
            final_image.save(os.path.join(output_folder, f"processed_{filename}"))
            print(f"Saved processed image as {os.path.join(output_folder, f'processed_{filename}')}")


if __name__ == "__main__":
    input_folder = "/Users/user/333/angelcore"  # Input folder with original images
    output_folder = "/Users/user/333/processed.angelcore"  # Output folder for processed images
    process_images(input_folder, output_folder)
