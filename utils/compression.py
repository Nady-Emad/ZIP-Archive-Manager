"""
Compression Methods Module
Handles different compression algorithms for ZIP archives
"""

import zipfile
from enum import Enum
from typing import Dict


class CompressionMethod(Enum):
    """Enumeration of supported compression methods"""
    STORE = zipfile.ZIP_STORED      # No compression
    DEFLATE = zipfile.ZIP_DEFLATED  # Standard ZIP compression
    BZIP2 = zipfile.ZIP_BZIP2       # BZIP2 compression
    LZMA = zipfile.ZIP_LZMA         # LZMA compression


class CompressionHandler:
    """Handles compression method selection and information"""
    
    # Compression method information
    COMPRESSION_INFO = {
        CompressionMethod.STORE: {
            'name': 'Store (No Compression)',
            'description': 'Files are stored without compression',
            'speed': 'Very Fast',
            'ratio': 'None',
            'cpu_usage': 'Very Low'
        },
        CompressionMethod.DEFLATE: {
            'name': 'Deflate (Standard)',
            'description': 'Standard ZIP compression using DEFLATE algorithm',
            'speed': 'Fast',
            'ratio': 'Good',
            'cpu_usage': 'Low'
        },
        CompressionMethod.BZIP2: {
            'name': 'BZIP2',
            'description': 'Better compression ratio, slower than DEFLATE',
            'speed': 'Medium',
            'ratio': 'Better',
            'cpu_usage': 'Medium'
        },
        CompressionMethod.LZMA: {
            'name': 'LZMA',
            'description': 'Best compression ratio, slowest compression',
            'speed': 'Slow',
            'ratio': 'Best',
            'cpu_usage': 'High'
        }
    }
    
    @classmethod
    def get_compression_value(cls, method: CompressionMethod) -> int:
        """
        Get the zipfile compression constant for a given method
        
        Args:
            method: CompressionMethod enum value
            
        Returns:
            int: zipfile compression constant
        """
        return method.value
    
    @classmethod
    def get_compression_name(cls, method: CompressionMethod) -> str:
        """Get the display name for a compression method"""
        return cls.COMPRESSION_INFO[method]['name']
    
    @classmethod
    def get_compression_info(cls, method: CompressionMethod) -> Dict[str, str]:
        """Get detailed information about a compression method"""
        return cls.COMPRESSION_INFO[method]
    
    @classmethod
    def get_all_methods(cls) -> list:
        """Get list of all available compression methods"""
        return list(CompressionMethod)
    
    @classmethod
    def from_string(cls, method_str: str) -> CompressionMethod:
        """
        Convert string to CompressionMethod enum
        
        Args:
            method_str: String representation of compression method
            
        Returns:
            CompressionMethod enum value
        """
        method_map = {
            'store': CompressionMethod.STORE,
            'deflate': CompressionMethod.DEFLATE,
            'bzip2': CompressionMethod.BZIP2,
            'lzma': CompressionMethod.LZMA
        }
        return method_map.get(method_str.lower(), CompressionMethod.DEFLATE)
    
    @classmethod
    def get_compression_type_name(cls, compress_type: int) -> str:
        """
        Get compression method name from zipfile compress_type value
        
        Args:
            compress_type: zipfile compress_type constant
            
        Returns:
            str: Compression method name
        """
        type_map = {
            zipfile.ZIP_STORED: 'Stored',
            zipfile.ZIP_DEFLATED: 'Deflate',
            zipfile.ZIP_BZIP2: 'BZIP2',
            zipfile.ZIP_LZMA: 'LZMA'
        }
        return type_map.get(compress_type, 'Unknown')
