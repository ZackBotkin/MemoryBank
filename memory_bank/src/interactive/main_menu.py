
from datetime import datetime, timedelta
from interactive_menu.src.interactive_menu import InteractiveMenu


class MainMenu(InteractiveMenu):

    def __init__(self, manager, path=[]):
        super().__init__(manager, path)
        self.sub_menu_modules = [
            RecordMemoryMenu(manager, self.path),
            ReadMemoriesMenu(manager, self.path),
            RemoveMemoryMenu(manager, self.path)
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
            ReadDatesMemoriesMenu(manager, self.path),
            KeywordSearchMenu(manager, self.path)
        ]

    def title(self):
        return "Remember"

class ReadTodaysMemoriesMenu(InteractiveMenu):

    def title(self):
        return "Today"

    def main_loop(self):
        date = datetime.now().strftime("%Y-%m-%d")
        print("")
        print(date)
        memories = self.manager.get_memories(date)
        for memory in memories:
            print("\t > %s" % memory[1])
        print("")

class ReadYesterdaysMemoriesMenu(InteractiveMenu):

    def title(self):
        return "Yesterday"

    def main_loop(self):
        date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        print("")
        print(date)
        memories = self.manager.get_memories(date)
        for memory in memories:
            print("\t > %s" % memory[1])
        print("")

class ReadDatesMemoriesMenu(InteractiveMenu):

    def title(self):
        return "Date"

    def main_loop(self):

        print("For what date (YYYY-MM-DD)?")
        date = self.fancy_input()
        print("")
        print(date)

        memories = self.manager.get_memories(date)
        for memory in memories:
            print("\t > %s" % memory[1])
        print("")

class RemoveMemoryMenu(InteractiveMenu):

    def title(self):
        return "Remove"

    def main_loop(self):

        print("For what date (YYYY-MM-DD)")
        date = self.fancy_input()

        print("Which text")
        text = self.fancy_input()

        print("%s\n%s\nOK?" % (date, text))
        answer = self.fancy_input()
        if answer in ["yes", "Yes", "ok", "OK"]:
            self.manager.delete_memory(date, text)

class KeywordSearchMenu(InteractiveMenu):

    def title(self):
        return "Search"

    def main_loop(self):
        print("Search term?")
        term = self.fancy_input()
        results = self.manager.keyword_search(term)
        if len(results.keys()) > 0:
            print("")
        for date, memories in results.items():
            print(date)
            for memory in memories:
                print("\t > %s" % memory)
        if len(results.keys()) > 0:
            print("")
