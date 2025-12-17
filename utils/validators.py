"""
Archive Validators Module
Handles verification and validation of ZIP archives
"""

import zipfile
import os
from typing import List, Dict, Optional


class ArchiveValidator:
    """Validates and verifies ZIP archive integrity"""
    
    @staticmethod
    def validate_archive(archive_path: str) -> tuple[bool, str]:
        """
        Validate ZIP archive integrity
        
        Args:
            archive_path: Path to the ZIP file
            
        Returns:
            tuple: (is_valid, message)
        """
        if not os.path.exists(archive_path):
            return False, "Archive file does not exist"
        
        if not os.path.isfile(archive_path):
            return False, "Path is not a file"
        
        try:
            with zipfile.ZipFile(archive_path, 'r') as zipf:
                # Test the archive
                bad_file = zipf.testzip()
                if bad_file:
                    return False, f"Corrupted file found: {bad_file}"
                
                return True, "Archive is valid"
                
        except zipfile.BadZipFile:
            return False, "Invalid or corrupted ZIP file"
        except Exception as e:
            return False, f"Error validating archive: {str(e)}"
    
    @staticmethod
    def verify_crc(archive_path: str) -> Dict[str, any]:
        """
        Verify CRC checksums for all files in archive
        
        Args:
            archive_path: Path to the ZIP file
            
        Returns:
            dict: Verification results
        """
        results = {
            'valid': True,
            'total_files': 0,
            'verified_files': 0,
            'failed_files': [],
            'errors': []
        }
        
        try:
            with zipfile.ZipFile(archive_path, 'r') as zipf:
                for info in zipf.infolist():
                    if not info.is_dir():
                        results['total_files'] += 1
                        try:
                            # Reading the file verifies the CRC
                            zipf.read(info.filename)
                            results['verified_files'] += 1
                        except Exception as e:
                            results['valid'] = False
                            results['failed_files'].append(info.filename)
                            results['errors'].append(f"{info.filename}: {str(e)}")
            
        except Exception as e:
            results['valid'] = False
            results['errors'].append(f"Error opening archive: {str(e)}")
        
        return results
    
    @staticmethod
    def check_compression_ratio(archive_path: str) -> Optional[float]:
        """
        Calculate compression ratio of archive
        
        Args:
            archive_path: Path to the ZIP file
            
        Returns:
            float: Compression ratio percentage, or None on error
        """
        try:
            with zipfile.ZipFile(archive_path, 'r') as zipf:
                total_compressed = sum(info.compress_size for info in zipf.infolist())
                total_uncompressed = sum(info.file_size for info in zipf.infolist())
                
                if total_uncompressed == 0:
                    return 0.0
                
                ratio = (1 - total_compressed / total_uncompressed) * 100
                return round(ratio, 2)
                
        except Exception:
            return None
    
    @staticmethod
    def get_archive_stats(archive_path: str) -> Optional[Dict]:
        """
        Get detailed statistics about archive
        
        Args:
            archive_path: Path to the ZIP file
            
        Returns:
            dict: Archive statistics, or None on error
        """
        try:
            with zipfile.ZipFile(archive_path, 'r') as zipf:
                infolist = zipf.infolist()
                
                # Count different file types
                file_extensions = {}
                total_files = 0
                total_dirs = 0
                
                for info in infolist:
                    if info.is_dir():
                        total_dirs += 1
                    else:
                        total_files += 1
                        ext = os.path.splitext(info.filename)[1].lower()
                        if ext:
                            file_extensions[ext] = file_extensions.get(ext, 0) + 1
                        else:
                            file_extensions['<no extension>'] = file_extensions.get('<no extension>', 0) + 1
                
                total_compressed = sum(info.compress_size for info in infolist)
                total_uncompressed = sum(info.file_size for info in infolist)
                
                return {
                    'total_files': total_files,
                    'total_directories': total_dirs,
                    'total_compressed_size': total_compressed,
                    'total_uncompressed_size': total_uncompressed,
                    'compression_ratio': (1 - total_compressed / total_uncompressed) * 100 if total_uncompressed > 0 else 0,
                    'archive_size': os.path.getsize(archive_path),
                    'file_types': file_extensions,
                    'largest_file': max((info for info in infolist if not info.is_dir()), 
                                      key=lambda x: x.file_size, default=None)
                }
                
        except Exception:
            return None
    
    @staticmethod
    def validate_path(path: str, must_exist: bool = True) -> tuple[bool, str]:
        """
        Validate a file/directory path
        
        Args:
            path: Path to validate
            must_exist: Whether the path must exist
            
        Returns:
            tuple: (is_valid, message)
        """
        if not path:
            return False, "Path cannot be empty"
        
        if must_exist and not os.path.exists(path):
            return False, "Path does not exist"
        
        # Check for invalid characters (Windows-specific)
        invalid_chars = '<>"|?*' if os.name == 'nt' else ''
        if any(char in path for char in invalid_chars):
            return False, "Path contains invalid characters"
        
        return True, "Path is valid"
