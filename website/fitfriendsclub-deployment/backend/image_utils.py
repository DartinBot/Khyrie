"""
FitFriendsClub Image Processing Utilities
Handles profile pictures, workout photos, and fitness progress images
"""

from PIL import Image, ImageOps, ImageDraw, ImageFont
import io
import os
import hashlib
from datetime import datetime


class ImageProcessor:
    """Image processing utilities for FitFriendsClub"""
    
    # Standard sizes for different image types
    PROFILE_SIZE = (200, 200)
    THUMBNAIL_SIZE = (150, 150)
    WORKOUT_PHOTO_SIZE = (800, 600)
    PROGRESS_PHOTO_SIZE = (400, 600)
    
    # Supported formats
    SUPPORTED_FORMATS = {'JPEG', 'JPG', 'PNG', 'WEBP', 'BMP'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    @staticmethod
    def validate_image(image_data):
        """Validate uploaded image data"""
        try:
            if len(image_data) > ImageProcessor.MAX_FILE_SIZE:
                return False, "Image file too large (max 10MB)"
            
            image = Image.open(io.BytesIO(image_data))
            
            if image.format not in ImageProcessor.SUPPORTED_FORMATS:
                return False, f"Unsupported format. Use: {', '.join(ImageProcessor.SUPPORTED_FORMATS)}"
            
            # Check image dimensions (prevent extremely large images)
            if image.width > 4000 or image.height > 4000:
                return False, "Image dimensions too large (max 4000x4000)"
            
            return True, "Valid image"
            
        except Exception as e:
            return False, f"Invalid image file: {str(e)}"
    
    @staticmethod
    def resize_profile_image(image_data, size=None):
        """Resize and optimize profile picture"""
        if size is None:
            size = ImageProcessor.PROFILE_SIZE
            
        try:
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if necessary (handles RGBA, P, etc.)
            if image.mode not in ('RGB', 'L'):
                image = image.convert('RGB')
            
            # Create square crop from center
            image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
            
            # Optimize and save
            output = io.BytesIO()
            image.save(output, format='JPEG', quality=85, optimize=True)
            return output.getvalue()
            
        except Exception as e:
            raise ValueError(f"Error processing profile image: {str(e)}")
    
    @staticmethod
    def create_thumbnail(image_data, size=None):
        """Create thumbnail from image"""
        if size is None:
            size = ImageProcessor.THUMBNAIL_SIZE
            
        try:
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if necessary
            if image.mode not in ('RGB', 'L'):
                image = image.convert('RGB')
            
            # Create thumbnail maintaining aspect ratio
            image.thumbnail(size, Image.Resampling.LANCZOS)
            
            # Center on square background
            background = Image.new('RGB', size, (255, 255, 255))
            x = (size[0] - image.width) // 2
            y = (size[1] - image.height) // 2
            background.paste(image, (x, y))
            
            output = io.BytesIO()
            background.save(output, format='JPEG', quality=80, optimize=True)
            return output.getvalue()
            
        except Exception as e:
            raise ValueError(f"Error creating thumbnail: {str(e)}")
    
    @staticmethod
    def process_workout_photo(image_data, add_watermark=True):
        """Process workout/progress photos"""
        try:
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize if too large while maintaining aspect ratio
            if image.width > ImageProcessor.WORKOUT_PHOTO_SIZE[0] or image.height > ImageProcessor.WORKOUT_PHOTO_SIZE[1]:
                image.thumbnail(ImageProcessor.WORKOUT_PHOTO_SIZE, Image.Resampling.LANCZOS)
            
            # Add watermark if requested
            if add_watermark:
                image = ImageProcessor._add_watermark(image)
            
            # Optimize and save
            output = io.BytesIO()
            image.save(output, format='JPEG', quality=85, optimize=True)
            return output.getvalue()
            
        except Exception as e:
            raise ValueError(f"Error processing workout photo: {str(e)}")
    
    @staticmethod
    def _add_watermark(image):
        """Add FitFriendsClub watermark to image"""
        try:
            # Create watermark
            watermark = Image.new('RGBA', image.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(watermark)
            
            # Calculate text size and position
            text = "FitFriendsClub"
            
            try:
                # Try to use a better font if available
                font = ImageFont.truetype("arial.ttf", 20)
            except (OSError, IOError):
                # Fall back to default font
                font = ImageFont.load_default()
            
            # Get text bounding box
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Position watermark in bottom-right corner
            x = image.width - text_width - 20
            y = image.height - text_height - 20
            
            # Draw text with semi-transparent background
            draw.rectangle([x-5, y-5, x+text_width+5, y+text_height+5], 
                          fill=(0, 0, 0, 100))
            draw.text((x, y), text, font=font, fill=(255, 255, 255, 200))
            
            # Composite watermark onto image
            if image.mode != 'RGBA':
                image = image.convert('RGBA')
            
            watermarked = Image.alpha_composite(image, watermark)
            return watermarked.convert('RGB')
            
        except Exception as e:
            # If watermarking fails, return original image
            print(f"Warning: Could not add watermark: {str(e)}")
            return image
    
    @staticmethod
    def generate_filename(user_id, image_type="image"):
        """Generate unique filename for uploaded image"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        random_hash = hashlib.md5(f"{user_id}_{timestamp}".encode()).hexdigest()[:8]
        return f"{image_type}_{user_id}_{timestamp}_{random_hash}.jpg"
    
    @staticmethod
    def create_progress_comparison(before_image_data, after_image_data):
        """Create before/after comparison image"""
        try:
            before_img = Image.open(io.BytesIO(before_image_data))
            after_img = Image.open(io.BytesIO(after_image_data))
            
            # Resize both images to same height
            target_height = 400
            before_ratio = target_height / before_img.height
            after_ratio = target_height / after_img.height
            
            before_width = int(before_img.width * before_ratio)
            after_width = int(after_img.width * after_ratio)
            
            before_resized = before_img.resize((before_width, target_height), Image.Resampling.LANCZOS)
            after_resized = after_img.resize((after_width, target_height), Image.Resampling.LANCZOS)
            
            # Create comparison image
            total_width = before_width + after_width + 20  # 20px gap
            comparison = Image.new('RGB', (total_width, target_height + 60), (255, 255, 255))
            
            # Paste images
            comparison.paste(before_resized, (0, 30))
            comparison.paste(after_resized, (before_width + 20, 30))
            
            # Add labels
            draw = ImageDraw.Draw(comparison)
            try:
                font = ImageFont.truetype("arial.ttf", 16)
            except (OSError, IOError):
                font = ImageFont.load_default()
            
            draw.text((before_width//2 - 25, 5), "BEFORE", font=font, fill=(0, 0, 0))
            draw.text((before_width + 20 + after_width//2 - 20, 5), "AFTER", font=font, fill=(0, 0, 0))
            
            # Add separator line
            line_x = before_width + 10
            draw.line([(line_x, 0), (line_x, target_height + 60)], fill=(200, 200, 200), width=2)
            
            output = io.BytesIO()
            comparison.save(output, format='JPEG', quality=90, optimize=True)
            return output.getvalue()
            
        except Exception as e:
            raise ValueError(f"Error creating progress comparison: {str(e)}")


def save_image_to_disk(image_data, filename, upload_dir="uploads"):
    """Save processed image to disk"""
    try:
        # Create upload directory if it doesn't exist
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save file
        filepath = os.path.join(upload_dir, filename)
        with open(filepath, 'wb') as f:
            f.write(image_data)
        
        return filepath
        
    except Exception as e:
        raise IOError(f"Error saving image: {str(e)}")


def delete_image_file(filepath):
    """Delete image file from disk"""
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False
        
    except Exception as e:
        print(f"Warning: Could not delete image file {filepath}: {str(e)}")
        return False