"""
Command Line Interface for ZIP Archive Manager
"""

import argparse
import sys
import os
from typing import Optional

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.zip_manager import ZIPManager
from utils.compression import CompressionMethod, CompressionHandler
from utils.security import SecurityManager
from utils.validators import ArchiveValidator
from utils.batch_operations import BatchProcessor
from utils.progress_tracker import ConsoleProgressTracker


def create_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser"""
    parser = argparse.ArgumentParser(
        description='ZIP Archive Manager - Command Line Interface',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Create an archive
  %(prog)s create output.zip file1.txt file2.txt folder/
  
  # Create with compression and password
  %(prog)s create output.zip file.txt -c lzma -p mypassword
  
  # Extract an archive
  %(prog)s extract archive.zip -o output_folder/
  
  # Extract with password
  %(prog)s extract archive.zip -o output_folder/ -p mypassword
  
  # List archive contents
  %(prog)s list archive.zip
  
  # Verify archive
  %(prog)s verify archive.zip
  
  # Batch extract
  %(prog)s batch-extract archive1.zip archive2.zip -o output_folder/
        '''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new ZIP archive')
    create_parser.add_argument('output', help='Output ZIP file path')
    create_parser.add_argument('files', nargs='+', help='Files/folders to add to archive')
    create_parser.add_argument('-c', '--compression', 
                              choices=['store', 'deflate', 'bzip2', 'lzma'],
                              default='deflate',
                              help='Compression method (default: deflate)')
    create_parser.add_argument('-p', '--password', help='Password for encryption')
    create_parser.add_argument('-b', '--base-dir', help='Base directory for relative paths')
    
    # Extract command
    extract_parser = subparsers.add_parser('extract', help='Extract a ZIP archive')
    extract_parser.add_argument('archive', help='ZIP file to extract')
    extract_parser.add_argument('-o', '--output', required=True, help='Output directory')
    extract_parser.add_argument('-p', '--password', help='Password for encrypted archive')
    extract_parser.add_argument('-m', '--members', nargs='+', help='Specific files to extract')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List archive contents')
    list_parser.add_argument('archive', help='ZIP file to list')
    list_parser.add_argument('-d', '--detailed', action='store_true', help='Show detailed information')
    list_parser.add_argument('-p', '--password', help='Password for encrypted archive')
    
    # Verify command
    verify_parser = subparsers.add_parser('verify', help='Verify archive integrity')
    verify_parser.add_argument('archive', help='ZIP file to verify')
    verify_parser.add_argument('--crc', action='store_true', help='Verify CRC checksums')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Get archive information')
    info_parser.add_argument('archive', help='ZIP file to analyze')
    
    # Batch extract command
    batch_extract_parser = subparsers.add_parser('batch-extract', help='Extract multiple archives')
    batch_extract_parser.add_argument('archives', nargs='+', help='ZIP files to extract')
    batch_extract_parser.add_argument('-o', '--output', required=True, help='Output directory')
    batch_extract_parser.add_argument('-p', '--password', help='Password for encrypted archives')
    
    # Batch verify command
    batch_verify_parser = subparsers.add_parser('batch-verify', help='Verify multiple archives')
    batch_verify_parser.add_argument('archives', nargs='+', help='ZIP files to verify')
    
    return parser


def cmd_create(args) -> int:
    """Handle create command"""
    # Validate password if provided
    if args.password:
        is_valid, msg = SecurityManager.validate_password(args.password)
        if not is_valid:
            print(f"Error: {msg}")
            return 1
        if msg and "warning" in msg.lower():
            print(f"Warning: {msg}")
    
    # Get compression method
    compression = CompressionHandler.from_string(args.compression)
    
    # Create progress tracker
    tracker = ConsoleProgressTracker()
    
    # Create archive
    zip_manager = ZIPManager(tracker._console_callback)
    
    print(f"Creating archive: {args.output}")
    print(f"Compression: {CompressionHandler.get_compression_name(compression)}")
    if args.password:
        print("Password protection: Enabled")
    
    success = zip_manager.create_archive(
        archive_path=args.output,
        files=args.files,
        compression_method=CompressionHandler.get_compression_value(compression),
        password=args.password,
        base_dir=args.base_dir
    )
    
    return 0 if success else 1


def cmd_extract(args) -> int:
    """Handle extract command"""
    # Create progress tracker
    tracker = ConsoleProgressTracker()
    
    # Extract archive
    zip_manager = ZIPManager(tracker._console_callback)
    
    print(f"Extracting: {args.archive}")
    print(f"Output directory: {args.output}")
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)
    
    success = zip_manager.extract_archive(
        archive_path=args.archive,
        extract_path=args.output,
        password=args.password,
        members=args.members
    )
    
    return 0 if success else 1


def cmd_list(args) -> int:
    """Handle list command"""
    zip_manager = ZIPManager()
    
    contents = zip_manager.list_contents(args.archive, args.password)
    
    if contents is None:
        print("Error: Failed to read archive")
        return 1
    
    print(f"\nContents of {args.archive}:")
    print("-" * 80)
    
    if args.detailed:
        # Detailed listing
        print(f"{'Name':<40} {'Size':>12} {'Compressed':>12} {'Ratio':>8} {'Type':<10}")
        print("-" * 80)
        
        for item in contents:
            if not item['is_dir']:
                ratio = 0
                if item['uncompressed_size'] > 0:
                    ratio = (1 - item['compressed_size'] / item['uncompressed_size']) * 100
                
                comp_type = CompressionHandler.get_compression_type_name(item['compression_type'])
                
                print(f"{item['filename']:<40} {item['uncompressed_size']:>12} "
                      f"{item['compressed_size']:>12} {ratio:>7.1f}% {comp_type:<10}")
    else:
        # Simple listing
        for item in contents:
            marker = '/' if item['is_dir'] else ''
            print(f"  {item['filename']}{marker}")
    
    print("-" * 80)
    print(f"Total files: {len([c for c in contents if not c['is_dir']])}")
    print(f"Total directories: {len([c for c in contents if c['is_dir']])}")
    
    return 0


def cmd_verify(args) -> int:
    """Handle verify command"""
    print(f"Verifying: {args.archive}")
    
    # Basic validation
    is_valid, message = ArchiveValidator.validate_archive(args.archive)
    
    if not is_valid:
        print(f"✗ Validation failed: {message}")
        return 1
    
    print(f"✓ Archive structure is valid")
    
    # CRC verification if requested
    if args.crc:
        print("Verifying CRC checksums...")
        results = ArchiveValidator.verify_crc(args.archive)
        
        if results['valid']:
            print(f"✓ All {results['verified_files']} files verified successfully")
        else:
            print(f"✗ CRC verification failed")
            print(f"Verified: {results['verified_files']}/{results['total_files']}")
            if results['errors']:
                print("Errors:")
                for error in results['errors']:
                    print(f"  - {error}")
            return 1
    
    print(f"✓ {message}")
    return 0


def cmd_info(args) -> int:
    """Handle info command"""
    zip_manager = ZIPManager()
    
    info = zip_manager.get_archive_info(args.archive)
    
    if info is None:
        print("Error: Failed to read archive information")
        return 1
    
    # Get additional stats
    stats = ArchiveValidator.get_archive_stats(args.archive)
    
    print(f"\nArchive Information: {args.archive}")
    print("=" * 60)
    print(f"Archive Size: {info['archive_size'] / 1024:.2f} KB ({info['archive_size']} bytes)")
    print(f"Total Files: {info['file_count']}")
    print(f"Compressed Size: {info['total_compressed_size'] / 1024:.2f} KB")
    print(f"Uncompressed Size: {info['total_uncompressed_size'] / 1024:.2f} KB")
    print(f"Compression Ratio: {info['compression_ratio']:.2f}%")
    
    # Check encryption
    is_encrypted = SecurityManager.is_encrypted(args.archive)
    print(f"Encrypted: {'Yes' if is_encrypted else 'No'}")
    
    if stats and stats['file_types']:
        print(f"\nFile Types:")
        for ext, count in sorted(stats['file_types'].items()):
            print(f"  {ext}: {count}")
    
    print("=" * 60)
    
    return 0


def cmd_batch_extract(args) -> int:
    """Handle batch extract command"""
    operations = []
    
    for archive in args.archives:
        archive_name = os.path.splitext(os.path.basename(archive))[0]
        extract_path = os.path.join(args.output, archive_name)
        operations.append({
            'archive_path': archive,
            'extract_path': extract_path
        })
    
    tracker = ConsoleProgressTracker()
    batch_processor = BatchProcessor(tracker._console_callback)
    
    print(f"Batch extracting {len(args.archives)} archives to {args.output}")
    
    results = batch_processor.batch_extract(operations, password=args.password)
    
    print(f"\nBatch Extract Results:")
    print(f"  Total: {results['total']}")
    print(f"  Successful: {results['successful']}")
    print(f"  Failed: {results['failed']}")
    
    if results['errors']:
        print("\nErrors:")
        for error in results['errors']:
            print(f"  - {error}")
    
    return 0 if results['failed'] == 0 else 1


def cmd_batch_verify(args) -> int:
    """Handle batch verify command"""
    tracker = ConsoleProgressTracker()
    batch_processor = BatchProcessor(tracker._console_callback)
    
    print(f"Batch verifying {len(args.archives)} archives")
    
    results = batch_processor.batch_verify(args.archives)
    
    print(f"\nBatch Verify Results:")
    print(f"  Total: {results['total']}")
    print(f"  Valid: {results['valid']}")
    print(f"  Invalid: {results['invalid']}")
    
    if results['errors']:
        print("\nErrors:")
        for error in results['errors']:
            print(f"  - {error}")
    
    return 0 if results['invalid'] == 0 else 1


def main() -> int:
    """Main entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Route to command handler
    handlers = {
        'create': cmd_create,
        'extract': cmd_extract,
        'list': cmd_list,
        'verify': cmd_verify,
        'info': cmd_info,
        'batch-extract': cmd_batch_extract,
        'batch-verify': cmd_batch_verify
    }
    
    handler = handlers.get(args.command)
    if handler:
        try:
            return handler(args)
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user")
            return 130
        except Exception as e:
            print(f"\nError: {str(e)}")
            return 1
    else:
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())
