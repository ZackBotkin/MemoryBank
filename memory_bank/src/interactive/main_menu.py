from interactive_menu.src.interactive_menu import InteractiveMenu
from memory_bank.src.interactive.read import ReadMemoriesMenu
from memory_bank.src.interactive.record import RecordMenu

class MainMenu(InteractiveMenu):

    def __init__(self, manager, path=[]):
        super().__init__(manager, path)
        self.sub_menu_modules = [
            RecordMenu(manager, self.path),
            ReadMemoriesMenu(manager, self.path)
        ]

    def title(self):
        return "Memory Bank"
