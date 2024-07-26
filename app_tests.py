import pytest
from app import app

# 1.2.4 Unit Tests

@pytest.fixture  
def client():
    with app.test_client() as client:
        yield client  

def test_get_data(client):

    response = client.get('/api/data')
    assert response.status_code == 200

    response = client.get('/api/data?page=3')
    assert response.status_code == 200

def test_get_attr_by_title_valid(client):
    """Test valid songs by title"""
    songs = ["24k Magic", "All Mine", "Bastia", "Choke", "CALL ME BABY"]

    for song in songs:
        response = client.get(f'/api/data/{song}')
        assert response.status_code == 200

    for song in songs:
        response = client.get(f'/api/data/{song}/loudness')
        assert response.status_code == 200

def test_get_attr_by_title_invalid(client):
    """Test valid songs by title"""
    songs = ["qwaekrtnmokwejmtnw", "12352135 2315 32141234", "this", "doesn't", "exist"]

    for song in songs:
        response = client.get(f'/api/data/{song}')
        assert response.status_code == 404
        assert response.json == {"error": "Song not found"}

    response = client.get(f'/api/data/Afterlife/fakecolumn')
    assert response.status_code == 400
    assert response.json == {"error": "Invalid column name"}
    
    response = client.get(f'/api/data/fakesong/fakecolumn')
    assert response.status_code == 404
    assert response.json == {"error": "Song not found"}

def test_rate_song_valid(client):
    """Test valid rating input"""
    songs = ["All Us", "Bad Romance", "Blue", "Cause", "City of Blinding Lights"]

    for song in songs:
        response = client.get(f'/api/data/{song}/rating/4')
        assert response.status_code == 200
        assert response.json == {'message': f"Rated '{song}' with 4"}

def test_rate_song_invalid_rating(client):
    """Test for an invalid rating, where the rating is not in the range of 1 and 5."""

    response = client.get('/api/data/All Night/rating/6')
    assert response.status_code == 400
    assert response.json == {'error': "Invalid rating (must be 1-5)"}

    response = client.get('/api/data/Afterlife/rating/0')
    assert response.status_code == 400
    assert response.json == {'error': "Invalid rating (must be 1-5)"}

    response = client.get('/api/data/Song That Doesn\'t Exist/rating/325325')
    assert response.status_code == 400
    assert response.json == {'error': "Invalid rating (must be 1-5)"}

def test_rate_song_invalid_title(client):
    """Test invalid song title"""

    response = client.get('/api/data/NonexistentSong/rating/4')
    assert response.status_code == 404
    assert response.json == {'error': "Song not found"}
