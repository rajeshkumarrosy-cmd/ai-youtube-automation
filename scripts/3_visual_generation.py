#!/usr/bin/env python3
"""
Step 3: Visual Generation
Creates images WITHOUT needing Stable Diffusion
Works on GitHub Actions!
"""

import os
import json
from PIL import Image, ImageDraw, ImageFont

print("\n" + "="*60)
print("🎨 STEP 3: VISUAL GENERATION")
print("="*60)

# Create output folder
os.makedirs("output/visuals", exist_ok=True)

# Load the script data
try:
    with open("output/scripts.json", "r") as f:
        scripts = json.load(f)
except:
    print("❌ No scripts found!")
    exit(1)

# ================================================================
# CREATE SHORT VIDEO SCENES
# ================================================================

print("\n📱 Generating SHORT video scenes...")

short_script = scripts.get("short", {})
short_scenes = short_script.get("scenes", [])

short_visuals = []

for i, scene in enumerate(short_scenes):
    print(f"   Scene {i+1}/{len(short_scenes)}...")
    
    # Create colorful background
    colors = [
        (255, 50, 50),      # Red
        (50, 100, 255),     # Blue
        (255, 150, 0),      # Orange
        (100, 200, 100)     # Green
    ]
    
    color = colors[i % len(colors)]
    
    # Create image
    img = Image.new('RGB', (1080, 1920), color=color)
    draw = ImageDraw.Draw(img)
    
    # Add text
    try:
        title_font = ImageFont.truetype("arial.ttf", 100)
        text_font = ImageFont.truetype("arial.ttf", 50)
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
    
    # Extract key words from scene description
    scene_desc = scene.get("description", f"Scene {i+1}")
    words = scene_desc.split()[:3]
    title = " ".join(words).upper()
    
    # Draw title
    draw.text((540, 400), title, font=title_font, fill=(255, 255, 255), anchor='mm')
    
    # Draw scene number
    draw.text((540, 800), f"SCENE {i+1}", font=text_font, fill=(200, 200, 200), anchor='mm')
    
    # Save
    visual_path = f"output/visuals/short_scene_{i}.png"
    img.save(visual_path)
    short_visuals.append(visual_path)
    
    print(f"      ✅ Saved: {visual_path}")

print(f"\n✅ SHORT scenes created: {len(short_visuals)}")

# ================================================================
# CREATE LONG VIDEO SCENES
# ================================================================

print("\n📺 Generating LONG video scenes...")

long_script = scripts.get("long", {})
long_scenes = long_script.get("scenes", [])

long_visuals = []

for i, scene in enumerate(long_scenes):
    print(f"   Scene {i+1}/{len(long_scenes)}...")
    
    # Create colorful background
    colors = [
        (255, 50, 50),
        (50, 100, 255),
        (255, 150, 0),
        (100, 200, 100),
        (200, 100, 200),
        (100, 200, 200),
        (255, 200, 50),
        (150, 100, 200)
    ]
    
    color = colors[i % len(colors)]
    
    # Create image (16:9 for long videos)
    img = Image.new('RGB', (1920, 1080), color=color)
    draw = ImageDraw.Draw(img)
    
    # Add text
    try:
        title_font = ImageFont.truetype("arial.ttf", 120)
        text_font = ImageFont.truetype("arial.ttf", 60)
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
    
    # Extract key words from scene description
    scene_desc = scene.get("description", f"Scene {i+1}")
    words = scene_desc.split()[:3]
    title = " ".join(words).upper()
    
    # Draw title
    draw.text((960, 400), title, font=title_font, fill=(255, 255, 255), anchor='mm')
    
    # Draw scene number
    draw.text((960, 750), f"SCENE {i+1}", font=text_font, fill=(200, 200, 200), anchor='mm')
    
    # Save
    visual_path = f"output/visuals/long_scene_{i}.png"
    img.save(visual_path)
    long_visuals.append(visual_path)
    
    print(f"      ✅ Saved: {visual_path}")

print(f"\n✅ LONG scenes created: {len(long_visuals)}")

# ================================================================
# SAVE VISUALS MANIFEST
# ================================================================

visuals_manifest = {
    "short_visuals": short_visuals,
    "long_visuals": long_visuals,
    "short_count": len(short_visuals),
    "long_count": len(long_visuals)
}

with open("output/visuals_manifest.json", "w") as f:
    json.dump(visuals_manifest, f, indent=2)

print("\n" + "="*60)
print("✅ VISUAL GENERATION COMPLETE")
print("="*60)
print(f"\n📊 Summary:")
print(f"   Short visuals: {len(short_visuals)}")
print(f"   Long visuals: {len(long_visuals)}")
print(f"   Total: {len(short_visuals) + len(long_visuals)} images")
print()
