from memory_bank.src.io.query_runner import QueryRunner


class ContextManager(object):

    def __init__(self, configs):
        self.config = configs
        self.query_runner = QueryRunner(configs)
        self.query_runner.create_all_tables()

    def record_memory(self, memory_text, date=None, hour=None, minute=None):
        self.query_runner.insert_memory(memory_text, date, hour, minute)

    def record_thought(self, thought_text, date=None):
        self.query_runner.insert_thought(thought_text, date)

    def get_memories(self, date=None):
        memories = self.query_runner.get_memories(date)
        return memories

    def get_thoughts(self, date=None):
        thoughts = self.query_runner.get_thoughts(date)
        return thoughts

    def keyword_search(self, term):
        memories = self.query_runner.get_memories_matching_search(term)
        seen_memories = {}
        for memory in memories:
            date = memory[0]
            text = memory[1]
            if date not in seen_memories:
                seen_memories[date] = []
            seen_memories[date].append(text)
        return seen_memories
