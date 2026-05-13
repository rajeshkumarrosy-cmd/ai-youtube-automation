import json
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

class ThumbnailGenerator:
    def __init__(self):
        self.output_dir = "output/thumbnails"
        os.makedirs(self.output_dir, exist_ok=True)
        self.thumbnail_size = (1280, 720)
    
    def load_topic(self):
        """Load trending topic"""
        try:
            with open("output/scripts/trending_topics.json", 'r') as f:
                data = json.load(f)
                return data['topics'][0]['title']
        except:
            return "Untitled"
    
    def create_high_ctr_thumbnail(self):
        """Create viral thumbnail"""
        topic = self.load_topic()
        
        # Create base image with bright gradient
        img = Image.new('RGB', self.thumbnail_size, color=(255, 100, 100))
        draw = ImageDraw.Draw(img)
        
        # Add gradient
        for y in range(self.thumbnail_size[1]):
            color_intensity = int(255 * (y / self.thumbnail_size[1]))
            draw.line(
                [(0, y), (self.thumbnail_size[0], y)],
                fill=(255 - color_intensity, 100 + color_intensity//2, 100)
            )
        
        # Add main text
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 90)
            secondary_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 50)
        except:
            title_font = ImageFont.load_default()
            secondary_font = ImageFont.load_default()
        
        # Add white border for text
        text_lines = topic.split()
        y_position = 200
        
        for line in text_lines[:2]:
            # Text shadow
            draw.text((20, y_position + 5), line, font=title_font, fill=(0, 0, 0))
            # Main text
            draw.text((15, y_position), line, font=title_font, fill=(255, 255, 255))
            y_position += 120
        
        # Add curiosity-triggering element
        draw.text(
            (50, 550),
            "SEE WHAT HAPPENS →",
            font=secondary_font,
            fill=(255, 255, 0)
        )
        
        # Save thumbnail
        output_path = f"{self.output_dir}/thumbnail_main.png"
        img.save(output_path)
        
        print(f"✅ Thumbnail created: {output_path}")
        return output_path
    
    def create_multiple_variants(self):
        """Create different thumbnail variants for A/B testing"""
        variants = []
        
        topic = self.load_topic()
        
        # Variant 1: Bold Red
        img = Image.new('RGB', self.thumbnail_size, color=(230, 50, 50))
        
        # Variant 2: Dark Mystery
        img2 = Image.new('RGB', self.thumbnail_size, color=(30, 30, 30))
        
        # Variant 3: Golden
        img3 = Image.new('RGB', self.thumbnail_size, color=(255, 200, 50))
        
        for i, img in enumerate([img, img2, img3], 1):
            output_path = f"{self.output_dir}/thumbnail_variant_{i}.png"
            img.save(output_path)
            variants.append(output_path)
            print(f"✅ Variant {i}: {output_path}")
        
        return variants
    
    def add_emotional_elements(self, img_path):
        """Add emotional design elements"""
        img = Image.open(img_path)
        
        # Could add emoji, shocked face emoji, etc.
        # For now, save as-is
        
        return img_path
    
    def save_thumbnail_data(self, main_thumbnail, variants):
        """Save thumbnail metadata"""
        data = {
            'main_thumbnail': main_thumbnail,
            'variants': variants,
            'ctr_tips': [
                'High contrast colors (red, yellow, blue)',
                'Large readable text',
                'Emotional faces',
                'Curiosity gap words (shocking, hidden, revealed)',
                'Arrow pointing to important element'
            ]
        }
        
        with open(f"{self.output_dir}/thumbnail_data.json", 'w') as f:
            json.dump(data, f, indent=2)
        
        return data
    
    def run(self):
        """Generate thumbnails"""
        print("🖼️ STEP 7: THUMBNAIL GENERATION STARTING...")
        
        main_thumbnail = self.create_high_ctr_thumbnail()
        variants = self.create_multiple_variants()
        
        thumbnail_data = self.save_thumbnail_data(main_thumbnail, variants)
        
        print(f"""
        ╔════════════════════════════════════╗
        ║   THUMBNAILS GENERATED              ║
        ╚════════════════════════════════════╝
        Main: {main_thumbnail}
        Variants: {len(variants)}
        """)
        
        return thumbnail_data

if __name__ == "__main__":
    generator = ThumbnailGenerator()
    generator.run()
