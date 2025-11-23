from RagModel.utils.load_config import LoadConfig
from RagModel.utils.db_manager import VectorDBManager
from RagModel.utils.custom_memory import SummaryMemory
from RagModel.utils.query_refiner import QueryRefiner


class ModelInvoker:
    def __init__(self):
        self.config = LoadConfig()
        self.llm = self.config.llm
        self.db = VectorDBManager()
        self.prompt_template = self.config.main_prompt
        self.refiner_prompt = self.config.refiner_prompt

        # Memory to enable follow-ups
        self.memory = SummaryMemory(llm=self.llm)

        # Query refiner to handle vague / follow-up questions
        self.refiner = QueryRefiner(llm=self.llm,refiner_prompt=self.refiner_prompt)


    def query(self, user_prompt: str, k: int = 4) -> str:

        print("-----USER PROMPT-----")
        print(user_prompt)
        # Step 1: load conversation history
        history = self.memory.get_chat_history()
        print("-----CHAT HISTORY-----")
        print(history)
        print("-----END CHAT HISTORY-----")
        # Step 2: rewrite the question (only for DB retrieval)
        refined_query = self.refiner.refine(user_prompt, history)
        print("-----REFINED QUERY-----")
        print(refined_query)
        # Step 3: retrieve relevant chunks via refined query
        results = self.db.query(refined_query, k=k)
        print("-----RETRIEVED CHUNKS-----")
        for r in results:
            print(r.page_content)
            print("-----END CHUNK-----")
        context = "\n\n".join([r.page_content for r in results]) if results else ""

        # Step 4: construct final prompt using original question
        prompt = self.prompt_template.format(
            chat_history=history,
            context=context,
            question=user_prompt
        )

        print("-----FINAL PROMPT TO LLM-----")
        print(prompt)
        # Step 5: final LLM answer
        response = self.llm.invoke(prompt)
        print("-----LLM RESPONSE OBJECT-----")
        print(response)
        answer = response.content.strip()

        # Step 6: store talk for follow-ups
        self.memory.save(user_prompt, answer)

        return answer

