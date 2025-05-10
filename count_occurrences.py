#!/usr/bin/env python3
import sys
import re
from collections import defaultdict

# Set console encoding to UTF-8 for Windows
if sys.platform == 'win32':
    import os
    os.system('chcp 65001 > NUL')

def count_occurrences(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
            # Dictionary to store counts per person
            counts = defaultdict(lambda: {'אלצ': 0, 'אלץ': 0})
            
            # Regular expression to match the WhatsApp message format
            # This pattern matches: date, time - name: message
            pattern = r'(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2}(?::\d{2})?) - ([^:]+): (.*?)(?=\n\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}(?::\d{2})? - |$)'
            
            # Find all messages
            messages = re.finditer(pattern, content, re.DOTALL)
            
            for match in messages:
                name = match.group(3).strip()
                message = match.group(4)
                
                # Count occurrences in this message
                counts[name]['אלצ'] += message.count('אלצ')
                counts[name]['אלץ'] += message.count('אלץ')
            
            # Print results to console
            print("Occurrences per person:")
            print("=" * 40)
            for name in sorted(counts.keys()):
                counts_dict = counts[name]
                total = counts_dict['אלצ'] + counts_dict['אלץ']
                if total > 0:
                    print(f"{name}:")
                    print(f"  'אלצ': {counts_dict['אלצ']}")
                    print(f"  'אלץ': {counts_dict['אלץ']}")
                    print(f"  Total: {total}\n")
            total_alts = sum(counts[name]['אלצ'] for name in counts)
            total_altz = sum(counts[name]['אלץ'] for name in counts)
            print("Overall totals:")
            print("=" * 40)
            print(f"  'אלצ': {total_alts}")
            print(f"  'אלץ': {total_altz}")
            print(f"  Total: {total_alts + total_altz}")
            
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python count_occurrences.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    count_occurrences(file_path) 