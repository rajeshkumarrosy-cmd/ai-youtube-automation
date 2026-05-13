import json
import os
from pathlib import Path

class FastVisualGenerator:
    """Creates DUMMY video files for testing (no downloads!)"""
    
    def __init__(self):
        self.output_dir = "output/visuals"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def create_dummy_video(self, filename, duration=5):
        """Create a small dummy MP4 file using FFmpeg"""
        import subprocess
        
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            # Create a black video (no download needed!)
            cmd = [
                'ffmpeg',
                '-f', 'lavfi',
                '-i', f'color=c=black:s=1280x720:d={duration}',
                '-pix_fmt', 'yuv420p',
                '-c:v', 'libx264',
                '-preset', 'ultrafast',  # Super fast!
                '-y',
                filepath
            ]
            
            print(f"      Creating {filename}...")
            result = subprocess.run(cmd, capture_output=True, timeout=30)
            
            if os.path.exists(filepath):
                size = os.path.getsize(filepath) / (1024 * 1024)
                print(f"      ✅ {filename} ({size:.2f} MB)")
                return filepath
            else:
                print(f"      ❌ Failed to create {filename}")
                return None
                
        except Exception as e:
            print(f"      ⚠️ Error: {e}")
            return None
    
    def run(self):
        print("\n" + "="*70)
        print("🎨 STEP 3: VISUAL GENERATION (FAST MODE - DUMMY VIDEOS)")
        print("="*70 + "\n")
        
        # Load script data
        print("   Loading script...")
        try:
            with open("output/scripts/short_script.json", 'r') as f:
                script_data = json.load(f)
                scenes = script_data.get('scenes', [])
                print(f"   ✅ Found {len(scenes)} scenes\n")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return None
        
        # Create dummy videos
        print("   Creating dummy videos...")
        visual_data = {'scenes': []}
        
        for i, scene in enumerate(scenes):
            video_file = self.create_dummy_video(f"scene_{i+1}.mp4", duration=5)
            
            if video_file:
                visual_data['scenes'].append({
                    'scene': i + 1,
                    'description': scene.get('description', ''),
                    'file': video_file
                })
        
        # Save visual data
        output_file = os.path.join(self.output_dir, "visual_data.json")
        with open(output_file, 'w') as f:
            json.dump(visual_data, f, indent=2)
        
        print(f"\n✅ STEP 3 COMPLETE!")
        print(f"   📊 Scenes created: {len(visual_data['scenes'])}")
        print(f"   📁 Saved to: {output_file}\n")
        
        return visual_data

if __name__ == "__main__":
    generator = FastVisualGenerator()
    generator.run()
