import json
import requests
from PIL import Image, ImageDraw, ImageFont
import os

class VisualGenerator:
    def __init__(self):
        self.script = self.load_script()
        self.output_dir = "output/visuals"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def load_script(self):
        """Load generated script"""
        try:
            with open("output/scripts/short_script.json", 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def generate_image_prompts(self):
        """Create detailed prompts for image generation"""
        prompts = []
        
        for scene in self.script.get('scenes', []):
            prompt = {
                'scene_num': scene.get('scene'),
                'prompt': f"""
                Create a Pixar-style 3D animated scene:
                {scene.get('visual')}
                
                Style Requirements:
                - Pixar cinematic quality
                - Warm, professional lighting
                - Emotional expressions on characters
                - Vibrant colors
                - 4K quality composition
                - Dynamic camera angle
                
                Scene Description: {scene.get('visual')}
                """,
                'negative': 'low quality, cartoon, flat, pixelated, ugly, distorted',
                'duration': scene.get('duration'),
                'camera_movement': scene.get('camera_movement')
            }
            prompts.append(prompt)
        
        return prompts
    
    def create_placeholder_images(self):
        """Create colorful placeholder images using PIL"""
        colors = [
            (255, 100, 100),  # Red
            (100, 150, 255),  # Blue
            (100, 255, 150),  # Green
            (255, 200, 100),  # Orange
        ]
        
        images = []
        
        for i, scene in enumerate(self.script.get('scenes', [])):
            # Create image
            img = Image.new('RGB', (1920, 1080), color=colors[i % len(colors)])
            draw = ImageDraw.Draw(img)
            
            # Add text
            text = f"Scene {i+1}: {scene.get('visual', 'Scene')}"
            
            # Save
            path = f"{self.output_dir}/scene_{i+1}.png"
            img.save(path)
            images.append(path)
            
            print(f"✅ Created placeholder: {path}")
        
        return images
    
    def generate_with_free_api(self):
        """Use free image APIs"""
        # Placeholder API calls
        images = self.create_placeholder_images()
        return images
    
    def save_visual_data(self, images):
        """Save visual metadata"""
        data = {
            'topic': self.script.get('topic'),
            'scenes': []
        }
        
        for i, img_path in enumerate(images):
            data['scenes'].append({
                'scene_num': i + 1,
                'image_path': img_path,
                'duration': self.script.get('scenes', [{}])[i].get('duration', 3),
                'camera_movement': self.script.get('scenes', [{}])[i].get('camera_movement', 'none')
            })
        
        with open(f"{self.output_dir}/visual_data.json", 'w') as f:
            json.dump(data, f, indent=2)
        
        return data
    
    def run(self):
        """Generate all visuals"""
        print("🎨 STEP 3: VISUAL GENERATION STARTING...")
        
        if not self.script:
            print("❌ No script found")
            return
        
        # Generate image prompts
        prompts = self.generate_image_prompts()
        print(f"✅ Generated {len(prompts)} image prompts")
        
        # Create placeholder images
        images = self.generate_with_free_api()
        
        # Save metadata
        visual_data = self.save_visual_data(images)
        
        print(f"""
        ╔════════════════════════════════════╗
        ║     VISUALS GENERATED               ║
        ╚════════════════════════════════════╝
        Total Scenes: {len(images)}
        Output Directory: {self.output_dir}
        """)
        
        return visual_data

if __name__ == "__main__":
    generator = VisualGenerator()
    generator.run()
