import json
import os
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

class ThumbnailGenerator:
    def __init__(self):
        self.output_dir = "output/thumbnails"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def run(self):
        print("\n" + "="*60)
        print("🖼️ STEP 7: THUMBNAIL")
        print("="*60)
        
        img = Image.new('RGB', (1280, 720), color=(255, 50, 50))
        draw = ImageDraw.Draw(img)
        draw.text((100, 300), "AMAZING STORY", fill=(255, 255, 255))
        
        output_file = f"{self.output_dir}/thumbnail.png"
        img.save(output_file)
        
        print(f"\n✅ Thumbnail created: {output_file}\n")
        
        return {'file': output_file}

if __name__ == "__main__":
    ThumbnailGenerator().run()
