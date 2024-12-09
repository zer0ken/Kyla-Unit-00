from typing import Any, Optional
from pydantic import BaseModel, Field
from langchain_core.tools import tool

from src.neo4j_db import Neo4jDBManager

neo4j_db = Neo4jDBManager()


class MemorizeObjectInput(BaseModel):
    """
    중요한 무언가를 기억하기 위해 일기를 적듯이 이 도구를 사용하세요.
    이 도구는 요청을 받지 않더라도 원한다면 언제든지 스스로 판단하여 사용할 수 있습니다.
    사물, 사람, 사건, 장소, 개념 등의 정보를 기억하기 위해 데이터베이스에 저장합니다.
    """
    class_: str = Field(
        ...,
        description="기억할 대상의 종류. "
                    "파스칼 케이스로 작성하는 것이 권장됩니다. "
                    "예를 들어, 사물은 'Object', 사람(인격체)은 'Person', 사건은 'Event', 장소는 'Place', 개념은 'Concept'와 같은 문자열로 나타냅니다. "
    )
    name: str = Field(
        ...,
        description="기억할 대상의 이름(고유명). "
                    "예를 들어 '카일라', '제로켄'과 같은 인물명이나 '가위', '숟가락' 등의 보편적인 사물의 이름이 여기에 들어갑니다."
    )
    additional_classes: Optional[list[str]] = Field(
        default_factory=list,
        description="기억할 대상의 추가 종류가 담긴 리스트."
    )
    properties: Optional[dict[str, Any]] = Field(
        default_factory=dict,
        description="기억할 대상의 이름을 제외한 속성이 담긴 딕셔너리. "
                    "예를 들어, 생일은 'birthday', 사물의 종류는 'type'과 같은 문자열 키로 저장합니다. "
                    "사람의 나이에 관한 정보는 되도록이면 현재 나이인 'age'보다는 출생 년도와 일자를 'birthday'로 저장하세요. "
    )


@tool
def memorize_object(class_: str, name: str, additional_classes: list[str] = []) -> str:
    """
    중요한 무언가를 기억하기 위해 일기를 적듯이 이 도구를 사용하세요.
    이 도구는 요청을 받지 않더라도 원한다면 언제든지 스스로 판단하여 사용할 수 있습니다.
    사물, 사람, 사건, 장소, 개념 등의 정보를 기억하기 위해 데이터베이스에 저장합니다.

    Args:
        class_: 기억할 대상의 종류. 파스칼 케이스로 작성하는 것이 권장됩니다. 예를 들어, 사물은 'Object', 사람(인격체)은 'Person', 사건은 'Event', 장소는 'Place', 개념은 'Concept'와 같은 문자열로 나타냅니다.
        name: 기억할 대상의 이름(고유명). 한국어로 적을 것이 권장됩니다.
        additional_classes: 기억할 대상의 추가 종류가 담긴 리스트.
    """
    try:
        neo4j_db.create_nodes([class_, *additional_classes], {'name': name})
    except Exception as e:
        return f"데이터베이스에 정보를 저장하는 데 실패했습니다. 오류 메시지: {e}"

    return "데이터베이스에 정보가 저장되었습니다."


tools = [memorize_object]
