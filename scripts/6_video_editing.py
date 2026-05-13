import json
import os
import subprocess
from datetime import datetime

class VideoEditor:
    def __init__(self):
        self.output_dir = "output/videos"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def load_assets(self):
        """Load visual and voiceover data"""
        print("   Loading assets...")
        
        visuals = []
        try:
            with open("output/visuals/visual_data.json", 'r') as f:
                visuals = json.load(f).get('scenes', [])
                print(f"      ✅ Found {len(visuals)} visual scenes")
        except Exception as e:
            print(f"      ❌ Visual error: {e}")
        
        voiceovers = []
        try:
            with open("output/voiceovers/voiceover_data.json", 'r') as f:
                voiceovers = json.load(f).get('voiceovers', [])
                print(f"      ✅ Found {len(voiceovers)} voiceovers")
        except Exception as e:
            print(f"      ❌ Voiceover error: {e}")
        
        return visuals, voiceovers
    
    def combine_video_audio_ffmpeg(self, video_file, audio_file, output_file, scene_num):
        """Combine video + audio using FFmpeg"""
        print(f"      Combining Scene {scene_num}...")
        
        try:
            # FFmpeg command to combine video and audio
            cmd = [
                'ffmpeg',
                '-i', video_file,
                '-i', audio_file,
                '-c:v', 'libx264',
                '-c:a', 'aac',
                '-shortest',
                '-y',
                output_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0 and os.path.exists(output_file):
                size = os.path.getsize(output_file) / (1024 * 1024)
                print(f"      ✅ Combined ({size:.2f} MB)")
                return output_file
            else:
                print(f"      ⚠️ Combine failed, using video as fallback")
                # Return video file as fallback
                return video_file
        
        except Exception as e:
            print(f"      ⚠️ Error: {e}")
            return video_file
    
    def concatenate_videos_ffmpeg(self, scene_files, output_file):
        """Concatenate multiple videos using FFmpeg"""
        print(f"\n   Concatenating {len(scene_files)} scenes...")
        
        # Create concat file
        concat_file = f"{self.output_dir}/concat.txt"
        with open(concat_file, 'w') as f:
            for sf in scene_files:
                abs_path = os.path.abspath(sf)
                f.write(f"file '{abs_path}'\n")
        
        try:
            # FFmpeg concat command
            cmd = [
                'ffmpeg',
                '-f', 'concat',
                '-safe', '0',
                '-i', concat_file,
                '-c', 'copy',
                '-y',
                output_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0 and os.path.exists(output_file):
                size = os.path.getsize(output_file) / (1024 * 1024)
                print(f"   ✅ Concatenated ({size:.2f} MB)")
                return output_file
            else:
                print(f"   ⚠️ Concat failed")
                # Return first scene as fallback
                if scene_files:
                    import shutil
                    shutil.copy(scene_files[0], output_file)
                    print(f"   ⚠️ Using first scene as output")
                    return output_file
        
        except Exception as e:
            print(f"   ⚠️ Error: {e}")
            return None
    
    def verify_files_exist(self, visuals, voiceovers):
        """Check if all files exist"""
        print("\n   Verifying files...")
        
        for visual in visuals:
            video_file = visual.get('file')
            if not os.path.exists(video_file):
                print(f"      ❌ Missing video: {video_file}")
                return False
            else:
                size = os.path.getsize(video_file) / (1024 * 1024)
                print(f"      ✅ Scene {visual['scene']}: {size:.2f} MB")
        
        for vo in voiceovers:
            audio_file = vo.get('file')
            if not os.path.exists(audio_file):
                print(f"      ❌ Missing audio: {audio_file}")
                return False
            else:
                size = os.path.getsize(audio_file) / 1024
                print(f"      ✅ Voice {vo['scene']}: {size:.1f} KB")
        
        return True
    
    def run(self):
        print("\n" + "="*70)
        print("🎬 STEP 6: VIDEO EDITING")
        print("="*70)
        
        # Load assets
        visuals, voiceovers = self.load_assets()
        
        if not visuals or not voiceovers:
            print("\n❌ Missing assets!")
            print(f"   Visuals: {len(visuals)}")
            print(f"   Voiceovers: {len(voiceovers)}")
            return None
        
        # Verify files exist
        if not self.verify_files_exist(visuals, voiceovers):
            print("\n❌ Some files are missing!")
            return None
        
        print(f"\n🎬 Creating final video...\n")
        
        # Combine each scene with audio
        scene_files = []
        
        for i, visual in enumerate(visuals):
            if i < len(voiceovers):
                video_file = visual.get('file')
                audio_file = voiceovers[i].get('file')
                
                scene_output = f"{self.output_dir}/scene_{i+1}_final.mp4"
                
                result = self.combine_video_audio_ffmpeg(
                    video_file, audio_file, scene_output, i+1
                )
                
                if result and os.path.exists(result):
                    scene_files.append(result)
                else:
                    print(f"      ⚠️ Scene {i+1} failed, skipping...")
        
        if not scene_files:
            print("\n❌ Failed to create any scene videos!")
            return None
        
        # Concatenate all scenes into final video
        final_video = f"{self.output_dir}/final_video_short.mp4"
        
        result = self.concatenate_videos_ffmpeg(scene_files, final_video)
        
        if result and os.path.exists(result):
            size = os.path.getsize(result) / (1024 * 1024)
            
            print(f"""
✅ VIDEO CREATED SUCCESSFULLY!

📹 File: {result}
📊 Size: {size:.2f} MB
✨ Ready for YouTube!
            """)
            
            return {'file': result, 'size_mb': size}
        else:
            print("\n❌ Final video creation failed!")
            return None

if __name__ == "__main__":
    editor = VideoEditor()
    editor.run()
