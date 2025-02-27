
from sources.tools import PyInterpreter, BashInterpreter
from sources.utility import pretty_print
from sources.agent import Agent

class CoderAgent(Agent):
    def __init__(self, model, name, prompt_path, provider):
        super().__init__(model, name, prompt_path, provider)
        self._tools = {
            "bash": BashInterpreter(),
            "python": PyInterpreter()
        }

    def remove_blocks(self, text: str) -> str:
        """
        Remove all code/query blocks within a tag from the answer text.
        """
        tag = f'```'
        lines = text.split('\n')
        post_lines = []
        in_block = False
        for line in lines:
            if tag in line and not in_block:
                in_block = True
                continue
            if not in_block:
                post_lines.append(line)
            if tag in line:
                in_block = False
        return "\n".join(post_lines)

    def answer(self, prompt, speech_module) -> str:
        answer = ""
        attempt = 0
        max_attempts = 3
        self._history.push('user', prompt)

        while attempt < max_attempts:
            pretty_print("Thinking...", color="status")
            self.wait_message(speech_module)
            answer, reasoning = self.llm_request()
            exec_success, feedback = self.execute_modules(answer)
            pretty_print(feedback, color="failure" if "failure" in feedback.lower() else "success")
            answer = self.remove_blocks(answer)
            pretty_print(answer, color="output")
            if exec_success:
                break
            attempt += 1

        return answer, reasoning

if __name__ == "__main__":
    from llm_provider import Provider

    #local_provider = Provider("ollama", "deepseek-r1:14b", None)
    server_provider = Provider("server", "deepseek-r1:14b", "192.168.1.100:5000")
    agent = CoderAgent("deepseek-r1:14b", "jarvis", "prompts/coder_agent.txt", server_provider)
    ans = agent.answer("What is the output of 5+5 in python ?")
    print(ans)