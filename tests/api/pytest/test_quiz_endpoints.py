import requests
import pytest
import json

BASE_URL = "http://127.0.0.1:8000"

class TestQuizAPI:
    
    def test_health_check(self):
        response = requests.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "message" in data
        assert response.elapsed.total_seconds() < 0.5

    def test_create_question_valid(self):
        payload = {
            "question_text": "What is Python?",
            "choises": [
                {"choice_text": "A programming language", "is_correct": True},
                {"choice_text": "A snake", "is_correct": False},
                {"choice_text": "A database", "is_correct": False}
            ]
        }
        response = requests.post(f"{BASE_URL}/questions/", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "message" in data

    def test_create_question_invalid_schema(self):
        payload = {"invalid_field": "test"}
        response = requests.post(f"{BASE_URL}/questions/", json=payload)
        assert response.status_code == 422
        assert "detail" in response.json()

    def test_get_question_valid_id(self):
        # First create a question
        payload = {
            "question_text": "Test question for retrieval",
            "choises": [
                {"choice_text": "Option A", "is_correct": True},
                {"choice_text": "Option B", "is_correct": False}
            ]
        }
        requests.post(f"{BASE_URL}/questions/", json=payload)
        
        # Then retrieve it
        response = requests.get(f"{BASE_URL}/questions/1")
        if response.status_code == 200:
            data = response.json()
            assert "id" in data
            assert "question_text" in data

    def test_get_question_invalid_id(self):
        response = requests.get(f"{BASE_URL}/questions/99999")
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_get_choices_valid_question_id(self):
        response = requests.get(f"{BASE_URL}/choices/1")
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, list)
            if len(data) > 0:
                choice = data[0]
                assert "id" in choice
                assert "choice_text" in choice
                assert "is_correct" in choice
                assert "question_id" in choice

    def test_get_choices_invalid_question_id(self):
        response = requests.get(f"{BASE_URL}/choices/99999")
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_get_all_questions(self):
        response = requests.get(f"{BASE_URL}/questions/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert response.elapsed.total_seconds() < 0.5

    def test_update_question(self):
        # First create a question
        payload = {
            "question_text": "Original question",
            "choises": [
                {"choice_text": "Option A", "is_correct": True},
                {"choice_text": "Option B", "is_correct": False}
            ]
        }
        create_response = requests.post(f"{BASE_URL}/questions/", json=payload)
        if create_response.status_code == 200:
            question_id = create_response.json()["id"]
            
            # Update the question
            update_payload = {
                "question_text": "Updated question",
                "choises": [
                    {"choice_text": "Updated Option A", "is_correct": True},
                    {"choice_text": "Updated Option B", "is_correct": False}
                ]
            }
            response = requests.put(f"{BASE_URL}/questions/{question_id}", json=update_payload)
            assert response.status_code == 200
            data = response.json()
            assert "message" in data
            assert "updated" in data["message"].lower()

    def test_delete_question(self):
        # First create a question
        payload = {
            "question_text": "Question to delete",
            "choises": [
                {"choice_text": "Option A", "is_correct": True}
            ]
        }
        create_response = requests.post(f"{BASE_URL}/questions/", json=payload)
        if create_response.status_code == 200:
            question_id = create_response.json()["id"]
            
            # Delete the question
            response = requests.delete(f"{BASE_URL}/questions/{question_id}")
            assert response.status_code == 200
            data = response.json()
            assert "message" in data
            assert "deleted" in data["message"].lower()

    def test_get_stats(self):
        response = requests.get(f"{BASE_URL}/stats")
        assert response.status_code == 200
        data = response.json()
        assert "total_questions" in data
        assert "total_choices" in data
        assert "avg_choices_per_question" in data
        assert isinstance(data["total_questions"], int)
        assert isinstance(data["total_choices"], int)
        assert isinstance(data["avg_choices_per_question"], (int, float))

    def test_update_nonexistent_question(self):
        payload = {
            "question_text": "Updated question",
            "choises": [{"choice_text": "Option A", "is_correct": True}]
        }
        response = requests.put(f"{BASE_URL}/questions/99999", json=payload)
        assert response.status_code == 404

    def test_delete_nonexistent_question(self):
        response = requests.delete(f"{BASE_URL}/questions/99999")
        assert response.status_code == 404