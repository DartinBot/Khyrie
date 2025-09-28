"""
Test Image Processing Utilities
Quick validation of FitFriendsClub image processing features
"""

import os
import sys
from io import BytesIO
from PIL import Image

# Add backend directory to path
sys.path.append('backend')

try:
    from image_utils import ImageProcessor, save_image_to_disk
    print("✅ Successfully imported image_utils")
except ImportError as e:
    print(f"❌ Import error: {e}")
    exit(1)


def create_test_image(size=(800, 600), color=(100, 150, 200)):
    """Create a test image for processing"""
    image = Image.new('RGB', size, color)
    output = BytesIO()
    image.save(output, format='JPEG')
    return output.getvalue()


def test_image_processing():
    """Test all image processing functions"""
    print("\n🧪 Testing FitFriendsClub Image Processing...")
    
    # Create test image
    print("📷 Creating test image...")
    test_image_data = create_test_image()
    
    # Test validation
    print("🔍 Testing image validation...")
    is_valid, message = ImageProcessor.validate_image(test_image_data)
    print(f"   Validation: {'✅' if is_valid else '❌'} {message}")
    
    # Test profile image resize
    print("👤 Testing profile image processing...")
    try:
        profile_image = ImageProcessor.resize_profile_image(test_image_data)
        print(f"   Profile resize: ✅ {len(profile_image)} bytes")
    except Exception as e:
        print(f"   Profile resize: ❌ {e}")
    
    # Test thumbnail creation
    print("🖼️  Testing thumbnail creation...")
    try:
        thumbnail = ImageProcessor.create_thumbnail(test_image_data)
        print(f"   Thumbnail: ✅ {len(thumbnail)} bytes")
    except Exception as e:
        print(f"   Thumbnail: ❌ {e}")
    
    # Test workout photo processing
    print("💪 Testing workout photo processing...")
    try:
        workout_photo = ImageProcessor.process_workout_photo(test_image_data, add_watermark=True)
        print(f"   Workout photo: ✅ {len(workout_photo)} bytes (with watermark)")
    except Exception as e:
        print(f"   Workout photo: ❌ {e}")
    
    # Test progress comparison
    print("📊 Testing progress comparison...")
    try:
        before_image = create_test_image(color=(200, 100, 100))
        after_image = create_test_image(color=(100, 200, 100))
        comparison = ImageProcessor.create_progress_comparison(before_image, after_image)
        print(f"   Progress comparison: ✅ {len(comparison)} bytes")
    except Exception as e:
        print(f"   Progress comparison: ❌ {e}")
    
    # Test filename generation
    print("📝 Testing filename generation...")
    try:
        filename = ImageProcessor.generate_filename(123, "test")
        print(f"   Filename: ✅ {filename}")
    except Exception as e:
        print(f"   Filename: ❌ {e}")
    
    print("\n🎉 Image processing tests completed!")


def test_file_operations():
    """Test file save/delete operations"""
    print("\n💾 Testing file operations...")
    
    # Create test image
    test_data = create_test_image((100, 100))
    test_filename = "test_image.jpg"
    
    try:
        # Test save
        filepath = save_image_to_disk(test_data, test_filename, "backend/uploads")
        print(f"   Save: ✅ {filepath}")
        
        # Check if file exists
        if os.path.exists(filepath):
            print(f"   File exists: ✅ {os.path.getsize(filepath)} bytes")
            
            # Clean up
            os.remove(filepath)
            print("   Cleanup: ✅ Test file removed")
        else:
            print("   File exists: ❌ File not found")
            
    except Exception as e:
        print(f"   File operations: ❌ {e}")


if __name__ == "__main__":
    print("🖼️  FitFriendsClub Image Processing Test Suite")
    print("=" * 50)
    
    test_image_processing()
    test_file_operations()
    
    print("\n✨ All tests completed!")
    print("\nReady for:")
    print("• Profile picture uploads")
    print("• Workout photo documentation") 
    print("• Progress tracking comparisons")
    print("• Fitness community image sharing")