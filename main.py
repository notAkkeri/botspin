import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import pyqtSignal, QObject
from rates import rates
from styling import create_ui, apply_styles

class Communicate(QObject):
    update_result = pyqtSignal(str)
    update_tries = pyqtSignal(int)

class SpinApp(QWidget):
    def __init__(self):
        super().__init__()
        self.tries = 0
        self.x2_rates = False
        self.initial_rates = rates.copy()
        self.comm = Communicate()
        self.comm.update_result.connect(self.update_result_label)
        self.comm.update_tries.connect(self.update_tries_label)
        self.init_ui()
        apply_styles(self)

    def init_ui(self):
        self.setWindowTitle("AOTR")
        self.setFixedSize(600, 600)
        self.ui_elements = create_ui(self)
        self.apply_connections()

    def apply_connections(self):
        self.ui_elements['x2_toggle'].clicked.connect(self.toggle_x2_rates)
        for rarity, button in self.ui_elements['buttons'].items():
            button.clicked.connect(lambda _, r=rarity: self.spin(r))

    def reset_tries(self):
        self.tries = 0
        self.update_tries_label()

    def update_tries_label(self, tries=None):
        if tries is None:
            tries = self.tries
        self.ui_elements['tries_label'].setText(f"Tries: {tries}")

    def update_result_label(self, result):
        self.ui_elements['result_label'].setText(result)

    def toggle_x2_rates(self):
        self.x2_rates = not self.x2_rates
        self.ui_elements['x2_toggle'].setText("X2 Rates On" if self.x2_rates else "X2 Rates Off")
        self.ui_elements['x2_toggle'].setStyleSheet(f"""
            QPushButton {{
                background-color: {"green" if self.x2_rates else "red"};
                color: white;
                border-radius: 10px;
                padding: 10px;
                margin: 10px;
            }}
            QPushButton:hover {{
                background-color: {"#33cc33" if self.x2_rates else "#ff3333"};
            }}
        """)
        self.update_rate_labels()

    def adjust_rate(self, rate, rarity):
        return rate * 2 if self.x2_rates else rate

    def spin(self, target_rarity):
        self.reset_tries()
        max_tries = 1000000
        found = False
        while not found and self.tries < max_tries:
            self.tries += 1
            item, rarity = self.perform_spin()
            if rarity == target_rarity:
                found = True
        if found:
            self.comm.update_result.emit(f"Congratulations! You got a {rarity} item: {item} in {self.tries} spins")
        else:
            self.comm.update_result.emit(f"Unable to get a {target_rarity} item within {max_tries} spins")
        self.comm.update_tries.emit(self.tries)

    def perform_spin(self):
        rand = random.random()
        cumulative = 0
        for rarity, data in self.get_adjusted_rates().items():
            cumulative += data["rate"]
            if rand < cumulative:
                item = random.choice(data["items"])
                return item, rarity
        return None, "none"

    def get_adjusted_rates(self):
        adjusted_rates = {}
        for rarity, data in self.initial_rates.items():
            adjusted_rates[rarity] = {
                "rate": data["x2_rate"] if self.x2_rates else data["rate"],
                "items": data["items"]
            }
        return adjusted_rates

    def update_rate_labels(self):
        for rarity, data in self.get_adjusted_rates().items():
            items_text = "\n".join([f"{item:<20} {data['rate']:.4%}" for item in data["items"]])
            self.ui_elements['rate_labels'][rarity].setText(items_text)
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = SpinApp()
    ex.show()
    sys.exit(app.exec_())
