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
            
            # Dictionary to store counts and occurrences per person
            counts = defaultdict(lambda: {
                'אלצ': {'count': 0, 'occurrences': []},
                'אלץ': {'count': 0, 'occurrences': []}
            })
            
            # Regular expression to match the WhatsApp message format
            # This pattern matches: date, time - name: message
            pattern = r'(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2}(?::\d{2})?) - ([^:]+): (.*?)(?=\n\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}(?::\d{2})? - |$)'
            
            # Find all messages
            messages = re.finditer(pattern, content, re.DOTALL)
            
            for match in messages:
                date = match.group(1)
                time = match.group(2)
                name = match.group(3).strip()
                message = match.group(4)
                
                # Count occurrences in this message
                if 'אלצ' in message:
                    counts[name]['אלצ']['count'] += message.count('אלצ')
                    counts[name]['אלצ']['occurrences'].append(f"{date} {time}")
                if 'אלץ' in message:
                    counts[name]['אלץ']['count'] += message.count('אלץ')
                    counts[name]['אלץ']['occurrences'].append(f"{date} {time}")
            
            # Print results to console
            print("Occurrences per person:")
            print("=" * 40)
            for name in sorted(counts.keys()):
                total = counts[name]['אלצ']['count'] + counts[name]['אלץ']['count']
                if total > 0:
                    print(f"\n{name}:")
                    if counts[name]['אלצ']['count'] > 0:
                        print(f"  'אלצ': {counts[name]['אלצ']['count']}")
                        print("  Occurred at:")
                        for occurrence in counts[name]['אלצ']['occurrences']:
                            print(f"    - {occurrence}")
                    if counts[name]['אלץ']['count'] > 0:
                        print(f"  'אלץ': {counts[name]['אלץ']['count']}")
                        print("  Occurred at:")
                        for occurrence in counts[name]['אלץ']['occurrences']:
                            print(f"    - {occurrence}")
                    print(f"  Total: {total}")
            
            # Print overall totals
            total_alts = sum(counts[name]['אלצ']['count'] for name in counts)
            total_altz = sum(counts[name]['אלץ']['count'] for name in counts)
            print("\nOverall totals:")
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