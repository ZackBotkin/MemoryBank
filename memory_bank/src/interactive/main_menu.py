
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
        form_results = self.interactive_form(
            [
                {
                    "question": "What is the memory?",
                    "expected_response_type": "VARCHAR",
                    "return_as": "memory",
                    "default": "",
                    "allow_empty": False
                },
                {
                    "question": "When did this occur? (YYYY-MM-DD) Hit enter for today",
                    "expected_response_type": "YYYYMMDD_Date",
                    "return_as": "date",
                    "default": datetime.now().strftime("%Y-%m-%d"),
                    "allow_empty": False
                }
            ]
        )
        if form_results["user_accept"] != True:
            print("Aborting!")
            return
        form_results.pop("user_accept")
        for answer_key in form_results.keys():
            if not form_results[answer_key]["valid"]:
                print("%s is not a valid value! Aborting" % answer_key)
                return
        memory = form_results["memory"]["value"]
        date = form_results["date"]["value"]
        self.manager.record_memory(memory, date)

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
        if len(results.keys()) == 0:
            print("")
            print("No memories containing the term(s) \"%s\"" % term)
            print("")
        for date, memories in results.items():
            print(date)
            print("")
            for memory in memories:
                print("\t > %s" % memory)
            print("")
