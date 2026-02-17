import pytest
from unittest.mock import MagicMock, AsyncMock
from google.adk.models.google_llm import Gemini, LlmResponse
from google.genai import types

class AsyncIterator:
    def __init__(self, seq):
        self.iter = iter(seq)
    def __aiter__(self):
        return self
    async def __anext__(self):
        try:
            return next(self.iter)
        except StopIteration:
            raise StopAsyncIteration
    async def aclose(self):
        pass

@pytest.fixture(autouse=True)
def mock_google_llm(monkeypatch):
    """Mocks the Gemini generate_content_async to avoid live API calls."""
    
    # Create the mock raw response
    mock_raw_response = MagicMock(spec=types.GenerateContentResponse)
    
    # Mock candidate
    mock_candidate = MagicMock()
    mock_candidate.content = types.Content(
        role="model",
        parts=[types.Part.from_text(text="Mocked response for integration tests.")]
    )
    mock_candidate.finish_reason = types.FinishReason.STOP
    mock_candidate.grounding_metadata = None
    mock_candidate.citation_metadata = None
    mock_candidate.avg_logprobs = None
    mock_candidate.logprobs_result = None
    
    mock_raw_response.candidates = [mock_candidate]
    mock_raw_response.usage_metadata = types.UsageMetadata(
        prompt_token_count=10, 
        response_token_count=10, 
        total_token_count=20
    )
    mock_raw_response.model_version = "gemini-1.5-flash"
    mock_raw_response.model_dump.return_value = {}

    def mock_gen_async(self, llm_request, stream=False):
        return AsyncIterator([LlmResponse.create(mock_raw_response)])

    # Mock the internal generate_content_async of Gemini
    monkeypatch.setattr(Gemini, "generate_content_async", mock_gen_async)
    
    # Also mock _preprocess_request to avoid validation errors
    monkeypatch.setattr(Gemini, "_preprocess_request", AsyncMock())
    # Mock api_client to avoid initialization errors
    monkeypatch.setattr(Gemini, "api_client", MagicMock())
    monkeypatch.setattr(Gemini, "_api_backend", MagicMock())
    
    monkeypatch.setattr(Gemini, "_maybe_append_user_content", lambda self, req: None)
