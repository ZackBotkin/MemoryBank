
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

    def title(self):
        return "Remember"

    def main_loop(self):
        memories = self.manager.get_memories()
        for memory in memories:
            print(memory)
