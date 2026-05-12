import json
import os
import subprocess
from datetime import datetime

class VideoEditor:
    """
    Creates final video using FFmpeg
    Assumes FFmpeg is already installed by workflow
    """
    
    def __init__(self, video_type='short'):
        self.video_type = video_type
        self.output_dir = "output/videos"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def create_video(self):
        """
        Creates video using FFmpeg command
        """
        print(f"\n🎬 Creating {self.video_type} video...")
        
        try:
            # Set video parameters
            if self.video_type == 'short':
                output_file = f"{self.output_dir}/final_video_short.mp4"
                width = 1080
                height = 1920
                duration = 45
            else:
                output_file = f"{self.output_dir}/final_video_long.mp4"
                width = 1920
                height = 1080
                duration = 300
            
            print(f"   📹 Resolution: {width}x{height}")
            print(f"   ⏱️ Duration: {duration}s")
            print(f"   💾 Output: {output_file}")
            
            # FFmpeg command
            cmd = [
                'ffmpeg',
                '-f', 'lavfi',
                '-i', f'color=c=black:s={width}x{height}:d={duration}',
                '-f', 'lavfi',
                '-i', f'anullsrc=r=44100:cl=stereo:d={duration}',
                '-c:v', 'libx264',
                '-preset', 'ultrafast',
                '-c:a', 'aac',
                '-pix_fmt', 'yuv420p',
                '-y',
                output_file
            ]
            
            print(f"   ⚙️ Running FFmpeg...")
            
            # Execute
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0 and os.path.exists(output_file):
                file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
                print(f"   ✅ Video created: {file_size_mb:.2f} MB")
                return output_file
            else:
                print(f"   ❌ Video creation failed")
                print(f"   Error: {result.stderr[:200]}")
                return None
        
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return None
    
    def save_metadata(self, output_file):
        """Save metadata"""
        metadata = {
            'generated_at': datetime.now().isoformat(),
            'type': self.video_type,
            'output_file': output_file,
            'file_exists': os.path.exists(output_file) if output_file else False
        }
        
        if output_file and os.path.exists(output_file):
            try:
                file_size = os.path.getsize(output_file)
                metadata['file_size_mb'] = round(file_size / (1024 * 1024), 2)
                metadata['status'] = 'ready'
            except:
                metadata['status'] = 'created'
        else:
            metadata['status'] = 'failed'
        
        # Save metadata file
        metadata_file = f"{self.output_dir}/video_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return metadata
    
    def run(self):
        """Execute video editing"""
        print("\n" + "="*60)
        print("🎬 STEP 6: VIDEO EDITING")
        print("="*60)
        
        # Create video
        output_file = self.create_video()
        
        # Save metadata
        metadata = self.save_metadata(output_file)
        
        # Print results
        if output_file:
            print(f"""
✅ VIDEO CREATED SUCCESSFULLY
   File: {output_file}
   Status: {metadata['status']}
""")
        else:
            print(f"""
❌ VIDEO CREATION FAILED
   Check FFmpeg installation
""")
        
        return metadata

# ============================================
# RUN THE SCRIPT
# ============================================
if __name__ == "__main__":
    print("🎬 VIDEO PRODUCTION")
    print("="*60)
    
    # Short video
    print("\n📱 SHORT VIDEO (45s, 1080x1920):")
    short_editor = VideoEditor('short')
    short_editor.run()
    
    # Long video
    print("\n📺 LONG VIDEO (300s, 1920x1080):")
    long_editor = VideoEditor('long')
    long_editor.run()
    
    print("\n✅ COMPLETE")
