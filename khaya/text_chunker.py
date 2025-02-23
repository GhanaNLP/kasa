from dataclasses import dataclass
import re
from typing import List, Dict, Any, Generator

from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import requests



@dataclass
class TextChunk:
    """
    Each chunk is reperesented with metadata
    Content: The text content of the chunk
    Index: Position of a chunk in the sequence of chunks
    word_count: Number of words in each chunk 
    is_partial_sentence: Shows if the chunk ends  in the middle of a sentence
    context_prefix: The text at the end of the previous chunk
    context_suffix: The text at the begining of the next chunk

    """
    content: str
    index: int
    word_count: int
    is_partial_sentence: bool = False
    context_prefix:str = " "
    context_suffix: str = " "



class TextChunker:
    """ 
    Chunks LargeText into smaller chunks for translation
    """
    def __init__(
            self,
            max_chunk_size: int =9900,
            overlap_size: int = 100,
            min_chunk_size: int = 100,


                 
    ):
        self.max_chunk_size = max_chunk_size
        self.overlap_size = overlap_size
        self.min_chunk_size = min_chunk_size

        #Identify Sentence Boundaries 
        self.sentence_endings = re.compile(r'[.!?।][\s\n]+')

    

    def _count_words(self, text:str) -> int:
        """
        Counts the number of words in a text 
        Split by whitespace.

        """

        return len(text.split())
    

    def _find_sentence_boundaries(self, text:str, position: int, reverse: bool = False) -> int:
        """
        Locates the nearest boundaries from a position in a sentence
        Function Arguments: 
        text: The text to find boundaries in
        position: The position in the text to search from 
        reverse:  Direction to search through, If set to True search backwards else forwards
        """
        if reverse:
            # backward search
            text_portion = text[:position]
            matches = list(self.sentence_endings.finditer(text_portion))
            if matches:
                return matches[-1].end()
        else:
            # forward search
            text_portion = text[position:]
            match = self.sentence_endings.search(text_portion)
            if match:
                return position + match.end()
        
        # if there are no boundaries, use the word boundary
        words = text.split()
        if reverse:
            return len(' '.join(words[:position]))
        return len(' '.join(words[:position+1]))
    
    def _extract_context(self, text:str, position: int, context_size: int =50) -> tuple[str,str]:
        """
        Extract context around a position in text.
    
        Arguments:
        text: The full text
        position: Position to extract context around
        context_size: Number of words for context (default 50)
    
        Returns:
        tuple of (prefix_context, suffix_context)
        """
        if not text or position < 0 or position > len(text):
            return "", ""
            
        words = text.split()
        if not words:
            return "", ""
            
        # Find word index based on character position
        total_length = 0
        word_position = 0
        
        for i, word in enumerate(words):
            total_length += len(word) + 1  # +1 for space
            if total_length >= position:
                word_position = i
                break
            if i == len(words) - 1:  # If we reach the end
                word_position = i
                break
        
        # Calculate context boundaries
        prefix_start = max(0, word_position - context_size)
        prefix_end = word_position
        suffix_start = word_position
        suffix_end = min(len(words), word_position + context_size)
        
        # Extract context
        prefix = ' '.join(words[prefix_start:prefix_end])
        suffix = ' '.join(words[suffix_start:suffix_end])
        
        return prefix, suffix
    

    def create_chunks(self,text:str) -> Generator[TextChunk, None,None]:
        """Split text into chunks while preserving sentence boundaries where possible."""
        if not text:
            return 
        
        # Split text into words first
        words = text.split()
        if not words:
            return
            
        current_position = 0
        chunk_index = 0
        text_length = len(text)
        
        while current_position < text_length:
            # Get remaining text
            remaining_text = text[current_position:]
            if not remaining_text.strip():
                break
                
            # Find a chunk boundary based on word count
            remaining_words = remaining_text.split()
            words_to_take = min(self.max_chunk_size, len(remaining_words))
            
            if words_to_take == 0:
                break
                
            # Join the words we want to take
            chunk_text = ' '.join(remaining_words[:words_to_take])
            chunk_end = current_position + len(chunk_text)
            
            # Try to find a sentence boundary before our word limit
            sentence_end = self._find_sentence_boundaries(text, chunk_end)
            if sentence_end > current_position and self._count_words(text[current_position:sentence_end]) <= self.max_chunk_size:
                chunk_end = sentence_end
            
            # Get the chunk text
            chunk_text = text[current_position:chunk_end].strip()
            if not chunk_text:
                break
                
            # Get context
            context_prefix = ""
            context_suffix = ""
            
            if chunk_index > 0:
                context_prefix = self._extract_context(text, current_position)[0]
            if chunk_end < text_length:
                context_suffix = self._extract_context(text, chunk_end)[1]
            
            # Check if chunk ends with sentence boundary
            is_partial = True
            if chunk_text:
                last_char_match = self.sentence_endings.search(chunk_text + "\n")
                is_partial = not bool(last_char_match)
            
            # Create and yield chunk
            chunk = TextChunk(
                content=chunk_text,
                index=chunk_index,
                word_count=self._count_words(chunk_text),
                is_partial_sentence=is_partial,
                context_prefix=context_prefix,
                context_suffix=context_suffix
            )
            
            yield chunk
            
            # Move to next position
            current_position = chunk_end
            chunk_index += 1
            
            # Safety check
            if current_position <= 0:
                break


class BatchTranslator:
    """
    Batch Translation of text chunks in parallel

    Would manage concurrent tranlation of chunks
    Error Handling 
    Preserve order of chunks
    Track transaltion progress

    """

    def __init__(self, translator, max_workers: int = 5):
        """
        Initialize batch tranlator

        Arguments:
        translator: the translation API instance 
        max_workers: Maximum number of parallell translations(default set to 5)
        """  

        self.translator = translator
        self.max_workers = max_workers
        self.logger = logging.getLogger(__name__)


    def translate_chunks(self, chunks: List[TextChunk]) -> List[Dict[str, Any]]:
        """
        Translate a list of text chunks in parallel

        Function would 
        create a thread pool 
        submit chunks to be translated
        collect the results as they come in 
        Handle errors 

        Arguments:
        chunks: List of TextChunk objects to translate

        would return a list of dictionaries containing translation results
        
        """

        translated_chunks = []


        with ThreadPoolExecutor(max_workers= self.max_workers) as executor:

            #Chunk Submission for translation
            future_to_chunk = {
                executor.submit(self._translate_chunk, chunk): chunk
                for chunk in chunks
            }

            #Processing Results  as they complete
            for future in as_completed(future_to_chunk):
                chunk = future_to_chunk[future]
                try:
                    result = future.result()
                    translated_chunks.append(result)
                    self.logger.info(f"Translated chunk {chunk.index}")
                except Exception as e:
                    self.logger.error(f"Error translating chunk {chunk.index}: {str(e)}")
                    #Error Information
                    translated_chunks.append({ 
                        'index': chunk.index,
                        'error':str(e),
                        'content':chunk.content,
                        'needs_retry': True

                    })
                
            return sorted(translated_chunks, key=lambda x: x['index'])
        
    
    def _translate_chunk(self,chunk:TextChunk) -> Dict[str,Any]:
        """
        Translate a single chunk with its context.
        
        This method:
        1. Prepares text with context
        2. Sends to translator
        3. Returns result with metadata
        
        Args:
            chunk: TextChunk object to translate
            
        Returns:
            Dictionary with translation results and metadata
        """
        try:
            # Prepare text with context
            text_parts = []
            if chunk.context_prefix and chunk.context_prefix.strip():
                text_parts.append(chunk.context_prefix.strip())
            text_parts.append(chunk.content.strip())
            if chunk.context_suffix and chunk.context_suffix.strip():
                text_parts.append(chunk.context_suffix.strip())
            
            text_to_translate = ' '.join(filter(None, text_parts))

            # Get translation
            response = self.translator.translate(text_to_translate)
            
            # First check if response is a dictionary (error case from base API)
            if isinstance(response, dict):
                error_msg = response.get('message', 'Unknown error')
                self.logger.error(f"Translation error for chunk {chunk.index}: {error_msg}")
                return {
                    'index': chunk.index,
                    'error': error_msg,
                    'content': chunk.content,
                    'needs_retry': True
                }
            
            # Handle successful response
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    # Get the translation from the response - adjust key based on API response
                    translated_text = response_data.get('out', response_data.get('translated_text', ''))
                    if not translated_text:
                        raise Exception("No translated text in response")
                        
                    # Return successful translation with all context
                    return {
                        'index': chunk.index,
                        'original_text': chunk.content,
                        'translated_text': translated_text,
                        'context_prefix': chunk.context_prefix,
                        'context_suffix': chunk.context_suffix,
                        'word_count': chunk.word_count,
                        'full_text_translated': text_to_translate  # Include full translated text for verification
                    }
                except Exception as e:
                    self.logger.error(f"Failed to parse response for chunk {chunk.index}: {str(e)}")
                    return {
                        'index': chunk.index,
                        'error': f"Failed to parse response: {str(e)}",
                        'content': chunk.content,
                        'needs_retry': True
                    }
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                self.logger.error(f"Translation error for chunk {chunk.index}: {error_msg}")
                return {
                    'index': chunk.index,
                    'error': error_msg,
                    'content': chunk.content,
                    'needs_retry': True
                }
                
        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"Unexpected error translating chunk {chunk.index}: {error_msg}")
            return {
                'index': chunk.index,
                'error': error_msg,
                'content': chunk.content,
                'needs_retry': True
            }
        
    
                        
                        
