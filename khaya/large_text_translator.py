from typing import List, Dict, Any
from .text_chunker import TextChunker, BatchTranslator, TextChunk

import logging


class LargeTextTranslator:
    """
    High-level interface for translating large texts.
    
    This class orchestrates the entire translation process:
    1. Text chunking
    2. Parallel translation
    3. Error handling and retries
    4. Progress tracking
    5. Result assembly
    """
    def __init__(
            self,
            translator,
            max_chunk_size: int = 9900,
            max_workers: int = 5,
            retry_count: int = 3
        ):
        """

        Initialize the large text translator.
        
        Args:
            translator: Translation API instance
            max_chunk_size: Maximum words per chunk
            max_workers: Maximum parallel translations
            retry_count: Number of retry attempts for failed chunks
        
        """
        self.chunker = TextChunker(max_chunk_size=max_chunk_size)
        self.batch_translator = BatchTranslator(translator, max_workers=max_workers)
        self.retry_count = retry_count
        self.logger = logging.getLogger(__name__)

    def translate(
        self,
        text: str,
        progress_callback: callable = None
    ) -> Dict[str, Any]:
        """
        Translate a large text by managing the entire process.
        
        Args:
            text: The text to translate
            progress_callback: Optional function to report progress
            
        Returns:
            Dictionary containing:
                - translated_text: The complete translated text
                - chunks: Information about the chunks processed
                - statistics: Processing statistics
        """
        try:
            # Step 1: Create chunks
            if progress_callback:
                progress_callback({"status": "starting", "message": "Starting chunking process..."})
            
            chunks = list(self.chunker.create_chunks(text))
            total_chunks = len(chunks)
            
            if progress_callback:
                progress_callback({
                    "status": "chunking_complete",
                    "total_chunks": total_chunks,
                    "message": f"Split text into {total_chunks} chunks"
                })
            
            # Step 2: Translate chunks
            translated_chunks = []
            for i, chunk in enumerate(chunks, 1):
                if progress_callback:
                    progress_callback({
                        "status": "chunk_processing",
                        "current_chunk": i,
                        "total_chunks": total_chunks,
                        "message": f"Translating chunk {i}/{total_chunks}"
                    })
                
                result = self.batch_translator._translate_chunk(chunk)
                translated_chunks.append(result)
                
                if progress_callback:
                    progress_callback({
                        "status": "chunk_complete",
                        "chunks_processed": i,
                        "total_chunks": total_chunks,
                        "message": f"Completed chunk {i}/{total_chunks}"
                    })
            
            # Step 3: Handle any failed chunks
            failed_chunks = [c for c in translated_chunks if c.get('needs_retry', False)]
            if failed_chunks:
                if progress_callback:
                    progress_callback({
                        "status": "retrying",
                        "failed_chunks": len(failed_chunks),
                        "message": f"Retrying {len(failed_chunks)} failed chunks"
                    })
                translated_chunks = self._handle_failed_chunks(failed_chunks, translated_chunks)
            
            if progress_callback:
                progress_callback({
                    "status": "translation_complete",
                    "chunks_processed": total_chunks,
                    "message": "Translation complete"
                })
            
            # Step 4: Compile statistics
            stats = self._compile_statistics(chunks, translated_chunks)
            
            # Step 5: Merge translations
            final_text = self._merge_translations(translated_chunks)
            
            return {
                "translated_text": final_text,
                "chunks": translated_chunks,
                "statistics": stats
            }
            
        except Exception as e:
            self.logger.error(f"Translation failed: {str(e)}")
            raise

    def _handle_failed_chunks(
        self,
        failed_chunks: List[Dict[str, Any]],
        all_chunks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Handle retry logic for failed chunks."""
        for chunk in failed_chunks:
            for attempt in range(self.retry_count):
                try:
                    # Retry translation
                    translation = self.batch_translator._translate_chunk(
                        TextChunk(
                            content=chunk['content'],
                            index=chunk['index'],
                            word_count=len(chunk['content'].split())
                        )
                    )
                    
                    # Update chunk with successful translation
                    chunk.update(translation)
                    chunk.pop('needs_retry', None)
                    chunk.pop('error', None)
                    break
                    
                except Exception as e:
                    self.logger.warning(
                        f"Retry {attempt + 1} failed for chunk {chunk['index']}: {str(e)}"
                    )
        
        return all_chunks
    
    def _compile_statistics(
        self,
        original_chunks: List[TextChunk],
        translated_chunks: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Compile statistics about the translation process."""
        total_chunks = len(original_chunks)
        
        if total_chunks == 0:
            return {
                "total_words": 0,
                "total_chunks": 0,
                "successful_chunks": 0,
                "failed_chunks": 0,
                "success_rate": 100.0  # Consider empty input as successful
            }
        
        total_words = sum(chunk.word_count for chunk in original_chunks)
        
        # Count chunks that have actual translations (not empty and not failed)
        successful_chunks = len([
            c for c in translated_chunks 
            if not c.get('needs_retry') and c.get('translated_text')
        ])
        
        failed_chunks = total_chunks - successful_chunks
        
        # Collect error messages for reporting
        errors = [
            f"Chunk {c['index']}: {c.get('error', 'Unknown error')}"
            for c in translated_chunks
            if c.get('needs_retry') or not c.get('translated_text')
        ]
        
        return {
            "total_words": total_words,
            "total_chunks": total_chunks,
            "successful_chunks": successful_chunks,
            "failed_chunks": failed_chunks,
            "success_rate": (successful_chunks / total_chunks) * 100,
            "errors": errors
        }
    
    def _merge_translations(self, chunks: List[Dict[str, Any]]) -> str:
        """Merge translated chunks into final text."""
        # Sort chunks by index to ensure correct order
        sorted_chunks = sorted(chunks, key=lambda x: x['index'])
        
        # Extract the translated text from each chunk's result
        translated_texts = []
        for chunk in sorted_chunks:
            # Skip failed chunks
            if chunk.get('needs_retry', False):
                self.logger.warning(f"Skipping failed chunk {chunk['index']}: {chunk.get('error', 'Unknown error')}")
                continue
            
            # Get the translation result
            translated_text = chunk.get('translated_text', '')
            if translated_text:
                translated_texts.append(translated_text)
            else:
                self.logger.warning(f"Empty translation for chunk {chunk['index']}")
        
        if not translated_texts:
            self.logger.error("No successful translations to merge")
            return ""
            
        return ' '.join(translated_texts)