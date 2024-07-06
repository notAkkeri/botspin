from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QFrame, QWidget, QTabWidget, QGridLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from rates import rates

def create_ui(app):
    ui_elements = {}

    tab_widget = QTabWidget()
    tab_widget.setStyleSheet("""
        QTabWidget::pane {
            border-top: 2px solid #333333;
        }
        QTabBar::tab {
            background: #333333;
            color: white;
            font-size: 16px;
            padding: 10px 20px;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            margin: 0 2px;
            min-width: 100px;
        }
        QTabBar::tab:selected, QTabBar::tab:hover {
            background: #555555;
        }
    """)

    spin_tab = QWidget()
    rates_tab = QWidget()

    spin_layout = QVBoxLayout(spin_tab)
    instruction_label = QLabel("Click an option to spin for a rarity", app)
    instruction_label.setFont(QFont("Arial", 16, QFont.Bold))
    instruction_label.setAlignment(Qt.AlignCenter)
    spin_layout.addWidget(instruction_label)

    tries_label = QLabel("Tries: 0", app)
    tries_label.setFont(QFont("Arial", 14))
    tries_label.setAlignment(Qt.AlignCenter)
    spin_layout.addWidget(tries_label)

    x2_toggle = QPushButton("X2 Rates Off", app)
    x2_toggle.setFont(QFont("Arial", 14))
    x2_toggle.setStyleSheet("""
        QPushButton {
            background-color: red;
            color: white;
            border-radius: 10px;
            padding: 10px;
            margin: 10px;
        }
        QPushButton:hover {
            background-color: #ff3333;
        }
    """)
    spin_layout.addWidget(x2_toggle)

    button_texts = ["Spin Common", "Spin Rare", "Spin Epic", "Spin Legendary", "Spin Mythical"]
    commands = ["common", "rare", "epic", "legendary", "mythical"]
    buttons = {}

    for i, text in enumerate(button_texts):
        button = QPushButton(text, app)
        button.setFont(QFont("Arial", 14))
        button.setStyleSheet("""
            QPushButton {
                background-color: #666666;
                color: white;
                border-radius: 10px;
                padding: 10px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #888888;
            }
        """)
        spin_layout.addWidget(button)
        buttons[commands[i]] = button

    result_label = QLabel("Spin the wheel to get an item", app)
    result_label.setFont(QFont("Arial", 14))
    result_label.setAlignment(Qt.AlignCenter)
    spin_layout.addWidget(result_label)

    tab_widget.addTab(spin_tab, "Spin")

    rates_layout = QVBoxLayout()
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_content = QWidget()
    scroll_layout = QVBoxLayout(scroll_content)

    rate_labels = {}
    for rarity, data in rates.items():
        rarity_label = QLabel(f"{rarity.capitalize()} Rates", app)
        rarity_label.setFont(QFont("Arial", 14))
        scroll_layout.addWidget(rarity_label)
        items_label = QLabel("\n".join([f"{item:<20} {data['rate']:.4%}" for item in data['items']]), app)
        items_label.setFont(QFont("Arial", 12))
        scroll_layout.addWidget(items_label)
        rate_labels[rarity] = items_label

    scroll_area.setWidget(scroll_content)
    rates_layout.addWidget(scroll_area)
    rates_tab.setLayout(rates_layout)
    tab_widget.addTab(rates_tab, "Rates")

    main_layout = QGridLayout(app)
    main_layout.addWidget(tab_widget)
    app.setLayout(main_layout)

    ui_elements['tries_label'] = tries_label
    ui_elements['x2_toggle'] = x2_toggle
    ui_elements['result_label'] = result_label
    ui_elements['buttons'] = buttons
    ui_elements['rate_labels'] = rate_labels

    return ui_elements

def apply_styles(app):
    app.setStyleSheet("""
        QWidget {
            background-color: #1e1e1e;
            color: white;
        }
        QLabel {
            font-size: 14px;
            padding: 10px;
            background-color: #1e1e1e;
            color: white;
        }
        QPushButton {
            font-size: 14px;
            background-color: #666666;
            color: white;
            padding: 10px;
            border-radius: 10px;
        }
        QPushButton:hover {
            background-color: #888888;
        }
        QScrollArea {
            background-color: #1e1e1e;
        }
        QScrollBar:vertical {
            border: none;
            background: #1e1e1e;
            width: 12px;
        }
        QScrollBar::handle:vertical {
            background: #888888;
            min-height: 20px;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            background: none;
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }
    """)

