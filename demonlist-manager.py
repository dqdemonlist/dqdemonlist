import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import re
from datetime import datetime
import os

class DemonlistGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Dolores Squad Demonlist Manager")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a1a')
        
        # Initialize attributes to avoid errors
        self.beating_demon = None
        self.beating_player = None
        self.beating_progress = None
        self.beating_date = None
        
        # File paths
        self.demons_file = "js/demons.js"
        self.players_file = "js/players.js" # Added missing file path
        self.future_demons_file = "js/futuredemons.js"
        self.list_file = "js/list.js"
        
        # Create js folder if it doesn't exist
        if not os.path.exists("js"):
            os.makedirs("js")
            
        self.setup_styles()
        self.create_widgets()
        self.load_data()
        
    def setup_styles(self):
        self.style = ttk.Style()
        
        # Modern Dark Theme
        self.style.configure('TFrame', background='#1a1a1a')
        self.style.configure('TLabel', background='#1a1a1a', foreground='#ffffff', font=('Segoe UI', 10))
        self.style.configure('TButton', font=('Segoe UI', 10), padding=8)
        self.style.configure('TNotebook', background='#1a1a1a')
        self.style.configure('TNotebook.Tab', 
                           background='#2d2d2d', 
                           foreground='#ffffff',
                           padding=[15, 5],
                           font=('Segoe UI', 9, 'bold'))
        self.style.map('TNotebook.Tab', 
                      background=[('selected', '#4a4a4a')],
                      foreground=[('selected', '#ff6b6b')])
        
        self.style.configure('Title.TLabel', font=('Segoe UI', 16, 'bold'), foreground='#ff6b6b')
        self.style.configure('Subtitle.TLabel', font=('Segoe UI', 12, 'bold'), foreground='#6bc5ff')
        self.style.configure('Accent.TButton', background='#ff6b6b', foreground='white')
        self.style.configure('Danger.TButton', background='#dc3545', foreground='white')
        self.style.configure('Success.TButton', background='#28a745', foreground='white')
        
    def create_widgets(self):
        # Main Frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Header
        title_label = ttk.Label(main_frame, text="🔥 DOLORES SQUAD DEMONLIST MANAGER", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Notebook
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True)
        
        # Tabs
        self.create_view_tab(notebook)
        self.create_demon_tab(notebook)
        self.create_player_tab(notebook)
        self.create_future_tab(notebook)
        self.create_completion_tab(notebook)
        self.create_calculator_tab(notebook)
        self.create_ranking_tab(notebook)
        self.create_code_editor_tab(notebook)
        self.create_delete_tab(notebook)
        
    def create_view_tab(self, notebook):
        view_frame = ttk.Frame(notebook)
        notebook.add(view_frame, text="👀 Просмотр") 

        view_notebook = ttk.Notebook(view_frame) 
        view_notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Demons View
        demons_frame = ttk.Frame(view_notebook)
        view_notebook.add(demons_frame, text="👹 Демоны")
        self.demons_text = scrolledtext.ScrolledText(demons_frame, width=80, height=20, 
                                              font=('Consolas', 9), bg='#2d2d2d', fg='white',
                                              insertbackground='white')
        self.demons_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Players View
        players_frame = ttk.Frame(view_notebook)
        view_notebook.add(players_frame, text="👤 Игроки")
        self.players_text = scrolledtext.ScrolledText(players_frame, width=80, height=20,
                                               font=('Consolas', 9), bg='#2d2d2d', fg='white',
                                               insertbackground='white')
        self.players_text.pack(fill='both', expand=True, padx=5, pady=5)

        # Future Demons View
        future_frame = ttk.Frame(view_notebook)
        view_notebook.add(future_frame, text="🔮 Будущие демоны")
        self.future_text = scrolledtext.ScrolledText(future_frame, width=80, height=20,
                                              font=('Consolas', 9), bg='#2d2d2d', fg='white',
                                              insertbackground='white')
        self.future_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        refresh_btn = ttk.Button(view_frame, text="🔄 Обновить данные", command=self.load_data)
        refresh_btn.pack(pady=10)

    def create_demon_tab(self, notebook):
        demon_frame = ttk.Frame(notebook)
        notebook.add(demon_frame, text="👹 Добавить демона")
        
        ttk.Label(demon_frame, text="Добавление нового демона", style='Subtitle.TLabel').pack(pady=20)
        
        form_frame = ttk.Frame(demon_frame)
        form_frame.pack(pady=20, padx=30)
        
        ttk.Label(form_frame, text="Название демона:").grid(row=0, column=0, sticky='w', pady=8)
        self.demon_name = ttk.Entry(form_frame, width=30, font=('Segoe UI', 10))
        self.demon_name.grid(row=0, column=1, pady=8, padx=10)
        
        ttk.Label(form_frame, text="Создатель:").grid(row=1, column=0, sticky='w', pady=8)
        self.demon_creator = ttk.Entry(form_frame, width=30, font=('Segoe UI', 10))
        self.demon_creator.grid(row=1, column=1, pady=8, padx=10)
        
        ttk.Label(form_frame, text="ID верификатора:").grid(row=2, column=0, sticky='w', pady=8)
        self.demon_verifier = ttk.Entry(form_frame, width=30, font=('Segoe UI', 10))
        self.demon_verifier.grid(row=2, column=1, pady=8, padx=10)
        
        ttk.Label(form_frame, text="Дата верификации (гггг-мм-дд):").grid(row=3, column=0, sticky='w', pady=8)
        self.demon_date = ttk.Entry(form_frame, width=30, font=('Segoe UI', 10))
        self.demon_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.demon_date.grid(row=3, column=1, pady=8, padx=10)
        
        add_btn = ttk.Button(demon_frame, text="➕ Добавить демона", command=self.add_demon_gui)
        add_btn.pack(pady=15)
        
        # Separator
        ttk.Separator(demon_frame, orient='horizontal').pack(fill='x', pady=20, padx=30)
        
        # Edit Section
        ttk.Label(demon_frame, text="Редактирование демонов", style='Subtitle.TLabel').pack(pady=(10, 5))
        edit_frame = ttk.Frame(demon_frame)
        edit_frame.pack(pady=15)
        
        ttk.Label(edit_frame, text="Выберите демона:").grid(row=0, column=0, padx=5)
        self.demon_combobox = ttk.Combobox(edit_frame, width=25, state="readonly", font=('Segoe UI', 10))
        self.demon_combobox.grid(row=0, column=1, padx=5)
        
        edit_btn = ttk.Button(edit_frame, text="✏️ Редактировать", command=self.edit_demon_gui)
        edit_btn.grid(row=0, column=2, padx=10)
        
    def create_player_tab(self, notebook):
        player_frame = ttk.Frame(notebook)
        notebook.add(player_frame, text="👤 Добавить игрока")
        
        ttk.Label(player_frame, text="Добавление игрока", style='Subtitle.TLabel').pack(pady=20)
        
        form_frame = ttk.Frame(player_frame)
        form_frame.pack(pady=20, padx=30)
        
        ttk.Label(form_frame, text="Имя игрока:").grid(row=0, column=0, sticky='w', pady=10)
        self.player_name = ttk.Entry(form_frame, width=30, font=('Segoe UI', 10))
        self.player_name.grid(row=0, column=1, pady=10, padx=10)
        
        add_btn = ttk.Button(player_frame, text="➕ Добавить игрока", command=self.add_player_gui)
        add_btn.pack(pady=15)
        
        ttk.Separator(player_frame, orient='horizontal').pack(fill='x', pady=20, padx=30)
        
        ttk.Label(player_frame, text="Редактирование игроков", style='Subtitle.TLabel').pack(pady=(10, 5))
        edit_frame = ttk.Frame(player_frame)
        edit_frame.pack(pady=15)
        
        ttk.Label(edit_frame, text="Выберите игрока:").grid(row=0, column=0, padx=5)
        self.player_combobox = ttk.Combobox(edit_frame, width=25, state="readonly", font=('Segoe UI', 10))
        self.player_combobox.grid(row=0, column=1, padx=5)
        
        edit_btn = ttk.Button(edit_frame, text="✏️ Редактировать", command=self.edit_player_gui)
        edit_btn.grid(row=0, column=2, padx=10)
    
    def create_future_tab(self, notebook):
        future_frame = ttk.Frame(notebook)
        notebook.add(future_frame, text="🔮 Будущие демоны")
        
        ttk.Label(future_frame, text="Будущие демоны", style='Subtitle.TLabel').pack(pady=20)
        
        form_frame = ttk.Frame(future_frame)
        form_frame.pack(pady=20, padx=30)
        
        ttk.Label(form_frame, text="Название демона:").grid(row=0, column=0, sticky='w', pady=8)
        self.future_name = ttk.Entry(form_frame, width=30, font=('Segoe UI', 10))
        self.future_name.grid(row=0, column=1, pady=8, padx=10)
        
        ttk.Label(form_frame, text="Создатель:").grid(row=1, column=0, sticky='w', pady=8)
        self.future_creator = ttk.Entry(form_frame, width=30, font=('Segoe UI', 10))
        self.future_creator.grid(row=1, column=1, pady=8, padx=10)
        
        ttk.Label(form_frame, text="Сложность:").grid(row=2, column=0, sticky='w', pady=8)
        self.future_difficulty = ttk.Entry(form_frame, width=30, font=('Segoe UI', 10))
        self.future_difficulty.grid(row=2, column=1, pady=8, padx=10)
        
        ttk.Label(form_frame, text="Описание:").grid(row=3, column=0, sticky='w', pady=8)
        self.future_description = tk.Text(form_frame, width=30, height=4, font=('Segoe UI', 10))
        self.future_description.grid(row=3, column=1, pady=8, padx=10)
        
        add_btn = ttk.Button(future_frame, text="➕ Добавить будущего демона", command=self.add_future_demon_gui)
        add_btn.pack(pady=15)
        
        # Add Beating Player
        ttk.Label(future_frame, text="Добавить игрока проходящего демон:", style='Subtitle.TLabel').pack(pady=(30, 10))
        
        beating_frame = ttk.Frame(future_frame)
        beating_frame.pack(pady=10, padx=30)
        
        ttk.Label(beating_frame, text="Демон:").grid(row=0, column=0, padx=5, pady=5)
        self.beating_demon = ttk.Combobox(beating_frame, width=20, state="readonly", font=('Segoe UI', 10))
        self.beating_demon.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(beating_frame, text="Игрок:").grid(row=0, column=2, padx=5, pady=5)
        self.beating_player = ttk.Combobox(beating_frame, width=20, state="readonly", font=('Segoe UI', 10))
        self.beating_player.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(beating_frame, text="Прогресс (%):").grid(row=1, column=0, padx=5, pady=5)
        self.beating_progress = ttk.Entry(beating_frame, width=10, font=('Segoe UI', 10))
        self.beating_progress.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(beating_frame, text="Дата обновления (гггг-мм-дд):").grid(row=2, column=0, padx=5, pady=5)
        self.beating_date = ttk.Entry(beating_frame, width=15, font=('Segoe UI', 10))
        self.beating_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.beating_date.grid(row=2, column=1, padx=5, pady=5)
        
        add_beating_btn = ttk.Button(beating_frame, text="🎯 Добавить прохождение", command=self.add_beating_player_gui)
        add_beating_btn.grid(row=2, column=2, columnspan=2, padx=5, pady=5)
        
    def create_completion_tab(self, notebook):
        completion_frame = ttk.Frame(notebook)
        notebook.add(completion_frame, text="✅ Прохождения")
        
        ttk.Label(completion_frame, text="Добавление прохождений", style='Subtitle.TLabel').pack(pady=20)
        
        form_frame = ttk.Frame(completion_frame)
        form_frame.pack(pady=20, padx=30)
        
        ttk.Label(form_frame, text="Демон:").grid(row=0, column=0, padx=5, pady=8)
        self.completion_demon = ttk.Combobox(form_frame, width=20, state="readonly", font=('Segoe UI', 10))
        self.completion_demon.grid(row=0, column=1, padx=5, pady=8)
        
        ttk.Label(form_frame, text="Игрок:").grid(row=0, column=2, padx=5, pady=8)
        self.completion_player = ttk.Combobox(form_frame, width=20, state="readonly", font=('Segoe UI', 10))
        self.completion_player.grid(row=0, column=3, padx=5, pady=8)
        
        ttk.Label(form_frame, text="Дата (гггг-мм-дд):").grid(row=1, column=0, padx=5, pady=8)
        self.completion_date = ttk.Entry(form_frame, width=20, font=('Segoe UI', 10))
        self.completion_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.completion_date.grid(row=1, column=1, padx=5, pady=8)
        
        add_btn = ttk.Button(form_frame, text="✅ Добавить прохождение", command=self.add_completion_gui)
        add_btn.grid(row=1, column=2, columnspan=2, padx=5, pady=8)

        refresh_btn = ttk.Button(completion_frame, text="🔄 Обновить списки демонов и игроков", command=self.load_data)
        refresh_btn.pack(pady=10)
    
    def create_calculator_tab(self, notebook):
        calc_frame = ttk.Frame(notebook)
        notebook.add(calc_frame, text="🧮 Калькулятор очков")
        
        ttk.Label(calc_frame, text="Калькулятор очков демонлиста", style='Subtitle.TLabel').pack(pady=20)
        calc_container = ttk.Frame(calc_frame)
        calc_container.pack(pady=20, padx=30)
        
        ttk.Label(calc_container, text="Позиция в демонлисте:").grid(row=0, column=0, sticky='w', pady=10)
        self.position_entry = ttk.Entry(calc_container, width=15, font=('Segoe UI', 12))
        self.position_entry.grid(row=0, column=1, pady=10, padx=10)
        
        calc_btn = ttk.Button(calc_container, text="🎯 Рассчитать очки", command=self.calculate_points)
        calc_btn.grid(row=0, column=2, padx=20)
        
        self.result_label = ttk.Label(calc_container, text="Очки: 0", font=('Segoe UI', 14, 'bold'), foreground='#6bc5ff')
        self.result_label.grid(row=1, column=0, columnspan=3, pady=20)
        
        ttk.Label(calc_container, text="Топ-20 позиций:", style='Subtitle.TLabel').grid(row=2, column=0, columnspan=3, pady=(30, 10))
        
        table_frame = ttk.Frame(calc_container)
        table_frame.grid(row=3, column=0, columnspan=3, sticky='we', pady=10)
        
        columns = ('#1', '#2', '#3', '#4', '#5')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=10)
        
        tree.heading('#1', text='Поз.')
        tree.heading('#2', text='Очки')
        tree.heading('#3', text='Поз.')
        tree.heading('#4', text='Очки')
        tree.heading('#5', text='Поз.')
        
        for i, col in enumerate(columns):
             tree.column(col, width=80 if i % 2 == 0 else 120, anchor='center')
        
        for i in range(0, 20, 5):
            values = []
            for j in range(5):
                pos = i + j + 1
                if pos <= 20:
                    points = self.calculate_points_for_position(pos)
                    values.extend([f"{pos}", f"{points:.2f}"])
                else:
                    values.extend(["", ""])
            tree.insert('', 'end', values=values)
        
        tree.pack(fill='both', expand=True)
        
        info_text = """📊 Формула расчета: Топ-1 = 500 очков, каждая следующая позиция теряет 19% от предыдущей"""
        info_label = ttk.Label(calc_container, text=info_text, font=('Segoe UI', 9), foreground='#cccccc')
        info_label.grid(row=4, column=0, columnspan=3, pady=20)
    
    def calculate_points_for_position(self, pos):
        if pos == 1: return 500.0
        return 500.0 * (0.81 ** (pos - 1))

    def calculate_points(self):
        try:
            pos = int(self.position_entry.get())
            points = self.calculate_points_for_position(pos)
            self.result_label.config(text=f"Очки: {points:.2f}")
        except:
            self.result_label.config(text="Ошибка ввода")

    def create_ranking_tab(self, notebook):
        ranking_frame = ttk.Frame(notebook)
        notebook.add(ranking_frame, text="🏆 Расстановка топа")
        
        ttk.Label(ranking_frame, text="Управление рейтингом демонов", style='Title.TLabel').pack(pady=20)
        main_container = ttk.Frame(ranking_frame)
        main_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        left_frame = ttk.LabelFrame(main_container, text="📋 Все демоны", padding=10)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(search_frame, text="Поиск:").pack(side='left')
        self.demon_search = ttk.Entry(search_frame, font=('Segoe UI', 10))
        self.demon_search.pack(side='left', fill='x', expand=True, padx=5)
        self.demon_search.bind('<KeyRelease>', self.filter_demons)
        
        demon_list_frame = ttk.Frame(left_frame)
        demon_list_frame.pack(fill='both', expand=True)
        
        self.demon_listbox = tk.Listbox(demon_list_frame, font=('Segoe UI', 10), bg='#2d2d2d', fg='white',
                                      selectbackground='#ff6b6b', selectforeground='white')
        demon_scrollbar = ttk.Scrollbar(demon_list_frame, orient='vertical', command=self.demon_listbox.yview)
        self.demon_listbox.configure(yscrollcommand=demon_scrollbar.set)
        
        self.demon_listbox.pack(side='left', fill='both', expand=True)
        demon_scrollbar.pack(side='right', fill='y')
        
        right_frame = ttk.LabelFrame(main_container, text="🏅 Текущий топ демонов", padding=10)
        right_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        control_frame = ttk.Frame(right_frame)
        control_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Button(control_frame, text="⬆️ Поднять", command=lambda: self.move_demon(-1)).pack(side='left', padx=2)
        ttk.Button(control_frame, text="⬇️ Опустить", command=lambda: self.move_demon(1)).pack(side='left', padx=2)
        ttk.Button(control_frame, text="🎯 В топ", command=self.add_to_top).pack(side='left', padx=2)
        ttk.Button(control_frame, text="🗑️ Убрать", command=self.remove_from_top, style='Danger.TButton').pack(side='left', padx=2)
        
        top_list_frame = ttk.Frame(right_frame)
        top_list_frame.pack(fill='both', expand=True)
        
        self.top_listbox = tk.Listbox(top_list_frame, font=('Segoe UI', 10), bg='#2d2d2d', fg='white',
                                    selectbackground='#6bc5ff', selectforeground='white')
        top_scrollbar = ttk.Scrollbar(top_list_frame, orient='vertical', command=self.top_listbox.yview)
        self.top_listbox.configure(yscrollcommand=top_scrollbar.set)
        
        self.top_listbox.pack(side='left', fill='both', expand=True)
        top_scrollbar.pack(side='right', fill='y')
        
        bottom_frame = ttk.Frame(ranking_frame)
        bottom_frame.pack(fill='x', pady=10)
        
        ttk.Button(bottom_frame, text="🔄 Обновить списки", command=self.update_ranking_lists).pack(side='left', padx=5)
        ttk.Button(bottom_frame, text="💾 Сохранить топ", command=self.save_top_list, style='Success.TButton').pack(side='left', padx=5)
        ttk.Button(bottom_frame, text="📊 Просмотреть топ", command=self.view_top_list).pack(side='left', padx=5)
        
        info_label = ttk.Label(ranking_frame, text="💡 Перетащите демонов между списками или используйте кнопки для управления топом",
                             font=('Segoe UI', 9), foreground='#cccccc')
        info_label.pack(pady=5)
        
    def create_code_editor_tab(self, notebook):
        editor_frame = ttk.Frame(notebook)
        notebook.add(editor_frame, text="📝 Редактор кода")
        
        ttk.Label(editor_frame, text="Редактор файлов демонлиста", style='Title.TLabel').pack(pady=20)
        
        file_frame = ttk.Frame(editor_frame)
        file_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(file_frame, text="Выберите файл:").pack(side='left')
        self.file_selector = ttk.Combobox(file_frame, width=20, state="readonly", font=('Segoe UI', 10))
        self.file_selector['values'] = ['demons.js', 'players.js', 'futuredemons.js', 'list.js']
        self.file_selector.set('demons.js')
        self.file_selector.pack(side='left', padx=10)
        
        ttk.Button(file_frame, text="📂 Загрузить файл", command=self.load_file_for_edit).pack(side='left', padx=5)
        
        editor_container = ttk.Frame(editor_frame)
        editor_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.code_editor = scrolledtext.ScrolledText(editor_container, font=('Consolas', 10), 
                                                   bg='#1e1e1e', fg='#d4d4d4',
                                                   insertbackground='white', wrap=tk.NONE)
        self.code_editor.pack(fill='both', expand=True)
        
        editor_controls = ttk.Frame(editor_frame)
        editor_controls.pack(fill='x', padx=20, pady=10)
        
        ttk.Button(editor_controls, text="💾 Сохранить файл", command=self.save_edited_file, style='Success.TButton').pack(side='left', padx=5)
        ttk.Button(editor_controls, text="🔄 Обновить из системы", command=self.reload_from_system).pack(side='left', padx=5)
        ttk.Button(editor_controls, text="🔍 Проверить синтаксис", command=self.validate_syntax).pack(side='left', padx=5)
        
        self.editor_status = ttk.Label(editor_frame, text="Готов к работе", font=('Segoe UI', 9))
        self.editor_status.pack(pady=5)

    def create_delete_tab(self, notebook):
        delete_frame = ttk.Frame(notebook)
        notebook.add(delete_frame, text="🗑️ Удаление")
        
        ttk.Label(delete_frame, text="Система удаления данных", style='Title.TLabel').pack(pady=20)
        
        delete_container = ttk.Frame(delete_frame)
        delete_container.pack(pady=20, padx=30)
        
        # Demon Delete
        demon_delete_frame = ttk.LabelFrame(delete_container, text="👹 Удаление демонов", padding=15)
        demon_delete_frame.grid(row=0, column=0, padx=10, pady=10, sticky='we')
        
        ttk.Label(demon_delete_frame, text="Выберите демона:").pack(pady=5)
        self.delete_demon_combobox = ttk.Combobox(demon_delete_frame, width=30, state="readonly", font=('Segoe UI', 10))
        self.delete_demon_combobox.pack(pady=5)
        
        delete_demon_btn = ttk.Button(demon_delete_frame, text="🗑️ Удалить демона", command=self.delete_demon_gui, style='Danger.TButton')
        delete_demon_btn.pack(pady=10)
        
        # Player Delete
        player_delete_frame = ttk.LabelFrame(delete_container, text="👤 Удаление игроков", padding=15)
        player_delete_frame.grid(row=0, column=1, padx=10, pady=10, sticky='we')
        
        ttk.Label(player_delete_frame, text="Выберите игрока:").pack(pady=5)
        self.delete_player_combobox = ttk.Combobox(player_delete_frame, width=30, state="readonly", font=('Segoe UI', 10))
        self.delete_player_combobox.pack(pady=5)
        
        delete_player_btn = ttk.Button(player_delete_frame, text="🗑️ Удалить игрока", command=self.delete_player_gui, style='Danger.TButton')
        delete_player_btn.pack(pady=10)
        
        # Future Demon Delete
        future_delete_frame = ttk.LabelFrame(delete_container, text="🔮 Удаление будущих демонов", padding=15)
        future_delete_frame.grid(row=1, column=0, padx=10, pady=10, sticky='we')
        
        ttk.Label(future_delete_frame, text="Выберите будущего демона:").pack(pady=5)
        self.delete_future_combobox = ttk.Combobox(future_delete_frame, width=30, state="readonly", font=('Segoe UI', 10))
        self.delete_future_combobox.pack(pady=5)
        
        delete_future_btn = ttk.Button(future_delete_frame, text="🗑️ Удалить будущего демона", command=self.delete_future_demon_gui, style='Danger.TButton')
        delete_future_btn.pack(pady=10)
        
        # Completion Delete
        completion_delete_frame = ttk.LabelFrame(delete_container, text="✅ Удаление прохождений", padding=15)
        completion_delete_frame.grid(row=1, column=1, padx=10, pady=10, sticky='we')
        
        ttk.Label(completion_delete_frame, text="Демон:").pack(pady=2)
        self.delete_completion_demon = ttk.Combobox(completion_delete_frame, width=25, state="readonly", font=('Segoe UI', 10))
        self.delete_completion_demon.pack(pady=2)
        
        ttk.Label(completion_delete_frame, text="Игрок:").pack(pady=2)
        self.delete_completion_player = ttk.Combobox(completion_delete_frame, width=25, state="readonly", font=('Segoe UI', 10))
        self.delete_completion_player.pack(pady=2)
        
        delete_completion_btn = ttk.Button(completion_delete_frame, text="🗑️ Удалить прохождение", command=self.delete_completion_gui, style='Danger.TButton')
        delete_completion_btn.pack(pady=10)
        
        # Beating Player Delete
        beating_delete_frame = ttk.LabelFrame(delete_container, text="🎯 Удаление проходящих игроков", padding=15)
        beating_delete_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='we')
        
        ttk.Label(beating_delete_frame, text="Будущий демон:").pack(pady=2)
        self.delete_beating_demon = ttk.Combobox(beating_delete_frame, width=25, state="readonly", font=('Segoe UI', 10))
        self.delete_beating_demon.pack(pady=2)
        
        ttk.Label(beating_delete_frame, text="Игрок:").pack(pady=2)
        self.delete_beating_player = ttk.Combobox(beating_delete_frame, width=25, state="readonly", font=('Segoe UI', 10))
        self.delete_beating_player.pack(pady=2)
        
        delete_beating_btn = ttk.Button(beating_delete_frame, text="🗑️ Удалить игрока", command=self.delete_beating_player_gui, style='Danger.TButton')
        delete_beating_btn.pack(pady=10)
        
        warning_label = ttk.Label(delete_frame, 
                                text="⚠️ ВНИМАНИЕ: Удаление данных необратимо! Создавайте резервные копии.",
                                font=('Segoe UI', 10, 'bold'), 
                                foreground='#ff6b6b')
        warning_label.pack(pady=20)

    # DATA MANAGEMENT METHODS
    def update_ranking_lists(self):
        try:
            demons = self.load_demons()
            top_list = self.load_top_list()
            self.demon_listbox.delete(0, tk.END)
            self.top_listbox.delete(0, tk.END)
            demon_ids_in_top = set(top_list)
            for demon in demons:
                display_text = f"{demon['id']}: {demon['name']} (by {demon['creator']})"
                if demon['id'] not in demon_ids_in_top:
                    self.demon_listbox.insert(tk.END, display_text)
            for demon_id in top_list:
                demon = next((d for d in demons if d['id'] == demon_id), None)
                if demon:
                    display_text = f"{demon['id']}: {demon['name']}"
                    self.top_listbox.insert(tk.END, display_text)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить списки: {e}")
           
    def filter_demons(self, event=None):
        search_term = self.demon_search.get().lower()
        demons = self.load_demons()
        top_list = self.load_top_list()
        self.demon_listbox.delete(0, tk.END)
        demon_ids_in_top = set(top_list)
        for demon in demons:
            if demon['id'] not in demon_ids_in_top:
                display_text = f"{demon['id']}: {demon['name']} (by {demon['creator']})"
                if search_term in display_text.lower():
                    self.demon_listbox.insert(tk.END, display_text)
                    
    def load_top_list(self):
        try:
            if not os.path.exists(self.list_file): return []
            with open(self.list_file, 'r', encoding='utf-8') as f:
                content = f.read()
            match = re.search(r'const demonList = (\[.*?\]);', content, re.DOTALL)
            if match:
                return json.loads(match.group(1))
            return []
        except:
            return []
            
    def add_to_top(self):
        try:
            selection = self.demon_listbox.curselection()
            if not selection:
                messagebox.showwarning("Предупреждение", "Выберите демона для добавления в топ!")
                return
            demon_text = self.demon_listbox.get(selection[0])
            demon_id = int(demon_text.split(':')[0])
            top_list = self.load_top_list()
            if demon_id in top_list:
                messagebox.showwarning("Предупреждение", "Этот демон уже в топе!")
                return
            top_list.append(demon_id)
            self.save_top_list_internal(top_list)
            self.update_ranking_lists()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить демона в топ: {e}")
            
    def remove_from_top(self):
        try:
            selection = self.top_listbox.curselection()
            if not selection:
                messagebox.showwarning("Предупреждение", "Выберите демона для удаления из топа!")
                return
            demon_text = self.top_listbox.get(selection[0])
            demon_id = int(demon_text.split(':')[0])
            top_list = self.load_top_list()
            top_list = [id for id in top_list if id != demon_id]
            self.save_top_list_internal(top_list)
            self.update_ranking_lists()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить демона из топа: {e}")
            
    def move_demon(self, direction):
        try:
            selection = self.top_listbox.curselection()
            if not selection:
                messagebox.showwarning("Предупреждение", "Выберите демона для перемещения!")
                return
            index = selection[0]
            top_list = self.load_top_list()
            if direction == -1 and index > 0: 
                top_list[index], top_list[index-1] = top_list[index-1], top_list[index]
            elif direction == 1 and index < len(top_list) - 1:
                top_list[index], top_list[index+1] = top_list[index+1], top_list[index]
            else:
                return
            self.save_top_list_internal(top_list)
            self.update_ranking_lists()
            self.top_listbox.select_set(index + direction)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось переместить демона: {e}")
            
    def save_top_list(self):
        try:
            top_list = self.load_top_list()
            self.save_top_list_internal(top_list)
            messagebox.showinfo("Успех", "Топ демонов сохранен!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить топ: {e}")
            
    def save_top_list_internal(self, top_list):
        if not os.path.exists(self.list_file):
             with open(self.list_file, 'w', encoding='utf-8') as f:
                f.write(f"const demonList = {json.dumps(top_list)};")
             return
        with open(self.list_file, 'r', encoding='utf-8') as f:
            content = f.read()
        new_list = f"const demonList = {json.dumps(top_list)};"
        content = re.sub(r'const demonList = \[.*?\];', new_list, content, flags=re.DOTALL)
        with open(self.list_file, 'w', encoding='utf-8') as f:
            f.write(content)
            
    def view_top_list(self):
        try:
            top_list = self.load_top_list()
            demons = self.load_demons()
            view_window = tk.Toplevel(self.root)
            view_window.title("Текущий топ демонов")
            view_window.geometry("600x400")
            text_area = scrolledtext.ScrolledText(view_window, font=('Consolas', 10))
            text_area.pack(fill='both', expand=True, padx=10, pady=10)
            text_area.insert(tk.END, "🏆 ТОП ДЕМОНОВ:\n\n")
            for i, demon_id in enumerate(top_list, 1):
                demon = next((d for d in demons if d['id'] == demon_id), None)
                if demon:
                    text_area.insert(tk.END, f"{i}. {demon['name']} (by {demon['creator']}) - ID: {demon_id}\n")
                else:
                    text_area.insert(tk.END, f"{i}. Демон с ID {demon_id} не найден\n")
            text_area.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось показать топ: {e}")

    # EDITOR METHODS
    def load_file_for_edit(self):
        try:
            filename = self.file_selector.get()
            filepath = f"js/{filename}"
            if not os.path.exists(filepath):
                open(filepath, 'w').close()
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            self.code_editor.delete(1.0, tk.END)
            self.code_editor.insert(1.0, content)
            self.editor_status.config(text=f"Файл {filename} загружен успешно")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")
            
    def save_edited_file(self):
        try:
            filename = self.file_selector.get()
            filepath = f"js/{filename}"
            content = self.code_editor.get(1.0, tk.END)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            self.editor_status.config(text=f"Файл {filename} сохранен успешно")
            messagebox.showinfo("Успех", f"Файл {filename} сохранен!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")
            
    def reload_from_system(self):
        try:
            filename = self.file_selector.get()
            content = ""
            if filename == 'demons.js':
                demons = self.load_demons()
                content = f"const demons = {json.dumps(demons, indent=2, ensure_ascii=False)};"
            elif filename == 'players.js':
                players = self.load_players()
                content = f"const players = {json.dumps(players, indent=2, ensure_ascii=False)};"
            elif filename == 'futuredemons.js':
                future_demons = self.load_future_demons()
                content = f"const futureDemons = {json.dumps(future_demons, indent=2, ensure_ascii=False)};"
            elif filename == 'list.js':
                 if os.path.exists(self.list_file):
                    with open(self.list_file, 'r', encoding='utf-8') as f:
                        content = f.read()
            self.code_editor.delete(1.0, tk.END)
            self.code_editor.insert(1.0, content)
            self.editor_status.config(text=f"Данные из системы загружены в {filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")
            
    def validate_syntax(self):
        try:
            content = self.code_editor.get(1.0, tk.END)
            json_match = re.search(r'=\s*(\[.*\]|{.*});', content, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                json.loads(json_str) 
                self.editor_status.config(text="✅ Синтаксис JSON корректен")
                messagebox.showinfo("Проверка", "Синтаксис JSON корректен!")
            else:
                self.editor_status.config(text="⚠️ JSON не найден в файле")
        except json.JSONDecodeError as e:
            self.editor_status.config(text="❌ Ошибка в синтаксисе JSON")
            messagebox.showerror("Ошибка синтаксиса", f"Некорректный JSON: {e}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось проверить синтаксис: {e}")

    # DELETE METHODS
    def delete_demon_gui(self):
        try:
            demon_str = self.delete_demon_combobox.get()
            if not demon_str:
                messagebox.showwarning("Предупреждение", "Выберите демона для удаления!")
                return
            demon_id = int(demon_str.split(':')[0])
            demon_name = demon_str.split(':', 1)[1].strip()
            if not messagebox.askyesno("Подтверждение", f"Удалить {demon_name}?"): return
            
            demons = self.load_demons()
            players = self.load_players()
            demons = [d for d in demons if d['id'] != demon_id]
            for player in players:
                if 'completedDemons' in player and demon_id in player['completedDemons']:
                    player['completedDemons'].remove(demon_id)
            self.save_demons(demons)
            self.save_players(players)
            
            demon_ids = [d['id'] for d in demons]
            self.update_demon_list(demon_ids)
            messagebox.showinfo("Успех", "Демон удален!")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить демона: {e}")
    
    def delete_player_gui(self):
        try:
            player_str = self.delete_player_combobox.get()
            if not player_str:
                messagebox.showwarning("Предупреждение", "Выберите игрока для удаления!")
                return
            player_id = int(player_str.split(':')[0])
            player_name = player_str.split(':', 1)[1].strip()
            if not messagebox.askyesno("Подтверждение", f"Удалить {player_name}?"): return
            
            players = self.load_players()
            demons = self.load_demons()
            future_demons = self.load_future_demons()
            
            players = [p for p in players if p['id'] != player_id]
            for demon in demons:
                 if 'completers' in demon:
                     demon['completers'] = [comp for comp in demon['completers'] if comp['playerId'] != player_id]
            for demon in future_demons:
                if 'beatingPlayers' in demon:
                    demon['beatingPlayers'] = [bp for bp in demon['beatingPlayers'] if bp['playerId'] != player_id]
            
            self.save_players(players)
            self.save_demons(demons)
            self.save_future_demons(future_demons)
            messagebox.showinfo("Успех", "Игрок удален!")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить игрока: {e}")
    
    def delete_future_demon_gui(self):
        try:
            future_str = self.delete_future_combobox.get()
            if not future_str:
                messagebox.showwarning("Предупреждение", "Выберите будущего демона!")
                return
            future_id = int(future_str.split(':')[0])
            if not messagebox.askyesno("Подтверждение", "Удалить будущего демона?"): return
            
            future_demons = self.load_future_demons()
            future_demons = [fd for fd in future_demons if fd['id'] != future_id]
            self.save_future_demons(future_demons)
            messagebox.showinfo("Успех", "Будущий демон удален!")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить будущего демона: {e}")
    
    def delete_completion_gui(self):
        try:
            demon_str = self.delete_completion_demon.get()
            player_str = self.delete_completion_player.get()
            if not all([demon_str, player_str]):
                messagebox.showwarning("Предупреждение", "Выберите демона и игрока!")
                return
            demon_id = int(demon_str.split(':')[0])
            player_id = int(player_str.split(':')[0])
            
            if not messagebox.askyesno("Подтверждение", "Удалить прохождение?"): return
            
            demons = self.load_demons()
            players = self.load_players()
            
            for demon in demons:
                if demon['id'] == demon_id and 'completers' in demon:
                    demon['completers'] = [comp for comp in demon['completers'] if comp['playerId'] != player_id]
                    break
            for player in players:
                if player['id'] == player_id:
                    if 'completedDemons' in player and demon_id in player['completedDemons']:
                        player['completedDemons'].remove(demon_id)
                    break
            
            self.save_demons(demons)
            self.save_players(players)
            messagebox.showinfo("Успех", "Прохождение удалено!")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить прохождение: {e}")
    
    def delete_beating_player_gui(self):
        try:
            demon_str = self.delete_beating_demon.get()
            player_str = self.delete_beating_player.get()
            if not all([demon_str, player_str]):
                messagebox.showwarning("Предупреждение", "Выберите демона и игрока!")
                return
            demon_id = int(demon_str.split(':')[0])
            player_id = int(player_str.split(':')[0])
            
            if not messagebox.askyesno("Подтверждение", "Удалить игрока из проходящих?"): return
            
            future_demons = self.load_future_demons()
            for demon in future_demons:
                if demon['id'] == demon_id and 'beatingPlayers' in demon:
                    demon['beatingPlayers'] = [bp for bp in demon['beatingPlayers'] if bp['playerId'] != player_id]
                    break
            self.save_future_demons(future_demons)
            messagebox.showinfo("Успех", "Игрок удален из проходящих!")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить игрока: {e}")

    # DATA LOADING & SAVING METHODS
    def load_data(self):
        try:
            demons = self.load_demons()
            players = self.load_players()
            future_demons = self.load_future_demons()
            
            self.update_demons_text(demons)
            self.update_players_text(players)
            self.update_future_text(future_demons)
            self.update_all_comboboxes(demons, players, future_demons)
            if hasattr(self, 'demon_listbox'):
                 self.update_ranking_lists()
        except Exception as e:
            # Silent fail for initial load if files empty
            pass
    
    def update_all_comboboxes(self, demons, players, future_demons):
        try:
            demon_values = [f"{d['id']}: {d['name']}" for d in demons]
            player_values = [f"{p['id']}: {p['name']}" for p in players]
            future_values = [f"{d['id']}: {d['name']}" for d in future_demons]
            
            if hasattr(self, 'completion_demon'): self.completion_demon['values'] = demon_values
            if hasattr(self, 'completion_player'): self.completion_player['values'] = player_values
            if hasattr(self, 'demon_combobox'): self.demon_combobox['values'] = demon_values
            if hasattr(self, 'player_combobox'): self.player_combobox['values'] = player_values
            if hasattr(self, 'beating_demon'): self.beating_demon['values'] = future_values
            if hasattr(self, 'beating_player'): self.beating_player['values'] = player_values
            if hasattr(self, 'delete_demon_combobox'): self.delete_demon_combobox['values'] = demon_values
            if hasattr(self, 'delete_player_combobox'): self.delete_player_combobox['values'] = player_values
            if hasattr(self, 'delete_future_combobox'): self.delete_future_combobox['values'] = future_values
            if hasattr(self, 'delete_completion_demon'): self.delete_completion_demon['values'] = demon_values
            if hasattr(self, 'delete_completion_player'): self.delete_completion_player['values'] = player_values
            if hasattr(self, 'delete_beating_demon'): self.delete_beating_demon['values'] = future_values
            if hasattr(self, 'delete_beating_player'): self.delete_beating_player['values'] = player_values
        except Exception as e:
            print(f"Combobox update error: {e}")
    
    def load_demons(self):
        if not os.path.exists(self.demons_file): return []
        try:
            with open(self.demons_file, 'r', encoding='utf-8') as f:
                content = f.read()
            match = re.search(r'const demons = (\[.*?\]);', content, re.DOTALL)
            if match:
                demons_json = match.group(1).replace("'", '"')
                demons_json = re.sub(r'(\w+):', r'"\1":', demons_json)
                return json.loads(demons_json)
            return []
        except: return []
    
    def load_players(self):
        if not os.path.exists(self.players_file): return []
        try:
            with open(self.players_file, 'r', encoding='utf-8') as f:
                content = f.read()
            match = re.search(r'const players = (\[.*?\]);', content, re.DOTALL)
            if match:
                players_json = match.group(1).replace("'", '"')
                players_json = re.sub(r'(\w+):', r'"\1":', players_json)
                return json.loads(players_json)
            return []
        except: return []
    
    def load_future_demons(self):
        if not os.path.exists(self.future_demons_file): return []
        try:
            with open(self.future_demons_file, 'r', encoding='utf-8') as f:
                content = f.read()
            match = re.search(r'const futureDemons = (\[.*?\]);', content, re.DOTALL)
            if match:
                future_json = match.group(1).replace("'", '"')
                future_json = re.sub(r'(\w+):', r'"\1":', future_json)
                return json.loads(future_json)
            return []
        except: return []
    
    def update_demons_text(self, demons):
        text = "👹 ВСЕ ДЕМОНЫ:\n\n"
        for demon in demons:
             text += f"ID: {demon['id']} - {demon['name']}\n"
             text += f"  Создатель: {demon['creator']}\n"
             text += f"  Верификатор: {demon['verifier']}\n"
             text += f"  Прохождений: {len(demon.get('completers', []))}\n\n"
        self.demons_text.delete(1.0, tk.END)
        self.demons_text.insert(1.0, text)
        
    def update_players_text(self, players):
        text = "👤 ВСЕ ИГРОКИ:\n\n"
        for player in players:
            text += f"ID: {player['id']} - {player['name']}\n"
            text += f"  Пройдено: {len(player.get('completedDemons', []))}\n\n"
        self.players_text.delete(1.0, tk.END)
        self.players_text.insert(1.0, text)
        
    def update_future_text(self, future):
        text = "🔮 БУДУЩИЕ ДЕМОНЫ:\n\n"
        for demon in future:
            text += f"ID: {demon['id']} - {demon['name']}\n"
            text += f"  Прогресс: {len(demon.get('beatingPlayers', []))} игроков\n\n"
        self.future_text.delete(1.0, tk.END)
        self.future_text.insert(1.0, text)

    def save_demons(self, demons):
        try:
            if not os.path.exists(self.demons_file):
                 with open(self.demons_file, 'w', encoding='utf-8') as f:
                    f.write(f"const demons = {json.dumps(demons, indent=2, ensure_ascii=False)};")
                 return
            with open(self.demons_file, 'r', encoding='utf-8') as f:
                content = f.read()
            new_js = f"const demons = {json.dumps(demons, indent=2, ensure_ascii=False)};"
            pattern = r'const demons = \[.*?\];'
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(pattern, new_js, content, flags=re.DOTALL)
            else:
                content += "\n\n" + new_js
            with open(self.demons_file, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Save demons error: {e}")

    def save_players(self, players):
        try:
            if not os.path.exists(self.players_file):
                 with open(self.players_file, 'w', encoding='utf-8') as f:
                    f.write(f"const players = {json.dumps(players, indent=2, ensure_ascii=False)};")
                 return
            with open(self.players_file, 'r', encoding='utf-8') as f:
                content = f.read()
            new_js = f"const players = {json.dumps(players, indent=2, ensure_ascii=False)};"
            pattern = r'const players = \[.*?\];'
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(pattern, new_js, content, flags=re.DOTALL)
            else:
                content += "\n\n" + new_js
            with open(self.players_file, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Save players error: {e}")

    def save_future_demons(self, future):
        try:
            if not os.path.exists(self.future_demons_file):
                 with open(self.future_demons_file, 'w', encoding='utf-8') as f:
                    f.write(f"const futureDemons = {json.dumps(future, indent=2, ensure_ascii=False)};")
                 return
            with open(self.future_demons_file, 'r', encoding='utf-8') as f:
                content = f.read()
            new_js = f"const futureDemons = {json.dumps(future, indent=2, ensure_ascii=False)};"
            pattern = r'const futureDemons = \[.*?\];'
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(pattern, new_js, content, flags=re.DOTALL)
            else:
                content += "\n\n" + new_js
            with open(self.future_demons_file, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Save future demons error: {e}")

    def update_demon_list(self, demon_ids):
        try:
            if not os.path.exists(self.list_file):
                with open(self.list_file, 'w', encoding='utf-8') as f:
                    f.write(f"const demonList = {json.dumps(demon_ids)};")
                return
            with open(self.list_file, 'r', encoding='utf-8') as f:
                content = f.read()
            new_list = f"const demonList = {json.dumps(demon_ids)};"
            content = re.sub(r'const demonList = \[.*?\];', new_list, content, flags=re.DOTALL)
            with open(self.list_file, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            messagebox.showerror("Ошибка", f"List update error: {e}")

    # ADDITION METHODS
    def add_demon_gui(self):
        try:
            name = self.demon_name.get().strip()
            if not name: return
            demons = self.load_demons()
            players = self.load_players()
            
            next_id = max([d['id'] for d in demons] + [0]) + 1
            verifier_str = self.demon_verifier.get().strip()
            verify_date = self.demon_date.get()
            
            # Try to get verifier ID from players
            verifier_id = None
            if verifier_str:
                try:
                    verifier_id = int(verifier_str)
                except ValueError:
                    # If verifier is a name, try to find the player
                    for p in players:
                        if p['name'].lower() == verifier_str.lower():
                            verifier_id = p['id']
                            break
            
            new_demon = {
                "id": next_id,
                "name": name,
                "creator": self.demon_creator.get(),
                "verifier": verifier_id if verifier_id else verifier_str,
                "verifyDate": verify_date,
                "completers": []
            }
            
            # Add verifier as first completer if verifier is a player ID
            # Note: Verifier is NOT added to completedDemons - they get credit via verification
            if verifier_id:
                new_demon["completers"].append({"playerId": verifier_id, "date": verify_date})
            
            demons.append(new_demon)
            self.save_demons(demons)
            self.save_players(players)
            
            self.demon_name.delete(0, tk.END)
            self.demon_creator.delete(0, tk.END)
            self.demon_verifier.delete(0, tk.END)
            messagebox.showinfo("Успех", "Демон добавлен! Верификатор получил очки.")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def add_player_gui(self):
        try:
            name = self.player_name.get().strip()
            if not name: return
            players = self.load_players()
            next_id = max([p['id'] for p in players] + [0]) + 1
            new_player = {"id": next_id, "name": name, "completedDemons": []}
            players.append(new_player)
            self.save_players(players)
            self.player_name.delete(0, tk.END)
            messagebox.showinfo("Успех", "Игрок добавлен!")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def add_future_demon_gui(self):
        try:
            name = self.future_name.get().strip()
            if not name: return
            future = self.load_future_demons()
            next_id = max([d['id'] for d in future] + [0]) + 1
            new_future = {
                "id": next_id,
                "name": name,
                "creator": self.future_creator.get(),
                "difficulty": self.future_difficulty.get(),
                "description": self.future_description.get(1.0, tk.END).strip(),
                "beatingPlayers": []
            }
            future.append(new_future)
            self.save_future_demons(future)
            self.future_name.delete(0, tk.END)
            self.future_description.delete(1.0, tk.END)
            messagebox.showinfo("Успех", "Будущий демон добавлен!")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def add_beating_player_gui(self):
        try:
            d_str = self.beating_demon.get()
            p_str = self.beating_player.get()
            if not d_str or not p_str: return
            d_id = int(d_str.split(':')[0])
            p_id = int(p_str.split(':')[0])
            progress = self.beating_progress.get()
            date = self.beating_date.get()
            
            future = self.load_future_demons()
            for f in future:
                if f['id'] == d_id:
                    if 'beatingPlayers' not in f: f['beatingPlayers'] = []
                    # check existing
                    found = False
                    for bp in f['beatingPlayers']:
                        if bp['playerId'] == p_id:
                            bp['progress'] = progress
                            bp['lastUpdate'] = date
                            found = True
                            break
                    if not found:
                        f['beatingPlayers'].append({"playerId": p_id, "progress": progress, "lastUpdate": date})
                    break
            self.save_future_demons(future)
            messagebox.showinfo("Успех", "Прогресс сохранен!")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def add_completion_gui(self):
        try:
            d_str = self.completion_demon.get()
            p_str = self.completion_player.get()
            if not d_str or not p_str: return
            d_id = int(d_str.split(':')[0])
            p_id = int(p_str.split(':')[0])
            date = self.completion_date.get()

            demons = self.load_demons()
            players = self.load_players()

            # Find the demon to get verifier info
            demon_obj = None
            for d in demons:
                if d['id'] == d_id:
                    demon_obj = d
                    break

            # Update Demon
            for d in demons:
                if d['id'] == d_id:
                    if 'completers' not in d: d['completers'] = []
                    if not any(c['playerId'] == p_id for c in d['completers']):
                        d['completers'].append({"playerId": p_id, "date": date})
                    break

            # Update Player (who completed the demon)
            for p in players:
                if p['id'] == p_id:
                    if 'completedDemons' not in p: p['completedDemons'] = []
                    if d_id not in p['completedDemons']:
                        p['completedDemons'].append(d_id)
                    break

            # Check if the player is the verifier - if so, give verifier points
            if demon_obj and 'verifier' in demon_obj:
                verifier_id = demon_obj['verifier']
                if verifier_id == p_id:
                    # Player is the verifier, already gets the demon in completedDemons above
                    pass

            self.save_demons(demons)
            self.save_players(players)
            messagebox.showinfo("Успех", "Прохождение добавлено!")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def edit_demon_gui(self):
        try:
            d_str = self.demon_combobox.get()
            if not d_str: return
            d_id = int(d_str.split(':')[0])
            demons = self.load_demons()
            demon = next((d for d in demons if d['id'] == d_id), None)
            
            if not demon: return
            
            edit_win = tk.Toplevel(self.root)
            edit_win.title(f"Edit {demon['name']}")
            edit_win.geometry("300x200")
            
            ttk.Label(edit_win, text="Название").pack()
            name_ent = ttk.Entry(edit_win)
            name_ent.insert(0, demon['name'])
            name_ent.pack()
            
            ttk.Label(edit_win, text="Создатель").pack()
            creator_ent = ttk.Entry(edit_win)
            creator_ent.insert(0, demon['creator'])
            creator_ent.pack()
            
            def save():
                demon['name'] = name_ent.get()
                demon['creator'] = creator_ent.get()
                self.save_demons(demons)
                self.load_data()
                edit_win.destroy()
                
            ttk.Button(edit_win, text="Save", command=save).pack(pady=10)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def edit_player_gui(self):
        try:
            p_str = self.player_combobox.get()
            if not p_str: return
            p_id = int(p_str.split(':')[0])
            players = self.load_players()
            player = next((p for p in players if p['id'] == p_id), None)
            
            if not player: return
            
            edit_win = tk.Toplevel(self.root)
            edit_win.title(f"Edit {player['name']}")
            edit_win.geometry("300x150")
            
            ttk.Label(edit_win, text="Имя").pack()
            name_ent = ttk.Entry(edit_win)
            name_ent.insert(0, player['name'])
            name_ent.pack()
            
            def save():
                player['name'] = name_ent.get()
                self.save_players(players)
                self.load_data()
                edit_win.destroy()
                
            ttk.Button(edit_win, text="Save", command=save).pack(pady=10)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = DemonlistGUI(root)
    root.mainloop()