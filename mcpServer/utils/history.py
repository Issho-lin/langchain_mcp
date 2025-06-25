'''
Author: linqibin
Date: 2025-05-29 10:02:45
LastEditors: linqibin
LastEditTime: 2025-05-29 11:09:59
Description: 

Copyright (c) 2025 by 智慧空间研究院/金地空间科技, All Rights Reserved. 
'''
from langchain_core.chat_history import BaseChatMessageHistory
from dataclasses import dataclass
from typing import List, Optional
from langchain_core.messages import BaseMessage

@dataclass
class JSONChatHistoryInput:
    session_id: str
    dir: Optional[str] = None


class JSONChatHistory(BaseChatMessageHistory):
    """Chat history stored in a list."""

    session_id: str
    dir: str

    def __init__(self, fields: JSONChatHistoryInput = None) -> None:
        """Initialize with no messages."""
        self.session_id = fields.session_id
        self.dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../', fields.dir if hasattr(fields, 'dir') and fields.dir is not None else 'chat_data'))

    async def get_messages(self) -> List[BaseMessage]:
        file_path = os.path.join(self.dir, f"{self.session_id}.json")
        try:
            if not os.path.exists(file_path):
                await self.save_messages_to_file([])
                return []
            with open(file_path, 'r', encoding='utf-8') as f:
                data = f.read()
            stored_messages = json.loads(data)
            return self.map_stored_messages_to_chat_messages(stored_messages)
        except Exception as error:
            print(f"Failed to read chat history from {file_path}", error)
            return []

    
    async def save_messages_to_file(messages: BaseMessage = []):
        print('save')