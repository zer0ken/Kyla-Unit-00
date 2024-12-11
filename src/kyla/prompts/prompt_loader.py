import os


def load_prompt(prompt_name: str) -> str:
    with open(os.path.join(f'{os.path.dirname(__file__)}', f'{prompt_name}.md'), 'r', encoding='utf-8') as file:
        return file.read().strip()


__all__ = ['load_prompt']
