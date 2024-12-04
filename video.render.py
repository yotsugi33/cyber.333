import os
os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/homebrew/bin/ffmpeg"
from moviepy.editor import VideoFileClip
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from tqdm import tqdm  # Import tqdm for progress tracking

def add_grain(image, grain_intensity=0.1):
    """Add grain to the image."""
    image_array = np.array(image)
    noise = np.random.normal(0, grain_intensity * 155, image_array.shape).astype(np.uint8)
    noisy_image = np.clip(image_array + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(noisy_image)

def apply_vcr_effect(image):
    """Apply an icy blue VCR distortion effect to the image."""
    if image.mode != 'RGB':
        image = image.convert('RGB')
    icy_blue = Image.new('RGB', image.size, (173, 216, 230))
    distorted_image = Image.blend(image, icy_blue, alpha=0.3)
    distorted_image = distorted_image.filter(ImageFilter.GaussianBlur(2))
    return distorted_image

def enhance_contrast(image, factor=1.5):
    """Enhance contrast of the image."""
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

def process_video(input_path, output_path):
    print(f"Processing video: {input_path}")
    clip = VideoFileClip(input_path)

    def apply_effects(get_frame, t):
        frame = Image.fromarray(get_frame(t))
        frame = add_grain(frame)
        frame = apply_vcr_effect(frame)
        frame = enhance_contrast(frame)
        return np.array(frame)

    # Apply effects to the video
    processed_clip = clip.fl(lambda gf, t: apply_effects(gf, t))

    # Get original dimensions
    original_width, original_height = clip.size  # Note: size is (width, height)

    # Write the processed video, ensuring the resolution matches the original
    processed_clip.write_videofile(output_path, codec='libx264', fps=clip.fps, 
                                    preset='medium', ffmpeg_params=["-s", f"{original_height}x{original_width}"])
    print(f"Processed video saved: {output_path}")

# Define paths explicitly
input_folder = "/Users/xyz/Desktop/video.clean"
output_folder = "/Users/xyz/Desktop/video.333filter"

# Debugging: Print folder paths
print(f"Input folder: {input_folder}")
print(f"Output folder: {output_folder}")

# Check if the output directory exists, if not create it
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print("Created output directory.")

# Process all MOV files in the input folder
files = os.listdir(input_folder)
print("Files found in input folder:", files)

for filename in tqdm(files):  # Using tqdm for progress tracking
    if filename.lower().endswith(".mov"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, f"filtered_{filename}")
        print(f"Found .mov file: {filename}. Starting processing...")
        process_video(input_path, output_path)
    else:
        print(f"Skipping non-.mov file: {filename}")

print("All processing complete.")

