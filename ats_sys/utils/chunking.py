from bas_val.logger import logging

def create_chunks(words, chunk_size):
    logging.info("Starting the chunking")
    chunks = []
    current_chunk = []
    current_chunk_word_count = 0

    for word in words.split():
        #print(word)
        # Add the current word to the current chunk
        current_chunk.append(word)
        current_chunk_word_count += 1
        # print(current_chunk)
        # print(current_chunk_word_count)
        # If the current chunk exceeds the desired word count
        if current_chunk_word_count == chunk_size:
            # Join the words in the current chunk to form a chunk string
            #chunk_string = ' '.join(current_chunk)
            chunks.append(current_chunk)
            #print(chunks)

            # Reset the current chunk and word count
            current_chunk = []
            current_chunk_word_count = 0
    if current_chunk is not None:
        chunks.append(current_chunk)
    logging.info("Ending the chunking")
    return chunks