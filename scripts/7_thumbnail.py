import os
from PIL import Image, ImageDraw
from datetime import datetime

class ThumbnailGenerator:
    def run(self):
        print("\n" + "="*70)
        print("🖼️ STEP 7: THUMBNAIL")
        print("="*70)
        
        os.makedirs("output/thumbnails", exist_ok=True)
        
        img = Image.new('RGB', (1280, 720), color=(255, 50, 50))
        draw = ImageDraw.Draw(img)
        
        try:
            draw.text((150, 300), "SHOCKING STORY", fill=(255, 255, 255))
        except:
            pass
        
        output_file = "output/thumbnails/thumbnail.png"
        img.save(output_file)
        
        print(f"\n✅ Thumbnail created\n")
        
        return {'file': output_file}

if __name__ == "__main__":
    ThumbnailGenerator().run()
