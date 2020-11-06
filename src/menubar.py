from aqt import QMenu, mw
from aqt.qt import QAction, QKeySequence, Qt
from .config import get_config_value
from .api import show_queue_picker, show_quick_open_pdf
from aqt.utils import showInfo, tooltip
from .dialogs.editor import NoteEditor
from .dialogs.zotero_import import ZoteroImporter
from .dialogs.quick_youtube_import import QuickYoutubeImport
from .dialogs.settings import SettingsDialog


class Menu():
    def __init__(self):
        menu_name = "test"
        menu = get_menu(mw, "&SIAC")

        submenu_import = get_sub_menu(menu, "Import")

        import_options=( #SHORTCUT_CONF_KEY, TITLE, CALLBACK
            ("shortcuts.menubar.import.create_new", "New",           self.import_create_new),
            ("shortcuts.menubar.import.youtube",    "YouTube",       self.import_youtube), # still dysfunctional
            ("shortcuts.menubar.import.zotero_csv", "Zotero CSV",    self.import_zotero)
        )

        add_menu_actions(submenu_import, import_options)

        menu_options=( # CONF_KEY, TITLE, CALLBACK
            ("shortcuts.menubar.queue_manager",  "Queue Manager",    self.queue_picker),
            ("shortcuts.menubar.quick_open",     "Quick Open...",    self.quick_open),
            ("shortcuts.menubar.addon_settings", "Add-On Settings",  self.settings)
        )

        add_menu_actions(menu, menu_options)

    def import_zotero(self):
        dialog = ZoteroImporter(mw.app.activeWindow())

        if dialog.exec_():
            tooltip(f"Created {dialog.total_count} notes.")

    def import_youtube(self):
        dialog = QuickYoutubeImport(mw.app.activeWindow())

        if dialog.exec_():
            title = dialog.youtube_title
            channel = dialog.youtube_channel
            url = dialog.youtube_url

            text=f"""Title: {title}""" + "\n" + f"""Channel: {channel}"""


            noteeditor = NoteEditor(mw.app.activeWindow(), title_prefill = title, text_prefill = text, source_prefill = url)

    def import_create_new(self):
        dialog = NoteEditor(mw.app.activeWindow())

    def quick_open(self):
        show_quick_open_pdf()

    def queue_picker(self):
        show_queue_picker()

    def settings(self):
        dialog = SettingsDialog(mw.app.activeWindow())


def get_menu(parent, menuName):
    menubar = parent.form.menubar
    for a in menubar.actions():
        if menuName == a.text():
            return a.menu()
    else:
        return menubar.addMenu(menuName)


def get_sub_menu(menu, subMenuName):
    for a in menu.actions():
        if subMenuName == a.text():
            return a.menu()
    else:
        subMenu = QMenu(subMenuName, menu)
        menu.addMenu(subMenu)
        return subMenu

def add_menu_actions(menu, menu_options):
    for k,t,cb in menu_options:
        hk = 0
        if k:
            hk = get_config_value(k)

        act = QAction(t,menu)
        if hk:
            act.setShortcut(QKeySequence(hk))
            act.setShortcutContext(Qt.ApplicationShortcut)

        act.triggered.connect(cb)
        menu.addAction(act)
