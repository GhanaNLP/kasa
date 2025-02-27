from dataclasses import dataclass
import re
from typing import List, Dict, Any, Generator
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import requests
from tenacity import retry, stop_after_attempt, wait_exponential
from tqdm import tqdm
from langchain.text_splitter import RecursiveCharacterTextSplitter

@dataclass
class TextChunk:
    """Text chunk with metadata for translation."""
    content: str
    index: int
    word_count: int
    is_partial_sentence: bool = False
    context_prefix: str = ""
    context_suffix: str = ""

class TextChunker:
    """Splits text into chunks using LangChain's RecursiveCharacterTextSplitter."""
    
    def __init__(self, max_chunk_size: int = 9900):
        self.max_chunk_size = max_chunk_size
        self.logger = logging.getLogger(__name__)
        
        # Calculate a reasonable overlap (20% of chunk size, max 200 words)
        overlap = min(int(self.max_chunk_size * 0.2), 200)
        overlap = min(overlap, max(1, self.max_chunk_size - 1))
        
        # Initialize LangChain text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.max_chunk_size,
            chunk_overlap=overlap,
            length_function=lambda text: len(text.split()),
            separators=["\n\n", "\n", ". ", "! ", "? ", ".", "!", "?", " ", ""]
        )
    
    def create_chunks(self, text: str) -> Generator[TextChunk, None, None]:
        """Split text into chunks using LangChain's text splitter."""
        if not text or not text.strip():
            self.logger.warning("Empty text provided for chunking")
            return
        
        try:
            # Split text using LangChain
            chunks = self.text_splitter.split_text(text)
            
            if not chunks:
                self.logger.warning("No chunks created from text")
                return
                
            # Process chunks and add context
            for i, chunk_text in enumerate(chunks):
                # Get context from adjacent chunks (up to 50 words)
                context_prefix = ""
                if i > 0:
                    prev_words = chunks[i-1].split()
                    context_prefix = " ".join(prev_words[-min(50, len(prev_words)):])
                
                context_suffix = ""
                if i < len(chunks) - 1:
                    next_words = chunks[i+1].split()
                    context_suffix = " ".join(next_words[:min(50, len(next_words))])
                
                yield TextChunk(
                    content=chunk_text,
                    index=i,
                    word_count=len(chunk_text.split()),
                    is_partial_sentence=not chunk_text.strip().endswith(('.', '!', '?')),
                    context_prefix=context_prefix,
                    context_suffix=context_suffix
                )
                
        except Exception as e:
            self.logger.error(f"Error during text chunking: {str(e)}")


class BatchTranslator:
    """Translates chunks in parallel."""

    def __init__(self, translator, max_workers: int = 5):
        self.translator = translator
        self.max_workers = max_workers
        self.logger = logging.getLogger(__name__)

    def translate_chunks(self, chunks: List[TextChunk]) -> List[Dict]:
        """Translate chunks in parallel with progress tracking."""
        if not chunks:
            return []
            
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self._translate_chunk, chunk): chunk for chunk in chunks}
            results = []
            
            for future in tqdm(as_completed(futures), total=len(chunks), desc="Translating"):
                try:
                    results.append(future.result())
                except Exception as e:
                    chunk = futures[future]
                    results.append({
                        'index': chunk.index, 
                        'error': str(e),
                        'needs_retry': True
                    })
                    
            return sorted(results, key=lambda x: x['index'])
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1))
    def _translate_chunk(self, chunk: TextChunk) -> Dict:
        """Translate a chunk with context."""
        text = ' '.join(filter(None, [chunk.context_prefix, chunk.content, chunk.context_suffix]))
        
        try:
            response = self.translator.translate(text)
            
            # Debug response
            self.logger.info(f"Response type: {type(response)}")
            
            # Handle error response (dictionary)
            if isinstance(response, dict) and 'type' in response:
                self.logger.error(f"API error: {response.get('message', 'Unknown API error')}")
                return {
                    'index': chunk.index, 
                    'error': response.get('message', 'Unknown API error'),
                    'needs_retry': True
                }
            
            # Handle successful response (Response object)
            if hasattr(response, 'text'):
                self.logger.info(f"Response status code: {response.status_code}")
                self.logger.info(f"Response text: {response.text[:100]}...")
                
                # The API returns a JSON string directly
                response_text = response.text
                
                # Remove quotes if the response is a quoted string
                if response_text.startswith('"') and response_text.endswith('"'):
                    response_text = response_text[1:-1]
                
                return {
                    'index': chunk.index,
                    'translated_text': response_text,
                    'word_count': chunk.word_count
                }
            
            # Unexpected response type
            self.logger.error(f"Unexpected response type: {type(response)}")
            return {
                'index': chunk.index,
                'error': f"Unexpected response type: {type(response)}",
                'needs_retry': True
            }
                
        except Exception as e:
            self.logger.exception(f"Exception in _translate_chunk: {str(e)}")
            return {'index': chunk.index, 'error': str(e), 'needs_retry': True}
        
    
                        
                        
