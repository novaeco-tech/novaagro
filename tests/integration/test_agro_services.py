import requests
import os
from unittest.mock import patch

API_URL = "http://api:8000"

# This test runs *locally* against the agro-api only.
# It MUST mock any calls to external enablers (e.g., hub-api).

@patch('requests.post')
def test_create_farm_project(mock_post):
    """
    Tests that the 'agro-api' correctly calls the 'hub-api' when
    a new farm is created.
    """
    
    # Configure the mock to return a successful response
    # This simulates the 'hub-api' returning a new project ID
    mock_post.return_value.status_code = 201
    mock_post.return_value.json.return_value = {"id": "project-uuid-123"}

    # This is our internal 'agro-api' endpoint
    response = requests.post(
        f"{API_URL}/v1/farms",
        json={"farm_name": "My New Farm", "location": "Nairobi"}
    )
    
    # Test 1: Did our own API succeed?
    assert response.status_code == 201
    assert response.json()["farm_name"] == "My New Farm"
    
    # Test 2: Did our API correctly call the external 'hub-api'?
    mock_post.assert_called_with(
        "http://hub-api:8000/v1/projects",
        json={"name": "My New Farm", "type": "agro"}
    )
    
    # Test 3: Did our API save the project ID it got from hub?
    assert response.json()["hub_project_id"] == "project-uuid-123"