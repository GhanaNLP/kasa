import pytest
import os
from unittest.mock import Mock

from khaya.text_chunker import BatchTranslator, TextChunk


class SimpleTranslator:
    """Simple translator that returns predictable responses for testing."""
    
    def translate(self, text, target_language=None):
        """Simple translate method that returns the text with a prefix."""
        class Response:
            def __init__(self, text):
                self.text = f"Translated: {text}"
        
        return Response(text)


@pytest.fixture
def batch_translator():
    """Create a BatchTranslator with a simple translator."""
    translator = SimpleTranslator()
    return BatchTranslator(
        translator=translator,
        max_chunk_size=50,  # Small size for testing
        max_workers=2
    )


class TestBatchTranslator:
    """Tests for the core functionality of BatchTranslator."""
    
    def test_create_chunks(self, batch_translator):
        """Test that text is properly split into chunks."""
        # Test with text shorter than max_chunk_size
        short_text = "Short text."
        short_chunks = batch_translator._create_chunks(short_text)
        assert len(short_chunks) == 1
        assert short_chunks[0].content == short_text
        
        # Test with text longer than max_chunk_size
        long_text = "First sentence. Second sentence. Third sentence. Fourth sentence."
        long_chunks = batch_translator._create_chunks(long_text)
        assert len(long_chunks) > 1
        
        # Test with empty text
        empty_chunks = batch_translator._create_chunks("")
        assert len(empty_chunks) == 0
    
    def test_translate_chunk(self, batch_translator):
        """Test translation of a single chunk."""
        chunk = TextChunk(content="Test content", index=0)
        result = batch_translator._translate_chunk(chunk)
        
        assert result["index"] == 0
        assert "translated_text" in result
        assert "Test content" in result["translated_text"]
    
    def test_multichunk_translate(self, batch_translator):
        """Test translation of multiple chunks."""
        chunks = [
            TextChunk(content="Chunk 1", index=0),
            TextChunk(content="Chunk 2", index=1),
            TextChunk(content="Chunk 3", index=2)
        ]
        
        results = batch_translator._multichunk_translate(chunks)
        
        assert len(results) == 3
        assert all("translated_text" in r for r in results)
        assert all(r["index"] in [0, 1, 2] for r in results)
    
    def test_chunk_translate(self, batch_translator):
        """Test the complete chunk_translate method."""
        # Test with small text
        small_text = "Hello world"
        small_result = batch_translator.chunk_translate(small_text)
        
        assert small_result
        assert isinstance(small_result, str)
        
        # Test with larger text
        large_text = "First sentence. Second sentence. Third sentence."
        large_result = batch_translator.chunk_translate(large_text)
        
        assert large_result
        assert isinstance(large_result, str)
        
        # Test with empty text
        empty_result = batch_translator.chunk_translate("")
        assert empty_result == ""
    
    def test_empty_text(self):
        """Test handling of empty text."""
        mock_translator = Mock()
        batch_translator = BatchTranslator(mock_translator)
        
        result = batch_translator.chunk_translate("")
        
        assert result == ""
        mock_translator.translate.assert_not_called()


def test_batch_translator_with_real_api(khaya_interface):
    """Test BatchTranslator with a real API call."""
    # Create a batch translator with the API
    batch_translator = BatchTranslator(
        translator=khaya_interface,
        max_chunk_size=50,
        max_workers=2
    )
    
    # Small text to minimize API usage
    text = "Hello, world."
    
    # Check the chunking
    chunks = batch_translator._create_chunks(text)
    print("\nChunks created:")
    for chunk in chunks:
        print(f"  Chunk {chunk.index}: {chunk.content!r}")
    
    # Try direct API call to see the response
    print("\nDirect API response:")
    try:
        response = khaya_interface.translate(text, "en-tw")
        print(f"  API response: {response}")
    except Exception as e:
        print(f"  API error: {str(e)}")
    
    # Perform the translation using BatchTranslator
    result = batch_translator.chunk_translate(text)
    print(f"\nTranslation result: {result!r}")
    
    # Basic assertion - just check that we get a string back
    assert isinstance(result, str), "Should return a string" 