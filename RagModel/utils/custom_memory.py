class SummaryMemory:
    def __init__(self, llm, max_turns=6):
        self.llm = llm
        self.max_turns = max_turns
        self.history = []

    def get_chat_history(self):
        if len(self.history) <= self.max_turns:
            return "\n".join(self.history)

        # summarize older messages
        to_summarize = "\n".join(self.history[:-self.max_turns])
        summary = self.llm.invoke(f"Summarize this conversation:\n\n{to_summarize}").content
        
        recent = "\n".join(self.history[-self.max_turns:])

        return summary + "\n\n" + recent

    def save(self, user, bot):
        self.history.append(f"User: {user}")
        self.history.append(f"AI: {bot}")
