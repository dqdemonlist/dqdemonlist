import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import json
import re
from datetime import datetime
import os
import shutil
from typing import List, Dict, Any

class ModernDemonlistGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔥 Dolores Squad Demonlist Manager v2.0")
        self.root.geometry("1280x800")
        self.root.minsize(1000, 700)
        self.root.configure(bg='#0f0f0f')

        # Система тем
        self.is_dark = True
        self.setup_styles()
        self.create_widgets()
        self.load_data()

        # Авто-бэкап при запуске
        self.create_backup()

    def create_backup(self):
        """Создаёт бэкап всех данных при запуске"""
        backup_dir = "backups"
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        for f in ["js/demons.js", "js/players.js", "js/futuredemons.js", "js/list.js"]:
            if os.path.exists(f):
                shutil.copy2(f, f"{backup_dir}/{os.path.basename(f)}.{timestamp}.bak")

    def setup_styles(self):
        """Настройка современных стилей"""
        self.style = ttk.Style()
        self.update_theme()

        # Общие настройки
        self.style.configure('TFrame', background='#0f0f0f')
        self.style.configure('TNotebook', background='#0f0f0f', borderwidth=0)
        self.style.configure('TNotebook.Tab', 
            background='#2d2d2d', 
            foreground='#ffffff',
            padding=[20, 8],
            font=('Inter', 11, 'bold')
        )
        self.style.map('TNotebook.Tab',
            background=[('selected', '#ff4757')],
            foreground=[('selected', '#000000')]
        )

        # Кнопки
        self.style.configure('Primary.TButton', font=('Inter', 10, 'bold'), padding=10)
        self.style.configure('Success.TButton', font=('Inter', 10, 'bold'), padding=10)
        self.style.configure('Danger.TButton', font=('Inter', 10, 'bold'), padding=10)

    def update_theme(self):
        bg = '#0f0f0f' if self.is_dark else '#ffffff'
        fg = '#ffffff' if self.is_dark else '#000000'
        secondary = '#2d2d2d' if self.is_dark else '#f0f0f0'
        accent = '#ff4757'

        self.style.map('Primary.TButton',
            background=[('active', accent)],
            foreground=[('!disabled', 'white')]
        )
        self.style.map('Success.TButton',
            background=[('active', '#28a745')],
            foreground=[('!disabled', 'white')]
        )
        self.style.map('Danger.TButton',
            background=[('active', '#dc3545')],
            foreground=[('!disabled', 'white')]
        )

    def create_widgets(self):
        # Главный контейнер
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Заголовок с логотипом
        header = ttk.Frame(main_frame)
        header.pack(fill='x', pady=(0, 20))
        title = tk.Label(header, text="🔥 Dolores Squad Demonlist Manager", 
                        font=('Inter', 24, 'bold'), 
                        fg='#ff4757', bg='#0f0f0f')
        title.pack(side='left')
        
        # Кнопка смены темы
        theme_btn = tk.Button(header, text="🌙", command=self.toggle_theme,
                             font=('Inter', 14), bg='#2d2d2d', fg='white',
                             relief='flat', padx=10, pady=5)
        theme_btn.pack(side='right')

        # Notebook
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True)

        # Создаём вкладки
        self.create_dashboard_tab()
        self.create_demons_tab()
        self.create_players_tab()
        self.create_future_tab()
        self.create_ranking_tab()
        self.create_activity_log_tab()

    def toggle_theme(self):
        self.is_dark = not self.is_dark
        bg = '#0f0f0f' if self.is_dark else '#ffffff'
        self.root.configure(bg=bg)
        self.update_theme()

    # === ВКЛАДКИ ===
    def create_dashboard_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📊 Dashboard")

        # Статистика
        stats_frame = ttk.Frame(tab)
        stats_frame.pack(fill='x', padx=20, pady=20)

        self.stats_labels = {}
        for i, (name, key) in enumerate([
            ("Всего демонов", "demons"),
            ("Игроков", "players"),
            ("Будущих", "future"),
            ("Прохождений", "completions")
        ]):
            f = ttk.Frame(stats_frame, style='TFrame')
            f.grid(row=0, column=i, padx=10, sticky='nsew')
            tk.Label(f, text=name, font=('Inter', 10), fg='#aaa', bg='#0f0f0f').pack()
            lbl = tk.Label(f, text="0", font=('Inter', 18, 'bold'), fg='#ff4757', bg='#0f0f0f')
            lbl.pack()
            self.stats_labels[key] = lbl

        stats_frame.columnconfigure(tuple(range(4)), weight=1)

        # Последние действия
        tk.Label(tab, text="📋 Последние действия", font=('Inter', 14, 'bold'), 
                fg='#ffffff', bg='#0f0f0f').pack(anchor='w', padx=20, pady=(20, 10))
        self.log_text = tk.Text(tab, height=10, bg='#1a1a1a', fg='white', 
                               font=('Consolas', 10), state='disabled')
        self.log_text.pack(fill='both', expand=True, padx=20, pady=(0, 20))

    def create_demons_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="👹 Демоны")

        # Поиск
        search_frame = ttk.Frame(tab)
        search_frame.pack(fill='x', padx=20, pady=10)
        tk.Label(search_frame, text="Поиск:", bg='#0f0f0f', fg='white').pack(side='left')
        self.demon_search = tk.Entry(search_frame, font=('Inter', 11), width=30)
        self.demon_search.pack(side='left', padx=10)
        self.demon_search.bind('<KeyRelease>', self.filter_demons)

        # Таблица
        table_frame = ttk.Frame(tab)
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)

        cols = ('ID', 'Название', 'Автор', 'Верификатор', 'Дата', 'Пройдено')
        self.demon_tree = ttk.Treeview(table_frame, columns=cols, show='headings', height=15)
        for col in cols:
            self.demon_tree.heading(col, text=col)
            self.demon_tree.column(col, width=100)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.demon_tree.yview)
        self.demon_tree.configure(yscroll=scrollbar.set)

        self.demon_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Кнопки
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill='x', padx=20, pady=10)
        ttk.Button(btn_frame, text="➕ Добавить", style='Success.TButton', command=self.add_demon).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="✏️ Редактировать", command=self.edit_demon).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🗑️ Удалить", style='Danger.TButton', command=self.delete_demon).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="📤 Экспорт", command=self.export_demons).pack(side='right', padx=5)

    def create_players_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="👤 Игроки")

        search_frame = ttk.Frame(tab)
        search_frame.pack(fill='x', padx=20, pady=10)
        tk.Label(search_frame, text="Поиск:", bg='#0f0f0f', fg='white').pack(side='left')
        self.player_search = tk.Entry(search_frame, font=('Inter', 11), width=30)
        self.player_search.pack(side='left', padx=10)
        self.player_search.bind('<KeyRelease>', self.filter_players)

        table_frame = ttk.Frame(tab)
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)

        cols = ('ID', 'Имя', 'Пройдено демонов', 'Очки')
        self.player_tree = ttk.Treeview(table_frame, columns=cols, show='headings', height=15)
        for col in cols:
            self.player_tree.heading(col, text=col)
            self.player_tree.column(col, width=120)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.player_tree.yview)
        self.player_tree.configure(yscroll=scrollbar.set)
        self.player_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill='x', padx=20, pady=10)
        ttk.Button(btn_frame, text="➕ Добавить", style='Success.TButton', command=self.add_player).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="✏️ Редактировать", command=self.edit_player).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🗑️ Удалить", style='Danger.TButton', command=self.delete_player).pack(side='left', padx=5)

    def create_future_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🔮 Будущие демоны")

        search_frame = ttk.Frame(tab)
        search_frame.pack(fill='x', padx=20, pady=10)
        tk.Label(search_frame, text="Поиск:", bg='#0f0f0f', fg='white').pack(side='left')
        self.future_search = tk.Entry(search_frame, font=('Inter', 11), width=30)
        self.future_search.pack(side='left', padx=10)
        self.future_search.bind('<KeyRelease>', self.filter_future)

        table_frame = ttk.Frame(tab)
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)

        cols = ('ID', 'Название', 'Автор', 'Сложность', 'Описание', 'Прогресс')
        self.future_tree = ttk.Treeview(table_frame, columns=cols, show='headings', height=15)
        for col in cols:
            self.future_tree.heading(col, text=col)
            self.future_tree.column(col, width=100)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.future_tree.yview)
        self.future_tree.configure(yscroll=scrollbar.set)
        self.future_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill='x', padx=20, pady=10)
        ttk.Button(btn_frame, text="➕ Добавить", style='Success.TButton', command=self.add_future).pack(side='left', padx=5)

    def create_ranking_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🏆 Топ-расстановка")

        # Два списка: все демоны | текущий топ
        lists_frame = ttk.Frame(tab)
        lists_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Все демоны
        left = ttk.LabelFrame(lists_frame, text="Все демоны", padding=10)
        left.pack(side='left', fill='both', expand=True, padx=(0, 10))
        self.all_demons_list = tk.Listbox(left, font=('Inter', 10), bg='#1a1a1a', fg='white', selectbackground='#ff4757')
        self.all_demons_list.pack(fill='both', expand=True)
        self.all_demons_list.bind('<Double-1>', lambda e: self.move_to_top())

        # Текущий топ
        right = ttk.LabelFrame(lists_frame, text="Топ-расстановка", padding=10)
        right.pack(side='right', fill='both', expand=True, padx=(10, 0))
        self.top_list = tk.Listbox(right, font=('Inter', 10), bg='#1a1a1a', fg='white', selectbackground='#4a9aff')
        self.top_list.pack(fill='both', expand=True)
        self.top_list.bind('<Double-1>', lambda e: self.remove_from_top())

        # Управление
        ctrl_frame = ttk.Frame(tab)
        ctrl_frame.pack(fill='x', padx=20, pady=10)

        ttk.Button(ctrl_frame, text="➡️ В топ", command=self.move_to_top).pack(side='left', padx=5)
        ttk.Button(ctrl_frame, text="⬅️ Убрать", command=self.remove_from_top).pack(side='left', padx=5)
        ttk.Button(ctrl_frame, text="⬆️ Вверх", command=lambda: self.move_in_top(-1)).pack(side='left', padx=5)
        ttk.Button(ctrl_frame, text="⬇️ Вниз", command=lambda: self.move_in_top(1)).pack(side='left', padx=5)

        save_frame = ttk.Frame(tab)
        save_frame.pack(fill='x', padx=20, pady=10)
        ttk.Button(save_frame, text="💾 Сохранить топ", style='Success.TButton', command=self.save_top).pack(side='left')
        ttk.Button(save_frame, text="📊 Просмотреть очки", command=self.show_points).pack(side='left', padx=10)

    def create_activity_log_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📝 Журнал")

        self.full_log = tk.Text(tab, bg='#1a1a1a', fg='white', font=('Consolas', 10), state='disabled')
        self.full_log.pack(fill='both', expand=True, padx=20, pady=20)

    # === ФУНКЦИИ ЗАГРУЗКИ/СОХРАНЕНИЯ ===
    def load_data(self):
        """Загружает все данные в интерфейс"""
        try:
            self.demons = self.load_json("js/demons.js", "demons")
            self.players = self.load_json("js/players.js", "players")
            self.future = self.load_json("js/futuredemons.js", "futureDemons")
            with open("js/list.js", "r", encoding="utf-8") as f:
                content = f.read()
            match = re.search(r'demonList\s*=\s*(\[.*?\])', content, re.DOTALL)
            self.top_ids = json.loads(match.group(1)) if match else []

            self.refresh_all_tables()
            self.update_stats()
            self.refresh_ranking_lists()
            self.log_action("Данные загружены")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные:\n{e}")

    def load_json(self, filepath: str, var_name: str) -> List[Dict[str, Any]]:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        match = re.search(f'{var_name}\\s*=\\s*(\\[.*?\\]);', content, re.DOTALL)
        if match:
            data_str = match.group(1)
            return json.loads(data_str)
        return []

    def save_json(self,  List, filepath: str, var_name: str):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        new_data = f"{var_name} = {json.dumps(data, ensure_ascii=False, indent=2)};"
        content = re.sub(f'{var_name}\\s*=\\s*\\[.*?\\];', new_data, content, flags=re.DOTALL)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    def save_top(self):
        """Сохраняет текущий топ в list.js"""
        top_data = f"const demonList = {json.dumps(self.top_ids)};"
        with open("js/list.js", "r", encoding="utf-8") as f:
            content = f.read()
        content = re.sub(r'const demonList = \[.*?\];', top_data, content, flags=re.DOTALL)
        with open("js/list.js", "w", encoding="utf-8") as f:
            f.write(content)
        self.log_action("Топ успешно сохранён!")

    # === ОБНОВЛЕНИЕ ИНТЕРФЕЙСА ===
    def refresh_all_tables(self):
        self.refresh_demons_table()
        self.refresh_players_table()
        self.refresh_future_table()

    def refresh_demons_table(self):
        for item in self.demon_tree.get_children():
            self.demon_tree.delete(item)
        for d in self.demons:
            self.demon_tree.insert('', 'end', values=(
                d['id'], d['name'], d['creator'], d['verifier'], d['verifyDate'], len(d['completers'])
            ))

    def refresh_players_table(self):
        for item in self.player_tree.get_children():
            self.player_tree.delete(item)
        for p in self.players:
            points = self.calculate_player_points(p['id'])
            self.player_tree.insert('', 'end', values=(
                p['id'], p['name'], len(p['completedDemons']), points
            ))

    def refresh_future_table(self):
        for item in self.future_tree.get_children():
            self.future_tree.delete(item)
        for f in self.future:
            progress = max((bp['progress'] for bp in f.get('beatingPlayers', [])), default=0)
            desc = f['description'][:30] + "..." if len(f['description']) > 30 else f['description']
            self.future_tree.insert('', 'end', values=(
                f['id'], f['name'], f['creator'], f['difficulty'], desc, f"{progress}%"
            ))

    def refresh_ranking_lists(self):
        self.all_demons_list.delete(0, tk.END)
        self.top_list.delete(0, tk.END)

        top_set = set(self.top_ids)
        for d in self.demons:
            text = f"{d['id']}: {d['name']} • by {d['creator']}"
            if d['id'] in top_set:
                idx = self.top_ids.index(d['id'])
                self.top_list.insert(tk.END, f"#{idx+1} — {text}")
            else:
                self.all_demons_list.insert(tk.END, text)

    def update_stats(self):
        total_completions = sum(len(d['completers']) for d in self.demons)
        self.stats_labels['demons'].config(text=str(len(self.demons)))
        self.stats_labels['players'].config(text=str(len(self.players)))
        self.stats_labels['future'].config(text=str(len(self.future)))
        self.stats_labels['completions'].config(text=str(total_completions))

    # === ДЕЙСТВИЯ ===
    def move_to_top(self):
        selection = self.all_demons_list.curselection()
        if not selection: return
        text = self.all_demons_list.get(selection[0])
        demon_id = int(text.split(':')[0])
        if demon_id not in self.top_ids:
            self.top_ids.append(demon_id)
            self.refresh_ranking_lists()
            self.log_action(f"Демон ID {demon_id} добавлен в топ")

    def remove_from_top(self):
        selection = self.top_list.curselection()
        if not selection: return
        idx_in_top = selection[0]
        self.top_ids.pop(idx_in_top)
        self.refresh_ranking_lists()
        self.log_action(f"Демон удалён из топа (позиция {idx_in_top+1})")

    def move_in_top(self, direction: int):
        selection = self.top_list.curselection()
        if not selection: return
        idx = selection[0]
        if 0 <= idx + direction < len(self.top_ids):
            self.top_ids[idx], self.top_ids[idx+direction] = self.top_ids[idx+direction], self.top_ids[idx]
            self.refresh_ranking_lists()
            self.top_list.selection_set(idx+direction)

    def calculate_player_points(self, player_id: int) -> int:
        player = next((p for p in self.players if p['id'] == player_id), None)
        if not player: return 0
        total = 0
        for demon_id in player['completedDemons']:
            if demon_id in self.top_ids:
                pos = self.top_ids.index(demon_id) + 1
                points = 500
                for _ in range(2, pos+1):
                    points = int(points * 0.81)
                total += points
        return total

    def log_action(self, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_line = f"[{timestamp}] {message}\n"
        self.log_text.config(state='normal')
        self.log_text.insert('end', log_line)
        self.log_text.see('end')
        self.log_text.config(state='disabled')

        self.full_log.config(state='normal')
        self.full_log.insert('end', log_line)
        self.full_log.see('end')
        self.full_log.config(state='disabled')

    def show_points(self):
        if not self.top_ids:
            messagebox.showinfo("Очки", "Топ пуст!")
            return
        text = "Очки по позициям:\n\n"
        for i, demon_id in enumerate(self.top_ids[:20], 1):
            points = 500
            for _ in range(2, i+1):
                points = int(points * 0.81)
            demon = next((d for d in self.demons if d['id'] == demon_id), None)
            name = demon['name'] if demon else f"ID {demon_id}"
            text += f"#{i}: {points} • {name}\n"
        messagebox.showinfo("Очки топа", text)

    # === ЗАГОТОВКИ ДЛЯ ДОБАВЛЕНИЯ (простой пример) ===
    def add_demon(self):
        name = simpledialog.askstring("Новый демон", "Название:")
        if not name: return
        creator = simpledialog.askstring("Автор", "Создатель:")
        if not creator: return
        next_id = max([d['id'] for d in self.demons]) + 1 if self.demons else 1
        self.demons.append({
            "id": next_id,
            "name": name,
            "creator": creator,
            "verifier": 1,
            "verifyDate": datetime.now().strftime("%Y-%m-%d"),
            "completers": []
        })
        self.save_json(self.demons, "js/demons.js", "demons")
        self.refresh_all_tables()
        self.refresh_ranking_lists()
        self.update_stats()
        self.log_action(f"Добавлен демон: {name} (ID {next_id})")

    def add_player(self):
        name = simpledialog.askstring("Новый игрок", "Имя:")
        if not name: return
        next_id = max([p['id'] for p in self.players]) + 1 if self.players else 1
        self.players.append({
            "id": next_id,
            "name": name,
            "completedDemons": []
        })
        self.save_json(self.players, "js/players.js", "players")
        self.refresh_all_tables()
        self.update_stats()
        self.log_action(f"Добавлен игрок: {name} (ID {next_id})")

    def add_future(self):
        name = simpledialog.askstring("Будущий демон", "Название:")
        if not name: return
        creator = simpledialog.askstring("Автор", "Создатель:")
        if not creator: return
        diff = simpledialog.askstring("Сложность", "Сложность (Extreme Demon и т.д.):")
        if not diff: return
        desc = simpledialog.askstring("Описание", "Описание:")
        if not desc: return
        next_id = max([f['id'] for f in self.future]) + 1 if self.future else 1
        self.future.append({
            "id": next_id,
            "name": name,
            "creator": creator,
            "difficulty": diff,
            "description": desc,
            "beatingPlayers": []
        })
        self.save_json(self.future, "js/futuredemons.js", "futureDemons")
        self.refresh_all_tables()
        self.update_stats()
        self.log_action(f"Добавлен будущий демон: {name} (ID {next_id})")

    # === ИНСТРУМЕНТЫ ===
    def export_demons(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.demons, f, ensure_ascii=False, indent=2)
            self.log_action(f"Демоны экспортированы в {filepath}")

    # === ФИЛЬТРАЦИЯ ===
    def filter_demons(self, event=None):
        term = self.demon_search.get().lower()
        for item in self.demon_tree.get_children():
            self.demon_tree.delete(item)
        for d in self.demons:
            if term in d['name'].lower() or term in d['creator'].lower():
                self.demon_tree.insert('', 'end', values=(
                    d['id'], d['name'], d['creator'], d['verifier'], d['verifyDate'], len(d['completers'])
                ))

    def filter_players(self, event=None):
        term = self.player_search.get().lower()
        for item in self.player_tree.get_children():
            self.player_tree.delete(item)
        for p in self.players:
            if term in p['name'].lower():
                points = self.calculate_player_points(p['id'])
                self.player_tree.insert('', 'end', values=(
                    p['id'], p['name'], len(p['completedDemons']), points
                ))

    def filter_future(self, event=None):
        term = self.future_search.get().lower()
        for item in self.future_tree.get_children():
            self.future_tree.delete(item)
        for f in self.future:
            if term in f['name'].lower() or term in f['creator'].lower():
                progress = max((bp['progress'] for bp in f.get('beatingPlayers', [])), default=0)
                desc = f['description'][:30] + "..." if len(f['description']) > 30 else f['description']
                self.future_tree.insert('', 'end', values=(
                    f['id'], f['name'], f['creator'], f['difficulty'], desc, f"{progress}%"
                ))

    # === ЗАГОТОВКИ УДАЛЕНИЯ/РЕДАКТИРОВАНИЯ ===
    def edit_demon(self):
        selection = self.demon_tree.selection()
        if not selection: return
        values = self.demon_tree.item(selection[0], 'values')
        demon_id = int(values[0])
        demon = next((d for d in self.demons if d['id'] == demon_id), None)
        if not demon: return
        name = simpledialog.askstring("Редактирование", "Название:", initialvalue=demon['name'])
        if name is None: return
        creator = simpledialog.askstring("Автор", "Создатель:", initialvalue=demon['creator'])
        if creator is None: return
        demon['name'] = name
        demon['creator'] = creator
        self.save_json(self.demons, "js/demons.js", "demons")
        self.refresh_all_tables()
        self.refresh_ranking_lists()
        self.log_action(f"Отредактирован демон ID {demon_id}")

    def delete_demon(self):
        selection = self.demon_tree.selection()
        if not selection: return
        values = self.demon_tree.item(selection[0], 'values')
        demon_id = int(values[0])
        if not messagebox.askyesno("Удаление", f"Удалить демон ID {demon_id}? Это необратимо!"):
            return
        self.demons = [d for d in self.demons if d['id'] != demon_id]
        self.top_ids = [i for i in self.top_ids if i != demon_id]
        # Удалить из игроков
        for p in self.players:
            if demon_id in p['completedDemons']:
                p['completedDemons'].remove(demon_id)
        self.save_json(self.demons, "js/demons.js", "demons")
        self.save_json(self.players, "js/players.js", "players")
        self.refresh_all_tables()
        self.refresh_ranking_lists()
        self.update_stats()
        self.log_action(f"Удалён демон ID {demon_id}")

    def edit_player(self):
        selection = self.player_tree.selection()
        if not selection: return
        values = self.player_tree.item(selection[0], 'values')
        player_id = int(values[0])
        player = next((p for p in self.players if p['id'] == player_id), None)
        if not player: return
        name = simpledialog.askstring("Редактирование", "Имя:", initialvalue=player['name'])
        if name is None: return
        player['name'] = name
        self.save_json(self.players, "js/players.js", "players")
        self.refresh_all_tables()
        self.log_action(f"Отредактирован игрок ID {player_id}")

    def delete_player(self):
        selection = self.player_tree.selection()
        if not selection: return
        values = self.player_tree.item(selection[0], 'values')
        player_id = int(values[0])
        if not messagebox.askyesno("Удаление", f"Удалить игрока ID {player_id}?"):
            return
        self.players = [p for p in self.players if p['id'] != player_id]
        # Удалить из демонов
        for d in self.demons:
            d['completers'] = [c for c in d['completers'] if c['playerId'] != player_id]
        self.save_json(self.players, "js/players.js", "players")
        self.save_json(self.demons, "js/demons.js", "demons")
        self.refresh_all_tables()
        self.update_stats()
        self.log_action(f"Удалён игрок ID {player_id}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernDemonlistGUI(root)
    root.mainloop()