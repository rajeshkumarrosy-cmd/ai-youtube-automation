import json
import os
import subprocess
from datetime import datetime

class VideoEditor:
    def __init__(self):
        self.output_dir = "output/videos"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def load_assets(self):
        try:
            with open("output/visuals/visual_data.json", 'r') as f:
                visuals = json.load(f)['scenes']
        except:
            visuals = []
        
        try:
            with open("output/voiceovers/voiceover_data.json", 'r') as f:
                voiceovers = json.load(f)['voiceovers']
        except:
            voiceovers = []
        
        return visuals, voiceovers
    
    def combine_video_and_audio(self, video_file, audio_file, output_file):
        """Combine video + audio using ffmpeg"""
        print(f"      Combining audio...")
        
        cmd = [
            'ffmpeg',
            '-i', video_file,
            '-i', audio_file,
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-shortest',
            '-y',
            output_file
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        return result.returncode == 0
    
    def concatenate_videos(self, video_files, output_file):
        """Concatenate multiple videos"""
        print(f"   Combining all scenes...")
        
        concat_file = f"{self.output_dir}/concat.txt"
        with open(concat_file, 'w') as f:
            for vf in video_files:
                f.write(f"file '{os.path.abspath(vf)}'\n")
        
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
        return result.returncode == 0
    
    def run(self):
        print("\n" + "="*60)
        print("🎬 STEP 6: VIDEO EDITING")
        print("="*60)
        
        visuals, voiceovers = self.load_assets()
        
        if not visuals or not voiceovers:
            print("❌ Missing assets!")
            return None
        
        print(f"\n🎬 Creating final video...\n")
        
        # Step 1: Combine each video with its audio
        print("   Creating scenes with audio...")
        scene_videos = []
        
        for i, visual in enumerate(visuals):
            if i < len(voiceovers):
                video_file = visual['file']
                audio_file = voiceovers[i]['file']
                
                scene_output = f"{self.output_dir}/scene_{i+1}_final.mp4"
                
                if self.combine_video_and_audio(video_file, audio_file, scene_output):
                    print(f"      ✅ Scene {i+1} combined")
                    scene_videos.append(scene_output)
                else:
                    print(f"      ⚠️ Scene {i+1} failed")
        
        if not scene_videos:
            print("❌ Failed to create scene videos!")
            return None
        
        # Step 2: Concatenate all scenes
        final_video = f"{self.output_dir}/final_video_short.mp4"
        
        if self.concatenate_videos(scene_videos, final_video):
            file_size = os.path.getsize(final_video) / (1024 * 1024)
            print(f"\n✅ FINAL VIDEO CREATED!")
            print(f"   File: {final_video}")
            print(f"   Size: {file_size:.2f} MB\n")
            
            return {'file': final_video, 'size_mb': file_size}
        else:
            print("❌ Video concatenation failed!")
            return None

if __name__ == "__main__":
    editor = VideoEditor()
    editor.run()
