from googletrans import Translator
import sys
import time
from datetime import datetime
import os

def translate_file(input_file):
    try:
        # Create a translator object
        translator = Translator()
        
        # Read the input file
        with open(input_file, 'r', encoding='utf-8') as file:
            text = file.read()
        
        # Split text into lines and remove empty lines
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Create chunks of approximately 1000 characters
        chunk_size = 1000
        chunks = []
        current_chunk = []
        current_size = 0
        
        for line in lines:
            line_size = len(line)
            if current_size + line_size > chunk_size and current_chunk:
                chunks.append('\n'.join(current_chunk))
                current_chunk = []
                current_size = 0
            current_chunk.append(line)
            current_size += line_size
        
        if current_chunk:  # Add the last chunk if it exists
            chunks.append('\n'.join(current_chunk))
        
        total_chunks = len(chunks)
        print(f"\nTotal chunks to translate: {total_chunks}")
        
        # Translate each chunk
        translated_chunks = []
        for i, chunk in enumerate(chunks, 1):
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    # Translate the chunk
                    translation = translator.translate(chunk, dest='en')
                    translated_chunks.append(translation.text)
                    
                    # Print progress
                    print(f"Translated chunk {i}/{total_chunks} ({(i/total_chunks)*100:.1f}%)", end='\r')
                    
                    # Add a small delay to avoid rate limiting
                    time.sleep(0.1)
                    break  # Success, exit retry loop
                except Exception as e:
                    if attempt == max_retries - 1:  # Last attempt
                        print(f"\nError translating chunk {i} after {max_retries} attempts: {str(e)}")
                        print(f"Problematic text: {chunk[:100]}...")
                        translated_chunks.append(f"[Translation Error in chunk {i}]")
                    else:
                        print(f"\nRetrying chunk {i} (attempt {attempt + 1}/{max_retries})...")
                        time.sleep(0.5)  # Wait longer between retries
        
        # Generate output filename
        file_name, file_ext = os.path.splitext(input_file)
        current_date = datetime.now().strftime("%Y%m%d")
        output_file = f"{file_name}_translated_{current_date}{file_ext}"
        
        # Save translated text to file
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write('\n\n'.join(translated_chunks))
        
        print(f"\n\nTranslation completed!")
        print(f"Original file: {input_file}")
        print(f"Translated file: {output_file}")
        
        # Print some statistics
        print(f"\nStatistics:")
        print(f"Total chunks processed: {total_chunks}")
        print(f"Total lines processed: {len(lines)}")
        print(f"Total characters translated: {len(text)}")
        
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python translate_file.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    translate_file(input_file) 