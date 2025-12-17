#!/usr/bin/env python3
"""
Example script demonstrating the ZIP Archive Manager API
"""

import sys
import os

# Add project directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.zip_manager import ZIPManager
from utils.compression import CompressionMethod, CompressionHandler
from utils.security import SecurityManager
from utils.validators import ArchiveValidator
from utils.batch_operations import BatchProcessor
from utils.progress_tracker import ConsoleProgressTracker


def example_create_archive():
    """Example: Create a password-protected archive with LZMA compression"""
    print("\n=== Example 1: Create Password-Protected Archive ===")
    
    # Create test files
    os.makedirs('/tmp/example_data', exist_ok=True)
    with open('/tmp/example_data/file1.txt', 'w') as f:
        f.write("This is a test file for demonstration")
    with open('/tmp/example_data/file2.txt', 'w') as f:
        f.write("Another test file with some content")
    
    # Create ZIP manager with console progress tracking
    tracker = ConsoleProgressTracker()
    manager = ZIPManager(tracker._console_callback)
    
    # Create archive with LZMA compression and password
    success = manager.create_archive(
        archive_path='/tmp/example_secure.zip',
        files=['/tmp/example_data/'],
        compression_method=CompressionHandler.get_compression_value(CompressionMethod.LZMA),
        password='SecurePassword123'
    )
    
    if success:
        print("\n✓ Archive created successfully!")
    else:
        print("\n✗ Failed to create archive")
    
    return success


def example_list_contents():
    """Example: List archive contents with detailed information"""
    print("\n=== Example 2: List Archive Contents ===")
    
    manager = ZIPManager()
    contents = manager.list_contents('/tmp/example_secure.zip')
    
    if contents:
        print(f"\nArchive contains {len(contents)} files:")
        for item in contents:
            size_kb = item['uncompressed_size'] / 1024
            compressed_kb = item['compressed_size'] / 1024
            compression_type = CompressionHandler.get_compression_type_name(item['compression_type'])
            print(f"  - {item['filename']}: {size_kb:.2f} KB ({compression_type})")
    
    # Get archive info
    info = manager.get_archive_info('/tmp/example_secure.zip')
    if info:
        print(f"\nArchive Statistics:")
        print(f"  Total files: {info['file_count']}")
        print(f"  Compression ratio: {info['compression_ratio']:.2f}%")
        print(f"  Archive size: {info['archive_size'] / 1024:.2f} KB")


def example_verify_archive():
    """Example: Verify archive integrity"""
    print("\n=== Example 3: Verify Archive Integrity ===")
    
    # Basic validation
    is_valid, message = ArchiveValidator.validate_archive('/tmp/example_secure.zip')
    print(f"\nValidation: {'✓ Valid' if is_valid else '✗ Invalid'}")
    print(f"Message: {message}")
    
    # CRC verification
    results = ArchiveValidator.verify_crc('/tmp/example_secure.zip')
    print(f"\nCRC Verification:")
    print(f"  Verified files: {results['verified_files']}/{results['total_files']}")
    print(f"  Status: {'✓ All files valid' if results['valid'] else '✗ Some files failed'}")


def example_extract_archive():
    """Example: Extract archive with password"""
    print("\n=== Example 4: Extract Archive ===")
    
    tracker = ConsoleProgressTracker()
    manager = ZIPManager(tracker._console_callback)
    
    success = manager.extract_archive(
        archive_path='/tmp/example_secure.zip',
        extract_path='/tmp/example_extracted',
        password='SecurePassword123'
    )
    
    if success:
        print("\n✓ Archive extracted successfully!")
        print("Extracted files:")
        for root, dirs, files in os.walk('/tmp/example_extracted'):
            for file in files:
                print(f"  - {os.path.join(root, file)}")
    else:
        print("\n✗ Failed to extract archive")


def example_compare_compression():
    """Example: Compare different compression methods"""
    print("\n=== Example 5: Compare Compression Methods ===")
    
    # Create test data
    test_data = "This is a test string that will be repeated many times. " * 100
    test_file = '/tmp/compression_test.txt'
    with open(test_file, 'w') as f:
        f.write(test_data)
    
    manager = ZIPManager()
    
    results = {}
    for method in CompressionHandler.get_all_methods():
        archive_path = f'/tmp/test_{method.name.lower()}.zip'
        manager.create_archive(
            archive_path=archive_path,
            files=[test_file],
            compression_method=CompressionHandler.get_compression_value(method)
        )
        
        # Get size
        size = os.path.getsize(archive_path)
        results[method.name] = size
    
    print(f"\nOriginal file size: {os.path.getsize(test_file) / 1024:.2f} KB")
    print("\nCompression Results:")
    for method_name, size in sorted(results.items(), key=lambda x: x[1]):
        print(f"  {method_name:8s}: {size / 1024:.2f} KB")


def example_batch_operations():
    """Example: Batch process multiple archives"""
    print("\n=== Example 6: Batch Operations ===")
    
    # Create multiple test archives
    archives = []
    for i in range(3):
        os.makedirs(f'/tmp/batch_data_{i}', exist_ok=True)
        with open(f'/tmp/batch_data_{i}/file.txt', 'w') as f:
            f.write(f"Batch file {i}")
        
        manager = ZIPManager()
        archive_path = f'/tmp/batch_archive_{i}.zip'
        manager.create_archive(archive_path, [f'/tmp/batch_data_{i}/'])
        archives.append(archive_path)
    
    # Batch verify
    tracker = ConsoleProgressTracker()
    processor = BatchProcessor(tracker._console_callback)
    
    print("\nBatch verifying archives...")
    results = processor.batch_verify(archives)
    print(f"\nVerification Results: {results['valid']}/{results['total']} valid")


def example_password_validation():
    """Example: Password validation and generation"""
    print("\n=== Example 7: Password Security ===")
    
    # Test weak password
    is_valid, msg = SecurityManager.validate_password("123")
    print(f"\nPassword '123': {'✓ Valid' if is_valid else '✗ Invalid'}")
    print(f"Message: {msg}")
    
    # Test stronger password
    is_valid, msg = SecurityManager.validate_password("MySecurePass123")
    print(f"\nPassword 'MySecurePass123': {'✓ Valid' if is_valid else '✗ Invalid'}")
    print(f"Message: {msg}")
    
    # Generate secure password
    generated = SecurityManager.generate_password(length=16)
    print(f"\nGenerated secure password: {generated}")
    is_valid, msg = SecurityManager.validate_password(generated)
    print(f"Validation: {msg}")


def main():
    """Run all examples"""
    print("=" * 60)
    print("ZIP Archive Manager - API Examples")
    print("=" * 60)
    
    try:
        example_create_archive()
        example_list_contents()
        example_verify_archive()
        example_extract_archive()
        example_compare_compression()
        example_batch_operations()
        example_password_validation()
        
        print("\n" + "=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Error running examples: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
