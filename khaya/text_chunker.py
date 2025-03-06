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
    
    def __init__(self, translator, max_chunk_size: int = 1000, max_workers: int = 5):
        self.translator = translator
        self.max_workers = max_workers
        self.max_chunk_size = max_chunk_size
    
    def chunk_translate(self, text: str) -> str:
        """Translate large text by chunking, translating in parallel, and reassembling."""
        if not text:
            return ""
            
        # create chunks
        chunks = self._create_chunks(text)
        
        # Translate chunks in parallel
        results = self._multichunk_translate(chunks)
        
        # assemble translated text
        translated_text = " ".join(
            r.get('translated_text', '') 
            for r in sorted(results, key=lambda x: x['index'])
            if 'translated_text' in r
        )
        
        return translated_text
    
    def _create_chunks(self, text: str) -> List[TextChunk]:
        """Split text into chunks with maximum character limit."""
        chunks = []
        start = 0
        chunk_index = 0
        
        while start < len(text):
            # determine end position 
            end = min(start + self.max_chunk_size, len(text))
            
            # search for a good point to chunk the text
            if end < len(text):
                chunk_text = text[start:end]
                
                # using seprators 
                for seperator in ['. ', '! ', '? ']:
                    position = chunk_text.rfind(seperator)
                    if position > 0:
                        end = start + position + 2  # Include the separator and space
                        break
                
                # try space if no seperator found 
                if end == min(start + self.max_chunk_size, len(text)):
                    position = chunk_text.rfind(' ')
                    if position > 0:
                        end = start + position + 1  # Include the space
            
            # create chunk and add to list
            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append(TextChunk(content=chunk_text, index=chunk_index))
                chunk_index += 1
            
            # move to next position
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
        
        # Sort results by index before returning
        return sorted(results, key=lambda x: x['index'])
    
    def _translate_chunk(self, chunk: TextChunk) -> Dict:
        """Translate a single chunk."""
        try:
            # Check if the translator has a translate method (KhayaInterface)
            if hasattr(self.translator, 'translate'):
                response = self.translator.translate(chunk.content, "en-tw")
            # Fallback to chunk_translate for backward compatibility
            elif hasattr(self.translator, 'chunk_translate'):
                response = self.translator.chunk_translate(chunk.content)
            else:
                return {
                    'index': chunk.index,
                    'error': "Translator has no translate or chunk_translate method"
                }
            
            if isinstance(response, dict) and 'type' in response:
                return {
                    'index': chunk.index, 
                    'error': response.get('message', 'Unknown API error')
                }
            
            if hasattr(response, 'text'):
                response_text = response.text
                
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
        
    
                        
                        
