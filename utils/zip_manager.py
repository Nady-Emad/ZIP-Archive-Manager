"""
Core ZIP Archive Manager Module
Handles creation, extraction, and listing of ZIP archives
"""

import os
import zipfile
import tempfile
from pathlib import Path
from typing import List, Optional, Callable, Union
from .compression import CompressionMethod
from .progress_tracker import ProgressTracker


class ZIPManager:
    """Main class for managing ZIP archive operations"""
    
    def __init__(self, progress_callback: Optional[Callable] = None):
        """
        Initialize ZIP Manager
        
        Args:
            progress_callback: Optional callback function for progress updates
        """
        self.progress_tracker = ProgressTracker(progress_callback)
    
    def create_archive(
        self,
        archive_path: str,
        files: List[str],
        compression_method: int = zipfile.ZIP_DEFLATED,
        password: Optional[str] = None,
        base_dir: Optional[str] = None
    ) -> bool:
        """
        Create a ZIP archive from files/directories
        
        Args:
            archive_path: Path where the ZIP file will be created
            files: List of file/directory paths to add to archive
            compression_method: Compression method (ZIP_STORED, ZIP_DEFLATED, ZIP_BZIP2, ZIP_LZMA)
            password: Optional password for encryption
            base_dir: Base directory for relative paths
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Count total files for progress tracking
            total_files = self._count_files(files)
            self.progress_tracker.start(total_files)
            
            with zipfile.ZipFile(archive_path, 'w', compression=compression_method) as zipf:
                # Set password if provided
                if password:
                    zipf.setpassword(password.encode('utf-8'))
                
                processed_files = 0
                for item in files:
                    if os.path.isfile(item):
                        arcname = self._get_arcname(item, base_dir)
                        zipf.write(item, arcname)
                        processed_files += 1
                        self.progress_tracker.update(processed_files, f"Adding: {os.path.basename(item)}")
                    elif os.path.isdir(item):
                        for root, dirs, file_list in os.walk(item):
                            for file in file_list:
                                file_path = os.path.join(root, file)
                                arcname = self._get_arcname(file_path, base_dir or item)
                                zipf.write(file_path, arcname)
                                processed_files += 1
                                self.progress_tracker.update(processed_files, f"Adding: {file}")
            
            self.progress_tracker.complete(f"Archive created: {archive_path}")
            return True
            
        except Exception as e:
            self.progress_tracker.error(f"Error creating archive: {str(e)}")
            return False
    
    def extract_archive(
        self,
        archive_path: str,
        extract_path: str,
        password: Optional[str] = None,
        members: Optional[List[str]] = None
    ) -> bool:
        """
        Extract a ZIP archive
        
        Args:
            archive_path: Path to the ZIP file
            extract_path: Directory where files will be extracted
            password: Optional password for encrypted archives
            members: Optional list of specific members to extract
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with zipfile.ZipFile(archive_path, 'r') as zipf:
                # Get list of members to extract
                members_list = members if members else zipf.namelist()
                total_members = len(members_list)
                self.progress_tracker.start(total_members)
                
                # Set password if provided
                pwd = password.encode('utf-8') if password else None
                
                # Extract files
                for idx, member in enumerate(members_list):
                    zipf.extract(member, extract_path, pwd=pwd)
                    self.progress_tracker.update(idx + 1, f"Extracting: {member}")
                
                self.progress_tracker.complete(f"Extraction complete: {extract_path}")
                return True
                
        except Exception as e:
            self.progress_tracker.error(f"Error extracting archive: {str(e)}")
            return False
    
    def list_contents(self, archive_path: str, password: Optional[str] = None) -> Optional[List[dict]]:
        """
        List contents of a ZIP archive
        
        Args:
            archive_path: Path to the ZIP file
            password: Optional password for encrypted archives
            
        Returns:
            List of dictionaries containing file information, or None on error
        """
        try:
            with zipfile.ZipFile(archive_path, 'r') as zipf:
                if password:
                    zipf.setpassword(password.encode('utf-8'))
                
                contents = []
                for info in zipf.infolist():
                    contents.append({
                        'filename': info.filename,
                        'compressed_size': info.compress_size,
                        'uncompressed_size': info.file_size,
                        'compression_type': info.compress_type,
                        'date_time': info.date_time,
                        'is_dir': info.is_dir(),
                        'crc': info.CRC
                    })
                
                return contents
                
        except Exception as e:
            self.progress_tracker.error(f"Error listing archive contents: {str(e)}")
            return None
    
    def get_archive_info(self, archive_path: str) -> Optional[dict]:
        """
        Get detailed information about a ZIP archive
        
        Args:
            archive_path: Path to the ZIP file
            
        Returns:
            Dictionary containing archive information, or None on error
        """
        try:
            with zipfile.ZipFile(archive_path, 'r') as zipf:
                contents = zipf.infolist()
                total_compressed = sum(info.compress_size for info in contents)
                total_uncompressed = sum(info.file_size for info in contents)
                
                return {
                    'path': archive_path,
                    'file_count': len(contents),
                    'total_compressed_size': total_compressed,
                    'total_uncompressed_size': total_uncompressed,
                    'compression_ratio': (1 - total_compressed / total_uncompressed) * 100 if total_uncompressed > 0 else 0,
                    'archive_size': os.path.getsize(archive_path)
                }
                
        except Exception as e:
            self.progress_tracker.error(f"Error getting archive info: {str(e)}")
            return None
    
    def _count_files(self, paths: List[str]) -> int:
        """Count total number of files to be processed"""
        total = 0
        for path in paths:
            if os.path.isfile(path):
                total += 1
            elif os.path.isdir(path):
                for root, dirs, files in os.walk(path):
                    total += len(files)
        return total
    
    def _get_arcname(self, file_path: str, base_dir: Optional[str]) -> str:
        """Get the archive name for a file"""
        if base_dir:
            return os.path.relpath(file_path, base_dir)
        return os.path.basename(file_path)
