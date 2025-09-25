#!/usr/bin/env python3
"""
Simple Icon Generator for PWA - Khyrie Fitness App
Creates basic SVG icons that can be converted to PNG later
"""

import os

def create_svg_icon(size, color="#4F46E5", text_color="white"):
    """Create an SVG icon with Khyrie branding"""
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{color};stop-opacity:1" />
      <stop offset="100%" style="stop-color:#7C3AED;stop-opacity:1" />
    </linearGradient>
  </defs>
  
  <!-- Background with rounded corners for modern look -->
  <rect x="0" y="0" width="{size}" height="{size}" rx="{size//8}" fill="url(#grad1)"/>
  
  <!-- Dumbbell icon -->
  <g transform="translate({size//2},{size//2})">
    <!-- Left weight -->
    <rect x="-{size//3}" y="-{size//8}" width="{size//6}" height="{size//4}" rx="{size//32}" fill="{text_color}"/>
    <!-- Right weight -->
    <rect x="{size//6}" y="-{size//8}" width="{size//6}" height="{size//4}" rx="{size//32}" fill="{text_color}"/>
    <!-- Bar -->
    <rect x="-{size//4}" y="-{size//32}" width="{size//2}" height="{size//16}" fill="{text_color}"/>
    
    <!-- Khyrie "K" -->
    <text x="0" y="{size//5}" text-anchor="middle" font-family="Arial, sans-serif" font-size="{size//8}" font-weight="bold" fill="{text_color}">K</text>
  </g>
</svg>'''
    return svg_content

def main():
    """Generate all required icon sizes for PWA"""
    # Create icons directory
    icons_dir = "icons"
    if not os.path.exists(icons_dir):
        os.makedirs(icons_dir)
    
    # Define required icon sizes for PWA manifest
    sizes = [16, 32, 48, 72, 96, 144, 192, 256, 384, 512, 1024]
    
    print("🎨 Generating Khyrie Fitness App Icons...")
    
    for size in sizes:
        # Create SVG icon
        svg_content = create_svg_icon(size)
        
        # Save SVG file
        svg_filename = f"icon-{size}x{size}.svg"
        svg_path = os.path.join(icons_dir, svg_filename)
        
        with open(svg_path, 'w') as f:
            f.write(svg_content)
        
        print(f"✅ Created {svg_filename}")
    
    # Create favicon.ico placeholder
    favicon_content = create_svg_icon(32)
    favicon_path = os.path.join(icons_dir, "favicon.svg")
    with open(favicon_path, 'w') as f:
        f.write(favicon_content)
    print("✅ Created favicon.svg")
    
    # Create Apple touch icon
    apple_icon_content = create_svg_icon(180)
    apple_icon_path = os.path.join(icons_dir, "apple-touch-icon.svg")
    with open(apple_icon_path, 'w') as f:
        f.write(apple_icon_content)
    print("✅ Created apple-touch-icon.svg")
    
    print("\n🎯 Icon Generation Complete!")
    print("📁 All icons saved to 'icons/' directory")
    print("\n📋 Next Steps:")
    print("1. Convert SVG files to PNG using online converter or ImageMagick")
    print("2. Update manifest.json with icon paths")
    print("3. Test PWA installation with new icons")
    
    # Generate manifest.json icon entries
    print("\n📄 Copy this to your manifest.json icons array:")
    print('  "icons": [')
    for i, size in enumerate(sizes):
        comma = "," if i < len(sizes) - 1 else ""
        print(f'    {{ "src": "icons/icon-{size}x{size}.png", "sizes": "{size}x{size}", "type": "image/png" }}{comma}')
    print('  ]')

if __name__ == "__main__":
    main()