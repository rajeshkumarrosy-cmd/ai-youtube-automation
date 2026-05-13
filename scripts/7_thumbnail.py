import os
import json
from PIL import Image, ImageDraw

os.makedirs("output/thumbnails", exist_ok=True)

print("\n🖼️ STEP 7: THUMBNAIL")

try:
    # Load topic
    with open("output/scripts/trending_topics.json") as f:
        topic = json.load(f)['selected_topic']['title']
except:
    topic = "Amazing Story"

# Create thumbnail
img = Image.new('RGB', (1280, 720), color=(255, 50, 50))
draw = ImageDraw.Draw(img)
draw.rectangle([0, 0, 1280, 720], fill=(20, 20, 60))
draw.rectangle([50, 200, 1230, 520], fill=(255, 50, 50))
draw.text((100, 300), topic[:30], fill=(255, 255, 255))

img.save("output/thumbnails/thumbnail.png")

print("✅ Thumbnail created: output/thumbnails/thumbnail.png\n")
