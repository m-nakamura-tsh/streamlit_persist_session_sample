#!/usr/bin/env python3
"""
データクリーンアップスクリプト
古いプロセスデータや完了済みプロセスを削除します。
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import json
import argparse

# Add packages to path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir / "packages" / "persistence" / "src"))

from persistence import JsonStorage, ProcessStatus


def clean_old_processes(days_old: int = 30, dry_run: bool = False):
    """指定日数以上前の完了済みプロセスを削除"""
    
    data_path = root_dir / "data" / "processes"
    storage = JsonStorage(data_path)
    
    cutoff_date = datetime.now() - timedelta(days=days_old)
    
    print(f"Cleaning processes older than {days_old} days (before {cutoff_date.date()})...")
    
    deleted_count = 0
    kept_count = 0
    
    for process_id in storage.list_processes():
        process = storage.load_process(process_id)
        
        if process:
            # Check if process is old and completed
            if (process.status == ProcessStatus.COMPLETED and 
                process.completed_at and 
                process.completed_at < cutoff_date):
                
                if dry_run:
                    print(f"  Would delete: {process_id} (completed on {process.completed_at.date()})")
                else:
                    if storage.delete_process(process_id):
                        print(f"  Deleted: {process_id}")
                        deleted_count += 1
            else:
                kept_count += 1
    
    print(f"\nSummary:")
    print(f"  Deleted: {deleted_count} processes")
    print(f"  Kept: {kept_count} processes")
    
    if dry_run:
        print("\n(This was a dry run. Use --execute to actually delete files)")


def clean_failed_processes(dry_run: bool = False):
    """失敗したプロセスを削除"""
    
    data_path = root_dir / "data" / "processes"
    storage = JsonStorage(data_path)
    
    print("Cleaning failed processes...")
    
    deleted_count = 0
    
    failed_processes = storage.list_processes_by_status(ProcessStatus.FAILED.value)
    
    for process_id in failed_processes:
        if dry_run:
            print(f"  Would delete: {process_id}")
        else:
            if storage.delete_process(process_id):
                print(f"  Deleted: {process_id}")
                deleted_count += 1
    
    print(f"\nDeleted {deleted_count} failed processes")
    
    if dry_run:
        print("(This was a dry run. Use --execute to actually delete files)")


def show_statistics():
    """プロセスデータの統計を表示"""
    
    data_path = root_dir / "data" / "processes"
    storage = JsonStorage(data_path)
    
    all_processes = storage.list_processes()
    
    print("Process Statistics:")
    print(f"  Total processes: {len(all_processes)}")
    
    # Count by status
    status_counts = {}
    for status in ProcessStatus:
        count = len(storage.list_processes_by_status(status.value))
        if count > 0:
            status_counts[status.value] = count
    
    print("\nBy Status:")
    for status, count in status_counts.items():
        print(f"  {status}: {count}")
    
    # Calculate storage size
    total_size = 0
    for json_file in data_path.glob("*.json"):
        total_size += json_file.stat().st_size
    
    print(f"\nTotal storage size: {total_size / 1024:.2f} KB")


def main():
    parser = argparse.ArgumentParser(description="Clean up process data")
    parser.add_argument(
        "action",
        choices=["old", "failed", "stats"],
        help="Action to perform"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=30,
        help="Number of days to keep (for 'old' action)"
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually delete files (default is dry run)"
    )
    
    args = parser.parse_args()
    
    if args.action == "old":
        clean_old_processes(args.days, dry_run=not args.execute)
    elif args.action == "failed":
        clean_failed_processes(dry_run=not args.execute)
    elif args.action == "stats":
        show_statistics()


if __name__ == "__main__":
    main()