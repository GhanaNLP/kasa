from dataclasses import dataclass
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed

@dataclass
class TextChunk:
    """Text chunk for translation."""
    content: str
    index: int

class BatchTranslator:
    """Simple chunking and translating for large texts."""
    
    def __init__(self, translator, max_chunk_size: int = 1000, max_workers: int = 5, target_language: str = "en-tw"):
        """Initialize the BatchTranslator.
        
        Args:
            translator: The translator object with a translate method
            max_chunk_size: Maximum size of each chunk in characters
            max_workers: Maximum number of parallel translation workers
            target_language: Target language code for translation
        """
        self.translator = translator
        self.max_workers = max_workers
        self.max_chunk_size = max_chunk_size
        self.target_language = target_language
    
    def chunk_translate(self, text: str) -> str:
        """Translate large text by chunking, translating in parallel, and reassembling."""
        if not text:
            return ""
            
        # create chunks
        chunks = self._create_chunks(text)
        
        # translate chunks in parallel
        results = self._multichunk_translate(chunks)
        
        # check if there are errors in chunk translation. 
        errors = [r for r in results if 'error' in r]
        if errors:
            error_msg = f"Translation failed for {len(errors)} of {len(results)} chunks: "
            error_details = [f"Chunk {r['index']}: {r['error']}" for r in errors]
            raise ValueError(error_msg + "; ".join(error_details))
        
        # assemble translated text
        translated_text = " ".join(r['translated_text'] for r in results)
        
        return translated_text
    
    def _create_chunks(self, text: str) -> List[TextChunk]:
        """Split text into chunks with maximum character limit."""
        chunks = []
        start = 0
        chunk_index = 0
        
        while start < len(text):
            # end position 
            end = min(start + self.max_chunk_size, len(text))
            
            # search for chunk boundary
            if end < len(text):
                chunk_text = text[start:end]
                
                # break at sentence boundaries or spaces
                separators = ['. ', '! ', '? ', ' ']
                for separator in separators:
                    position = chunk_text.rfind(separator)
                    if position > 0:
                        end = start + position + len(separator)
                        break
            
            # create chunk and add to list
            if (chunk_text := text[start:end].strip()):
                chunks.append(TextChunk(content=chunk_text, index=chunk_index))
                chunk_index += 1
            
            # next position
            start = end
        
        return chunks
    
    def _multichunk_translate(self, chunks: List[TextChunk]) -> List[Dict]:
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
        
        # sort results by index before returning
        return sorted(results, key=lambda x: x['index'])
    
    def _translate_chunk(self, chunk: TextChunk) -> Dict:
        """Translate a single chunk."""
        try:
            # call the translate method
            response = self.translator.translate(chunk.content, self.target_language)
            
            if isinstance(response, dict) and 'type' in response:
                return {
                    'index': chunk.index, 
                    'error': response.get('message', 'Unknown API error')
                }
            
            if hasattr(response, 'text'):
                return {
                    'index': chunk.index,
                    'translated_text': response.text
                }
            
            return {
                'index': chunk.index,
                'error': f"Unexpected response type: {type(response)}"
            }
                
        except Exception as e:
            return {'index': chunk.index, 'error': str(e)}
        
    
                        
                        
