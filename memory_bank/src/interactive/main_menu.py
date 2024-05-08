
from datetime import datetime, timedelta
from interactive_menu.src.interactive_menu import InteractiveMenu

def print_memories(memories):
    for memory in memories:
        memory_text = memory[1]
        memory_hour = memory[2]
        am_pm = "AM"
        if memory_hour is not None and memory_hour > 12:
            memory_hour = memory_hour % 12
            am_pm = "PM"
        memory_minute = memory[3]
        if memory_hour is None and memory_minute is None:
            print("\t          > %s" % memory_text)
        elif memory_hour is None and memory_minute is not None:
            raise Exception("Minute should not be without an hour")
        elif memory_hour is not None and memory_minute is None:
            print("\t %s    %s > %s" % (memory_hour, am_pm, memory_text))
        else:
            print("\t %s:%s %s  > %s" % (memory_hour, memory_minute, am_pm, memory_text))

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
                },
                {
                    "question": "What time did this occur? (HH:MM in military time) Hit enter to skip",
                    "expected_response_type": "HHMM_Time",
                    "return_as": "time",
                    "default": None,
                    "allow_empty": True
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
        time = form_results["time"]["value"] if "time" in form_results else None
        if time is not None:
            hour, minute = time.split(':')
        else:
            hour = None
            minute = None
        self.manager.record_memory(memory, date, hour, minute)

class ReadMemoriesMenu(InteractiveMenu):

    def __init__(self, manager, path):
        super().__init__(manager, path)
        self.sub_menu_modules = [
            ReadTodaysMemoriesMenu(manager, self.path),
            ReadYesterdaysMemoriesMenu(manager, self.path),
            ReadWeekMemoriesMenu(manager, self.path),
            ReadDatesMemoriesMenu(manager, self.path),
            KeywordSearchMenu(manager, self.path)
        ]

    def title(self):
        return "Remember"

class ReadTodaysMemoriesMenu(InteractiveMenu):

    def title(self):
        return "Today"

    def main_loop(self):
        date = datetime.now()
        date_str = date.strftime("%Y-%m-%d")
        print("")
        print(date_str)
        memories = self.manager.get_memories(date_str)
        print_memories(memories)
        print("")

class ReadYesterdaysMemoriesMenu(InteractiveMenu):

    def title(self):
        return "Yesterday"

    def main_loop(self):
        date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        print("")
        print(date)
        memories = self.manager.get_memories(date)
        print_memories(memories)
        print("")

class ReadWeekMemoriesMenu(InteractiveMenu):

    def title(self):
        return "Week"

    def print_prior_week_memories(self):
        # Get today's date
        today = datetime.now()

        seven_days_ago = today - timedelta(days=7)

        # Print out the date range for the prior week
        print(f"Memories from {seven_days_ago.strftime('%Y-%m-%d')} to {today.strftime('%Y-%m-%d')}\n")

        # Get memories for all of last week
        for i in range(8):
            date = seven_days_ago + timedelta(days=i)
            memories = self.manager.get_memories(date.strftime("%Y-%m-%d"))
            print(date.strftime("%A: %Y-%m-%d"))
            print_memories(memories)
            print("\n")

    def main_loop(self):
        self.print_prior_week_memories()

class ReadDatesMemoriesMenu(InteractiveMenu):

    def title(self):
        return "Date"

    def main_loop(self):

        print("For what date (YYYY-MM-DD)?")
        date = self.fancy_input()
        print("")
        print(date)

        memories = self.manager.get_memories(date)
        print_memories(memories)
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
