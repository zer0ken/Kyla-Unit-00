def weather_tool(location: str) -> str:
    """
    특정 지역의 날씨를 알려주는 도구입니다.
    """
    return {"weather": f'{location}의 날씨는 맑습니다.'}


tools = [weather_tool]