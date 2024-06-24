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

class ToolTip:
    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.id = None
        self.x = self.y = 0
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(500, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x, y, _cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + cy + self.widget.winfo_rooty() + 25
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack()

    def hidetip(self):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()

def show_calendar(year, month, memories, thoughts):
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

    # Create labels for the days of the week
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i, day in enumerate(days):
        tk.Label(frame, text=day, width=4).grid(row=0, column=i)

    memories_data = {}
    for memory in memories:
        date_str = memory[0]
        memory_text = memory[1]
        date = datetime.strptime(date_str, "%Y-%m-%d")
        if date.year == year and date.month == month:
            if date.day not in memories_data:
                memories_data[date.day] = []
            memories_data[date.day].append(memory_text)

    # Create labels for each day in the calendar
    for week_idx, week in enumerate(cal):
        for day_idx, day in enumerate(week):
            if day == 0:
                tk.Label(frame, text="   ", width=4).grid(row=week_idx + 1, column=day_idx)
            else:
                date_label = tk.Label(frame, text=f"{day:2}", width=4)
                date_label.grid(row=week_idx + 1, column=day_idx)
                memories_for_day = memories_data.get(day, [])
                message = f"No memories for today"
                if len(memories_for_day) > 0:
                    message = '\n'.join(memories_for_day)
                ToolTip(date_label, text=message)

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
        memories = self.manager.get_memories()
        thoughts = self.manager.get_thoughts()
        show_calendar(year, month, memories, thoughts)

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
