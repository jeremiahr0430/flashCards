import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QCheckBox, QLabel, QSlider, QStackedLayout
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

        self.undisplayed_phrases = self.undisplayed_phrases_global = undisplayed_phrases_global
        self.selected_phrases = self.selected_phrases_global = selected_phrases_global
        self.unselected_phrases = self.unselected_phrases_global = unselected_phrases_global
        # self.unselected_count_msg = 'initial test'
        # self.selected_count_msg = 'initial test2'
        
        self.displayed_phrases = []
        self.number_of_new_words = 0

        self.init_ui()

    def init_ui(self):
        #create two main widget working as two pages
        self.widget1 = QWidget()
        self.widget2 = QWidget()

        #create elements for the 1st page (widget)
        self.slider_label = QLabel('Number of New Words to Display: 0', self.widget1)
        self.slider = QSlider(Qt.Horizontal, self.widget1)
        self.slider.setRange(0, 5)
        self.slider.setTickInterval(1)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.valueChanged.connect(self.slider_value_changed)

        self.generate_button = QPushButton('Generate Phrases', self.widget1)
        self.generate_button.clicked.connect(self.generate_phrases)

        #create elements for the 2nd page (widget)
        self.checkbox_list = [QCheckBox('') for c in range(5)]
        
        self.msgLabel1 = QLabel('',self.widget2)
        self.msgLabel2 = QLabel('',self.widget2)
        self.displayed_phrases_widget = QWidget(self.widget2)

        self.test_finished_button = QPushButton('Test Finished', self.widget2)
        self.test_finished_button.clicked.connect(self.generate_python_file)
        #self.test_finished_button.hide()

        layout1 = QVBoxLayout(self.widget1)
        layout1.addWidget(self.slider_label)
        layout1.addWidget(self.slider)
        layout1.addWidget(self.generate_button)

        self.layout2 = QVBoxLayout(self.widget2)
        
        self.layout2.addWidget(self.displayed_phrases_widget) 
        displayed_phrases_layout = QVBoxLayout(self.displayed_phrases_widget)
        for checkbox in self.checkbox_list:
            checkbox.setChecked(False)  # Ensure checkboxes for new phrases are unchecked
            displayed_phrases_layout.addWidget(checkbox) #not adding checkbox in yet
        self.layout2.addWidget(self.msgLabel1)
        self.layout2.addWidget(self.msgLabel2)
        self.layout2.addWidget(self.test_finished_button)


        # Create stacked layout and add widgets
        self.stacked_layout = QStackedLayout()
        self.stacked_layout.addWidget(self.widget1)
        self.stacked_layout.addWidget(self.widget2)

        # Set the stacked layout as the main layout for the window
        self.setLayout(self.stacked_layout)

        # Connect buttons to switch widgets
        
        self.generate_button.clicked.connect(lambda: self.stacked_layout.setCurrentIndex(1))
        self.test_finished_button.clicked.connect(lambda: self.stacked_layout.setCurrentIndex(0))


        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('Phrase Recall Trainer')
    

    def slider_value_changed(self):
        self.number_of_new_words = self.slider.value()
        self.slider_label.setText(f'Number of New Phrases to Display: {self.number_of_new_words}')

    def generate_phrases(self):
        # Calculate the number of phrases needed from each source
        slider_value = self.slider.value()
        undisplayed_count = min(slider_value, len(self.undisplayed_phrases_global))
        #if phrases from undisplayed group are less than 5
        unselected_count = min(5 - slider_value, len(self.unselected_phrases_global))
        unselected_count_msg = f'Previously checked phrases : {unselected_count}'
        #if phrases from unselected group are less than 5
        selected_count = min(5 - slider_value - unselected_count, len(self.selected_phrases))
        selected_count_msg = f'Previously seen phrases :       {selected_count}'
        # Calculate the extra count needed to make it 5 phrases
        extra = 5 - (undisplayed_count + unselected_count + selected_count)
        undisplayed_count += extra
        print(f'extra is {extra}')
        # Randomly select phrases from each source
        undisplayed_phrases = random.sample(self.undisplayed_phrases, undisplayed_count)
        unselected_phrases = random.sample(self.unselected_phrases, unselected_count)
        selected_phrases = random.sample(list(self.selected_phrases), selected_count)

        # Combine the selected phrases
        self.displayed_phrases = undisplayed_phrases + unselected_phrases + selected_phrases

        for count, checkbox in enumerate(self.checkbox_list):
            checkbox.setChecked(False)  # Ensure checkboxes for new phrases are unchecked
            checkbox.setText(self.displayed_phrases[count])
            #displayed_phrases_layout.addWidget(checkbox)  # Add checkbox to the displayed phrases widget
        self.msgLabel1.setText(selected_count_msg)
        self.msgLabel2.setText(unselected_count_msg)
        self.selected_phrases = {checkbox.text() for checkbox in self.checkbox_list if checkbox.isChecked()}
        self.unselected_phrases = list(set(self.displayed_phrases) - set(self.selected_phrases))
        

    def generate_python_file(self):
        selected_phrases_output = {checkbox.text() for checkbox in self.checkbox_list if checkbox.isChecked()}
        print(f'global before is {self.selected_phrases_global}')
        ##update self.selected_phrases_global for multiple test
        selected_phrases_output = list(selected_phrases_output) + list(self.selected_phrases_global)
        self.selected_phrases_global = selected_phrases_output
        print(f'global after is {self.selected_phrases_global}',f'selected_phrases_output after is {selected_phrases_output}')
        

        # Generate Python file
        #print(self.displayed_phrases, selected_phrases_output)
        
        ##update self.unselected_phrases_global for multiple test
        unselected_phrases_output = list(set(self.displayed_phrases) - set(selected_phrases_output))
        unselected_phrases_output.extend(self.unselected_phrases_global)
        self.unselected_phrases_global = unselected_phrases_output

        # Create a new variable containing undisplayed phrases excluding displayed phrases
        undisplayed_phrases_output = list(set(self.undisplayed_phrases_global) - set(self.displayed_phrases))
        self.undisplayed_phrases_global = undisplayed_phrases_output
        #print(undisplayed_phrases_output)
        
        selected_phrases = selected_phrases_global
        with open('generated_phrases.py', 'w') as file:
            file.write(f'undisplayed_phrases = {undisplayed_phrases_output}\n\n')
            file.write(f'selected_phrases = {list(selected_phrases_output)}\n\n')
            file.write(f'unselected_phrases = {list(unselected_phrases_output)}\n')

        print('Python file generated: generated_phrases.py')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PhraseRecallTrainer()
    ex.show()
    sys.exit(app.exec_())
