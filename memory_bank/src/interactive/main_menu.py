
from datetime import datetime, timedelta
from interactive_menu.src.interactive_menu import InteractiveMenu


class MainMenu(InteractiveMenu):

    def __init__(self, manager, path=[]):
        super().__init__(manager, path)
        self.sub_menu_modules = [
            RecordMemoryMenu(manager, self.path),
            ReadMemoriesMenu(manager, self.path)
        ]

    def title(self):
        return "Main"


class RecordMemoryMenu(InteractiveMenu):

    def title(self):
        return "Record"

    def main_loop(self):
        print("What is the memory?")
        answer = self.fancy_input()
        self.manager.record_memory(answer)


class ReadMemoriesMenu(InteractiveMenu):

    def __init__(self, manager, path):
        super().__init__(manager, path)
        self.sub_menu_modules = [
            ReadTodaysMemoriesMenu(manager, self.path),
            ReadYesterdaysMemoriesMenu(manager, self.path),
            ReadDatesMemoriesMenu(manager, self.path)
        ]

    def title(self):
        return "Remember"

class ReadTodaysMemoriesMenu(InteractiveMenu):

    def title(self):
        return "Today"

    def main_loop(self):
        date = datetime.now().strftime("%Y-%m-%d")
        memories = self.manager.get_memories(date)
        for memory in memories:
            print(memory)

class ReadYesterdaysMemoriesMenu(InteractiveMenu):

    def title(self):
        return "Yesterday"

    def main_loop(self):
        date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        memories = self.manager.get_memories(date)
        for memory in memories:
            print(memory)

class ReadDatesMemoriesMenu(InteractiveMenu):

    def title(self):
        return "Date"

    def main_loop(self):

        print("For what date (YYYY-MM-DD)?")
        date = self.fancy_input()

        memories = self.manager.get_memories(date)
        for memory in memories:
            print(memory)
