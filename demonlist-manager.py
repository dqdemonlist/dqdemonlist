import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import re
from datetime import datetime
import os

class DemonlistGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Geometry Dash Demonlist Manager")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2b2b2b')
        
        # Стиль
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#2b2b2b')
        self.style.configure('TLabel', background='#2b2b2b', foreground='white', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10), padding=5)
        self.style.configure('TNotebook', background='#2b2b2b')
        self.style.configure('TNotebook.Tab', background='#3b3b3b', foreground='white', padding=[10, 5])
        
        # Файлы
        self.demons_file = "js/demons.js"
        self.players_file = "js/players.js"
        self.future_demons_file = "js/futuredemons.js"
        self.list_file = "js/list.js"
        
        self.create_widgets()
        self.load_data()
        
    def create_widgets(self):
        # Создаем notebook для вкладок
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Вкладка просмотра данных
        self.create_view_tab(notebook)
        
        # Вкладка добавления демонов
        self.create_demon_tab(notebook)
        
        # Вкладка добавления игроков
        self.create_player_tab(notebook)
        
        # Вкладка будущих демонов
        self.create_future_tab(notebook)
        
        # Вкладка прохождений
        self.create_completion_tab(notebook)
        
    def create_view_tab(self, notebook):
        view_frame = ttk.Frame(notebook)
        notebook.add(view_frame, text="📊 Просмотр данных")
        
        # Создаем notebook внутри вкладки для разных типов данных
        view_notebook = ttk.Notebook(view_frame)
        view_notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Демоны
        demons_frame = ttk.Frame(view_notebook)
        view_notebook.add(demons_frame, text="👹 Демоны")
        
        demons_text = scrolledtext.ScrolledText(demons_frame, width=80, height=20, font=('Consolas', 9))
        demons_text.pack(fill='both', expand=True, padx=5, pady=5)
        self.demons_text = demons_text
        
        # Игроки
        players_frame = ttk.Frame(view_notebook)
        view_notebook.add(players_frame, text="👤 Игроки")
        
        players_text = scrolledtext.ScrolledText(players_frame, width=80, height=20, font=('Consolas', 9))
        players_text.pack(fill='both', expand=True, padx=5, pady=5)
        self.players_text = players_text
        
        # Будущие демоны
        future_frame = ttk.Frame(view_notebook)
        view_notebook.add(future_frame, text="🔮 Будущие демоны")
        
        future_text = scrolledtext.ScrolledText(future_frame, width=80, height=20, font=('Consolas', 9))
        future_text.pack(fill='both', expand=True, padx=5, pady=5)
        self.future_text = future_text
        
        # Кнопка обновления
        refresh_btn = ttk.Button(view_frame, text="🔄 Обновить данные", command=self.load_data)
        refresh_btn.pack(pady=10)
        
    def create_demon_tab(self, notebook):
        demon_frame = ttk.Frame(notebook)
        notebook.add(demon_frame, text="👹 Добавить демона")
        
        # Форма добавления демона
        fields_frame = ttk.Frame(demon_frame)
        fields_frame.pack(pady=20)
        
        ttk.Label(fields_frame, text="Название демона:").grid(row=0, column=0, sticky='w', pady=5)
        self.demon_name = ttk.Entry(fields_frame, width=30)
        self.demon_name.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(fields_frame, text="Создатель:").grid(row=1, column=0, sticky='w', pady=5)
        self.demon_creator = ttk.Entry(fields_frame, width=30)
        self.demon_creator.grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Label(fields_frame, text="ID верификатора:").grid(row=2, column=0, sticky='w', pady=5)
        self.demon_verifier = ttk.Entry(fields_frame, width=30)
        self.demon_verifier.grid(row=2, column=1, pady=5, padx=5)
        
        ttk.Label(fields_frame, text="Дата верификации (гггг-мм-дд):").grid(row=3, column=0, sticky='w', pady=5)
        self.demon_date = ttk.Entry(fields_frame, width=30)
        self.demon_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.demon_date.grid(row=3, column=1, pady=5, padx=5)
        
        add_btn = ttk.Button(demon_frame, text="➕ Добавить демона", command=self.add_demon_gui)
        add_btn.pack(pady=10)
        
        # Список демонов для редактирования
        ttk.Label(demon_frame, text="Редактировать существующего демона:").pack(pady=(20, 5))
        
        edit_frame = ttk.Frame(demon_frame)
        edit_frame.pack(pady=10)
        
        ttk.Label(edit_frame, text="Выберите демона:").grid(row=0, column=0, padx=5)
        self.demon_combobox = ttk.Combobox(edit_frame, width=25, state="readonly")
        self.demon_combobox.grid(row=0, column=1, padx=5)
        
        edit_btn = ttk.Button(edit_frame, text="✏️ Редактировать", command=self.edit_demon_gui)
        edit_btn.grid(row=0, column=2, padx=5)
        
    def create_player_tab(self, notebook):
        player_frame = ttk.Frame(notebook)
        notebook.add(player_frame, text="👤 Добавить игрока")
        
        # Форма добавления игрока
        fields_frame = ttk.Frame(player_frame)
        fields_frame.pack(pady=20)
        
        ttk.Label(fields_frame, text="Имя игрока:").grid(row=0, column=0, sticky='w', pady=5)
        self.player_name = ttk.Entry(fields_frame, width=30)
        self.player_name.grid(row=0, column=1, pady=5, padx=5)
        
        add_btn = ttk.Button(player_frame, text="➕ Добавить игрока", command=self.add_player_gui)
        add_btn.pack(pady=10)
        
        # Список игроков для редактирования
        ttk.Label(player_frame, text="Редактировать существующего игрока:").pack(pady=(20, 5))
        
        edit_frame = ttk.Frame(player_frame)
        edit_frame.pack(pady=10)
        
        ttk.Label(edit_frame, text="Выберите игрока:").grid(row=0, column=0, padx=5)
        self.player_combobox = ttk.Combobox(edit_frame, width=25, state="readonly")
        self.player_combobox.grid(row=0, column=1, padx=5)
        
        edit_btn = ttk.Button(edit_frame, text="✏️ Редактировать", command=self.edit_player_gui)
        edit_btn.grid(row=0, column=2, padx=5)
        
    def create_future_tab(self, notebook):
        future_frame = ttk.Frame(notebook)
        notebook.add(future_frame, text="🔮 Будущие демоны")
        
        # Форма добавления будущего демона
        fields_frame = ttk.Frame(future_frame)
        fields_frame.pack(pady=20)
        
        ttk.Label(fields_frame, text="Название демона:").grid(row=0, column=0, sticky='w', pady=5)
        self.future_name = ttk.Entry(fields_frame, width=30)
        self.future_name.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(fields_frame, text="Создатель:").grid(row=1, column=0, sticky='w', pady=5)
        self.future_creator = ttk.Entry(fields_frame, width=30)
        self.future_creator.grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Label(fields_frame, text="Сложность:").grid(row=2, column=0, sticky='w', pady=5)
        self.future_difficulty = ttk.Entry(fields_frame, width=30)
        self.future_difficulty.grid(row=2, column=1, pady=5, padx=5)
        
        ttk.Label(fields_frame, text="Описание:").grid(row=3, column=0, sticky='w', pady=5)
        self.future_description = tk.Text(fields_frame, width=30, height=4)
        self.future_description.grid(row=3, column=1, pady=5, padx=5)
        
        add_btn = ttk.Button(future_frame, text="➕ Добавить будущего демона", command=self.add_future_demon_gui)
        add_btn.pack(pady=10)
        
        # Добавление игрока проходящего демон
        ttk.Label(future_frame, text="Добавить игрока проходящего демон:").pack(pady=(20, 5))
        
        beating_frame = ttk.Frame(future_frame)
        beating_frame.pack(pady=10)
        
        ttk.Label(beating_frame, text="Демон:").grid(row=0, column=0, padx=5)
        self.beating_demon = ttk.Combobox(beating_frame, width=20, state="readonly")
        self.beating_demon.grid(row=0, column=1, padx=5)
        
        ttk.Label(beating_frame, text="Игрок:").grid(row=0, column=2, padx=5)
        self.beating_player = ttk.Combobox(beating_frame, width=20, state="readonly")
        self.beating_player.grid(row=0, column=3, padx=5)
        
        ttk.Label(beating_frame, text="Прогресс (%):").grid(row=1, column=0, padx=5, pady=5)
        self.beating_progress = ttk.Entry(beating_frame, width=10)
        self.beating_progress.grid(row=1, column=1, padx=5, pady=5)
        
        add_beating_btn = ttk.Button(beating_frame, text="🎯 Добавить прохождение", command=self.add_beating_player_gui)
        add_beating_btn.grid(row=1, column=2, columnspan=2, padx=5, pady=5)
        
    def create_completion_tab(self, notebook):
        completion_frame = ttk.Frame(notebook)
        notebook.add(completion_frame, text="✅ Прохождения")
        
        ttk.Label(completion_frame, text="Добавить прохождение демона:").pack(pady=20)
        
        completion_form = ttk.Frame(completion_frame)
        completion_form.pack(pady=10)
        
        ttk.Label(completion_form, text="Демон:").grid(row=0, column=0, padx=5, pady=5)
        self.completion_demon = ttk.Combobox(completion_form, width=20, state="readonly")
        self.completion_demon.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(completion_form, text="Игрок:").grid(row=0, column=2, padx=5, pady=5)
        self.completion_player = ttk.Combobox(completion_form, width=20, state="readonly")
        self.completion_player.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(completion_form, text="Дата (гггг-мм-дд):").grid(row=1, column=0, padx=5, pady=5)
        self.completion_date = ttk.Entry(completion_form, width=20)
        self.completion_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.completion_date.grid(row=1, column=1, padx=5, pady=5)
        
        add_completion_btn = ttk.Button(completion_form, text="✅ Добавить прохождение", command=self.add_completion_gui)
        add_completion_btn.grid(row=1, column=2, columnspan=2, padx=5, pady=5)
        
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
            
            # Обновляем комбобоксы
            self.update_comboboxes(demons, players, future_demons)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")
    
    def load_demons(self):
        with open(self.demons_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        match = re.search(r'const demons = (\[.*?\]);', content, re.DOTALL)
        if match:
            demons_json = match.group(1)
            demons_json = demons_json.replace("'", '"')
            demons_json = re.sub(r'(\w+):', r'"\1":', demons_json)
            return json.loads(demons_json)
        return []
    
    def load_players(self):
        with open(self.players_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        match = re.search(r'const players = (\[.*?\]);', content, re.DOTALL)
        if match:
            players_json = match.group(1)
            players_json = players_json.replace("'", '"')
            players_json = re.sub(r'(\w+):', r'"\1":', players_json)
            return json.loads(players_json)
        return []
    
    def load_future_demons(self):
        with open(self.future_demons_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        match = re.search(r'const futureDemons = (\[.*?\]);', content, re.DOTALL)
        if match:
            future_json = match.group(1)
            future_json = future_json.replace("'", '"')
            future_json = re.sub(r'(\w+):', r'"\1":', future_json)
            return json.loads(future_json)
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
            text += f"  Игроков проходят: {len(demon['beatingPlayers'])}\n"
            for bp in demon['beatingPlayers']:
                text += f"    - Игрок ID: {bp['playerId']}, Прогресс: {bp['progress']}%, Обновлено: {bp['lastUpdate']}\n"
            text += "\n"
        
        self.future_text.delete(1.0, tk.END)
        self.future_text.insert(1.0, text)
    
    def update_comboboxes(self, demons, players, future_demons):
        # Демоны для редактирования
        demon_values = [f"{d['id']}: {d['name']}" for d in demons]
        self.demon_combobox['values'] = demon_values
        
        # Игроки для редактирования
        player_values = [f"{p['id']}: {p['name']}" for p in players]
        self.player_combobox['values'] = player_values
        
        # Для прохождений
        self.completion_demon['values'] = [f"{d['id']}: {d['name']}" for d in demons]
        self.completion_player['values'] = [f"{p['id']}: {p['name']}" for p in players]
        
        # Для будущих демонов
        self.beating_demon['values'] = [f"{d['id']}: {d['name']}" for d in future_demons]
        self.beating_player['values'] = [f"{p['id']}: {p['name']}" for p in players]
    
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
            self.clear_demon_fields()
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
            self.clear_player_fields()
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
            self.clear_future_fields()
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
            self.clear_completion_fields()
            self.load_data()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить прохождение: {e}")
    
    def add_beating_player_gui(self):
        try:
            demon_str = self.beating_demon.get()
            player_str = self.beating_player.get()
            progress = self.beating_progress.get().strip()
            
            if not all([demon_str, player_str, progress]):
                messagebox.showwarning("Предупреждение", "Все поля должны быть заполнены!")
                return
            
            demon_id = int(demon_str.split(':')[0])
            player_id = int(player_str.split(':')[0])
            progress_val = int(progress)
            
            future_demons = self.load_future_demons()
            
            for demon in future_demons:
                if demon['id'] == demon_id:
                    if not any(bp['playerId'] == player_id for bp in demon['beatingPlayers']):
                        demon['beatingPlayers'].append({
                            "playerId": player_id,
                            "progress": progress_val,
                            "lastUpdate": datetime.now().strftime("%Y-%m-%d")
                        })
                    break
            
            self.save_future_demons(future_demons)
            
            messagebox.showinfo("Успех", "Игрок добавлен к проходящим демон!")
            self.clear_beating_fields()
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
        
        ttk.Label(edit_window, text="Название:").pack(pady=5)
        name_entry = ttk.Entry(edit_window, width=30)
        name_entry.insert(0, demon['name'])
        name_entry.pack(pady=5)
        
        ttk.Label(edit_window, text="Создатель:").pack(pady=5)
        creator_entry = ttk.Entry(edit_window, width=30)
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
        
        ttk.Label(edit_window, text="Имя игрока:").pack(pady=5)
        name_entry = ttk.Entry(edit_window, width=30)
        name_entry.insert(0, player['name'])
        name_entry.pack(pady=5)
        
        def save_changes():
            player['name'] = name_entry.get().strip()
            self.save_players(players)
            messagebox.showinfo("Успех", "Игрок обновлен!")
            edit_window.destroy()
            self.load_data()
        
        ttk.Button(edit_window, text="💾 Сохранить", command=save_changes).pack(pady=20)
    
    def save_demons(self, demons):
        js_content = f"""const demons = {json.dumps(demons, indent=2, ensure_ascii=False)};

// Функция для получения демона по ID
function getDemonById(id) {{
    return demons.find(demon => demon.id === id);
}}

// Функция для получения всех демонов
function getAllDemons() {{
    return demons;
}}
"""
        with open(self.demons_file, 'w', encoding='utf-8') as f:
            f.write(js_content)
    
    def save_players(self, players):
        js_content = f"""const players = {json.dumps(players, indent=2, ensure_ascii=False)};

// Функция для получения игрока по ID
function getPlayerById(id) {{
    return players.find(player => player.id === id);
}}

// Функция для получения всех игроков
function getAllPlayers() {{
    return players;
}}

// Функция для получения демонов игрока
function getPlayerDemons(playerId) {{
    const player = getPlayerById(playerId);
    if (!player) return [];
    
    return player.completedDemons.map(demonId => {{
        const demon = getDemonById(demonId);
        return {{
            ...demon,
            completionDate: getCompletionDate(playerId, demonId)
        }};
    }});
}}

// Функция для получения даты прохождения демона игроком
function getCompletionDate(playerId, demonId) {{
    const demon = getDemonById(demonId);
    if (!demon) return null;
    
    const completion = demon.completers.find(comp => comp.playerId === playerId);
    return completion ? completion.date : null;
}}

// Функция для расчета очков игрока
function calculatePlayerPoints(playerId) {{
    const player = getPlayerById(playerId);
    if (!player) return 0;
    
    let totalPoints = 0;
    player.completedDemons.forEach(demonId => {{
        const demonIndex = demonList.indexOf(demonId);
        if (demonIndex !== -1) {{
            const position = demonIndex + 1;
            totalPoints += calculateDemonPoints(position);
        }}
    }});
    return totalPoints;
}}
"""
        with open(self.players_file, 'w', encoding='utf-8') as f:
            f.write(js_content)
    
    def save_future_demons(self, future_demons):
        js_content = f"""const futureDemons = {json.dumps(future_demons, indent=2, ensure_ascii=False)};

// Функция для получения будущего демона по ID
function getFutureDemonById(id) {{
    return futureDemons.find(demon => demon.id === id);
}}

// Функция для получения всех будущих демонов
function getAllFutureDemons() {{
    return futureDemons;
}}

// Функция для получения игроков, проходящих демон
function getBeatingPlayers(demonId) {{
    const demon = getFutureDemonById(demonId);
    if (!demon) return [];
    
    return demon.beatingPlayers.map(bp => {{
        const player = getPlayerById(bp.playerId);
        return {{
            ...bp,
            playerName: player ? player.name : 'Unknown'
        }};
    }}).sort((a, b) => b.progress - a.progress);
}}
"""
        with open(self.future_demons_file, 'w', encoding='utf-8') as f:
            f.write(js_content)
    
    def update_demon_list(self, demon_ids):
        with open(self.list_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_list = f"const demonList = {json.dumps(demon_ids)};"
        content = re.sub(r'const demonList = \[.*?\];', new_list, content, flags=re.DOTALL)
        
        with open(self.list_file, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def clear_demon_fields(self):
        self.demon_name.delete(0, tk.END)
        self.demon_creator.delete(0, tk.END)
        self.demon_verifier.delete(0, tk.END)
        self.demon_date.delete(0, tk.END)
        self.demon_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
    
    def clear_player_fields(self):
        self.player_name.delete(0, tk.END)
    
    def clear_future_fields(self):
        self.future_name.delete(0, tk.END)
        self.future_creator.delete(0, tk.END)
        self.future_difficulty.delete(0, tk.END)
        self.future_description.delete(1.0, tk.END)
    
    def clear_completion_fields(self):
        self.completion_demon.set('')
        self.completion_player.set('')
        self.completion_date.delete(0, tk.END)
        self.completion_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
    
    def clear_beating_fields(self):
        self.beating_demon.set('')
        self.beating_player.set('')
        self.beating_progress.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = DemonlistGUI(root)
    root.mainloop()