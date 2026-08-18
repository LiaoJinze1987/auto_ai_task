from pathlib import Path

class PromptManager:

    def __init__(self):
        self.prompt_dir = Path(__file__).parent / "prompts"

    def load(self, prompt_name: str) -> str:
        prompt_file = self.prompt_dir / f"{prompt_name}.txt"
        if not prompt_file.exists():
            raise FileNotFoundError(
                f"Prompt 不存在: {prompt_file}"
            )
        return prompt_file.read_text(encoding="utf-8")

    def render(self, prompt_name: str, **kwargs) -> str:
        template = self.load(prompt_name)
        try:
            return template.format(**kwargs)
        except KeyError as e:
            raise ValueError(
                f"Prompt 缺少参数: {e}"
            ) from e