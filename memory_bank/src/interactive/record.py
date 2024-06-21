from datetime import datetime, timedelta
from interactive_menu.src.interactive_menu import InteractiveMenu


class RecordMenu(InteractiveMenu):

    def __init__(self, manager, path=[]):
        super().__init__(manager, path)
        self.sub_menu_modules = [
            RecordMemoryMenu(manager, self.path),
            RecordThoughtMenu(manager, self.path)
        ]

    def title(self):
        return "Record"


class RecordMemoryMenu(InteractiveMenu):

    def title(self):
        return "Memory"

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

class RecordThoughtMenu(InteractiveMenu):

    def title(self):
        return "Thought"

    def main_loop(self):
        form_results = self.interactive_form(
            [
                {
                    "question": "What are your thoughts?",
                    "expected_response_type": "VARCHAR",
                    "return_as": "thought",
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
        thought = form_results["thought"]["value"]
        date = form_results["date"]["value"]
        self.manager.record_thought(thought, date)
