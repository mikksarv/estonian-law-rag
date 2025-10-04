import json

# Load your chunks file
with open("../processed_data/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

# Calculate word counts for each chunk
word_counts = [len(chunk.split()) for chunk in chunks]

avg_words = sum(word_counts) / len(word_counts)
max_words = max(word_counts)
min_words = min(word_counts)

print(f"Total chunks: {len(chunks)}")
print(f"Average chunk size (words): {avg_words:.1f}")
print(f"Max chunk size (words): {max_words}")
print(f"Min chunk size (words): {min_words}")

# Optionally, print the largest chunks to inspect
largest_chunks = sorted(zip(word_counts, chunks), key=lambda x: x[0], reverse=True)[:3]
print("\nLargest chunks:")
for i, (count, text) in enumerate(largest_chunks, 1):
    print(f"\nChunk #{i} - {count} words:\n{text[:500]}...")  # print first 500 chars