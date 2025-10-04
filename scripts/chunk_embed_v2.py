import os
import re
import json

def chunk_law_structurally(input_path, output_dir):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    law_title = data.get('title', 'Unknown Title')
    text = data.get('text', '')
    url = data.get('url', '')
    filename = os.path.basename(input_path)

    # 1. Split into sections based on §
    sections = re.split(r'(?=\n?§\s*\d+[^\n]*)', text)

    chunks = []
    metadata = []
    chunk_id = 0

    for section in sections:
        section = section.strip()
        if not section:
            continue

        # Extract § number and title
        match = re.match(r'^§\s*(\d+[^\n]*)', section)
        paragraph_id = match.group(1).strip() if match else 'unknown'

        # Extract lõigud (subsections)
        lines = re.split(r'(?=\(\d+\))', section)
        header = lines[0].strip()
        subsections = lines[1:] if len(lines) > 1 else []

        if not subsections:
            chunks.append(section)
            metadata.append({
                'chunk_id': chunk_id,
                'title': law_title,
                'paragraph': paragraph_id,
                'source_file': filename,
                'url': url
            })
            chunk_id += 1
        else:
            for lõik in subsections:
                full_text = f"{header}\n{lõik.strip()}"
                chunks.append(full_text)

                lõik_match = re.match(r'\((\d+)\)', lõik.strip())
                lõik_number = lõik_match.group(1) if lõik_match else 'unknown'

                metadata.append({
                    'chunk_id': chunk_id,
                    'title': law_title,
                    'paragraph': paragraph_id,
                    'subsection': lõik_number,
                    'source_file': filename,
                    'url': url
                })
                chunk_id += 1

    # Save outputs
    os.makedirs(output_dir, exist_ok=True)
    chunks_path = os.path.join(output_dir, 'chunks.json')
    metadata_path = os.path.join(output_dir, 'metadata.json')

    with open(chunks_path, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    print(f"[✓] Successfully structured {len(chunks)} chunks from: {filename}")

if __name__ == "__main__":
    input_path = "../data/raw_laws/Kaitseväeteenistuse_seaduse_rakendamise_seadus_(lühend - KVTRS).json"  # Replace as needed
    output_dir = "../processed_data"
    chunk_law_structurally(input_path, output_dir)