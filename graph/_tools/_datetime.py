from datetime import datetime

awaken = datetime.now()


def get_time() -> dict:
    """
    프로그램의 시작 시간, 실행된 시간, 현재 시각을 반환합니다.
    """
    now = datetime.now()
    return {
        'awaken': awaken,
        'uptime': now - awaken,
        'now': now.strftime('%Y-%m-%d %H:%M:%S')
    }


tools = [get_time]
