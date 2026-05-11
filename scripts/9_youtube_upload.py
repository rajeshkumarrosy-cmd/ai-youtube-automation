import json
import os
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import google_auth_oauthlib.flow

class YouTubeUploader:
    def __init__(self):
        self.seo_data = self.load_seo_data()
    
    def load_seo_data(self):
        """Load SEO optimization data"""
        try:
            with open("output/seo_package.json", 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def authenticate_youtube(self):
        """Authenticate with YouTube API"""
        try:
            # Using OAuth2 - store token in GitHub secrets
            CLIENT_SECRETS_FILE = "credentials.json"
            
            # For GitHub Actions, read from environment variable
            if not os.path.exists(CLIENT_SECRETS_FILE):
                creds_json = os.environ.get('YOUTUBE_CREDENTIALS')
                if creds_json:
                    with open(CLIENT_SECRETS_FILE, 'w') as f:
                        f.write(creds_json)
                else:
                    print("❌ YouTube credentials not found")
                    return None
            
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE,
                scopes=['https://www.googleapis.com/auth/youtube.upload']
            )
            
            creds = flow.run_local_server(port=0)
            
            return build('youtube', 'v3', credentials=creds)
        
        except Exception as e:
            print(f"⚠️ Authentication error: {e}")
            print("📝 Manual upload required or use YouTube CLI")
            return None
    
    def prepare_video_metadata(self, video_type='short'):
        """Prepare video metadata"""
        metadata = {
            'snippet': {
                'title': self.seo_data.get('best_title', 'Untitled Video'),
                'description': self.seo_data.get('description', ''),
                'tags': self.seo_data.get('tags', []),
                'categoryId': '24'  # Entertainment
            },
            'status': {
                'privacyStatus': 'public',
                'selfDeclaredMadeForKids': False
            }
        }
        
        return metadata
    
    def upload_to_youtube(self, video_file, video_type='short'):
        """Upload video to YouTube"""
        youtube = self.authenticate_youtube()
        
        if not youtube:
            print("❌ Upload failed - authentication error")
            print("📝 Please upload manually using: youtube-cli upload <file>")
            return None
        
        try:
            metadata = self.prepare_video_metadata(video_type)
            
            # Create media upload
            media = MediaFileUpload(
                video_file,
                mimetype='video/mp4',
                resumable=True,
                chunksize=1024*1024
            )
            
            # Create request
            request = youtube.videos().insert(
                part='snippet,status',
                body=metadata,
                media_body=media
            )
            
            # Execute
            print(f"📤 Uploading {video_file}...")
            response = request.execute()
            
            video_id = response['id']
            print(f"✅ Video uploaded! ID: {video_id}")
            
            return {
                'video_id': video_id,
                'url': f'https://youtube.com/watch?v={video_id}',
                'status': 'uploaded'
            }
        
        except Exception as e:
            print(f"⚠️ Upload error: {e}")
            return None
    
    def upload_thumbnail(self, thumbnail_file, video_id):
        """Upload custom thumbnail"""
        youtube = self.authenticate_youtube()
        
        if not youtube or not video_id:
            return None
        
        try:
            request = youtube.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(thumbnail_file)
            )
            
            response = request.execute()
            print(f"✅ Thumbnail uploaded for {video_id}")
            return response
        
        except Exception as e:
            print(f"⚠️ Thumbnail upload error: {e}")
            return None
    
    def add_hashtags_to_description(self):
        """Add hashtags to description"""
        description = self.seo_data.get('description', '')
        hashtags = ' '.join(self.seo_data.get('hashtags', []))
        
        return f"{description}\n\n{hashtags}"
    
    def schedule_upload(self, upload_time='14:00'):
        """Schedule video for best engagement time"""
        # Best times: Tuesday-Thursday, 2-4 PM UTC
        
        scheduled_info = {
            'scheduled_time': upload_time,
            'upload_days': ['Tuesday', 'Thursday', 'Saturday'],
            'timezone': 'UTC'
        }
        
        return scheduled_info
    
    def run(self):
        """Execute upload"""
        print("📤 STEP 9: YOUTUBE UPLOAD STARTING...")
        
        # Find video files
        video_files = [
            'output/videos/final_video_short.mp4',
            'output/videos/final_video_short_ffmpeg.mp4'
        ]
        
        video_file = None
        for vf in video_files:
            if os.path.exists(vf):
                video_file = vf
                break
        
        if not video_file:
            print("❌ No video file found")
            print("📝 Creating dummy upload record...")
            
            # Create dummy upload record
            upload_result = {
                'status': 'pending',
                'message': 'Video file not found - check video editing step',
                'recommended_action': 'Run video editing step and retry'
            }
        else:
            # Attempt upload
            upload_result = self.upload_to_youtube(video_file, 'short')
            
            if upload_result:
                # Upload thumbnail
                thumbnail_file = 'output/thumbnails/thumbnail_main.png'
                if os.path.exists(thumbnail_file):
                    self.upload_thumbnail(thumbnail_file, upload_result['video_id'])
        
        # Save upload record
        with open('output/upload_record.json', 'w') as f:
            json.dump(upload_result or {}, f, indent=2)
        
        print(f"""
        ╔════════════════════════════════════╗
        ║     YOUTUBE UPLOAD COMPLETE         ║
        ╚════════════════════════════════════╝
        Status: {upload_result.get('status', 'pending') if upload_result else 'failed'}
        """)
        
        return upload_result

if __name__ == "__main__":
    uploader = YouTubeUploader()
    uploader.run()
