import tkinter as tk
import random
import gc  
from rates import rates
from styling import label_style, button_style, toggle_button_style, frame_style, rate_frame_style, item_rates_bg

class SpinApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AOTR")
        self.root.geometry("900x900")
        self.root.resizable(False, False)
        self.tries = 0
        self.spinning = False
        self.x2_rates = False
        self.initial_rates = rates.copy()  
        self.setup_ui()

    def setup_ui(self):
        left_frame = tk.Frame(self.root, **frame_style)
        left_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH, expand=True)

        instruction_label = tk.Label(left_frame, text="Click an option to spin for a rarity", **label_style)
        instruction_label.pack(pady=10)

        self.tries_label = tk.Label(left_frame, text="Tries: 0", **label_style)
        self.tries_label.pack(pady=10)

        self.x2_toggle = tk.Button(left_frame, text="X2 Rates Off", command=self.toggle_x2_rates, **toggle_button_style)
        self.update_x2_toggle()  
        self.x2_toggle.pack(pady=10)


        frame_buttons = tk.Frame(left_frame, bg="#f0f0f0")
        frame_buttons.pack(pady=10)

        button_texts = ["Spin Common", "Spin Rare", "Spin Epic", "Spin Legendary"]
        commands = [self.spin_until("common"), self.spin_until("rare"), self.spin_until("epic"), self.spin_until("legendary")]

        self.buttons = []
        for i, text in enumerate(button_texts):
            button = tk.Button(frame_buttons, text=text, command=commands[i], **button_style)
            button.pack(fill=tk.X, padx=10, pady=5)
            self.buttons.append(button)

        self.result_label = tk.Label(left_frame, text="Spin the wheel to get an item", **label_style)
        self.result_label.pack(pady=20)

        self.right_frame = tk.Frame(self.root, **frame_style)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        rates_label = tk.Label(self.right_frame, text="Item Rates", font=("Arial", 16, "bold"), bg="white", fg="black", padx=10, pady=5)
        rates_label.pack(pady=10)

        self.rate_labels = {}
        self.rate_label_frames = {}
        for rarity, data in rates.items():
            rarity_frame = tk.LabelFrame(self.right_frame, text=f"{rarity.capitalize()} Rates", **rate_frame_style)
            rarity_frame.pack(padx=10, pady=5, anchor="w", fill=tk.X, expand=True)

            items_text = "\n".join([f"{item:<20} {self.adjust_rate(data['rate'], rarity):.2%}" for item in data["items"]])
            items_label = tk.Label(rarity_frame, text=items_text, font=("Arial", 12), justify=tk.LEFT, bg="#f9f9f9")
            items_label.pack(anchor="w")

            self.rate_labels[rarity] = items_label
            self.rate_label_frames[rarity] = rarity_frame

    def reset_tries(self):
        self.tries = 0
        self.update_tries_label()

    def update_tries_label(self):
        self.tries_label.config(text=f"Tries: {self.tries}")

    def toggle_x2_rates(self):
        self.x2_rates = not self.x2_rates
        self.update_x2_toggle()  
        self.update_rate_labels() 

    def update_x2_toggle(self):
        if self.x2_rates:
            self.x2_toggle.config(text="X2 Rates On", bg="#4CAF50")
        else:
            self.x2_toggle.config(text="X2 Rates Off", bg="#f44336")

    def adjust_rate(self, rate, rarity):
        if rarity == "legendary":
            if self.x2_rates:
                return 0.001 
            else:
                return 0.0005 
        else:
            return rate

    def spin_until(self, target_rarity):
        def command():
            if self.spinning:
                return  
            self.spinning = True
            self.reset_tries()
            while True:
                self.tries += 1
                item, rarity = self.spin()
                self.result_label.config(text=f"Spinning... {item}")
                self.update_tries_label()
                if rarity == target_rarity:
                    self.result_label.config(text=f"Congratulations! You got a {rarity} item: {item}")
                    self.spinning = False
                    break
                self.root.update() 
                self.root.after(1)  
                gc.collect()  
        return command

    def spin(self):
        rand = random.random()
        cumulative = 0
        for rarity, data in self.get_adjusted_rates().items():
            cumulative += data["rate"]
            if rand < cumulative:
                item = random.choice(data["items"])
                return item, rarity
        return None, "none"

    def get_adjusted_rates(self):
        adjusted_rates = rates.copy()
        return adjusted_rates

    def update_rate_labels(self):
        for rarity, data in rates.items():
            items_text = "\n".join([f"{item:<20} {self.adjust_rate(data['rate'], rarity):.2%}" for item in data["items"]])
            self.rate_labels[rarity].config(text=items_text)

            self.rate_label_frames[rarity].destroy()
            rarity_frame = tk.LabelFrame(self.right_frame, text=f"{rarity.capitalize()} Rates", **rate_frame_style)
            rarity_frame.pack(padx=10, pady=5, anchor="w", fill=tk.X, expand=True)

            items_label = tk.Label(rarity_frame, text=items_text, font=("Arial", 12), justify=tk.LEFT, bg="#f9f9f9")
            items_label.pack(anchor="w")
            self.rate_labels[rarity] = items_label
            self.rate_label_frames[rarity] = rarity_frame

if __name__ == "__main__":
    root = tk.Tk()
    app = SpinApp(root)
    root.mainloop()
