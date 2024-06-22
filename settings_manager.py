import json

class SettingsManager:
    def __init__(self, filename='settings.json'):
        self.filename = filename
        self.load()
        self.text_size = "Medium"  # Default text size
    def load(self):
        try:
            with open(self.filename, 'r') as f:
                self.data = json.load(f)
            print(f"Settings loaded from {self.filename}")
        except FileNotFoundError:
            print(f"No existing settings found, starting with default.")
            self.data = {'date_format': '%m-%d-%Y'}  # Default date format: Month, Day, Year
            self.save()

    def save(self):
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=4)
        print(f"Settings saved to {self.filename}")

    def get_date_format(self):
        return self.data['date_format']

    def set_date_format(self, date_format):
        self.data['date_format'] = date_format
        self.save()
