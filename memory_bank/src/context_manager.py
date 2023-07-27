from memory_bank.src.io.query_runner import QueryRunner


class ContextManager(object):

    def __init__(self, configs):
        self.config = configs
        self.query_runner = QueryRunner(configs)
        self.query_runner.create_all_tables()

    def record_memory(self, memory_text):
        self.query_runner.insert_memory(memory_text)

    def get_memories(self):
        memories = self.query_runner.get_memories()
        return memories
