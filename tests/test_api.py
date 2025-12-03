"""
Tests for the WriteWise API server.
"""

import pytest
from fastapi.testclient import TestClient
from writewise.api.server import app


@pytest.fixture
def client():
    """Create a test client for the API."""
    return TestClient(app)


def test_root_endpoint(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data


def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_check_endpoint_valid_text(client):
    """Test the check endpoint with valid text."""
    response = client.post(
        "/api/check",
        json={"text": "This is a test sentence.", "auto_correct": False}
    )
    assert response.status_code == 200
    data = response.json()
    
    assert "original_text" in data
    assert "grammar_issues" in data
    assert "style_suggestions" in data
    assert "readability" in data
    assert "score" in data
    assert data["original_text"] == "This is a test sentence."


def test_check_endpoint_with_grammar_error(client):
    """Test the check endpoint with text containing grammar errors."""
    response = client.post(
        "/api/check",
        json={"text": "She don't like apples.", "auto_correct": False}
    )
    assert response.status_code == 200
    data = response.json()
    
    # Should detect grammar issues
    assert len(data["grammar_issues"]) > 0


def test_check_endpoint_auto_correct(client):
    """Test the check endpoint with auto-correction enabled."""
    response = client.post(
        "/api/check",
        json={"text": "She don't like apples.", "auto_correct": True}
    )
    assert response.status_code == 200
    data = response.json()
    
    # Should return corrected text
    assert data["corrected_text"] is not None
    assert data["corrected_text"] != data["original_text"]


def test_check_endpoint_empty_text(client):
    """Test the check endpoint with empty text."""
    response = client.post(
        "/api/check",
        json={"text": "", "auto_correct": False}
    )
    assert response.status_code == 400


def test_check_endpoint_whitespace_only(client):
    """Test the check endpoint with whitespace-only text."""
    response = client.post(
        "/api/check",
        json={"text": "   ", "auto_correct": False}
    )
    assert response.status_code == 400


def test_check_endpoint_readability_metrics(client):
    """Test that readability metrics are included in response."""
    response = client.post(
        "/api/check",
        json={"text": "The cat sat on the mat.", "auto_correct": False}
    )
    assert response.status_code == 200
    data = response.json()
    
    readability = data["readability"]
    assert "flesch_reading_ease" in readability
    assert "flesch_kincaid_grade" in readability
    assert "gunning_fog" in readability
    assert "smog_index" in readability
    assert "difficult_words" in readability
    assert "reading_time_minutes" in readability


def test_check_endpoint_statistics(client):
    """Test that text statistics are included in response."""
    text = "First sentence. Second sentence. Third sentence."
    response = client.post(
        "/api/check",
        json={"text": text, "auto_correct": False}
    )
    assert response.status_code == 200
    data = response.json()
    
    assert data["word_count"] == 6
    assert data["sentence_count"] == 3
    assert data["character_count"] == len(text)


def test_check_endpoint_score(client):
    """Test that quality score is calculated."""
    response = client.post(
        "/api/check",
        json={"text": "This is a well-written sentence.", "auto_correct": False}
    )
    assert response.status_code == 200
    data = response.json()
    
    assert "score" in data
    assert 0 <= data["score"] <= 100
