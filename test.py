import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QCheckBox, QLabel, QSlider
from PyQt5.QtCore import Qt
undisplayed_phrases_global = []
selected_phrases_global = []
unselected_phrases_global = []
try:
    from generated_phrases import undisplayed_phrases as undisplayed_phrases_global, selected_phrases as selected_phrases_global, unselected_phrases as unselected_phrases_global

except ImportError:
    pass
class PhraseRecallTrainer(QWidget):
    def __init__(self):
        super().__init__()

        self.selected_phrases_current_session = set()
        self.undisplayed_phrases = []
        self.selected_phrases = []
        self.unselected_phrases = []
###################
        #######################
        ######################
        #this needs to be changed since it won't initialise an empty select and unselect list
        
        self.undisplayed_phrases = undisplayed_phrases_global
        self.selected_phrases = selected_phrases_global
        self.unselected_phrases = unselected_phrases_global

        
        self.displayed_phrases = []
        self.number_of_new_words = 0

        self.init_ui()

    def init_ui(self):
        self.slider_label = QLabel('Number of New Words to Display: 0', self)
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setRange(0, 5)
        self.slider.setTickInterval(1)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.valueChanged.connect(self.slider_value_changed)

        self.generate_button = QPushButton('Generate Phrases', self)
        self.generate_button.clicked.connect(self.generate_phrases)

        self.test_finished_button = QPushButton('Test Finished', self)
        self.test_finished_button.clicked.connect(self.generate_python_file)
        self.test_finished_button.hide()

        self.checkbox_list = []
        self.displayed_phrases_widget = QWidget(self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.slider_label)
        layout.addWidget(self.slider)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.displayed_phrases_widget)

        self.setGeometry(300, 300, 400, 200)
        self.setWindowTitle('Phrase Recall Trainer')

    def slider_value_changed(self):
        self.number_of_new_words = self.slider.value()
        self.slider_label.setText(f'Number of New Words to Display: {self.number_of_new_words}')

    def generate_phrases(self):
        # Calculate the number of phrases needed from each source
        slider_value = self.slider.value()
        undisplayed_count = min(slider_value, len(self.undisplayed_phrases))
        unselected_count = min(5 - slider_value, len(self.unselected_phrases))
        selected_count = min(5 - slider_value - unselected_count, len(self.selected_phrases))

        # Calculate the extra count needed to make it 5 phrases
        extra = 5 - (undisplayed_count + unselected_count + selected_count)
        undisplayed_count += extra

        # Randomly select phrases from each source
        undisplayed_phrases = random.sample(self.undisplayed_phrases, undisplayed_count)
        unselected_phrases = random.sample(self.unselected_phrases, unselected_count)
        selected_phrases = random.sample(self.selected_phrases, selected_count)

        # Combine the selected phrases
        self.displayed_phrases = undisplayed_phrases + unselected_phrases + selected_phrases

        # Clear previous checkboxes
        for checkbox in self.checkbox_list:
            checkbox.setParent(None)

        # Display new phrases
        self.checkbox_list = [QCheckBox(phrase) for phrase in self.displayed_phrases]

        displayed_phrases_layout = QVBoxLayout(self.displayed_phrases_widget)
        for checkbox in self.checkbox_list:
            checkbox.setChecked(False)  # Ensure checkboxes for new phrases are unchecked
            displayed_phrases_layout.addWidget(checkbox)  # Add checkbox to the displayed phrases widget

        # Show the Test Finished button below displayed phrases
        displayed_phrases_layout.addWidget(self.test_finished_button)
        self.test_finished_button.show()
        # Update self.selected_phrases and self.unselected_phrases based on checkbox state
        self.selected_phrases = {checkbox.text() for checkbox in self.checkbox_list if checkbox.isChecked()}
        self.unselected_phrases = list(set(self.displayed_phrases) - set(self.selected_phrases))
        

    def generate_python_file(self):
        self.selected_phrases_current_session = {checkbox.text() for checkbox in self.checkbox_list if checkbox.isChecked()}
        
        # Generate Python file
        
        unselected_phrases = list(set(self.displayed_phrases) - self.selected_phrases_current_session)
        
        # Create a new variable containing undisplayed phrases excluding displayed phrases
        undisplayed_phrases_output = list(set(undisplayed_phrases_global) - set(self.displayed_phrases))
        unselected_phrases = unselected_phrases_global.append(unselected_phrases)
        selected_phrases = selected_phrases_global
        with open('generated_phrases.py', 'w') as file:
            file.write(f'undisplayed_phrases = {undisplayed_phrases_output}\n\n')
            file.write(f'selected_phrases = {list(self.selected_phrases_current_session)}\n\n')
            file.write(f'unselected_phrases = {unselected_phrases}\n')

        print('Python file generated: generated_phrases.py')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PhraseRecallTrainer()
    ex.show()
    sys.exit(app.exec_())
