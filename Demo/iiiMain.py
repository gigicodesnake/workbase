'''
Created on 26 Jan 2018

@author: chris
'''
from kivy.app import App
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.behaviors.focus import FocusBehavior

import db_methods

from email.policy import default
#from os.path import join
from bcrypt import hashpw, gensalt   
    

#the manager for the various screens
class Screen_manager(ScreenManager):
    pass
class Login_screen(Screen):
    def try_to_log(self):
        if self.ids.name_input.text == '' or self.ids.pass_input.text == '':
            popup = Popup(title='Input error', content=Label(text='Name field and password field cannot be left blank.\nPlease click outside this popup to enter a new value.'),
            size_hint= (0.5, 0.5))
            popup.open(0)
            return True
        else:
            db_methods.log_attempt(self.ids.name_input.text, self.ids.pass_input.text)

# this is the current opening screen, to be preceded by a login 
class Main_screen(Screen):
    pass

#main screen for lab operations    
class Lab_screen(Screen):
    pass

#main screen for production operations
class Production_screen(Screen):
    
    def resetall(self):
        db_methods.reset_orders_id()
    

#input screen for lab orders
class Lab_orders_input_screen(Screen):
    
    #x_hint labels controls overall division of screen between labels and inputs 
    
    x_hint_labels = 0.25
    y_hint_buttons = 0.1
    font_labels = 18
    font_buttons = 50
    font_text_input = 20
    
    # inputs order to database
    def input_order_to_db(self):
        
        input_list = []
        
        #create list from text fields and toggle buttons
        for keys, val in self.ids.items():
            if (val.group) == 'toggle':
                if(val.state) == 'down':
                    input_list.append(val.text)
            else:
                input_list.append(val.text)
        # check that name field is not empty       
        if (input_list[0]) == '':
            popup = Popup(title='Input error', content=Label(text='Name field cannot be left blank.\nPlease click outside this popup to enter a new value.'),
            size_hint= (0.5, 0.5))
            popup.open(0)
            return True     
        
        db_methods.input_into_orders_table(input_list)
        
        self.ids['name_field'].text = ''
        self.ids['catalouge_field'].text = ''
        self.ids['cas_field'].text = ''
        self.ids['manufacturer_field'].text = ''
        self.ids['supplier_field'].text = ''
        self.ids['price_field'].text = '0'
        self.ids['quantity_field'].text = ''
        self.ids['ordered_field'].text = '0'
        self.ids['user_field'].text = ''
        self.ids['reference_field'].text = ''
        self.ids['order_open_toggle'].state = 'down'
        self.ids['order_partial_toggle'].state = 'normal'
        self.ids['order_closed_toggle'].state = 'normal'
        self.ids['notes_field'].text = ''

        
class Lab_stock_input_screen(Screen):
    
    x_hint_labels = 0.25
    y_hint_buttons = 0.1
    font_labels = 18
    font_buttons = 50
    font_text_input = 20

# this handles which screen to open (orders,stock) via the status of toggle buttons
class Lab_operations_buttons(BoxLayout):
    
    def input_press(self):
        if self.parent.parent.ids.lab_tables_list.ids.order_toggle.state == 'down':
            self.parent.parent.manager.current = 'lab_orders_input_screen'
        elif self.parent.parent.ids.lab_tables_list.ids.stock_toggle.state == 'down':
            self.parent.parent.manager.current = 'lab_stock_input_screen'
    def edit_press(self):
        pass
    def view_press(self):
        if self.parent.parent.ids.lab_tables_list.ids.order_toggle.state == 'down':
            db_methods.view_table('lab_orders_table', [])
        elif self.parent.parent.ids.lab_tables_list.ids.stock_toggle.state == 'down':
            db_methods.view_table('lab_stock_table', [])
    def query_press(self):
        pass
class Lab_tables_list(BoxLayout):
    pass
class TextField(TextInput):
    
    write_tab = False
    
class FloatInput(TextField):
    
    default_value = '0'
   
    def check_float(self):
        
        try:
            float(self.text)
        except ValueError:
            self.text =''
            popup = Popup(title='Input error', content=Label(text='Input is not a valid number.\nPlease click outside this popup to enter a new value.'),
            size_hint= (0.5, 0.5))
            popup.open(0)

class iiiApp(App):
    title = 'ICP Interactive Interface'
    def build(self):
        return Screen_manager()

if __name__ == "__main__":
    iiiApp().run()

        
