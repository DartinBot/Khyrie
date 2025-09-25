#!/usr/bin/env python3
"""
Khyrie App Icon Generator
Generates all required app icon sizes for PWA, iOS, and Android
"""

from PIL import Image, ImageDraw, ImageFont
import os
import math

def create_app_icon(size, filename):
    """Create a professional Khyrie app icon"""
    
    # Create image with rounded corners for modern look
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Background gradient (blue to purple)
    for y in range(size):
        # Calculate gradient
        ratio = y / size
        r = int(102 + (118 - 102) * ratio)  # 102 -> 118
        g = int(126 + (100 - 126) * ratio)  # 126 -> 100
        b = int(234 + (162 - 234) * ratio)  # 234 -> 162
        
        draw.line([(0, y), (size, y)], fill=(r, g, b, 255))
    
    # Add rounded corners
    corner_radius = size // 8
    mask = Image.new('L', (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle((0, 0, size, size), corner_radius, fill=255)
    
    # Apply mask for rounded corners
    output = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    output.paste(img, (0, 0))
    output.putalpha(mask)
    
    # Add icon elements
    draw = ImageDraw.Draw(output)
    
    # Calculate proportional sizes
    center = size // 2
    
    # Draw main fitness icon (dumbbell)
    bar_width = size // 20
    bar_height = size // 3
    weight_size = size // 8
    
    # Dumbbell bar (white)
    bar_x = center - bar_width // 2
    bar_y = center - bar_height // 2
    draw.rectangle([bar_x, bar_y, bar_x + bar_width, bar_y + bar_height], 
                   fill=(255, 255, 255, 255))
    
    # Dumbbell weights (white)
    weight_y1 = bar_y - weight_size // 2
    weight_y2 = bar_y + bar_height - weight_size // 2
    
    # Top weights
    draw.ellipse([bar_x - weight_size//2, weight_y1, 
                  bar_x + bar_width + weight_size//2, weight_y1 + weight_size], 
                 fill=(255, 255, 255, 255))
    
    # Bottom weights  
    draw.ellipse([bar_x - weight_size//2, weight_y2, 
                  bar_x + bar_width + weight_size//2, weight_y2 + weight_size], 
                 fill=(255, 255, 255, 255))
    
    # Add "K" letter for Khyrie
    font_size = size // 4
    try:
        # Try to use system font
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except:
        try:
            # Fallback for other systems
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            # Use default font
            font = ImageFont.load_default()
    
        # Draw K text (centered in the bottom half)
    text = "K"
    try:
        font_size = max(8, size // 4)  # Ensure minimum font size of 8
        font = ImageFont.truetype("/System/Library/Fonts/Arial Bold.ttf", font_size)
    except:
        # Fallback to default font if custom font not available
        font = ImageFont.load_default()
    
    # Get text dimensions and center it in bottom half
    try:
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
    except:
        # Fallback for very small sizes
        text_width = font_size
        text_height = font_size
    
    text_x = (size - text_width) // 2
    text_y = size // 2 + (size // 4 - text_height // 2)
    
    # Draw text with slight shadow effect
    shadow_offset = max(1, size // 100)
    draw.text((text_x + shadow_offset, text_y + shadow_offset), text, 
              font=font, fill=(0, 0, 0, 100))
    draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255, 255))
    
    # Add subtle highlight
    highlight_size = size // 6
    highlight = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    highlight_draw = ImageDraw.Draw(highlight)
    
    # Radial highlight in upper left
    for i in range(highlight_size):
        alpha = int(30 * (1 - i / highlight_size))
        highlight_draw.ellipse([size//4 - i, size//4 - i, 
                               size//4 + highlight_size + i, 
                               size//4 + highlight_size + i], 
                              outline=(255, 255, 255, alpha))
    
    # Composite highlight
    output = Image.alpha_composite(output, highlight)
    
    # Save icon
    output.save(filename, 'PNG')
    print(f"✅ Generated {filename} ({size}x{size})")

def generate_all_icons():
    """Generate all required app icon sizes"""
    
    print("🎨 Generating Khyrie App Icons...")
    
    # Required icon sizes for PWA and app stores
    icon_sizes = [
        # PWA and web
        (72, "khyrie-72.png"),
        (96, "khyrie-96.png"), 
        (128, "khyrie-128.png"),
        (144, "khyrie-144.png"),
        (152, "khyrie-152.png"),
        (192, "khyrie-192.png"),
        (384, "khyrie-384.png"),
        (512, "khyrie-512.png"),
        
        # iOS specific
        (57, "khyrie-57.png"),   # iPhone original
        (60, "khyrie-60.png"),   # iPhone 2x
        (72, "khyrie-72.png"),   # iPad
        (76, "khyrie-76.png"),   # iPad
        (114, "khyrie-114.png"), # iPhone retina
        (120, "khyrie-120.png"), # iPhone 2x
        (144, "khyrie-144.png"), # iPad retina  
        (152, "khyrie-152.png"), # iPad retina
        (180, "khyrie-180.png"), # iPhone 3x
        
        # Android specific
        (36, "khyrie-36.png"),   # LDPI
        (48, "khyrie-48.png"),   # MDPI
        (72, "khyrie-72.png"),   # HDPI
        (96, "khyrie-96.png"),   # XHDPI
        (144, "khyrie-144.png"), # XXHDPI
        (192, "khyrie-192.png"), # XXXHDPI
        
        # App store and marketing
        (1024, "khyrie-1024.png"), # App Store
        (16, "khyrie-16.png"),     # Favicon
        (32, "khyrie-32.png"),     # Favicon
    ]
    
    # Create icons directory
    icons_dir = "icons"
    os.makedirs(icons_dir, exist_ok=True)
    
    # Generate unique sizes only
    generated_sizes = set()
    for size, filename in icon_sizes:
        if size not in generated_sizes:
            filepath = os.path.join(icons_dir, filename)
            create_app_icon(size, filepath)
            generated_sizes.add(size)
    
    print(f"\n🎉 Generated {len(generated_sizes)} unique icon sizes")
    print("📱 Icons ready for PWA, iOS App Store, and Google Play Store!")
    
    # Generate favicon.ico
    generate_favicon()

def generate_favicon():
    """Generate favicon.ico with multiple sizes"""
    print("\n🌐 Generating favicon.ico...")
    
    # Load the 32px icon
    icon_32 = Image.open("icons/khyrie-32.png")
    icon_16 = Image.open("icons/khyrie-16.png")
    
    # Save as ICO with multiple sizes
    icon_32.save("favicon.ico", format='ICO', sizes=[(16, 16), (32, 32)])
    print("✅ Generated favicon.ico")

if __name__ == "__main__":
    generate_all_icons()
    print("\n🚀 All app icons generated successfully!")
    print("📋 Next steps:")
    print("   - Icons are ready for manifest.json")
    print("   - Use khyrie-1024.png for App Store submissions")
    print("   - Upload khyrie-512.png to Google Play Console")
    print("   - Favicon.ico ready for web deployment")