import asyncio
from typing import Callable, Dict, List, Any
from datetime import datetime
import json
import logging

logger = logging.getLogger("ai7.event_bus")

class EventBus:
    """
    Central event-driven bus for the AI7 Multi-Agent Career Operating System.
    Enables reactive execution without polling loops.
    """
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._event_history: List[Dict[str, Any]] = []

    def subscribe(self, event_type: str, handler: Callable):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)
        logger.info(f"Subscribed handler {handler.__name__} to event {event_type}")

    async def publish(self, event_type: str, payload: Dict[str, Any]):
        event_record = {
            "event_type": event_type,
            "payload": payload,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        self._event_history.append(event_record)
        logger.info(f"Event published: {event_type}")

        handlers = self._subscribers.get(event_type, [])
        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    asyncio.create_task(handler(payload))
                else:
                    handler(payload)
            except Exception as e:
                logger.error(f"Error executing handler {handler} for {event_type}: {e}")

    def get_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        return self._event_history[-limit:]

# Singleton instance
event_bus = EventBus()
