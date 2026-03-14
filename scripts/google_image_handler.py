"""Fetch images from Google Custom Search API (Legal and Recommended)"""
import requests
from PIL import Image
from io import BytesIO
import time
import random
import os


class GoogleImageSearchHandler:
    """
    Uses Google Custom Search API - LEGAL and RECOMMENDED
    
    Setup:
    1. Go to https://console.cloud.google.com/apis/credentials
    2. Create API key (enable Custom Search API)
    3. Go to https://programmablesearchengine.google.com/
    4. Create Custom Search Engine
    5. Enable "Image Search" and "Search the entire web"
    6. Get your Search Engine ID
    7. Add to GitHub Secrets:
       - GOOGLE_SEARCH_API_KEY
       - GOOGLE_SEARCH_ENGINE_ID
    """
    
    def __init__(self, api_key=None, search_engine_id=None):
        # Get from environment if not provided
        self.api_key = api_key or os.environ.get('GOOGLE_SEARCH_API_KEY')
        self.search_engine_id = search_engine_id or os.environ.get('GOOGLE_SEARCH_ENGINE_ID')
        self.base_url = "https://www.googleapis.com/customsearch/v1"
        
        if not self.api_key or not self.search_engine_id:
            raise ValueError(
                "Google Custom Search credentials not found!\n"
                "Please set GOOGLE_SEARCH_API_KEY and GOOGLE_SEARCH_ENGINE_ID environment variables.\n"
                "Get them from:\n"
                "- API Key: https://console.cloud.google.com/apis/credentials\n"
                "- Search Engine ID: https://programmablesearchengine.google.com/"
            )
    
    def search_images(self, query, num_images=10, image_size='large'):
        """
        Search images using Google Custom Search API
        
        Args:
            query: Search query
            num_images: Number of images to fetch (max 10 per request)
            image_size: 'large', 'medium', or 'small'
            
        Returns:
            List of image data dicts
        """
        
        print(f"🔍 Searching Google for: {query}")
        
        try:
            params = {
                'key': self.api_key,
                'cx': self.search_engine_id,
                'q': query,
                'searchType': 'image',
                'num': min(num_images, 10),  # Max 10 per request
                'imgSize': image_size,
                'safe': 'active',
                'fileType': 'jpg,png,webp',
                'imgType': 'photo'  # Focus on photos, not clipart
            }
            
            response = requests.get(self.base_url, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            
            if 'items' not in data:
                print(f"⚠️ No images found for query: {query}")
                # --- DEBUG: show full API response to diagnose the issue ---
                print(f"🔎 Full API response keys: {list(data.keys())}")
                if 'error' in data:
                    err = data['error']
                    print(f"❌ API Error {err.get('code')}: {err.get('message')}")
                    for detail in err.get('errors', []):
                        print(f"   reason={detail.get('reason')} domain={detail.get('domain')}")
                if 'searchInformation' in data:
                    si = data['searchInformation']
                    print(f"📊 Total results: {si.get('totalResults', '0')}")
                if 'queries' in data:
                    req = data['queries'].get('request', [{}])[0]
                    print(f"📋 Query sent: cx={req.get('cx')}, q={req.get('searchTerms')}, type={req.get('searchType')}")
                # --- END DEBUG ---
                return []
            
            image_results = []
            for item in data.get('items', []):
                image_results.append({
                    'url': item['link'],
                    'thumbnail': item.get('image', {}).get('thumbnailLink'),
                    'title': item.get('title', 'Untitled'),
                    'source': item.get('displayLink', 'Unknown'),
                    'width': item.get('image', {}).get('width', 0),
                    'height': item.get('image', {}).get('height', 0),
                })
            
            print(f"✅ Found {len(image_results)} images from Google")
            return image_results
            
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code
            if status == 429:
                print("❌ Google API rate limit exceeded (429). Wait and try again.")
            elif status == 403:
                print("❌ Google API 403 Forbidden - likely causes:")
                print("   1. API key invalid or Custom Search API not enabled")
                print("   2. Daily quota of 100 queries exceeded")
                print("   3. Billing not set up on Google Cloud project")
                try:
                    err_data = e.response.json()
                    print(f"   API message: {err_data.get('error', {}).get('message', 'unknown')}")
                except Exception:
                    pass
            elif status == 400:
                print("❌ Google API 400 Bad Request - Search Engine ID (cx) may be wrong")
                try:
                    err_data = e.response.json()
                    print(f"   API message: {err_data.get('error', {}).get('message', 'unknown')}")
                except Exception:
                    pass
            else:
                print(f"❌ Google Custom Search API HTTP {status} error: {e}")
            return []
        except Exception as e:
            print(f"❌ Error searching Google: {e}")
            return []
    
    def download_image(self, url):
        """
        Download image from URL and return PIL Image
        
        Args:
            url: Image URL
            
        Returns:
            PIL Image object or None if failed
        """
        try:
            # Add delay between downloads
            time.sleep(random.uniform(0.3, 0.8))
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15, stream=True)
            response.raise_for_status()
            
            # Check if content is actually an image
            content_type = response.headers.get('content-type', '')
            if 'image' not in content_type.lower():
                print(f"⚠️ URL is not an image: {url[:60]}...")
                return None
            
            # Load image
            img = Image.open(BytesIO(response.content))
            
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Basic validation - ensure minimum quality (lowered to 300x300)
            if img.width < 300 or img.height < 300:
                print(f"⚠️ Image too small: {img.width}x{img.height}")
                return None
            
            return img
            
        except Exception as e:
            print(f"⚠️ Failed to download image from {url[:60]}...: {e}")
            return None
    
    def get_images_for_collage(self, query, num_images=4):
        """
        Get images for collage creation
        
        Args:
            query: Search query
            num_images: Number of images needed (3-4 recommended)
            
        Returns:
            List of dicts with image info compatible with collage generator
        """
        
        # Search for more images than needed (some may fail to download)
        search_count = min(num_images * 2, 10)  # Max 10 per API call
        search_results = self.search_images(query, search_count)
        
        if not search_results:
            print("❌ No images found from Google Custom Search")
            return []
        
        # Try to download images
        images_data = []
        
        for i, result in enumerate(search_results):
            if len(images_data) >= num_images:
                break
            
            print(f"📥 Downloading image {len(images_data)+1}/{num_images}...")
            
            img = self.download_image(result['url'])
            if img:
                images_data.append({
                    'url': result['url'],
                    'image': img,
                    'photographer': result.get('source', 'Google Search'),
                    'photographer_url': result['url'],
                    'source': 'google',
                    'title': result.get('title', '')
                })
                print(f"   ✅ {result.get('title', 'Untitled')[:50]}...")
        
        if len(images_data) < 2:
            print(f"⚠️ Only got {len(images_data)} images, need at least 2")
        else:
            print(f"✅ Successfully downloaded {len(images_data)} images")
        
        return images_data