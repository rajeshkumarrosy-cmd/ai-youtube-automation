import os
import json
from datetime import datetime

class YouTubeUploader:
    def __init__(self):
        self.output_dir = "output"
    
    def check_video_exists(self):
        """Check if video file exists"""
        video_paths = [
            "output/videos/final_video_short.mp4",
            "output/videos/final_video_long.mp4"
        ]
        
        existing_videos = []
        
        for path in video_paths:
            if os.path.exists(path):
                size = os.path.getsize(path) / (1024 * 1024)
                existing_videos.append({
                    'path': path,
                    'size_mb': round(size, 2)
                })
        
        return existing_videos
    
    def load_seo_data(self):
        """Load SEO data if exists"""
        try:
            with open("output/seo_package.json", 'r') as f:
                return json.load(f)
        except:
            return {
                'title': 'Amazing AI Story - You Won\'t Believe What Happened',
                'description': 'This incredible story will change your perspective.',
                'tags': ['#Story', '#Amazing', '#AI']
            }
    
    def create_upload_record(self, videos, seo_data):
        """Create upload instructions"""
        record = {
            'generated_at': datetime.now().isoformat(),
            'status': 'ready_for_manual_upload',
            'videos_found': len(videos),
            'videos': videos,
            'seo_data': seo_data,
            'instructions': [
                "1. Download the video file from output/videos/",
                "2. Go to https://youtube.com/studio",
                "3. Click 'Create' → 'Upload video'",
                "4. Upload the video file",
                "5. Copy title and description from seo_data",
                "6. Add tags",
                "7. Upload thumbnail from output/thumbnails/",
                "8. Publish!"
            ]
        }
        
        output_file = f"{self.output_dir}/upload_record.json"
        with open(output_file, 'w') as f:
            json.dump(record, f, indent=2)
        
        return record
    
    def print_instructions(self, videos, seo_data):
        """Print upload instructions"""
        print("\n" + "="*70)
        print("📤 STEP 9: YOUTUBE UPLOAD")
        print("="*70)
        
        if videos:
            print(f"\n✅ VIDEO READY FOR YOUTUBE!")
            print(f"\n📹 Video Files Found:")
            
            for video in videos:
                print(f"   ✅ {video['path']}")
                print(f"      Size: {video['size_mb']} MB")
            
            print(f"\n📋 UPLOAD INFORMATION:")
            print(f"   Title: {seo_data.get('title', 'Amazing Story')}")
            print(f"   Description: {seo_data.get('description', 'Amazing story')[:100]}...")
            print(f"   Tags: {', '.join(seo_data.get('tags', [])[:5])}")
            
            print(f"\n📝 MANUAL UPLOAD STEPS:")
            print(f"   1. Download video from GitHub")
            print(f"   2. Go to: https://youtube.com/studio")
            print(f"   3. Click 'Create' → 'Upload video'")
            print(f"   4. Upload the video file")
            print(f"   5. Copy title & description above")
            print(f"   6. Upload thumbnail")
            print(f"   7. Publish!")
            
            print(f"\n✅ Upload record saved: output/upload_record.json")
        
        else:
            print(f"\n❌ NO VIDEO FILES FOUND!")
            print(f"   Check Step 6 (Video Editing)")
            print(f"   Ensure videos exist in output/videos/")
        
        print("\n")
    
    def run(self):
        """Execute upload step"""
        # Check videos
        videos = self.check_video_exists()
        
        # Load SEO data
        seo_data = self.load_seo_data()
        
        # Create upload record
        self.create_upload_record(videos, seo_data)
        
        # Print instructions
        self.print_instructions(videos, seo_data)
        
        return {
            'videos_found': len(videos),
            'status': 'ready' if videos else 'failed'
        }

if __name__ == "__main__":
    uploader = YouTubeUploader()
    uploader.run()
