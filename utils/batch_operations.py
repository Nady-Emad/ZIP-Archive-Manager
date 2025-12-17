"""
Batch Operations Module
Handles batch processing of multiple ZIP archives
"""

import os
from typing import List, Dict, Optional, Callable
from .zip_manager import ZIPManager
from .progress_tracker import ProgressTracker


class BatchProcessor:
    """Handles batch operations on multiple archives"""
    
    def __init__(self, progress_callback: Optional[Callable] = None):
        """
        Initialize batch processor
        
        Args:
            progress_callback: Optional callback for progress updates
        """
        self.progress_tracker = ProgressTracker(progress_callback)
        self.zip_manager = ZIPManager(progress_callback)
    
    def batch_create(
        self,
        operations: List[Dict],
        compression_method: int,
        password: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Create multiple ZIP archives in batch
        
        Args:
            operations: List of dicts with 'archive_path' and 'files' keys
            compression_method: Compression method to use
            password: Optional password for all archives
            
        Returns:
            dict: Results summary
        """
        results = {
            'total': len(operations),
            'successful': 0,
            'failed': 0,
            'errors': []
        }
        
        self.progress_tracker.start(len(operations))
        
        for idx, op in enumerate(operations):
            archive_path = op.get('archive_path')
            files = op.get('files', [])
            base_dir = op.get('base_dir')
            
            try:
                success = self.zip_manager.create_archive(
                    archive_path=archive_path,
                    files=files,
                    compression_method=compression_method,
                    password=password,
                    base_dir=base_dir
                )
                
                if success:
                    results['successful'] += 1
                else:
                    results['failed'] += 1
                    results['errors'].append(f"Failed to create: {archive_path}")
                
                self.progress_tracker.update(idx + 1, f"Processing: {os.path.basename(archive_path)}")
                
            except Exception as e:
                results['failed'] += 1
                results['errors'].append(f"{archive_path}: {str(e)}")
        
        self.progress_tracker.complete(f"Batch create complete: {results['successful']}/{results['total']} successful")
        return results
    
    def batch_extract(
        self,
        operations: List[Dict],
        password: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Extract multiple ZIP archives in batch
        
        Args:
            operations: List of dicts with 'archive_path' and 'extract_path' keys
            password: Optional password for encrypted archives
            
        Returns:
            dict: Results summary
        """
        results = {
            'total': len(operations),
            'successful': 0,
            'failed': 0,
            'errors': []
        }
        
        self.progress_tracker.start(len(operations))
        
        for idx, op in enumerate(operations):
            archive_path = op.get('archive_path')
            extract_path = op.get('extract_path')
            members = op.get('members')
            
            try:
                success = self.zip_manager.extract_archive(
                    archive_path=archive_path,
                    extract_path=extract_path,
                    password=password,
                    members=members
                )
                
                if success:
                    results['successful'] += 1
                else:
                    results['failed'] += 1
                    results['errors'].append(f"Failed to extract: {archive_path}")
                
                self.progress_tracker.update(idx + 1, f"Processing: {os.path.basename(archive_path)}")
                
            except Exception as e:
                results['failed'] += 1
                results['errors'].append(f"{archive_path}: {str(e)}")
        
        self.progress_tracker.complete(f"Batch extract complete: {results['successful']}/{results['total']} successful")
        return results
    
    def batch_verify(self, archive_paths: List[str]) -> Dict[str, any]:
        """
        Verify multiple ZIP archives in batch
        
        Args:
            archive_paths: List of archive paths to verify
            
        Returns:
            dict: Verification results
        """
        from .validators import ArchiveValidator
        
        results = {
            'total': len(archive_paths),
            'valid': 0,
            'invalid': 0,
            'errors': []
        }
        
        self.progress_tracker.start(len(archive_paths))
        
        for idx, archive_path in enumerate(archive_paths):
            try:
                is_valid, message = ArchiveValidator.validate_archive(archive_path)
                
                if is_valid:
                    results['valid'] += 1
                else:
                    results['invalid'] += 1
                    results['errors'].append(f"{archive_path}: {message}")
                
                self.progress_tracker.update(idx + 1, f"Verifying: {os.path.basename(archive_path)}")
                
            except Exception as e:
                results['invalid'] += 1
                results['errors'].append(f"{archive_path}: {str(e)}")
        
        self.progress_tracker.complete(f"Batch verify complete: {results['valid']}/{results['total']} valid")
        return results
