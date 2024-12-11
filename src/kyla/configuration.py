"""Define the configurable parameters for the agent."""

from __future__ import annotations

from dataclasses import dataclass, fields, field
from typing import Optional

from langchain_core.runnables import RunnableConfig

from src.kyla.prompts.prompt_loader import load_prompt


@dataclass(kw_only=True)
class KylaConfiguration:
    """The configuration for the agent."""

    user_name: str = field(
        default='제로켄',
        metadata={
            'description': '사용자의 식별자(이름)'
        },
    )
    system_instruction: str = field(
        default=load_prompt('system'),
        metadata={
            'description': '시스템 지시사항'
        },
    )
    message_instruction: str = field(
        default=load_prompt('message'),
        metadata={
            'description': '메시지 지시사항'
        },
    )
    context_instruction: str = field(
        default=load_prompt('context'),
        metadata={
            'description': '맥락 지시사항'
        },
    )
    load_db_instruction: str = field(
        default=load_prompt('load_db'),
        metadata={
            'description': '데이터베이스 로드 지시사항'
        },
    )
    save_db_instruction: str = field(
        default=load_prompt('save_db'),
        metadata={
            'description': '데이터베이스 저장 지시사항'
        },
    )
    after_tool_instruction: str = field(
        default=load_prompt('after_tool'),
        metadata={
            'description': '도구 사용 후 지시사항'
        },
    )


    @classmethod
    def from_runnable_config(
        cls, config: Optional[RunnableConfig] = None
    ) -> KylaConfiguration:
        """Create a Configuration instance from a RunnableConfig object."""
        configurable = (config.get("configurable") or {}) if config else {}
        _fields = {f.name for f in fields(cls) if f.init}
        return cls(**{k: v for k, v in configurable.items() if k in _fields})
