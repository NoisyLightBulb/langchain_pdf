from langchain_core.messages import BaseMessage
from pydantic import BaseModel
from langchain.memory import ConversationBufferMemory
from langchain.schema import BaseChatMessageHistory

from app.web.api import get_messages_by_conversation_id, add_message_to_conversation

class SqlMessageHistory(BaseChatMessageHistory, BaseModel):
    converstation_id: str

    @property
    def messages(self):
        return get_messages_by_conversation_id(self.converstation_id)

    def add_message(self, message):
        return add_message_to_conversation(
            conversation_id = self.converstation_id,
            role = message.type,
            content = message.content
        )

    def clear(self):
        pass

def build_memory(chat_args):
    return ConversationBufferMemory(
        chat_memory = SqlMessageHistory(converstation_id = chat_args.conversation_id),
        return_messages = True,
        memory_key = "chat_history",
        output_key = "answer"
    )
