from RagModel.utils.load_config import LoadConfig

class QueryRefiner:
    """
    Refines user questions using conversation history,
    so that follow-up queries become self-contained.
    """

    def __init__(self, llm,refiner_prompt: str ):
        self.config = LoadConfig()
        self.llm = llm
        self.refiner_prompt = refiner_prompt


    def refine(self, user_query: str, history: str) -> str:
        """
        Returns a rewritten version of the user query,
        adding missing context from chat history if needed.
        """
        if not history.strip():
            return user_query  # No history to consider
        prompt = self.refiner_prompt.format(
            history=history,
            user_query=user_query
        )
        refined = self.llm.invoke(prompt)
        return refined.content.strip()
