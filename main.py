#Food Diary V1.0
#Andrew Aurand
import json #for saving food/calories
import csv # for exporting to CSV
import tkinter as tk #GUI program
import os  # Import the os module for file handling
from tkinter import messagebox, filedialog, StringVar, OptionMenu, END
from datetime import datetime
from settings_manager import SettingsManager #supposed to get date
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import shutil

class FoodDiary:
    def __init__(self, filename='food_diary.json'):
        self.filename = filename
        self.entries = []
        self.settings_manager = SettingsManager()
        self.date_format = self.settings_manager.get_date_format() #This doesn't do anything?
        self.load()
        
    
    def backup(self):
        # Prompt the user to choose a file location for backup
        backup_filename = filedialog.asksaveasfilename(defaultextension=".json",
                                                        filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if backup_filename:
            with open(backup_filename, 'w') as f:
                json.dump(self.entries, f, indent=4)
            print(f"Backup saved to {backup_filename}")

    def restore(self):
        # Prompt the user to choose a backup file for restore
        backup_filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if backup_filename:
            try:
                with open(backup_filename, 'r') as f:
                    self.entries = json.load(f)
                print(f"Backup '{backup_filename}' restored successfully")
            except FileNotFoundError:
                print("No backup file selected.")
    

    def add_entry(self, date, meal, food_items, calories, protein, carbs, fats, sugar):
        date_format = self.settings_manager.get_date_format()
        
      #  try:
         #   datetime.strptime(date, self.date_format)
       # except ValueError:
           # print(f"Invalid date format. Date should be in '{date_format}' format.")
          #  return
        entry = {
            'date': date,
            'meal': meal,
            'food_items': food_items,
            'calories': calories,
            'protein': protein,
            'carbs': carbs,
            'fats': fats,
            'sugar': sugar
            }
        self.entries.append(entry)
        self.save()
        print(f"Added entry: {entry}") 

    def view_entries(self):
        return self.entries

    def save(self):
        with open(self.filename, 'w') as f:
            json.dump(self.entries, f, indent=4)
        print(f"Diary saved to {self.filename}")

    def load(self):
        try:
            with open(self.filename, 'r') as f:
                self.entries = json.load(f)
            print(f"Diary loaded from {self.filename}")
        except FileNotFoundError:
            print(f"No existing diary found, starting a new one.")
            self.entries = []

    def export_to_csv(self, csv_filename='food_diary.csv'):
        with open(csv_filename, 'w', newline='') as csvfile:
            fieldnames = ['date', 'meal', 'food_items', 'calories', 'protein', 'carbs', 'fats', 'sugar']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for entry in self.entries:
                writer.writerow(entry)
        print(f"Diary exported to {csv_filename}")

    def get_entries_in_date_range(self, start_date, end_date):
        return [entry for entry in self.entries if start_date <= datetime.strptime(entry['date'], self.date_format) <= end_date]

    def delete_entry(self, index):
        if 0 <= index < len(self.entries):
            del self.entries[index]
            self.save()
            print(f"Deleted entry at index {index}")
            return True
        else:
            print("Invalid index")
            return False


class FoodDiaryApp:
    def __init__(self, root, diary):
        self.root = root
        self.diary = diary
        self.root.title("Food Diary")
        #self.date_format = "%Y-%m-%d" #This changes what is initally accepted.
        self.date_format = "%m-%d-%Y"
        self.meal_options = ["breakfast", "lunch", "dinner", "snack"]
        self.create_widgets()
        self.create_menu()
        self.populate_entries_listbox()
    def open_help_pdf(self):
        help_file = 'Food Diary Manual.pdf'  # Specify the path to your PDF file
        if os.path.exists(help_file):
            os.system('start "" "' + help_file + '"')  # Open the PDF file
        else:
            messagebox.showerror("Error", "Help document not found.")
   
    def create_widgets(self):
        # Date
        tk.Label(self.root, text="Date:").grid(row=0, column=0)
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=0, column=1)
        self.date_entry.insert(0, datetime.now().strftime(self.diary.settings_manager.get_date_format()))  # Set current date with the format

        # Meal
        tk.Label(self.root, text="Meal:").grid(row=1, column=0)
        self.meal_var = StringVar(self.root)
        self.meal_var.set(self.meal_options[0])  # default value
        self.meal_menu = OptionMenu(self.root, self.meal_var, *self.meal_options)
        self.meal_menu.grid(row=1, column=1)

        # Food Items
        tk.Label(self.root, text="Food Items (comma separated):").grid(row=2, column=0)
        self.food_items_entry = tk.Entry(self.root)
        self.food_items_entry.grid(row=2, column=1)

        # Calories
        tk.Label(self.root, text="Calories:").grid(row=3, column=0)
        self.calories_entry = tk.Entry(self.root)
        self.calories_entry.grid(row=3, column=1)

        # Protein
        tk.Label(self.root, text="Protein (grams):").grid(row=4, column=0)
        self.protein_entry = tk.Entry(self.root)
        self.protein_entry.grid(row=4, column=1)

        # Carbs
        tk.Label(self.root, text="Carbs (grams):").grid(row=5, column=0)
        self.carbs_entry = tk.Entry(self.root)
        self.carbs_entry.grid(row=5, column=1)

        # Fats
        tk.Label(self.root, text="Fats (grams):").grid(row=6, column=0)
        self.fats_entry = tk.Entry(self.root)
        self.fats_entry.grid(row=6, column=1)
        
        # Sugar
        tk.Label(self.root, text="Sugar (grams):").grid(row=7, column=0)
        self.sugar_entry = tk.Entry(self.root)
        self.sugar_entry.grid(row=7, column=1)


        # Entries Listbox
        self.entries_listbox = tk.Listbox(self.root, width=120, height=20)
        self.entries_listbox.grid(row=8, columnspan=2)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.entries_listbox.yview)
        scrollbar.grid(row=8, column=2, sticky="ns")
        self.entries_listbox.config(yscrollcommand=scrollbar.set)
        
        #Empty Row for formatting
        #tk.Label(self.root, text="").grid(row=9)

        # Buttons
        tk.Button(self.root, text="Add Entry", command=self.add_entry).grid(row=10, column=0)
        tk.Button(self.root, text="Delete Selected Entry", command=self.delete_selected_entry).grid(row=10, column=1)

    def create_menu(self):
        menubar = tk.Menu(self.root)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Add Entry", command=self.add_entry)
        #filemenu.add_command(label="Delete Selected Entry", command=self.delete_selected_entry)
        filemenu.add_command(label="View Entries", command=self.view_entries)
        filemenu.add_command(label="Delete Selected Entry", command=self.delete_selected_entry)
        filemenu.add_separator()
        filemenu.add_command(label="Export to CSV", command=self.export_to_csv)
        filemenu.add_command(label="Export to PDF", command=self.export_to_pdf)
        filemenu.add_separator()
        filemenu.add_command(label="Backup", command=self.diary.backup)  # New option for backup
        filemenu.add_command(label="Restore", command=self.diary.restore)  # New option for restore
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.close_window)
        menubar.add_cascade(label="File", menu=filemenu)

        settingsmenu = tk.Menu(menubar, tearoff=0)
        settingsmenu.add_command(label="Settings", command=self.open_settings)
        menubar.add_cascade(label="Settings", menu=settingsmenu)
        
        helpmenu = tk.Menu(menubar, tearoff=0)  # New "Help" menu
        helpmenu.add_command(label="Manual", command=self.open_help_pdf)  # Moved from "Settings" menu
        menubar.add_cascade(label="Help", menu=helpmenu)  # Add "Help" menu to the menubar 
        

        self.root.config(menu=menubar)
    
    
   # Define a new method for exporting to PDF
    def export_to_pdf(self):
        pdf_filename = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                 filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
        if pdf_filename:
            c = canvas.Canvas(pdf_filename, pagesize=letter)
            c.drawString(100, 750, "Food Diary Entries")
            entries = self.diary.view_entries()
            y = 730
            for entry in entries:
                entry_str = (f"Date: {entry['date']}, Meal: {entry['meal']}, Food Items: {entry['food_items']}, "
                         f"Calories: {entry['calories']}, Protein: {entry['protein']}g, Carbs: {entry['carbs']}g, Fats: {entry['fats']}g, Sugar: {entry['sugar']}g")
                lines = entry_str.split(',')
                for line in lines:
                    c.drawString(100, y, line[:80])  # Limiting to 80 characters per line
                    y -= 15
                y -= 30  # Add extra space between entries
            c.save()
            messagebox.showinfo("Success", f"Diary exported to {pdf_filename}")
  
    
    
    def open_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")

        tk.Label(settings_window, text="Date Format:").grid(row=0, column=0)
        self.date_format_var = StringVar(settings_window)
        self.date_format_var.set(self.date_format)
        date_format_options = ['Month-Day-Year', 'Day-Month-Year', 'Year-Month-Day']
       # self.date_format_menu = OptionMenu(settings_window, self.date_format_var, *date_format_options, command=self.update_date_format)
        self.date_format_menu = OptionMenu(settings_window, self.date_format_var, *date_format_options, command=lambda format: self.update_date_format(format))
        self.date_format_menu.grid(row=0, column=1)
        
    def update_date_format(self, format_name):
        # Map human-readable format name to corresponding format string
        format_map = {'Month-Day-Year': '%m-%d-%Y', 'Day-Month-Year': '%d-%m-%Y', 'Year-Month-Day': '%Y-%m-%d'}
        self.date_format = format_map.get(format_name)
        self.date_entry.delete(0, tk.END)  # Clear the date entry widget
        self.date_entry.insert(0, datetime.now().strftime(self.date_format))  # Insert current date with the new format
        print(f"Date format updated to: {format_name}")

   # def update_date_format(self, format):
   # def update_date_format(self, format):
      #  self.date_format = format
      #  self.date_entry.delete(0, tk.END)  # Clear the date entry widget
      #  self.date_entry.insert(0, datetime.now().strftime(self.date_format))  # Insert current date with the new format
      #  print(f"Date format updated to: {self.date_format}")


    def add_entry(self):
        date = self.date_entry.get()
        meal = self.meal_var.get()
        food_items = self.food_items_entry.get().split(', ')
        calories = float(self.calories_entry.get())
        protein = float(self.protein_entry.get())
        carbs = float(self.carbs_entry.get())
        fats = float(self.fats_entry.get())
        sugar = float(self.sugar_entry.get()) 
        try:
            datetime.strptime(date, self.date_format)  # Parse date using current date format
        except ValueError:
            messagebox.showerror("Error", f"Date format should be {self.date_format}.")
        self.date_entry.delete(0, tk.END)
        self.meal_var.set(self.meal_options[0])
        self.food_items_entry.delete(0, tk.END)
        self.calories_entry.delete(0, tk.END)
        self.protein_entry.delete(0, tk.END)
        self.carbs_entry.delete(0, tk.END)
        self.fats_entry.delete(0, tk.END)
        self.sugar_entry.delete(0, tk.END)

        self.diary.add_entry(date, meal, food_items, calories, protein, carbs, fats, sugar)
        messagebox.showinfo("Success", "Entry added successfully!")
        self.populate_entries_listbox()

    def delete_selected_entry(self):
        selected_index = self.entries_listbox.curselection()
        if selected_index:
            index = int(selected_index[0])
            success = self.diary.delete_entry(index)
            if success:
                messagebox.showinfo("Success", f"Entry at index {index} deleted successfully!")
                self.populate_entries_listbox()
        else:
            messagebox.showerror("Error", "No entry selected for deletion.")

    def view_entries(self):
        self.populate_entries_listbox()

    def export_to_csv(self):
        csv_filename = filedialog.asksaveasfilename(defaultextension=".csv",
                                                     filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if csv_filename:
            self.diary.export_to_csv(csv_filename)
            messagebox.showinfo("Success", f"Diary exported to {csv_filename}")

    def close_window(self):
        self.root.destroy()

    def populate_entries_listbox(self):
        self.entries_listbox.delete(0, tk.END)
        entries = self.diary.view_entries()
        for i, entry in enumerate(entries):
            food_items_str = ', '.join(entry['food_items'])  # Join food items into a single string
            entry_str = (f"Date: {entry['date']}, Meal: {entry['meal']}, Food Items: {food_items_str}, "
                     f"Calories: {entry['calories']}, Protein: {entry['protein']}g, Carbs: {entry['carbs']}g, Fats: {entry['fats']}g")
            self.entries_listbox.insert(tk.END, entry_str)


if __name__ == "__main__":
    diary = FoodDiary()
    root = tk.Tk()
    app = FoodDiaryApp(root, diary)
    root.mainloop()





