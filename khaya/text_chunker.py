from dataclasses import dataclass
from typing import List, Dict, Any, Generator, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from langchain.text_splitter import RecursiveCharacterTextSplitter

@dataclass
class TextChunk:
    """Text chunk with metadata for translation."""
    content: str
    index: int
    chunk_pfx: str = ""
    chunk_sfx: str = ""

class BatchTranslator:
    """chunking and translating large texts."""
    
    def __init__(self, translator, max_chunk_size: int = 9900, max_workers: int = 5):
        self.translator = translator
        self.max_workers = max_workers
        self.max_chunk_size = max_chunk_size
        
        # text splitter initialisaing
        overlap = min(int(max_chunk_size * 0.2), 200)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=max_chunk_size,
            chunk_overlap=overlap,
            length_function=lambda text: len(text.split()),
            separators=["\n\n", "\n", ". ", "! ", "? ", ".", "!", "?", " ", ""]
        )
    
    def chunk_translate(self, text: str) -> str:
        """Translate large text by chunking, translating in parallel, and reassembling."""
        # create chunks
        chunks = list(self._create_chunks(text))
        if not chunks:
            return ""
        
        #  chunk translation
        results = self.multichunk_translate(chunks)
        
        # assembling translated text
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
            # ensure context after chunks 
            chunk_pfx = ""
            if i > 0:
                prev_words = chunks[i-1].split()
                chunk_pfx = " ".join(prev_words[-min(50, len(prev_words)):])
            
            chunk_sfx = ""
            if i < len(chunks) - 1:
                next_words = chunks[i+1].split()
                chunk_sfx = " ".join(next_words[:min(50, len(next_words))])
            
            yield TextChunk(
                content=chunk,
                index=i,
                chunk_pfx=chunk_pfx,
                chunk_sfx=chunk_sfx
            )
    
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
                    
        return results
    
    def _translate_chunk(self, chunk: TextChunk) -> Dict:
        """Translate a single chunk with context."""
        text = ' '.join(filter(None, [chunk.chunk_pfx, chunk.content, chunk.chunk_sfx]))
        
        try:
            response = self.translator.chunk_translate(text)
            
            # handle response
            if isinstance(response, dict) and 'type' in response:
                return {
                    'index': chunk.index, 
                    'error': response.get('message', 'Unknown API error')
                }
            
            if hasattr(response, 'text'):
                response_text = response.text
                
                # check for quotes in response
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
        
    
                        
                        
