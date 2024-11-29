# api/base_service.py
import requests
from typing import Dict, Any, Optional, List

class BaseService:
    def __init__(self, base_url: str = "http://127.0.0.1:5000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def set_auth_token(self, token: str):
        self.session.headers.update({"Authorization": f"Bearer {token}"})
    
    def _handle_response(self, response: requests.Response) -> Dict:
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            error_data = response.json().get('error', {})
            raise Exception(f"HTTP Error: {error_data.get('message', str(e))}")
        except Exception as e:
            raise Exception(f"Error: {str(e)}")

class UserService(BaseService):
    def get_user_by_id(self, user_id: str) -> Dict:
        endpoint = f"{self.base_url}/users/{user_id}"
        response = self.session.get(endpoint)
        return self._handle_response(response)
    
    def create_user(self, email: str, name: str, organization: Optional[str] = None) -> Dict:
        endpoint = f"{self.base_url}/users"
        data = {
            "email": email,
            "name": name,
            "organization": organization
        }
        response = self.session.post(endpoint, json=data)
        return self._handle_response(response)
    
    def update_user(self, user_id: str, updates: Dict[str, Any]) -> Dict:
        endpoint = f"{self.base_url}/users/{user_id}"
        response = self.session.put(endpoint, json=updates)
        return self._handle_response(response)
    
    def delete_user(self, user_id: str) -> None:
        endpoint = f"{self.base_url}/users/{user_id}"
        response = self.session.delete(endpoint)
        self._handle_response(response)

class ChatService(BaseService):
    def create_chat(self, title: str, model_type: str) -> Dict:
        endpoint = f"{self.base_url}/chats"
        data = {
            "title": title,
            "model_type": model_type
        }
        response = self.session.post(endpoint, json=data)
        return self._handle_response(response)
    
    def get_chat(self, chat_id: str) -> Dict:
        endpoint = f"{self.base_url}/chats/{chat_id}"
        response = self.session.get(endpoint)
        return self._handle_response(response)
    
    def get_user_chats(self, limit: int = 20, offset: int = 0, sort: str = "created_at:desc") -> Dict:
        endpoint = f"{self.base_url}/chats"
        params = {
            "limit": limit,
            "offset": offset,
            "sort": sort
        }
        response = self.session.get(endpoint, params=params)
        return self._handle_response(response)
    
    def add_message(self, chat_id: str, role: str, content: str, files: Optional[list] = None) -> Dict:
        endpoint = f"{self.base_url}/chats/{chat_id}/messages"
        data = {
            "content": content,
            "role": role
        }
        if files:
            data["file_ids"] = [f.file_id for f in files]
        response = self.session.post(endpoint, json=data)
        return self._handle_response(response)
    
    def get_messages(self, chat_id: str, include_files: bool = False) -> Dict:
        endpoint = f"{self.base_url}/chats/{chat_id}/messages"
        params = {
            "include_files": include_files
        }
        response = self.session.get(endpoint, params=params)
        return self._handle_response(response)
    
    def delete_chat(self, chat_id: str) -> None:
        endpoint = f"{self.base_url}/chats/{chat_id}"
        response = self.session.delete(endpoint)
        self._handle_response(response)

class FileService(BaseService):
    def upload_file(self, file_obj: Any, chat_id: Optional[str] = None) -> Dict:
        endpoint = f"{self.base_url}/files"
        files = {
            'file': file_obj
        }
        data = {}
        if chat_id:
            data['chat_id'] = chat_id
            
        response = self.session.post(endpoint, files=files, data=data)
        return self._handle_response(response)
    
    def get_file_url(self, file_id: str) -> str:
        endpoint = f"{self.base_url}/files/{file_id}/url"
        response = self.session.get(endpoint)
        return self._handle_response(response)["url"]
    
    def delete_file(self, file_id: str) -> None:
        endpoint = f"{self.base_url}/files/{file_id}"
        response = self.session.delete(endpoint)
        self._handle_response(response)

class LLMService(BaseService):
    def get_completion(self, messages: List[Dict[str, Any]]) -> Dict:
        endpoint = f"{self.base_url}/llm/rag"
        data = {
            "messages": messages,
        }
        response = self.session.post(endpoint, json=data)
        return self._handle_response(response)