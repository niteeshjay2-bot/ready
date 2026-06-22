"""
INFY Real Estate - Generate Placeholder Property Images (SVG)
Creates local SVG image files for all properties
"""
import os
import random

IMAGES_DIR = os.path.join(os.path.dirname(__file__), 'static', 'images', 'properties')
os.makedirs(IMAGES_DIR, exist_ok=True)

COLORS = [
    ('#1a56db', '#3b82f6'), ('#059669', '#10b981'), ('#7c3aed', '#8b5cf6'),
    ('#dc2626', '#ef4444'), ('#d97706', '#f59e0b'), ('#0891b2', '#06b6d4'),
    ('#4f46e5', '#6366f1'), ('#be185d', '#ec4899'), ('#065f46', '#047857'),
]

ROOM_TYPES = {
    '1': ('Living Room', '&#127968;'),
    '2': ('Bedroom', '&#128716;'),
    '3': ('Kitchen', '&#127859;'),
    '4': ('Exterior', '&#127961;'),
}


def generate_svg(prop_id, img_num, width=800, height=500):
    """Generate a unique SVG placeholder image"""
    color1, color2 = random.choice(COLORS)
    room_type = ROOM_TYPES.get(str(img_num), ('Property', '&#127968;'))

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs>
    <linearGradient id="bg{prop_id}_{img_num}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{color1};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{color2};stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="{width}" height="{height}" fill="url(#bg{prop_id}_{img_num})"/>
  <rect x="50" y="120" width="700" height="300" rx="20" fill="rgba(255,255,255,0.15)"/>
  <text x="400" y="250" font-family="Arial,sans-serif" font-size="72" fill="white" text-anchor="middle" dominant-baseline="middle">&#127968;</text>
  <text x="400" y="330" font-family="Arial,sans-serif" font-size="24" fill="rgba(255,255,255,0.9)" text-anchor="middle">INFY Real Estate</text>
  <text x="400" y="370" font-family="Arial,sans-serif" font-size="18" fill="rgba(255,255,255,0.7)" text-anchor="middle">Property #{prop_id} - {room_type[0]}</text>
  <text x="400" y="80" font-family="Arial,sans-serif" font-size="16" fill="rgba(255,255,255,0.6)" text-anchor="middle">India's Smartest AI Powered Real Estate Platform</text>
</svg>'''
    return svg


def generate_all_images(max_property_id=500):
    """Generate SVG images for all properties"""
    count = 0
    for prop_id in range(1, max_property_id + 1):
        num_images = random.randint(1, 4)
        for img_num in range(1, num_images + 1):
            filename = f"property_{prop_id}_{img_num}.svg"
            filepath = os.path.join(IMAGES_DIR, filename)
            if not os.path.exists(filepath):
                svg_content = generate_svg(prop_id, img_num)
                with open(filepath, 'w') as f:
                    f.write(svg_content)
                count += 1
    print(f"Generated {count} property images in {IMAGES_DIR}")


if __name__ == '__main__':
    generate_all_images()
