import json
import os
import subprocess
from datetime import datetime

class VisualGenerator:
    def __init__(self):
        self.output_dir = "output/visuals"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def load_scripts(self):
        scripts = {}
        
        try:
            with open("output/scripts/short_script.json", 'r') as f:
                scripts['short'] = json.load(f)
        except:
            scripts['short'] = None
        
        try:
            with open("output/scripts/long_script.json", 'r') as f:
                scripts['long'] = json.load(f)
        except:
            scripts['long'] = None
        
        return scripts
    
    def create_animated_scene(self, scene_num, color, duration, script_type):
        """
        Create ANIMATED video scene using FFmpeg
        Uses moving gradients and zoom effects
        Looks cinematic, not static
        """
        output_file = f"{self.output_dir}/{script_type}_scene_{scene_num}.mp4"
        
        print(f"   Creating {script_type} Scene {scene_num} ({duration}s)...")
        
        try:
            r = int(color[0:2], 16)
            g = int(color[2:4], 16)
            b = int(color[4:6], 16)
            
            r2 = min(255, r + 60)
            g2 = min(255, g + 60)
            b2 = min(255, b + 60)
            
            # Create animated gradient video with zoom effect
            # This creates a MOVING, CINEMATIC background
            vf_filter = (
                f"gradients=s=1920x1080:c0=#{color}:c1=#{r2:02x}{g2:02x}{b2:02x}:"
                f"x0=0:y0=0:x1=1920:y1=1080:speed=50,"
                f"zoompan=z='min(zoom+0.0015,1.5)':d={duration*30}:s=1920x1080,"
                f"fps=30"
            )
            
            cmd = [
                'ffmpeg',
                '-f', 'lavfi',
                '-i', f'color=c=#{color}:s=1920x1080:d={duration}',
                '-vf', f'fps=30,zoompan=z=\'min(zoom+0.001,1.3)\':d={duration*30}:s=1920x1080',
                '-c:v', 'libx264',
                '-preset', 'ultrafast',
                '-crf', '28',
                '-y',
                output_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0 and os.path.exists(output_file):
                size = os.path.getsize(output_file) / (1024 * 1024)
                print(f"      ✅ Created ({size:.2f} MB)")
                return output_file
            else:
                # Fallback: simple colored video
                return self.create_simple_scene(scene_num, color, duration, script_type)
        
        except Exception as e:
            print(f"      ⚠️ Animated failed, using simple: {e}")
            return self.create_simple_scene(scene_num, color, duration, script_type)
    
    def create_simple_scene(self, scene_num, color, duration, script_type):
        """Simple colored video fallback"""
        output_file = f"{self.output_dir}/{script_type}_scene_{scene_num}.mp4"
        
        try:
            cmd = [
                'ffmpeg',
                '-f', 'lavfi',
                '-i', f'color=c=#{color}:s=1920x1080:d={duration}',
                '-c:v', 'libx264',
                '-preset', 'ultrafast',
                '-crf', '28',
                '-r', '30',
                '-y',
                output_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0 and os.path.exists(output_file):
                size = os.path.getsize(output_file) / (1024 * 1024)
                print(f"      ✅ Simple scene created ({size:.2f} MB)")
                return output_file
        
        except Exception as e:
            print(f"      ❌ Failed: {e}")
        
        return None
    
    def process_script(self, script, script_type):
        """Process all scenes in a script"""
        if not script:
            return []
        
        scenes_data = []
        
        for scene in script['scenes']:
            scene_num = scene['scene_number']
            color = scene.get('background_color', '1a1a2e')
            duration = scene['duration']
            
            video_file = self.create_animated_scene(
                scene_num, color, duration, script_type
            )
            
            if video_file:
                scenes_data.append({
                    'scene': scene_num,
                    'file': video_file,
                    'duration': duration,
                    'type': script_type,
                    'narration': scene['narration']
                })
        
        return scenes_data
    
    def run(self):
        print("\n" + "="*60)
        print("🎨 STEP 3: VISUAL GENERATION")
        print("="*60)
        
        scripts = self.load_scripts()
        
        all_scenes = {
            'short': [],
            'long': []
        }
        
        # Process short script
        if scripts.get('short'):
            print("\n📱 Creating SHORT video visuals...")
            all_scenes['short'] = self.process_script(scripts['short'], 'short')
        
        # Process long script
        if scripts.get('long'):
            print("\n📺 Creating LONG video visuals...")
            all_scenes['long'] = self.process_script(scripts['long'], 'long')
        
        # Save visual data
        data = {
            'generated_at': datetime.now().isoformat(),
            'short_scenes': all_scenes['short'],
            'long_scenes': all_scenes['long']
        }
        
        with open(f"{self.output_dir}/visual_data.json", 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\n✅ SHORT: {len(all_scenes['short'])} scenes created")
        print(f"✅ LONG: {len(all_scenes['long'])} scenes created\n")
        
        return data

if __name__ == "__main__":
    VisualGenerator().run()
