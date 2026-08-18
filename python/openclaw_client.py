import json
import subprocess
import tempfile
from pathlib import Path
from prompt_manager import PromptManager

class OpenClawClient:

    def __init__(self):
        self.openclaw_dir = Path(r"D:\auto_ai_task\openclaw")
        self.prompt_manager = PromptManager()

    def analyze(self, user_msg: str) -> dict:
        # 读取并渲染意图分析 Prompt
        prompt = self.prompt_manager.render(
            "intent_classifier",
            USER_MESSAGE=user_msg
        )
        # 创建临时 Prompt 文件
        prompt_file = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                suffix=".txt",
                delete=False
            ) as f:
                f.write(prompt)
                prompt_file = Path(f.name)
            # 调用 OpenClaw
            result = subprocess.run(
                [
                    "pnpm.cmd",
                    "openclaw",
                    "agent",
                    "--message-file",
                    str(prompt_file.resolve()),
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                cwd=self.openclaw_dir,
                timeout=600,
            )
            if result.returncode != 0:
                raise RuntimeError(
                    f"OpenClaw 调用失败：\n{result.stderr}"
                )
            response = result.stdout.strip()
            print("===== OpenClaw 原始返回 =====")
            print(response)
            # 提取 JSON
            start = response.find("{")
            end = response.rfind("}")
            if start == -1 or end == -1:
                raise ValueError(
                    f"OpenClaw 没有返回有效 JSON：\n{response}"
                )
            json_text = response[start:end + 1]
            try:
                return json.loads(json_text)
            except json.JSONDecodeError as e:
                raise ValueError(
                    f"OpenClaw 返回的内容不是有效 JSON：\n{json_text}"
                ) from e
        finally:
            # 删除运行时临时文件
            if prompt_file and prompt_file.exists():
                prompt_file.unlink()