from typing import List, Dict, Any, Callable, Optional
import logging
from concurrent.futures import ThreadPoolExecutor
from .text_chunker import TextChunker, BatchTranslator, TextChunk

class LargeTextTranslator:
    """Translates large texts using chunking and parallel processing."""
    
    def __init__(self, translator, max_chunk_size: int = 9900, max_workers: int = 5):
        """Initialize with translation API client and processing parameters."""
        self.translator = translator
        self.chunker = TextChunker(max_chunk_size=max_chunk_size)
        self.batch_translator = BatchTranslator(translator, max_workers=max_workers)
        self.logger = logging.getLogger(__name__)
    
    def translate(self, text: str, progress_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """Translate large text with chunking and parallel processing."""
        # Notify start
        if progress_callback:
            progress_callback({"status": "starting"})
        
        # Split text into chunks
        chunks = list(self.chunker.create_chunks(text))
        
        if progress_callback:
            progress_callback({
                "status": "chunking_complete", 
                "total_chunks": len(chunks)
            })
        
        # Translate chunks in parallel
        results = self.batch_translator.translate_chunks(chunks)
        
        # Handle failed chunks
        failed_chunks = [r for r in results if r.get('needs_retry', False)]
        if failed_chunks and progress_callback:
            progress_callback({
                "status": "retrying", 
                "failed_chunks": len(failed_chunks)
            })
        
        # Retry failed chunks
        if failed_chunks:
            retry_chunks = []
            for chunk_result in failed_chunks:
                # Find the original chunk by index
                original_chunk = next((c for c in chunks if c.index == chunk_result['index']), None)
                if original_chunk:
                    retry_chunks.append(original_chunk)
            
            if retry_chunks:
                retry_results = self.batch_translator.translate_chunks(retry_chunks)
                
                # Update results with successful retries
                for retry in retry_results:
                    if not retry.get('needs_retry', False):
                        for i, result in enumerate(results):
                            if result['index'] == retry['index']:
                                results[i] = retry
                                break
        
        # Minimal statistics
        stats = self._get_minimal_stats(results, len(chunks))
        
        # Merge translated chunks
        translated_text = " ".join(
            r.get('translated_text', '') 
            for r in sorted(results, key=lambda x: x['index'])
            if 'translated_text' in r and r.get('translated_text')
        )
        
        # Notify completion
        if progress_callback:
            progress_callback({"status": "complete"})
        
        return {
            "translated_text": translated_text,
            "statistics": stats
        }
    
    def _get_minimal_stats(self, results: List[Dict], total_chunks: int) -> Dict[str, Any]:
        """Generate minimal translation statistics."""
        successful = sum(1 for r in results if r.get('translated_text'))
        failed = total_chunks - successful
        
        return {
            "total_chunks": total_chunks,
            "successful_chunks": successful,
            "failed_chunks": failed
        }