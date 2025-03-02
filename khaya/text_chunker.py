from dataclasses import dataclass
from typing import List, Dict, Any, Generator, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from langchain.text_splitter import RecursiveCharacterTextSplitter

@dataclass
class TextChunk:
    """Text chunk with metadata for translation."""
    content: str
    index: int
    context_prefix: str = ""
    context_suffix: str = ""

class BatchTranslator:
    """Minimal implementation for chunking and translating large texts."""
    
    def __init__(self, translator, max_chunk_size: int = 9900, max_workers: int = 5):
        self.translator = translator
        self.max_workers = max_workers
        self.max_chunk_size = max_chunk_size
        
        # Initialize text splitter
        overlap = min(int(max_chunk_size * 0.2), 200)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=max_chunk_size,
            chunk_overlap=overlap,
            length_function=lambda text: len(text.split()),
            separators=["\n\n", "\n", ". ", "! ", "? ", ".", "!", "?", " ", ""]
        )
    
    def translate(self, text: str) -> str:
        """Translate large text by chunking, translating in parallel, and reassembling."""
        # Create chunks
        chunks = list(self._create_chunks(text))
        if not chunks:
            return ""
        
        # Translate chunks in parallel
        results = self._translate_chunks(chunks)
        
        # Reassemble translated text
        translated_text = " ".join(
            r.get('translated_text', '') 
            for r in sorted(results, key=lambda x: x['index'])
            if 'translated_text' in r
        )
        
        return translated_text
    
    def _create_chunks(self, text: str) -> Generator[TextChunk, None, None]:
        """Split text into chunks with context from adjacent chunks."""
        if not text or not text.strip():
            return
        
        chunks = self.text_splitter.split_text(text)
        if not chunks:
            return
            
        for i, chunk in enumerate(chunks):
            # Add context from adjacent chunks
            context_prefix = ""
            if i > 0:
                prev_words = chunks[i-1].split()
                context_prefix = " ".join(prev_words[-min(50, len(prev_words)):])
            
            context_suffix = ""
            if i < len(chunks) - 1:
                next_words = chunks[i+1].split()
                context_suffix = " ".join(next_words[:min(50, len(next_words))])
            
            yield TextChunk(
                content=chunk,
                index=i,
                context_prefix=context_prefix,
                context_suffix=context_suffix
            )
    
    def _translate_chunks(self, chunks: List[TextChunk]) -> List[Dict]:
        """Translate chunks in parallel."""
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self._translate_chunk, chunk): chunk for chunk in chunks}
            
            for future in as_completed(futures):
                try:
                    results.append(future.result())
                except Exception as e:
                    chunk = futures[future]
                    results.append({
                        'index': chunk.index, 
                        'error': str(e)
                    })
                    
        return results
    
    def _translate_chunk(self, chunk: TextChunk) -> Dict:
        """Translate a single chunk with context."""
        text = ' '.join(filter(None, [chunk.context_prefix, chunk.content, chunk.context_suffix]))
        
        try:
            response = self.translator.translate(text)
            
            # Handle different response types
            if isinstance(response, dict) and 'type' in response:
                return {
                    'index': chunk.index, 
                    'error': response.get('message', 'Unknown API error')
                }
            
            if hasattr(response, 'text'):
                response_text = response.text
                
                # Remove quotes if present
                if response_text.startswith('"') and response_text.endswith('"'):
                    response_text = response_text[1:-1]
                
                return {
                    'index': chunk.index,
                    'translated_text': response_text
                }
            
            return {
                'index': chunk.index,
                'error': f"Unexpected response type: {type(response)}"
            }
                
        except Exception as e:
            return {'index': chunk.index, 'error': str(e)}
        
    
                        
                        
