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
        
        # Инициализируем атрибуты чтобы избежать ошибок
        self.beating_demon = None
        self.beating_player = None
        self.beating_progress = None
        self.beating_date = None
        
        # Файлы
        self.demons_file = "js/demons.js"
        self.players_file = "js/players.js"
        self.future_demons_file = "js/futuredemons.js"
        self.list_file = "js/list.js"
        
        self.setup_styles()
        self.create_widgets()
        self.load_data()
        
    def setup_styles(self):
        self.style = ttk.Style()
        
        # Современная темная тема
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
        # Главный фрейм
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="🔥 DOLORES SQUAD DEMONLIST MANAGER", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Создаем notebook для вкладок
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True)
        
        # Вкладки
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
        notebook.add(view_frame, text="📊 Просмотр данных")
        
        # Создаем notebook внутри вкладки для разных типов данных
        view_notebook = ttk.Notebook(view_frame)
        view_notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Демоны
        demons_frame = ttk.Frame(view_notebook)
        view_notebook.add(demons_frame, text="👹 Демоны")
        
        demons_text = scrolledtext.ScrolledText(demons_frame, width=80, height=20, 
                                              font=('Consolas', 9), bg='#2d2d2d', fg='white',
                                              insertbackground='white')
        demons_text.pack(fill='both', expand=True, padx=5, pady=5)
        self.demons_text = demons_text
        
        # Игроки
        players_frame = ttk.Frame(view_notebook)
        view_notebook.add(players_frame, text="👤 Игроки")
        
        players_text = scrolledtext.ScrolledText(players_frame, width=80, height=20,
                                               font=('Consolas', 9), bg='#2d2d2d', fg='white',
                                               insertbackground='white')
        players_text.pack(fill='both', expand=True, padx=5, pady=5)
        self.players_text = players_text
        
        # Будущие демоны
        future_frame = ttk.Frame(view_notebook)
        view_notebook.add(future_frame, text="🔮 Будущие демоны")
        
        future_text = scrolledtext.ScrolledText(future_frame, width=80, height=20,
                                              font=('Consolas', 9), bg='#2d2d2d', fg='white',
                                              insertbackground='white')
        future_text.pack(fill='both', expand=True, padx=5, pady=5)
        self.future_text = future_text
        
        # Кнопка обновления
        refresh_btn = ttk.Button(view_frame, text="🔄 Обновить данные", command=self.load_data)
        refresh_btn.pack(pady=10)

    def create_demon_tab(self, notebook):
        demon_frame = ttk.Frame(notebook)
        notebook.add(demon_frame, text="👹 Добавить демона")
        
        # Заголовок
        ttk.Label(demon_frame, text="Добавление нового демона", style='Subtitle.TLabel').pack(pady=20)
        
        # Форма добавления демона
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
        
        # Разделитель
        separator = ttk.Separator(demon_frame, orient='horizontal')
        separator.pack(fill='x', pady=20, padx=30)
        
        # Список демонов для редактирования
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
        
        separator = ttk.Separator(player_frame, orient='horizontal')
        separator.pack(fill='x', pady=20, padx=30)
        
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
        
        # Добавление игрока проходящего демон
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

        # Кнопка обновления списков
        refresh_btn = ttk.Button(completion_frame, text="🔄 Обновить списки демонов и игроков", 
                               command=self.load_data)
        refresh_btn.pack(pady=10)
    
    def create_calculator_tab(self, notebook):
        calc_frame = ttk.Frame(notebook)
        notebook.add(calc_frame, text="🧮 Калькулятор очков")
        
        # Заголовок
        ttk.Label(calc_frame, text="Калькулятор очков демонлиста", style='Subtitle.TLabel').pack(pady=20)
        
        calc_container = ttk.Frame(calc_frame)
        calc_container.pack(pady=20, padx=30)
        
        # Ввод позиции
        ttk.Label(calc_container, text="Позиция в демонлисте:").grid(row=0, column=0, sticky='w', pady=10)
        self.position_entry = ttk.Entry(calc_container, width=15, font=('Segoe UI', 12))
        self.position_entry.grid(row=0, column=1, pady=10, padx=10)
        
        # Кнопка расчета
        calc_btn = ttk.Button(calc_container, text="🎯 Рассчитать очки", 
                             command=self.calculate_points)
        calc_btn.grid(row=0, column=2, padx=20)
        
        # Результат
        self.result_label = ttk.Label(calc_container, text="Очки: 0", 
                                    font=('Segoe UI', 14, 'bold'), foreground='#6bc5ff')
        self.result_label.grid(row=1, column=0, columnspan=3, pady=20)
        
        # Таблица топ-20 позиций
        ttk.Label(calc_container, text="Топ-20 позиций:", style='Subtitle.TLabel').grid(row=2, column=0, columnspan=3, pady=(30, 10))
        
        # Фрейм для таблицы
        table_frame = ttk.Frame(calc_container)
        table_frame.grid(row=3, column=0, columnspan=3, sticky='we', pady=10)
        
        # Создаем таблицу
        columns = ('#1', '#2', '#3', '#4', '#5')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=10)
        
        # Заголовки
        tree.heading('#1', text='Поз.')
        tree.heading('#2', text='Очки')
        tree.heading('#3', text='Поз.')
        tree.heading('#4', text='Очки')
        tree.heading('#5', text='Поз.')
        
        tree.column('#1', width=80, anchor='center')
        tree.column('#2', width=120, anchor='center')
        tree.column('#3', width=80, anchor='center')
        tree.column('#4', width=120, anchor='center')
        tree.column('#5', width=80, anchor='center')
        
        # Заполняем таблицу
        for i in range(0, 20, 5):
            values = []
            for j in range(5):
                pos = i + j + 1
                if pos <= 20:
                    points = self.calculate_points_for_position(pos)
                    if j == 0:
                        values.extend([f"{pos}", f"{points:.2f}"])
                    else:
                        values.extend([f"{pos}", f"{points:.2f}"])
                else:
                    values.extend(["", ""])
            tree.insert('', 'end', values=values)
        
        tree.pack(fill='both', expand=True)
        
        # Информация о формуле
        info_text = """📊 Формула расчета: Топ-1 = 500 очков, каждая следующая позиция теряет 19% от предыдущей"""
        info_label = ttk.Label(calc_container, text=info_text, font=('Segoe UI', 9), foreground='#cccccc')
        info_label.grid(row=4, column=0, columnspan=3, pady=20)
    
    def create_ranking_tab(self, notebook):
        ranking_frame = ttk.Frame(notebook)
        notebook.add(ranking_frame, text="🏆 Расстановка топа")
        
        # Заголовок
        ttk.Label(ranking_frame, text="Управление рейтингом демонов", style='Title.TLabel').pack(pady=20)
        
        # Основной контейнер
        main_container = ttk.Frame(ranking_frame)
        main_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Левая панель - список демонов
        left_frame = ttk.LabelFrame(main_container, text="📋 Все демоны", padding=10)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Поиск демонов
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(search_frame, text="Поиск:").pack(side='left')
        self.demon_search = ttk.Entry(search_frame, font=('Segoe UI', 10))
        self.demon_search.pack(side='left', fill='x', expand=True, padx=5)
        self.demon_search.bind('<KeyRelease>', self.filter_demons)
        
        # Список демонов с прокруткой
        demon_list_frame = ttk.Frame(left_frame)
        demon_list_frame.pack(fill='both', expand=True)
        
        self.demon_listbox = tk.Listbox(demon_list_frame, font=('Segoe UI', 10), bg='#2d2d2d', fg='white',
                                      selectbackground='#ff6b6b', selectforeground='white')
        demon_scrollbar = ttk.Scrollbar(demon_list_frame, orient='vertical', command=self.demon_listbox.yview)
        self.demon_listbox.configure(yscrollcommand=demon_scrollbar.set)
        
        self.demon_listbox.pack(side='left', fill='both', expand=True)
        demon_scrollbar.pack(side='right', fill='y')
        
        # Правая панель - текущий топ
        right_frame = ttk.LabelFrame(main_container, text="🏅 Текущий топ демонов", padding=10)
        right_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # Управление топом
        control_frame = ttk.Frame(right_frame)
        control_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Button(control_frame, text="⬆️ Поднять", 
                  command=lambda: self.move_demon(-1)).pack(side='left', padx=2)
        ttk.Button(control_frame, text="⬇️ Опустить", 
                  command=lambda: self.move_demon(1)).pack(side='left', padx=2)
        ttk.Button(control_frame, text="🎯 В топ", 
                  command=self.add_to_top).pack(side='left', padx=2)
        ttk.Button(control_frame, text="🗑️ Убрать", 
                  command=self.remove_from_top, style='Danger.TButton').pack(side='left', padx=2)
        
        # Список топа с прокруткой
        top_list_frame = ttk.Frame(right_frame)
        top_list_frame.pack(fill='both', expand=True)
        
        self.top_listbox = tk.Listbox(top_list_frame, font=('Segoe UI', 10), bg='#2d2d2d', fg='white',
                                    selectbackground='#6bc5ff', selectforeground='white')
        top_scrollbar = ttk.Scrollbar(top_list_frame, orient='vertical', command=self.top_listbox.yview)
        self.top_listbox.configure(yscrollcommand=top_scrollbar.set)
        
        self.top_listbox.pack(side='left', fill='both', expand=True)
        top_scrollbar.pack(side='right', fill='y')
        
        # Панель управления
        bottom_frame = ttk.Frame(ranking_frame)
        bottom_frame.pack(fill='x', pady=10)
        
        ttk.Button(bottom_frame, text="🔄 Обновить списки", 
                  command=self.update_ranking_lists).pack(side='left', padx=5)
        ttk.Button(bottom_frame, text="💾 Сохранить топ", 
                  command=self.save_top_list, style='Success.TButton').pack(side='left', padx=5)
        ttk.Button(bottom_frame, text="📊 Просмотреть топ", 
                  command=self.view_top_list).pack(side='left', padx=5)
        
        # Информация
        info_label = ttk.Label(ranking_frame, 
                              text="💡 Перетащите демонов между списками или используйте кнопки для управления топом",
                              font=('Segoe UI', 9), foreground='#cccccc')
        info_label.pack(pady=5)
        
    def create_code_editor_tab(self, notebook):
        editor_frame = ttk.Frame(notebook)
        notebook.add(editor_frame, text="📝 Редактор кода")
        
        # Заголовок
        ttk.Label(editor_frame, text="Редактор файлов демонлиста", style='Title.TLabel').pack(pady=20)
        
        # Выбор файла
        file_frame = ttk.Frame(editor_frame)
        file_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(file_frame, text="Выберите файл:").pack(side='left')
        self.file_selector = ttk.Combobox(file_frame, width=20, state="readonly", font=('Segoe UI', 10))
        self.file_selector['values'] = ['demons.js', 'players.js', 'futuredemons.js', 'list.js']
        self.file_selector.set('demons.js')
        self.file_selector.pack(side='left', padx=10)
        
        ttk.Button(file_frame, text="📂 Загрузить файл", 
                  command=self.load_file_for_edit).pack(side='left', padx=5)
        
        # Редактор кода
        editor_container = ttk.Frame(editor_frame)
        editor_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.code_editor = scrolledtext.ScrolledText(editor_container, 
                                                   font=('Consolas', 10), 
                                                   bg='#1e1e1e', 
                                                   fg='#d4d4d4',
                                                   insertbackground='white',
                                                   wrap=tk.NONE)
        self.code_editor.pack(fill='both', expand=True)
        
        # Панель управления редактором
        editor_controls = ttk.Frame(editor_frame)
        editor_controls.pack(fill='x', padx=20, pady=10)
        
        ttk.Button(editor_controls, text="💾 Сохранить файл", 
                  command=self.save_edited_file, style='Success.TButton').pack(side='left', padx=5)
        ttk.Button(editor_controls, text="🔄 Обновить из системы", 
                  command=self.reload_from_system).pack(side='left', padx=5)
        ttk.Button(editor_controls, text="🔍 Проверить синтаксис", 
                  command=self.validate_syntax).pack(side='left', padx=5)
        
        # Статус
        self.editor_status = ttk.Label(editor_frame, text="Готов к работе", font=('Segoe UI', 9))
        self.editor_status.pack(pady=5)

    def create_delete_tab(self, notebook):
        delete_frame = ttk.Frame(notebook)
        notebook.add(delete_frame, text="🗑️ Удаление")
        
        # Заголовок
        ttk.Label(delete_frame, text="Система удаления данных", style='Title.TLabel').pack(pady=20)
        
        # Контейнер для кнопок удаления
        delete_container = ttk.Frame(delete_frame)
        delete_container.pack(pady=20, padx=30)
        
        # Удаление демонов
        demon_delete_frame = ttk.LabelFrame(delete_container, text="👹 Удаление демонов", padding=15)
        demon_delete_frame.grid(row=0, column=0, padx=10, pady=10, sticky='we')
        
        ttk.Label(demon_delete_frame, text="Выберите демона:").pack(pady=5)
        self.delete_demon_combobox = ttk.Combobox(demon_delete_frame, width=30, state="readonly", font=('Segoe UI', 10))
        self.delete_demon_combobox.pack(pady=5)
        
        delete_demon_btn = ttk.Button(demon_delete_frame, text="🗑️ Удалить демона", 
                                    command=self.delete_demon_gui, style='Danger.TButton')
        delete_demon_btn.pack(pady=10)
        
        # Удаление игроков
        player_delete_frame = ttk.LabelFrame(delete_container, text="👤 Удаление игроков", padding=15)
        player_delete_frame.grid(row=0, column=1, padx=10, pady=10, sticky='we')
        
        ttk.Label(player_delete_frame, text="Выберите игрока:").pack(pady=5)
        self.delete_player_combobox = ttk.Combobox(player_delete_frame, width=30, state="readonly", font=('Segoe UI', 10))
        self.delete_player_combobox.pack(pady=5)
        
        delete_player_btn = ttk.Button(player_delete_frame, text="🗑️ Удалить игрока", 
                                     command=self.delete_player_gui, style='Danger.TButton')
        delete_player_btn.pack(pady=10)
        
        # Удаление будущих демонов
        future_delete_frame = ttk.LabelFrame(delete_container, text="🔮 Удаление будущих демонов", padding=15)
        future_delete_frame.grid(row=1, column=0, padx=10, pady=10, sticky='we')
        
        ttk.Label(future_delete_frame, text="Выберите будущего демона:").pack(pady=5)
        self.delete_future_combobox = ttk.Combobox(future_delete_frame, width=30, state="readonly", font=('Segoe UI', 10))
        self.delete_future_combobox.pack(pady=5)
        
        delete_future_btn = ttk.Button(future_delete_frame, text="🗑️ Удалить будущего демона", 
                                     command=self.delete_future_demon_gui, style='Danger.TButton')
        delete_future_btn.pack(pady=10)
        
        # Удаление прохождений
        completion_delete_frame = ttk.LabelFrame(delete_container, text="✅ Удаление прохождений", padding=15)
        completion_delete_frame.grid(row=1, column=1, padx=10, pady=10, sticky='we')
        
        ttk.Label(completion_delete_frame, text="Демон:").pack(pady=2)
        self.delete_completion_demon = ttk.Combobox(completion_delete_frame, width=25, state="readonly", font=('Segoe UI', 10))
        self.delete_completion_demon.pack(pady=2)
        
        ttk.Label(completion_delete_frame, text="Игрок:").pack(pady=2)
        self.delete_completion_player = ttk.Combobox(completion_delete_frame, width=25, state="readonly", font=('Segoe UI', 10))
        self.delete_completion_player.pack(pady=2)
        
        delete_completion_btn = ttk.Button(completion_delete_frame, text="🗑️ Удалить прохождение", 
                                         command=self.delete_completion_gui, style='Danger.TButton')
        delete_completion_btn.pack(pady=10)
        
        # Удаление игроков из будущих демонов
        beating_delete_frame = ttk.LabelFrame(delete_container, text="🎯 Удаление проходящих игроков", padding=15)
        beating_delete_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='we')
        
        ttk.Label(beating_delete_frame, text="Будущий демон:").pack(pady=2)
        self.delete_beating_demon = ttk.Combobox(beating_delete_frame, width=25, state="readonly", font=('Segoe UI', 10))
        self.delete_beating_demon.pack(pady=2)
        
        ttk.Label(beating_delete_frame, text="Игрок:").pack(pady=2)
        self.delete_beating_player = ttk.Combobox(beating_delete_frame, width=25, state="readonly", font=('Segoe UI', 10))
        self.delete_beating_player.pack(pady=2)
        
        delete_beating_btn = ttk.Button(beating_delete_frame, text="🗑️ Удалить игрока", 
                                      command=self.delete_beating_player_gui, style='Danger.TButton')
        delete_beating_btn.pack(pady=10)
        
        # Предупреждение
        warning_label = ttk.Label(delete_frame, 
                                text="⚠️ ВНИМАНИЕ: Удаление данных необратимо! Создавайте резервные копии.",
                                font=('Segoe UI', 10, 'bold'), 
                                foreground='#ff6b6b')
        warning_label.pack(pady=20)

    # МЕТОДЫ ДЛЯ СИСТЕМЫ РАССТАНОВКИ ТОПА
    def update_ranking_lists(self):
        """Обновляет списки демонов и топа"""
        try:
            demons = self.load_demons()
            top_list = self.load_top_list()
            
            # Очищаем списки
            self.demon_listbox.delete(0, tk.END)
            self.top_listbox.delete(0, tk.END)
            
            # Заполняем список всех демонов
            demon_ids_in_top = set(top_list)
            for demon in demons:
                display_text = f"{demon['id']}: {demon['name']} (by {demon['creator']})"
                if demon['id'] not in demon_ids_in_top:
                    self.demon_listbox.insert(tk.END, display_text)
            
            # Заполняем список топа
            for demon_id in top_list:
                demon = next((d for d in demons if d['id'] == demon_id), None)
                if demon:
                    display_text = f"{demon['id']}: {demon['name']}"
                    self.top_listbox.insert(tk.END, display_text)
                    
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить списки: {e}")
            
    def filter_demons(self, event=None):
        """Фильтрует демонов по поисковому запросу"""
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
        """Загружает текущий список топа"""
        try:
            with open(self.list_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            match = re.search(r'const demonList = (\[.*?\]);', content, re.DOTALL)
            if match:
                return json.loads(match.group(1))
            return []
        except:
            return []
            
    def add_to_top(self):
        """Добавляет выбранного демона в топ"""
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
        """Убирает выбранного демона из топа"""
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
        """Перемещает демона в топе вверх или вниз"""
        try:
            selection = self.top_listbox.curselection()
            if not selection:
                messagebox.showwarning("Предупреждение", "Выберите демона для перемещения!")
                return
                
            index = selection[0]
            top_list = self.load_top_list()
            
            if direction == -1 and index > 0:  # Вверх
                top_list[index], top_list[index-1] = top_list[index-1], top_list[index]
            elif direction == 1 and index < len(top_list) - 1:  # Вниз
                top_list[index], top_list[index+1] = top_list[index+1], top_list[index]
            else:
                return
                
            self.save_top_list_internal(top_list)
            self.update_ranking_lists()
            self.top_listbox.select_set(index + direction)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось переместить демона: {e}")
            
    def save_top_list(self):
        """Сохраняет текущий топ"""
        try:
            top_list = self.load_top_list()
            self.save_top_list_internal(top_list)
            messagebox.showinfo("Успех", "Топ демонов сохранен!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить топ: {e}")
            
    def save_top_list_internal(self, top_list):
        """Внутренний метод сохранения топа"""
        with open(self.list_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_list = f"const demonList = {json.dumps(top_list)};"
        content = re.sub(r'const demonList = \[.*?\];', new_list, content, flags=re.DOTALL)
        
        with open(self.list_file, 'w', encoding='utf-8') as f:
            f.write(content)
            
    def view_top_list(self):
        """Показывает текущий топ в отдельном окне"""
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

    # МЕТОДЫ ДЛЯ РЕДАКТОРА КОДА
    def load_file_for_edit(self):
        """Загружает выбранный файл в редактор"""
        try:
            filename = self.file_selector.get()
            filepath = f"js/{filename}"
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.code_editor.delete(1.0, tk.END)
            self.code_editor.insert(1.0, content)
            self.editor_status.config(text=f"Файл {filename} загружен успешно")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")
            
    def save_edited_file(self):
        """Сохраняет изменения из редактора в файл"""
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
        """Перезагружает данные из системы в редактор"""
        try:
            filename = self.file_selector.get()
            
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
                with open(self.list_file, 'r', encoding='utf-8') as f:
                    content = f.read()
            
            self.code_editor.delete(1.0, tk.END)
            self.code_editor.insert(1.0, content)
            self.editor_status.config(text=f"Данные из системы загружены в {filename}")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")
            
    def validate_syntax(self):
        """Проверяет синтаксис JSON в редакторе"""
        try:
            content = self.code_editor.get(1.0, tk.END)
            
            # Пытаемся найти JSON в содержимом
            json_match = re.search(r'=\s*(\[.*\]|{.*});', content, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                json.loads(json_str)  # Проверяем валидность JSON
                self.editor_status.config(text="✅ Синтаксис JSON корректен")
                messagebox.showinfo("Проверка", "Синтаксис JSON корректен!")
            else:
                self.editor_status.config(text="⚠️ JSON не найден в файле")
                
        except json.JSONDecodeError as e:
            self.editor_status.config(text="❌ Ошибка в синтаксисе JSON")
            messagebox.showerror("Ошибка синтаксиса", f"Некорректный JSON: {e}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось проверить синтаксис: {e}")

    # МЕТОДЫ УДАЛЕНИЯ
    def delete_demon_gui(self):
        """Удаляет выбранного демона"""
        try:
            demon_str = self.delete_demon_combobox.get()
            if not demon_str:
                messagebox.showwarning("Предупреждение", "Выберите демона для удаления!")
                return
            
            demon_id = int(demon_str.split(':')[0])
            demon_name = demon_str.split(':', 1)[1].strip()
            
            # Подтверждение удаления
            if not messagebox.askyesno("Подтверждение", 
                                     f"Вы уверены, что хотите удалить демона:\n{demon_name}?\n\nЭто действие нельзя отменить!"):
                return
            
            demons = self.load_demons()
            players = self.load_players()
            
            # Удаляем демона из списка
            demons = [d for d in demons if d['id'] != demon_id]
            
            # Удаляем демона из списка пройденных у всех игроков
            for player in players:
                if demon_id in player['completedDemons']:
                    player['completedDemons'].remove(demon_id)
            
            self.save_demons(demons)
            self.save_players(players)
            
            # Обновляем основной список демонов
            demon_ids = [d['id'] for d in demons]
            self.update_demon_list(demon_ids)
            
            messagebox.showinfo("Успех", f"Демон '{demon_name}' успешно удален!")
            self.load_data()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить демона: {e}")
    
    def delete_player_gui(self):
        """Удаляет выбранного игрока"""
        try:
            player_str = self.delete_player_combobox.get()
            if not player_str:
                messagebox.showwarning("Предупреждение", "Выберите игрока для удаления!")
                return
            
            player_id = int(player_str.split(':')[0])
            player_name = player_str.split(':', 1)[1].strip()
            
            # Подтверждение удаления
            if not messagebox.askyesno("Подтверждение", 
                                     f"Вы уверены, что хотите удалить игрока:\n{player_name}?\n\nЭто действие нельзя отменить!"):
                return
            
            players = self.load_players()
            demons = self.load_demons()
            future_demons = self.load_future_demons()
            
            # Удаляем игрока из списка
            players = [p for p in players if p['id'] != player_id]
            
            # Удаляем прохождения игрока из всех демонов
            for demon in demons:
                demon['completers'] = [comp for comp in demon['completers'] if comp['playerId'] != player_id]
            
            # Удаляем игрока из будущих демонов
            for demon in future_demons:
                if 'beatingPlayers' in demon:
                    demon['beatingPlayers'] = [bp for bp in demon['beatingPlayers'] if bp['playerId'] != player_id]
            
            self.save_players(players)
            self.save_demons(demons)
            self.save_future_demons(future_demons)
            
            messagebox.showinfo("Успех", f"Игрок '{player_name}' успешно удален!")
            self.load_data()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить игрока: {e}")
    
    def delete_future_demon_gui(self):
        """Удаляет выбранного будущего демона"""
        try:
            future_str = self.delete_future_combobox.get()
            if not future_str:
                messagebox.showwarning("Предупреждение", "Выберите будущего демона для удаления!")
                return
            
            future_id = int(future_str.split(':')[0])
            future_name = future_str.split(':', 1)[1].strip()
            
            # Подтверждение удаления
            if not messagebox.askyesno("Подтверждение", 
                                     f"Вы уверены, что хотите удалить будущего демона:\n{future_name}?\n\nЭто действие нельзя отменить!"):
                return
            
            future_demons = self.load_future_demons()
            future_demons = [fd for fd in future_demons if fd['id'] != future_id]
            
            self.save_future_demons(future_demons)
            
            messagebox.showinfo("Успех", f"Будущий демон '{future_name}' успешно удален!")
            self.load_data()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить будущего демона: {e}")
    
    def delete_completion_gui(self):
        """Удаляет прохождение демона игроком"""
        try:
            demon_str = self.delete_completion_demon.get()
            player_str = self.delete_completion_player.get()
            
            if not all([demon_str, player_str]):
                messagebox.showwarning("Предупреждение", "Выберите демона и игрока!")
                return
            
            demon_id = int(demon_str.split(':')[0])
            player_id = int(player_str.split(':')[0])
            demon_name = demon_str.split(':', 1)[1].strip()
            player_name = player_str.split(':', 1)[1].strip()
            
            # Подтверждение удаления
            if not messagebox.askyesno("Подтверждение", 
                                     f"Удалить прохождение демона {demon_name}\nигроком {player_name}?"):
                return
            
            demons = self.load_demons()
            players = self.load_players()
            
            # Удаляем прохождение из демона
            for demon in demons:
                if demon['id'] == demon_id:
                    demon['completers'] = [comp for comp in demon['completers'] if comp['playerId'] != player_id]
                    break
            
            # Удаляем демона из списка игрока
            for player in players:
                if player['id'] == player_id:
                    if demon_id in player['completedDemons']:
                        player['completedDemons'].remove(demon_id)
                    break
            
            self.save_demons(demons)
            self.save_players(players)
            
            messagebox.showinfo("Успех", "Прохождение успешно удалено!")
            self.load_data()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить прохождение: {e}")
    
    def delete_beating_player_gui(self):
        """Удаляет игрока из списка проходящих будущий демон"""
        try:
            demon_str = self.delete_beating_demon.get()
            player_str = self.delete_beating_player.get()
            
            if not all([demon_str, player_str]):
                messagebox.showwarning("Предупреждение", "Выберите будущего демона и игрока!")
                return
            
            demon_id = int(demon_str.split(':')[0])
            player_id = int(player_str.split(':')[0])
            demon_name = demon_str.split(':', 1)[1].strip()
            player_name = player_str.split(':', 1)[1].strip()
            
            # Подтверждение удаления
            if not messagebox.askyesno("Подтверждение", 
                                     f"Удалить игрока {player_name}\nиз проходящих демон {demon_name}?"):
                return
            
            future_demons = self.load_future_demons()
            
            for demon in future_demons:
                if demon['id'] == demon_id and 'beatingPlayers' in demon:
                    demon['beatingPlayers'] = [bp for bp in demon['beatingPlayers'] if bp['playerId'] != player_id]
                    break
            
            self.save_future_demons(future_demons)
            
            messagebox.showinfo("Успех", "Игрок успешно удален из проходящих!")
            self.load_data()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить игрока: {e}")

    # ОСНОВНЫЕ МЕТОДЫ РАБОТЫ С ДАННЫМИ
    def calculate_points_for_position(self, position):
        """Рассчитывает очки для позиции по формуле"""
        if position < 1:
            return 0
        base_points = 500.0
        decay_rate = 0.19  # 19%
        
        points = base_points
        for i in range(2, position + 1):
            points *= (1 - decay_rate)
        
        return points
    
    def calculate_points(self):
        """Рассчитывает очки для введенной позиции"""
        try:
            position = int(self.position_entry.get())
            if position < 1:
                messagebox.showwarning("Ошибка", "Позиция должна быть больше 0!")
                return
            
            points = self.calculate_points_for_position(position)
            self.result_label.config(text=f"Очки за позицию {position}: {points:.2f}")
            
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректную позицию!")

    def load_data(self):
        """Загружает все данные и обновляет интерфейс"""
        try:
            demons = self.load_demons()
            players = self.load_players()
            future_demons = self.load_future_demons()
            
            # Обновляем текстовые поля
            self.update_demons_text(demons)
            self.update_players_text(players)
            self.update_future_text(future_demons)
            
            # ОБНОВЛЯЕМ ВСЕ КОМБОБОКСЫ
            self.update_all_comboboxes(demons, players, future_demons)
            
            # Обновляем списки для расстановки топа
            if hasattr(self, 'demon_listbox'):
                self.update_ranking_lists()
            
        except Exception as e:
            if "'DemonlistGUI' object has no attribute" not in str(e):
                messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")
    
    def update_all_comboboxes(self, demons, players, future_demons):
        """Обновляет все комбобоксы в программе"""
        try:
            # Значения для комбобоксов
            demon_values = [f"{d['id']}: {d['name']}" for d in demons]
            player_values = [f"{p['id']}: {p['name']}" for p in players]
            future_values = [f"{d['id']}: {d['name']}" for d in future_demons]
            
            # Комбобоксы для прохождений
            if hasattr(self, 'completion_demon') and self.completion_demon:
                self.completion_demon['values'] = demon_values
            if hasattr(self, 'completion_player') and self.completion_player:
                self.completion_player['values'] = player_values
            
            # Комбобоксы для редактирования
            if hasattr(self, 'demon_combobox') and self.demon_combobox:
                self.demon_combobox['values'] = demon_values
            if hasattr(self, 'player_combobox') and self.player_combobox:
                self.player_combobox['values'] = player_values
            
            # Комбобоксы для будущих демонов
            if hasattr(self, 'beating_demon') and self.beating_demon:
                self.beating_demon['values'] = future_values
            if hasattr(self, 'beating_player') and self.beating_player:
                self.beating_player['values'] = player_values
            
            # Комбобоксы для удаления
            if hasattr(self, 'delete_demon_combobox') and self.delete_demon_combobox:
                self.delete_demon_combobox['values'] = demon_values
            if hasattr(self, 'delete_player_combobox') and self.delete_player_combobox:
                self.delete_player_combobox['values'] = player_values
            if hasattr(self, 'delete_future_combobox') and self.delete_future_combobox:
                self.delete_future_combobox['values'] = future_values
            if hasattr(self, 'delete_completion_demon') and self.delete_completion_demon:
                self.delete_completion_demon['values'] = demon_values
            if hasattr(self, 'delete_completion_player') and self.delete_completion_player:
                self.delete_completion_player['values'] = player_values
            if hasattr(self, 'delete_beating_demon') and self.delete_beating_demon:
                self.delete_beating_demon['values'] = future_values
            if hasattr(self, 'delete_beating_player') and self.delete_beating_player:
                self.delete_beating_player['values'] = player_values
                
        except Exception as e:
            print(f"Ошибка при обновлении комбобоксов: {e}")
    
    def load_demons(self):
        try:
            with open(self.demons_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            match = re.search(r'const demons = (\[.*?\]);', content, re.DOTALL)
            if match:
                demons_json = match.group(1)
                demons_json = demons_json.replace("'", '"')
                demons_json = re.sub(r'(\w+):', r'"\1":', demons_json)
                demons_data = json.loads(demons_json)
                return demons_data
            return []
        except Exception as e:
            print(f"Ошибка загрузки демонов: {e}")
            return []
    
    def load_players(self):
        try:
            with open(self.players_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            match = re.search(r'const players = (\[.*?\]);', content, re.DOTALL)
            if match:
                players_json = match.group(1)
                players_json = players_json.replace("'", '"')
                players_json = re.sub(r'(\w+):', r'"\1":', players_json)
                players_data = json.loads(players_json)
                return players_data
            return []
        except Exception as e:
            print(f"Ошибка загрузки игроков: {e}")
            return []
    
    def load_future_demons(self):
        try:
            with open(self.future_demons_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            match = re.search(r'const futureDemons = (\[.*?\]);', content, re.DOTALL)
            if match:
                future_json = match.group(1)
                future_json = future_json.replace("'", '"')
                future_json = re.sub(r'(\w+):', r'"\1":', future_json)
                return json.loads(future_json)
            return []
        except Exception as e:
            print(f"Ошибка загрузки будущих демонов: {e}")
            return []
    
    def update_demons_text(self, demons):
        text = "👹 ВСЕ ДЕМОНЫ:\n\n"
        for demon in demons:
            text += f"ID: {demon['id']}\n"
            text += f"  Название: {demon['name']}\n"
            text += f"  Создатель: {demon['creator']}\n"
            text += f"  Верификатор: {demon['verifier']}\n"
            text += f"  Дата верификации: {demon['verifyDate']}\n"
            text += f"  Прошли: {len(demon['completers'])} игроков\n"
            if demon['completers']:
                text += "  Прошедшие игроки:\n"
                for comp in demon['completers']:
                    text += f"    - Игрок ID: {comp['playerId']}, Дата: {comp['date']}\n"
            text += "\n"
        
        self.demons_text.delete(1.0, tk.END)
        self.demons_text.insert(1.0, text)
    
    def update_players_text(self, players):
        text = "👤 ВСЕ ИГРОКИ:\n\n"
        for player in players:
            text += f"ID: {player['id']}\n"
            text += f"  Имя: {player['name']}\n"
            text += f"  Пройдено демонов: {len(player['completedDemons'])}\n"
            if player['completedDemons']:
                text += f"  Пройденные демоны: {player['completedDemons']}\n"
            text += "\n"
        
        self.players_text.delete(1.0, tk.END)
        self.players_text.insert(1.0, text)
    
    def update_future_text(self, future_demons):
        text = "🔮 БУДУЩИЕ ДЕМОНЫ:\n\n"
        for demon in future_demons:
            text += f"ID: {demon['id']}\n"
            text += f"  Название: {demon['name']}\n"
            text += f"  Создатель: {demon['creator']}\n"
            text += f"  Сложность: {demon['difficulty']}\n"
            text += f"  Описание: {demon['description']}\n"
            text += f"  Игроков проходят: {len(demon.get('beatingPlayers', []))}\n"
            if demon.get('beatingPlayers'):
                for bp in demon['beatingPlayers']:
                    text += f"    - Игрок ID: {bp['playerId']}, Прогресс: {bp['progress']}%, Обновлено: {bp['lastUpdate']}\n"
            text += "\n"
        
        self.future_text.delete(1.0, tk.END)
        self.future_text.insert(1.0, text)

    # ИСПРАВЛЕННЫЕ МЕТОДЫ СОХРАНЕНИЯ
    def save_demons(self, demons):
        """Сохраняет демонов, сохраняя структуру исходного файла"""
        try:
            with open(self.demons_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Находим и заменяем только массив demons
            new_demons_js = f"const demons = {json.dumps(demons, indent=2, ensure_ascii=False)};"
            
            # Используем регулярное выражение для замены именно массива demons
            pattern = r'const demons = \[.*?\];'
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(pattern, new_demons_js, content, flags=re.DOTALL)
            else:
                # Если не нашли старый массив, добавляем новый (сохраняя остальное содержимое)
                content = content + "\n\n" + new_demons_js
            
            with open(self.demons_file, 'w', encoding='utf-8') as f:
                f.write(content)
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить демонов: {e}")

    def save_players(self, players):
        """Сохраняет игроков, сохраняя структуру исходного файла"""
        try:
            with open(self.players_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Находим и заменяем только массив players
            new_players_js = f"const players = {json.dumps(players, indent=2, ensure_ascii=False)};"
            
            # Используем регулярное выражение для замены именно массива players
            pattern = r'const players = \[.*?\];'
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(pattern, new_players_js, content, flags=re.DOTALL)
            else:
                # Если не нашли старый массив, добавляем новый (сохраняя остальное содержимое)
                content = content + "\n\n" + new_players_js
            
            with open(self.players_file, 'w', encoding='utf-8') as f:
                f.write(content)
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить игроков: {e}")

    def save_future_demons(self, future_demons):
        """Сохраняет будущих демонов, сохраняя структуру исходного файла"""
        try:
            with open(self.future_demons_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Находим и заменяем только массив futureDemons
            new_future_js = f"const futureDemons = {json.dumps(future_demons, indent=2, ensure_ascii=False)};"
            
            # Используем регулярное выражение для замены именно массива futureDemons
            pattern = r'const futureDemons = \[.*?\];'
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(pattern, new_future_js, content, flags=re.DOTALL)
            else:
                # Если не нашли старый массив, добавляем новый (сохраняя остальное содержимое)
                content = content + "\n\n" + new_future_js
            
            with open(self.future_demons_file, 'w', encoding='utf-8') as f:
                f.write(content)
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить будущих демонов: {e}")

    # МЕТОДЫ ДОБАВЛЕНИЯ ДАННЫХ
    def add_demon_gui(self):
        try:
            name = self.demon_name.get().strip()
            creator = self.demon_creator.get().strip()
            verifier = self.demon_verifier.get().strip()
            date = self.demon_date.get().strip()
            
            if not all([name, creator, verifier, date]):
                messagebox.showwarning("Предупреждение", "Все поля должны быть заполнены!")
                return
            
            demons = self.load_demons()
            next_id = max([d['id'] for d in demons]) + 1 if demons else 1
            
            demon = {
                "id": next_id,
                "name": name,
                "creator": creator,
                "verifier": int(verifier),
                "verifyDate": date,
                "completers": [{"playerId": int(verifier), "date": date}]
            }
            
            demons.append(demon)
            self.save_demons(demons)
            
            # Обновляем список демонов
            demon_ids = [d['id'] for d in demons]
            self.update_demon_list(demon_ids)
            
            messagebox.showinfo("Успех", f"Демон '{name}' добавлен с ID {next_id}")
            
            # Очищаем поля и обновляем данные
            self.demon_name.delete(0, tk.END)
            self.demon_creator.delete(0, tk.END)
            self.demon_verifier.delete(0, tk.END)
            self.demon_date.delete(0, tk.END)
            self.demon_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
            
            self.load_data()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить демона: {e}")
    
    def add_player_gui(self):
        try:
            name = self.player_name.get().strip()
            
            if not name:
                messagebox.showwarning("Предупреждение", "Введите имя игрока!")
                return
            
            players = self.load_players()
            next_id = max([p['id'] for p in players]) + 1 if players else 1
            
            player = {
                "id": next_id,
                "name": name,
                "completedDemons": []
            }
            
            players.append(player)
            self.save_players(players)
            
            messagebox.showinfo("Успех", f"Игрок '{name}' добавлен с ID {next_id}")
            
            # Очищаем поле и обновляем данные
            self.player_name.delete(0, tk.END)
            self.load_data()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить игрока: {e}")
    
    def add_future_demon_gui(self):
        try:
            name = self.future_name.get().strip()
            creator = self.future_creator.get().strip()
            difficulty = self.future_difficulty.get().strip()
            description = self.future_description.get(1.0, tk.END).strip()
            
            if not all([name, creator, difficulty, description]):
                messagebox.showwarning("Предупреждение", "Все поля должны быть заполнены!")
                return
            
            future_demons = self.load_future_demons()
            next_id = max([d['id'] for d in future_demons]) + 1 if future_demons else 1
            
            future_demon = {
                "id": next_id,
                "name": name,
                "creator": creator,
                "difficulty": difficulty,
                "description": description,
                "beatingPlayers": []
            }
            
            future_demons.append(future_demon)
            self.save_future_demons(future_demons)
            
            messagebox.showinfo("Успех", f"Будущий демон '{name}' добавлен с ID {next_id}")
            
            # Очищаем поля и обновляем данные
            self.future_name.delete(0, tk.END)
            self.future_creator.delete(0, tk.END)
            self.future_difficulty.delete(0, tk.END)
            self.future_description.delete(1.0, tk.END)
            
            self.load_data()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить будущего демона: {e}")
    
    def add_completion_gui(self):
        try:
            demon_str = self.completion_demon.get()
            player_str = self.completion_player.get()
            date = self.completion_date.get().strip()
            
            if not all([demon_str, player_str, date]):
                messagebox.showwarning("Предупреждение", "Все поля должны быть заполнены!")
                return
            
            demon_id = int(demon_str.split(':')[0])
            player_id = int(player_str.split(':')[0])
            
            demons = self.load_demons()
            players = self.load_players()
            
            # Добавляем прохождение к демону
            for demon in demons:
                if demon['id'] == demon_id:
                    if not any(comp['playerId'] == player_id for comp in demon['completers']):
                        demon['completers'].append({
                            "playerId": player_id,
                            "date": date
                        })
                    break
            
            # Добавляем демона к игроку
            for player in players:
                if player['id'] == player_id:
                    if demon_id not in player['completedDemons']:
                        player['completedDemons'].append(demon_id)
                    break
            
            self.save_demons(demons)
            self.save_players(players)
            
            messagebox.showinfo("Успех", "Прохождение успешно добавлено!")
            
            # Очищаем поля и обновляем данные
            self.completion_demon.set('')
            self.completion_player.set('')
            self.completion_date.delete(0, tk.END)
            self.completion_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
            
            self.load_data()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить прохождение: {e}")

    def add_beating_player_gui(self):
        try:
            demon_str = self.beating_demon.get()
            player_str = self.beating_player.get()
            progress = self.beating_progress.get().strip()
            date = self.beating_date.get().strip()
            
            if not all([demon_str, player_str, progress, date]):
                messagebox.showwarning("Предупреждение", "Все поля должны быть заполнены!")
                return
            
            demon_id = int(demon_str.split(':')[0])
            player_id = int(player_str.split(':')[0])
            progress_val = int(progress)
            
            future_demons = self.load_future_demons()
            
            for demon in future_demons:
                if demon['id'] == demon_id:
                    # Инициализируем beatingPlayers если его нет
                    if 'beatingPlayers' not in demon:
                        demon['beatingPlayers'] = []
                    
                    # Проверяем, есть ли уже этот игрок
                    existing_player = None
                    for i, bp in enumerate(demon['beatingPlayers']):
                        if bp['playerId'] == player_id:
                            existing_player = i
                            break
                    
                    if existing_player is not None:
                        # Обновляем существующего игрока
                        demon['beatingPlayers'][existing_player]['progress'] = progress_val
                        demon['beatingPlayers'][existing_player]['lastUpdate'] = date
                    else:
                        # Добавляем нового игрока
                        demon['beatingPlayers'].append({
                            "playerId": player_id,
                            "progress": progress_val,
                            "lastUpdate": date
                        })
                    break
            
            self.save_future_demons(future_demons)
            
            messagebox.showinfo("Успех", "Игрок добавлен/обновлен в проходящих демон!")
            
            # Очищаем поля
            self.beating_demon.set('')
            self.beating_player.set('')
            self.beating_progress.delete(0, tk.END)
            self.beating_date.delete(0, tk.END)
            self.beating_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
            
            self.load_data()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить игрока: {e}")

    def edit_demon_gui(self):
        try:
            demon_str = self.demon_combobox.get()
            if not demon_str:
                messagebox.showwarning("Предупреждение", "Выберите демона для редактирования!")
                return
            
            demon_id = int(demon_str.split(':')[0])
            demons = self.load_demons()
            
            for demon in demons:
                if demon['id'] == demon_id:
                    # Создаем окно редактирования
                    self.create_edit_demon_window(demon, demons)
                    break
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось редактировать демона: {e}")
    
    def edit_player_gui(self):
        try:
            player_str = self.player_combobox.get()
            if not player_str:
                messagebox.showwarning("Предупреждение", "Выберите игрока для редактирования!")
                return
            
            player_id = int(player_str.split(':')[0])
            players = self.load_players()
            
            for player in players:
                if player['id'] == player_id:
                    # Создаем окно редактирования
                    self.create_edit_player_window(player, players)
                    break
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось редактировать игрока: {e}")
    
    def create_edit_demon_window(self, demon, demons):
        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Редактирование демона: {demon['name']}")
        edit_window.geometry("400x300")
        edit_window.configure(bg='#2d2d2d')
        
        ttk.Label(edit_window, text="Название:").pack(pady=5)
        name_entry = ttk.Entry(edit_window, width=30, font=('Segoe UI', 10))
        name_entry.insert(0, demon['name'])
        name_entry.pack(pady=5)
        
        ttk.Label(edit_window, text="Создатель:").pack(pady=5)
        creator_entry = ttk.Entry(edit_window, width=30, font=('Segoe UI', 10))
        creator_entry.insert(0, demon['creator'])
        creator_entry.pack(pady=5)
        
        def save_changes():
            demon['name'] = name_entry.get().strip()
            demon['creator'] = creator_entry.get().strip()
            self.save_demons(demons)
            messagebox.showinfo("Успех", "Демон обновлен!")
            edit_window.destroy()
            self.load_data()
        
        ttk.Button(edit_window, text="💾 Сохранить", command=save_changes).pack(pady=20)
    
    def create_edit_player_window(self, player, players):
        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Редактирование игрока: {player['name']}")
        edit_window.geometry("400x200")
        edit_window.configure(bg='#2d2d2d')
        
        ttk.Label(edit_window, text="Имя игрока:").pack(pady=5)
        name_entry = ttk.Entry(edit_window, width=30, font=('Segoe UI', 10))
        name_entry.insert(0, player['name'])
        name_entry.pack(pady=5)
        
        def save_changes():
            player['name'] = name_entry.get().strip()
            self.save_players(players)
            messagebox.showinfo("Успех", "Игрок обновлен!")
            edit_window.destroy()
            self.load_data()
        
        ttk.Button(edit_window, text="💾 Сохранить", command=save_changes).pack(pady=20)

    def update_demon_list(self, demon_ids):
        """Обновляет список демонов в list.js"""
        try:
            with open(self.list_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_list = f"const demonList = {json.dumps(demon_ids)};"
            content = re.sub(r'const demonList = \[.*?\];', new_list, content, flags=re.DOTALL)
            
            with open(self.list_file, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить список демонов: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DemonlistGUI(root)
    root.mainloop()