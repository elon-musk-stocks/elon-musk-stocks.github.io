"""
Autoblogging 
Works with Gumroad's built-in license keys
"""
import os
import hashlib
import re


class LicenseValidator:
    """
    Validates license keys before running autoblogging scripts
    Accepts Gumroad's automatically generated license keys
    """
    
    def __init__(self):
        # Customer's license key (they add this to their GitHub secrets)
        self.customer_license = os.environ.get("LICENSE_KEY")
        
        # Repository identifier
        self.repo_id = os.environ.get("GITHUB_REPOSITORY")
        
    def validate_license(self):
        """
        Validate license before running scripts
        
        Returns:
            bool: True if valid, False otherwise
        """
        
        print("=" * 60)
        print("🔐 VALIDATING LICENSE")
        print("=" * 60)
        
        # Check if license key exists
        if not self.customer_license:
            print("❌ LICENSE_KEY not found in environment variables")
            print("")
            print("💡 This script requires a valid license.")
            print("📧 Purchase at: https://gumroad.com/your-product")
            print("")
            print("After purchase:")
            print("1. Go to Settings → Secrets → Actions")
            print("2. Add: LICENSE_KEY = (your key from email)")
            print("3. Run workflow again")
            return False
        
        # Check if running in GitHub Actions (optional - remove if you want local testing)
        if not self.repo_id:
            print("⚠️  GITHUB_REPOSITORY not found")
            print("💡 This script is designed to run in GitHub Actions")
            # Allow local testing by uncommenting:
            # return self._validate_format()
            return False
        
        # Validate license format
        if not self._validate_format():
            print("❌ Invalid license key format")
            print("")
            print("💡 Your license key should look like:")
            print("   - XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX (Gumroad format)")
            print("   - Or similar alphanumeric format")
            print("")
            print("🆘 If you purchased but key doesn't work:")
            print("   Contact support: your-email@domain.com")
            return False
        
        # Basic validation passed
        print("✅ License key format valid!")
        print(f"📦 Repository: {self.repo_id}")
        print(f"🔑 License: {self.customer_license[:8]}...{self.customer_license[-4:]}")
        
        return True
    
    def _validate_format(self):
        """
        Check if license key has valid format
        Accepts multiple formats:
        - Gumroad: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
        - UUID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        - Alphanumeric: Any 20+ character alphanumeric string
        """
        try:
            key = self.customer_license.strip()
            
            # Remove any whitespace
            key = key.replace(" ", "")
            
            # Check minimum length
            if len(key) < 16:
                print(f"⚠️  License too short: {len(key)} chars (minimum 16)")
                return False
            
            # Check if it's alphanumeric with optional hyphens
            if not re.match(r'^[A-Za-z0-9\-_]+$', key):
                print("⚠️  License contains invalid characters")
                return False
            
            # Format looks good
            return True
            
        except Exception as e:
            print(f"⚠️  Format validation error: {e}")
            return False


def check_license_before_run():
    """
    Call this at the start of generate_posts.py
    Exits script if license is invalid
    """
    validator = LicenseValidator()
    
    if not validator.validate_license():
        print("\n" + "=" * 60)
        print("🚫 SCRIPT EXECUTION BLOCKED")
        print("=" * 60)
        print("This autoblogging script requires a valid license key.")
        print("Purchase at: https://gumroad.com/your-product")
        print("=" * 60)
        exit(1)
    
    print("=" * 60)
    print("✅ LICENSE VALID - CONTINUING EXECUTION")
    print("=" * 60)
    print()


if __name__ == "__main__":
    # Test validation
    print("🧪 Testing license validation...")
    print()
    
    test_key = os.environ.get("LICENSE_KEY", "TEST1234-5678-90AB-CDEF-GHIJKLMNOPQR")
    print(f"Test key: {test_key}")
    print()
    
    validator = LicenseValidator()
    if validator.validate_license():
        print("\n✅ Validation successful!")
    else:
        print("\n❌ Validation failed!")