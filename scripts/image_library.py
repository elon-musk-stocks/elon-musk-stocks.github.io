MUSK_LIBRARY = "assets/images/musk-library"
IMAGE_CATEGORIES = {
    "technology": ["tech", "ai", "robot", "software", "innovation"],
    "aerospace": ["spacex", "rocket", "satellite", "starlink", "mars"],
    "finance": ["stock", "chart", "trading", "investment", "money"],
    "lifestyle": ["elon", "ceo", "visionary", "office", "minimalist"]
}

def get_curated_musk_image(title="", category=None):
    """Get a curated Musk/Tech image, optionally matching category
    
    Args:
        title: Blog post title (used to match relevant images)
        category: Specific category (training, field, celebration, lifestyle)
    
    Returns:
        Path to selected image or None
    """
    
    if not os.path.exists(MUSK_LIBRARY):
        print(f"⚠️ Musk library not found: {MUSK_LIBRARY}")
        return None
    
    # Get all images
    image_extensions = ('.jpg', '.jpeg', '.png', '.webp')
    all_images = [
        f for f in os.listdir(MUSK_LIBRARY)
        if f.lower().endswith(image_extensions)
    ]
    
    if not all_images:
        print(f"⚠️ No images found in {MUSK_LIBRARY}")
        return None
    
    # Try to match category from title
    if not category and title:
        title_lower = title.lower()
        for cat, keywords in IMAGE_CATEGORIES.items():
            if any(kw in title_lower for kw in keywords):
                category = cat
                break
    
    # Filter by category if specified
    if category:
        category_images = [
            img for img in all_images 
            if any(kw in img.lower() for kw in IMAGE_CATEGORIES.get(category, []))
        ]
        if category_images:
            selected = random.choice(category_images)
            print(f"🎯 Selected {category} image: {selected}")
            return os.path.join(MUSK_LIBRARY, selected)
    
    # Random selection if no category match
    selected = random.choice(all_images)
    print(f"🖼️ Selected random image: {selected}")
    return os.path.join(MUSK_LIBRARY, selected)


def optimize_image(source_path, output_path, max_width=1920, max_height=960, quality=85):
    """Optimize and resize image for web
    
    Args:
        source_path: Original image path
        output_path: Where to save optimized image
        max_width: Maximum width in pixels
        max_height: Maximum height in pixels
        quality: WebP quality (1-100)
    """
    
    try:
        img = Image.open(source_path).convert("RGB")
        original_size = os.path.getsize(source_path)
        original_width, original_height = img.size
        
        print(f"📊 Original: {original_width}x{original_height}, {original_size / 1024:.1f} KB")
        
        # Resize if needed (maintain aspect ratio)
        if original_width > max_width or original_height > max_height:
            img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            new_width, new_height = img.size
            print(f"🔧 Resized to: {new_width}x{new_height}")
        
        # Save as WebP
        img.save(output_path, "WEBP", quality=quality, method=6, optimize=True)
        
        compressed_size = os.path.getsize(output_path)
        compression_ratio = (1 - compressed_size / original_size) * 100
        
        print(f"📊 Optimized: {compressed_size / 1024:.1f} KB (saved {compression_ratio:.1f}%)")
        print(f"✅ Image saved: {output_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error optimizing image: {e}")
        return False