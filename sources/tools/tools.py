
"""
define a generic tool class, any tool can be used by the agent.

A tool can be used by deepseek like so:
```<tool name>
<code or query to execute>
```

For example:
```python
print("Hello world")
```

This is then executed by the tool with its own class implementation of execute().

A tool is not just for code tool but also API, internet, etc..
For example a flight API tool could be used like so:
```flight_search
HU787
```
"""

import sys
from abc import abstractmethod

sys.path.append('..')

class Tools():
    """
    Abstract class for all tools.
    """
    def __init__(self):
        self.tag = "undefined"
        self.api_key = None
        self.client = None
        self.messages = []

    @abstractmethod
    def execute(self, codes:str, safety:bool) -> str:
        """
        abstract method, implementation in child class.
        """
        pass

    @abstractmethod
    def execution_failure_check(self, output:str) -> bool:
        """
        abstract method, implementation in child class.
        """
        pass

    @abstractmethod
    def interpreter_feedback(self, output:str) -> str:
        """
        abstract method, implementation in child class.
        """
        pass

    def remove_block(self, text:str) -> str:
        """
        Remove all code/query blocks within a tag from the answer text.
        """
        assert self.tag != "undefined", "Tag not defined"
        start_tag = f'```{self.tag}' 
        end_tag = '```' 
        start_idx = text.find(start_tag)
        end_idx = text.rfind(end_tag)+3
        if start_idx == -1 or end_idx == -1:
            return text
        return text[:start_idx] + text[end_idx:]

    def load_exec_block(self, generation: str) -> str:
        """
        Extract the code/query blocks from the answer text, removing consistent leading whitespace.
        """
        assert self.tag != "undefined", "Tag not defined"
        start_tag = f'```{self.tag}' 
        end_tag = '```'
        code_blocks = []
        start_index = 0

        if start_tag not in generation:
            return None

        while True:
            start_pos = generation.find(start_tag, start_index)
            if start_pos == -1:
                break

            line_start = generation.rfind('\n', 0, start_pos) + 1
            if line_start == 0:
                line_start = 0
            leading_whitespace = generation[line_start:start_pos]

            end_pos = generation.find(end_tag, start_pos + len(start_tag))
            if end_pos == -1:
                break
            content = generation[start_pos + len(start_tag):end_pos]
            lines = content.split('\n')
            if leading_whitespace:
                processed_lines = []
                for line in lines:
                    if line.startswith(leading_whitespace):
                        processed_lines.append(line[len(leading_whitespace):])
                    else:
                        processed_lines.append(line)
                content = '\n'.join(processed_lines)

            code_blocks.append(content)
            start_index = end_pos + len(end_tag)

        return code_blocks