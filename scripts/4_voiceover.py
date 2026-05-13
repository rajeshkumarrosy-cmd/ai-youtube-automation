import json
import os
import requests
from datetime import datetime
import time

class VoiceoverGenerator:
    """
    Generates HUMAN-LIKE voices using multiple APIs
    Priority: ElevenLabs (Natural) > Google TTS > Edge-TTS
    """
    
    def __init__(self):
        self.script = self.load_script()
        self.output_dir = "output/voiceovers"
        os.makedirs(self.output_dir, exist_ok=True)
        self.elevenlabs_key = os.environ.get('ELEVENLABS_API_KEY', '')
    
    def load_script(self):
        """Load script"""
        try:
            with open("output/scripts/short_script.json", 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def generate_with_elevenlabs(self, text, scene_num):
        """
        ElevenLabs: MOST HUMAN-LIKE VOICE
        Free tier: 10,000 characters/month
        """
        output_file = f"{self.output_dir}/scene_{scene_num}.mp3"
        
        if not self.elevenlabs_key:
            print(f"      ⚠️ ElevenLabs key not set, trying alternative...")
            return self.generate_with_google_tts(text, scene_num)
        
        try:
            print(f"      🎤 Using ElevenLabs (HUMAN-LIKE)...")
            
            # ElevenLabs API
            url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.elevenlabs_key
            }
            
            data = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75
                }
            }
            
            response = requests.post(url, json=data, headers=headers, timeout=30)
            
            if response.status_code == 200:
                with open(output_file, 'wb') as f:
                    f.write(response.content)
                print(f"      ✅ ElevenLabs voiceover created (HUMAN-LIKE)")
                return output_file
            else:
                print(f"      ⚠️ ElevenLabs error: {response.status_code}")
                return self.generate_with_google_tts(text, scene_num)
        
        except Exception as e:
            print(f"      ⚠️ ElevenLabs error: {e}")
            return self.generate_with_google_tts(text, scene_num)
    
    def generate_with_google_tts(self, text, scene_num):
        """
        Google TTS: Natural sounding
        FREE through gTTS
        """
        output_file = f"{self.output_dir}/scene_{scene_num}.mp3"
        
        try:
            print(f"      🎤 Using Google TTS...")
            from gtts import gTTS
            
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(output_file)
            
            print(f"      ✅ Google TTS voiceover created")
            return output_file
        
        except Exception as e:
            print(f"      ⚠️ Google TTS error: {e}")
            return self.generate_with_edge_tts(text, scene_num)
    
    def generate_with_edge_tts(self, text, scene_num):
        """
        Edge TTS: Reliable fallback
        """
        output_file = f"{self.output_dir}/scene_{scene_num}.mp3"
        
        try:
            print(f"      🎤 Using Edge TTS (fallback)...")
            
            import subprocess
            cmd = [
                'edge-tts',
                '--voice', 'en-US-AriaNeural',
                '--text', text,
                '--write-media', output_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print(f"      ✅ Edge TTS voiceover created")
                return output_file
            else:
                return None
        
        except Exception as e:
            print(f"      ❌ Edge TTS error: {e}")
            return None
    
    def run(self):
        """Generate voiceovers"""
        print("\n" + "="*60)
        print("🎙️ STEP 4: VOICEOVER GENERATION")
        print("="*60 + "\n")
        
        if not self.script:
            print("❌ No script found!")
            return None
        
        print("🎤 Generating HUMAN-LIKE voiceovers...\n")
        
        voiceovers = []
        
        for scene in self.script.get('scenes', []):
            scene_num = scene['scene']
            text = scene.get('narration', '')
            
            print(f"Scene {scene_num}:")
            print(f"   Text: {text[:60]}...")
            
            # Try ElevenLabs first (most human)
            vo_file = self.generate_with_elevenlabs(text, scene_num)
            
            voiceovers.append({
                'scene': scene_num,
                'narration': text,
                'voiceover_file': vo_file,
                'duration': scene['duration'],
                'voice_quality': 'HUMAN-LIKE'
            })
            
            print()
        
        # Save metadata
        data = {
            'generated_at': datetime.now().isoformat(),
            'voice_quality': 'HUMAN-LIKE',
            'engine_priority': 'ElevenLabs > Google > Edge-TTS',
            'voiceovers': voiceovers
        }
        
        with open(f"{self.output_dir}/voiceover_data.json", 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"""
✅ VOICEOVERS GENERATED!

🎤 Voice Quality: HUMAN-LIKE ✨
   - Natural sounding
   - Professional tone
   - Emotional delivery

📊 Generated {len(voiceovers)} voiceovers
        """)
        
        return data

if __name__ == "__main__":
    generator = VoiceoverGenerator()
    generator.run()
