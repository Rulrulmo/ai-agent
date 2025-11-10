import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# cred = credentials.Certificate("path/to/serviceAccountKey.json")
# firebase_admin.initialize_app(cred)

class FirebaseDB:

    def __init__(self):
        cred = credentials.Certificate("firebase_keys.json")
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        self.collection_name = "conversations"

    def save_conversation(self, user_message: str, bot_message: str):
        doc_data = {
            "user_message": user_message,
            "bot_message": bot_message,
            "timestamp": datetime.now()
        }

        self.db.collection(self.collection_name).add(doc_data)

    def get_conversation_context(self, limit: int = 10):
        docs = self.db.collection(self.collection_name)\
            .order_by("timestamp", direction=firestore.Query.DESCENDING)\
            .limit(limit)\
            .get()

        if not docs:
            return ""

        context = "=== 최근 대화 기록 ===\n"
        for i, doc in enumerate(reversed(docs), 1):
            data = doc.to_dict()
            context += f"{i}. 사용자: {data.get('user_message', '')}\n"
            context += f"     봇: {data.get('bot_message', '')}\n\n"

        return context


db = FirebaseDB()

def add_to_conversation(user_message: str, bot_message: str):
    db.save_conversation(user_message, bot_message)

def get_conversation_context():
    return db.get_conversation_context()
