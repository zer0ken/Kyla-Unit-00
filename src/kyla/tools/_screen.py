import base64
import os
from datetime import datetime
from PIL import ImageGrab
from langchain_core.tools import tool


def get_screenshot_file_name(file_name=None):
    if file_name is None:
        return f'resources/screenshots/{datetime.now().strftime("%Y년 %m월 %d일 %H시 %M분 %S초")}.png'
    else:
        return f'resources/screenshots/{file_name}'

@tool
def take_screenshot():
    """
    현재 화면 전체를 캡처하고 이미지 파일로 저장합니다.
    저장된 파일의 이름을 반환합니다.
    """
    try:
        os.makedirs('resources/screenshots', exist_ok=True)
        screenshot = ImageGrab.grab(bbox=None, include_layered_windows=False, all_screens=True)
        i = screenshot.size   # current size (height,width)
        i = i[0]//4, i[1]//4  # new size
        screenshot = screenshot.resize(i)
        file = get_screenshot_file_name()
        screenshot.save(file)
    except Exception as e:
        return f'캡처 실패: {e}'
    return file


@tool
def list_screenshots():
    """
    지금까지 캡쳐한 이미지의 파일 이름 목록을 반환합니다.
    """
    return [get_screenshot_file_name(file) for file in os.listdir('resources/screenshots') if file.endswith('.png')]

@tool
def analyze_screenshot(file_name: str):
    """
    스크린샷을 관찰하고 내용을 분석해 설명합니다.
    `take_screenshot` 도구를 사용해 스크린샷을 캡처하고, 이 도구를 사용해 스크린샷을 해석해보세요.
    화면 전체에 무엇이 보이는지, 특정 부분에 무엇이 보이는지 적절히 집중하며 분석하세요.

    Args:
        file_name: 스크린샷 파일의 정확한 이름.
    """
    try:
        image_data = base64.b64encode(open(file_name, 'rb').read()).decode('utf-8')
        return f'data:image/png;base64,{image_data}'
    except Exception as e:
        return f'오류 발생: {e}'


tools = [take_screenshot, list_screenshots, analyze_screenshot]
