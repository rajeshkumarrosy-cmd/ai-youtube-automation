import json
import os
import subprocess
from datetime import datetime

class VisualGenerator:
    def __init__(self):
        self.output_dir = "output/visuals"
        os.makedirs(self.output_dir, exist_ok=True)
        self.load_script()
    
    def load_script(self):
        try:
            with open("output/scripts/short_script.json", 'r') as f:
                self.script = json.load(f)
        except:
            self.script = None
    
    def create_video_background(self, scene_num, duration):
        """Create a simple colored video background"""
        output_file = f"{self.output_dir}/scene_{scene_num}.mp4"
        
        colors = ["#1a1a2e", "#16213e", "#0f3460", "#e94560"]
        color = colors[scene_num % len(colors)]
        
        print(f"   Creating scene {scene_num} video...")
        
        cmd = f'ffmpeg -f lavfi -i color=c={color}:s=1920x1080:d={duration} -vf fps=30 -c:v libx264 -preset ultrafast -crf 23 -y {output_file} 2>/dev/null'
        
        os.system(cmd)
        
        if os.path.exists(output_file):
            print(f"   ✅ Scene {scene_num} created")
            return output_file
        return None
    
    def run(self):
        print("\n" + "="*60)
        print("🎨 STEP 3: VISUAL GENERATION")
        print("="*60)
        
        if not self.script:
            print("❌ No script found!")
            return None
        
        print("\n🎬 Creating video backgrounds...\n")
        
        visuals = []
        for scene in self.script['scenes']:
            scene_num = scene['scene']
            duration = scene['duration']
            
            video_file = self.create_video_background(scene_num, duration)
            if video_file:
                visuals.append({
                    'scene': scene_num,
                    'file': video_file,
                    'duration': duration
                })
        
        data = {
            'generated_at': datetime.now().isoformat(),
            'scenes': visuals
        }
        
        with open(f"{self.output_dir}/visual_data.json", 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\n✅ Created {len(visuals)} video backgrounds\n")
        
        return data

if __name__ == "__main__":
    generator = VisualGenerator()
    generator.run()
