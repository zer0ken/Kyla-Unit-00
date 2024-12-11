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
    data = {
        'awaken': '%Y-%m-%d %H시 %M분%S초'.format(awaken),
        'uptime': '%H시간 %M분 %S초'.format(now - awaken),
        'now': '%Y-%m-%d %H시 %M분 %S초'.format(now)
    }
    return f'이번 세션 시작 시간: {data["awaken"]}\n프로그램 실행 시간: {data["uptime"]}\n현재 시간: {data["now"]}', data


tools = [get_time]
