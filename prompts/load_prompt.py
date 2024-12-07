def load_prompt(prompt_name: str) -> str:
    with open(f'prompts/{prompt_name}.md', 'r', encoding='utf-8') as file:
        return file.read().strip()

