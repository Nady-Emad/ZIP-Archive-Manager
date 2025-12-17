"""
Security Module
Handles password protection and encryption for ZIP archives
"""

import zipfile
import hashlib
import secrets
from typing import Optional


class SecurityManager:
    """Manages security features for ZIP archives"""
    
    # Minimum password length for security
    MIN_PASSWORD_LENGTH = 4
    RECOMMENDED_PASSWORD_LENGTH = 12
    
    @classmethod
    def validate_password(cls, password: str) -> tuple[bool, str]:
        """
        Validate password strength
        
        Args:
            password: Password to validate
            
        Returns:
            tuple: (is_valid, message)
        """
        if not password:
            return False, "Password cannot be empty"
        
        if len(password) < cls.MIN_PASSWORD_LENGTH:
            return False, f"Password must be at least {cls.MIN_PASSWORD_LENGTH} characters"
        
        # Check for basic strength (optional warnings)
        warnings = []
        if len(password) < cls.RECOMMENDED_PASSWORD_LENGTH:
            warnings.append(f"Recommended password length is {cls.RECOMMENDED_PASSWORD_LENGTH} characters")
        
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)
        
        if not (has_upper and has_lower and has_digit):
            warnings.append("Strong passwords include uppercase, lowercase, and numbers")
        
        message = " - ".join(warnings) if warnings else "Password is acceptable"
        return True, message
    
    @classmethod
    def generate_password(cls, length: int = 16, include_special: bool = True) -> str:
        """
        Generate a secure random password
        
        Args:
            length: Password length
            include_special: Include special characters
            
        Returns:
            str: Generated password
        """
        import string
        
        chars = string.ascii_letters + string.digits
        if include_special:
            chars += string.punctuation
        
        return ''.join(secrets.choice(chars) for _ in range(length))
    
    @classmethod
    def hash_password(cls, password: str) -> str:
        """
        Create a hash of the password for verification (not for encryption)
        
        Args:
            password: Password to hash
            
        Returns:
            str: Hexadecimal hash
        """
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    @classmethod
    def test_archive_password(cls, archive_path: str, password: str) -> bool:
        """
        Test if a password is correct for an encrypted archive
        
        Args:
            archive_path: Path to the ZIP file
            password: Password to test
            
        Returns:
            bool: True if password is correct, False otherwise
        """
        try:
            with zipfile.ZipFile(archive_path, 'r') as zipf:
                # Try to read the first file with the password
                for name in zipf.namelist():
                    if not name.endswith('/'):  # Skip directories
                        zipf.read(name, pwd=password.encode('utf-8'))
                        return True
            return True
        except RuntimeError:
            # Wrong password
            return False
        except Exception:
            # Other error
            return False
    
    @classmethod
    def is_encrypted(cls, archive_path: str) -> bool:
        """
        Check if a ZIP archive is password-protected
        
        Args:
            archive_path: Path to the ZIP file
            
        Returns:
            bool: True if encrypted, False otherwise
        """
        try:
            with zipfile.ZipFile(archive_path, 'r') as zipf:
                for info in zipf.infolist():
                    if info.flag_bits & 0x1:  # Check encryption bit
                        return True
            return False
        except Exception:
            return False
    
    @classmethod
    def get_encryption_info(cls, archive_path: str) -> dict:
        """
        Get encryption information for an archive
        
        Args:
            archive_path: Path to the ZIP file
            
        Returns:
            dict: Encryption information
        """
        try:
            is_encrypted = cls.is_encrypted(archive_path)
            with zipfile.ZipFile(archive_path, 'r') as zipf:
                encrypted_files = sum(1 for info in zipf.infolist() if info.flag_bits & 0x1)
                total_files = len(zipf.infolist())
                
                return {
                    'is_encrypted': is_encrypted,
                    'encrypted_files': encrypted_files,
                    'total_files': total_files,
                    'encryption_type': 'ZIP 2.0 (Legacy)' if is_encrypted else 'None'
                }
        except Exception as e:
            return {
                'is_encrypted': False,
                'encrypted_files': 0,
                'total_files': 0,
                'encryption_type': 'Unknown',
                'error': str(e)
            }
