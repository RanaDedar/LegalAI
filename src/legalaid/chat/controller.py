from datetime import datetime
from openai import OpenAIError
from sqlalchemy.orm import Session
from legalaid.agent.agentix import get_response
from legalaid.chat.dtos import Querry_Schema
from legalaid.chat.models import ChatMessage, ChatSession
def _chat_fragment(prompt: str, answer: str, agent_label: str) -> str:
    return f"""
    <div class="user-msg">
        <strong>You:</strong> {prompt}
    </div>
    <div class="agent-msg" style="border-left: 2px solid #c5a059; padding-left: 10px; margin-top: 10px;">
        <strong>{agent_label}:</strong> {answer}
    </div>
    """
async def ask_agent(query: Querry_Schema, db: Session):
    try:
        answer, ag_name = await get_response(query.prompt)
    except OpenAIError as exc:
        return _chat_fragment(
            query.prompt,
            str(exc),
            "System",
        )
    session = db.query(ChatSession).filter(ChatSession.uid == query.uid).first()
    if not session:
        new_ses = ChatSession(uid=query.uid, timestamp=datetime.now())
        db.add(new_ses)
        db.commit()
        db.refresh(new_ses)
        session = new_ses
    user_query = ChatMessage(sid=session.id, role="user", content=query.prompt)
    agent_response = ChatMessage(sid=session.id, role="agent", content=answer)
    db.add_all([user_query, agent_response])
    db.commit()
    return _chat_fragment(query.prompt, answer, ag_name)
    