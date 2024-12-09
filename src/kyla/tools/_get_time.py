from datetime import datetime
from langchain_core.tools import tool

awaken = datetime.now()


@tool
def get_time() -> dict:
    """
    프로그램의 시작 시간, 실행된 시간, 현재 시각을 반환합니다.
    마치 시계처럼 항상 정확한 시간을 알려줍니다.
    """
    now = datetime.now()
    return {
        'awaken': awaken,
        'uptime': now - awaken,
        'now': now.strftime('%Y-%m-%d %H:%M:%S')
    }


tools = [get_time]
