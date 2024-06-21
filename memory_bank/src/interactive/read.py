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

def print_thoughts(thoughts):
    for thought in thoughts:
        thought_date = thought[0]
        thought_description = thought[1]
        print("\t          > %s" % thought_description)

def print_memories_and_thoughts(memories, thoughts):
    if len(memories) > 0:
        print("")
        print("************")
        print("* Memories *")
        print("************")
        print_memories(memories)
    if len(thoughts) > 0:
        print("")
        print("************")
        print("* Thoughts *")
        print("************")
        print_thoughts(thoughts)
        print("")
    else:
        print("")

import calendar
import tkinter as tk

def show_calendar(year, month):
    # Create a calendar instance
    cal = calendar.monthcalendar(year, month)

    # Create a Tkinter window
    root = tk.Tk()
    root.title(f"Calendar - {calendar.month_name[month]} {year}")

    # Create a label for the month and year
    label = tk.Label(root, text=f"{calendar.month_name[month]} {year}", font=("Helvetica", 16))
    label.pack()

    # Create a frame to hold the calendar
    frame = tk.Frame(root)
    frame.pack()

    # Create labels for each day in the calendar
    for week in cal:
        for day in week:
            if day == 0:
                tk.Label(frame, text="   ", width=4).pack(side=tk.LEFT)
            else:
                tk.Label(frame, text=f"{day:2}", width=4).pack(side=tk.LEFT)

    root.mainloop()

class ReadMemoriesMenu(InteractiveMenu):

    def __init__(self, manager, path):
        super().__init__(manager, path)
        self.sub_menu_modules = [
            ReadTodaysMemoriesMenu(manager, self.path),
            ReadYesterdaysMemoriesMenu(manager, self.path),
            ReadWeekMemoriesMenu(manager, self.path),
            ReadCalendarMemoriesMenu(manager, self.path),
            ReadDatesMemoriesMenu(manager, self.path),
            KeywordSearchMenu(manager, self.path)
        ]

    def title(self):
        return "Read"

class ReadTodaysMemoriesMenu(InteractiveMenu):

    def title(self):
        return "Today"

    def main_loop(self):
        date = datetime.now()
        date_str = date.strftime("%Y-%m-%d")
        print("")
        print(date_str)
        memories = self.manager.get_memories(date_str)
        thoughts = self.manager.get_thoughts(date_str)
        print_memories_and_thoughts(memories, thoughts)
        print("")

class ReadYesterdaysMemoriesMenu(InteractiveMenu):

    def title(self):
        return "Yesterday"

    def main_loop(self):
        date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        print("")
        print(date)
        memories = self.manager.get_memories(date)
        thoughts = self.manager.get_thoughts(date)
        print_memories_and_thoughts(memories, thoughts)
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
            thoughts = self.manager.get_thoughts(date.strftime("%Y-%m-%d"))
            print(date.strftime("%A: %Y-%m-%d"))
            print_memories_and_thoughts(memories, thoughts)
            print("\n")

    def main_loop(self):
        self.print_prior_week_memories()

class ReadCalendarMemoriesMenu(InteractiveMenu):

    def title(self):
        return "Calendar"

    def main_loop(self):
        today = datetime.now()
        year = today.year
        month = today.month
        show_calendar(year, month)

class ReadDatesMemoriesMenu(InteractiveMenu):

    def title(self):
        return "Date"

    def main_loop(self):

        print("For what date (YYYY-MM-DD)?")
        date = self.fancy_input()
        print("")
        print(date)

        memories = self.manager.get_memories(date)
        thoughts = self.manager.get_thoughts(date)
        print_memories_and_thoughts(memories, thoughts)
        print("")

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
