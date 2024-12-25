import tkinter as tk
from tkinter import ttk, messagebox

# Главный класс приложения
class RecipeBookApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Книга рецептов")
        self.geometry("600x400")

        # Список для хранения рецептов
        self.recipes = []

        # Настройка интерфейса
        self.create_widgets()

    def create_widgets(self):
        """Создаём виджеты основного интерфейса"""

        # Заголовок приложения
        title_label = tk.Label(self, text="📖 Книга Рецептов", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Кнопки для действий
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        add_button = ttk.Button(button_frame, text="Добавить рецепт", command=self.open_add_recipe_window)
        add_button.grid(row=0, column=0, padx=10)

        view_button = ttk.Button(button_frame, text="Просмотреть рецепты", command=self.view_recipes)
        view_button.grid(row=0, column=1, padx=10)

        # Поле для списка рецептов
        self.recipe_listbox = tk.Listbox(self, width=80, height=15)
        self.recipe_listbox.pack(pady=10)

        # Категории рецептов
        self.categories = ['Все', 'Завтраки', 'Ужины', 'Салаты', 'Десерты']
        self.category_combobox = ttk.Combobox(self, values=self.categories, state="readonly")
        self.category_combobox.set('Все')
        self.category_combobox.pack(pady=5)

    def open_add_recipe_window(self):
        """Открывает окно для добавления нового рецепта"""

        add_window = tk.Toplevel(self)
        add_window.title("Добавить рецепт")
        add_window.geometry("400x400")

        # Поля для ввода рецепта
        tk.Label(add_window, text="Название рецепта:").pack(pady=5)
        title_entry = tk.Entry(add_window, width=40)
        title_entry.pack(pady=5)

        tk.Label(add_window, text="Ингредиенты (через запятую):").pack(pady=5)
        ingredients_entry = tk.Text(add_window, width=40, height=3)
        ingredients_entry.pack(pady=5)

        tk.Label(add_window, text="Шаги приготовления:").pack(pady=5)
        steps_entry = tk.Text(add_window, width=40, height=5)
        steps_entry.pack(pady=5)

        tk.Label(add_window, text="Категория рецепта:").pack(pady=5)
        category_entry = ttk.Combobox(add_window, values=self.categories, state="readonly")
        category_entry.set('Завтраки')  # Устанавливаем категорию по умолчанию
        category_entry.pack(pady=5)

        tk.Label(add_window, text="Автор рецепта:").pack(pady=5)
        author_entry = tk.Entry(add_window, width=40)
        author_entry.pack(pady=5)

        # Кнопка сохранения
        def save_recipe():
            title = title_entry.get()
            ingredients = ingredients_entry.get("1.0", "end").strip()
            steps = steps_entry.get("1.0", "end").strip()
            author = author_entry.get().strip()
            category = category_entry.get().strip()

            # Проверка на пустые поля
            if not title or not ingredients or not steps or not author or not category:
                messagebox.showwarning("Ошибка", "Заполните все поля!")
                return

            # Сохранение рецепта
            self.recipes.append({
                "title": title,
                "ingredients": ingredients,
                "steps": steps,
                "author": author,
                "category": category
            })
            messagebox.showinfo("Успех", "Рецепт добавлен!")
            add_window.destroy()
            self.update_recipe_list()

        save_button = ttk.Button(add_window, text="Сохранить", command=save_recipe)
        save_button.pack(pady=10)

    def update_recipe_list(self):
        """Обновляет список рецептов в Listbox с учетом выбранной категории"""
        selected_category = self.category_combobox.get()
        self.recipe_listbox.delete(0, tk.END)
        for idx, recipe in enumerate(self.recipes, start=1):
            if selected_category == 'Все' or recipe["category"] == selected_category:
                self.recipe_listbox.insert(tk.END, f"{idx}. {recipe['title']} ({recipe['category']})")

    def view_recipes(self):
        """Отображает детали выбранного рецепта"""
        selected = self.recipe_listbox.curselection()
        if selected:
            index = selected[0]
            recipe = self.recipes[index]

            # Окно с подробностями
            view_window = tk.Toplevel(self)
            view_window.title(recipe["title"])
            view_window.geometry("400x400")

            tk.Label(view_window, text=f"Название: {recipe['title']}", font=("Arial", 12, "bold")).pack(pady=5)
            tk.Label(view_window, text="Ингредиенты:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10)
            tk.Label(view_window, text=recipe["ingredients"], wraplength=380, justify="left").pack(anchor="w", padx=10)

            tk.Label(view_window, text="Шаги приготовления:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10)
            tk.Label(view_window, text=recipe["steps"], wraplength=380, justify="left").pack(anchor="w", padx=10)

            tk.Label(view_window, text=f"Автор: {recipe['author']}", font=("Arial", 10, "italic")).pack(pady=5)

        else:
            messagebox.showwarning("Ошибка", "Выберите рецепт для просмотра!")

# Запуск приложения
if __name__ == "__main__":
    app = RecipeBookApp()
    app.mainloop()
