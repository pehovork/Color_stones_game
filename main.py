import kivy 
kivy.require('1.11.1')


from kivy.app import App                    # this must always be imported! it's the main thing for every app
from kivy.lang import Builder               # it allows to connect kivy file
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition   # it will manage individual screens 
from kivy.uix.button import Button, ButtonBehavior
from kivy.uix.image import Image
from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock   
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import  BoxLayout
from kivy.graphics import Rectangle, Color


class HomeScreen(Screen):
    pass

class ImageButton(ButtonBehavior, Image):
    pass

class SettingsScreen(Screen):
    pass


class StatisticsScreen(Screen):
    pass   



class HelpScreen(Screen):
    pass
class BoxLayout_help(BoxLayout):
    pass
class ScrollableLabel_help(ScrollView):
    pass  



class FieldSizeScreen(Screen):
    x1 = ObjectProperty(None)                # this will connect variable "x1" with "size_of_field" in field_size_screen.kv file
    
    def eraser(self, *args):                 # function will delete temporary label 
        self.remove_widget(self.temporary)
    
    def btn (self):                          # executes if the start_game button is pressed - it is defined in the .kv file 
        
        x2 = self.x1.text                    # I had to create a new variable to convert text to string. 'X1' is connection through kivy.   
        
        while True:                       
            try:                       
                if 10 > int(x2) > 2:  
                    self.parent.current = "GameScreen"              # I have to place 'change screen' here and not to kv file because condition have to met !
                    sm.get_screen('GameScreen').generate(self)      # it will generate a playing field in the next screen                                        
                    break                
            except:                          
                self.temporary = Label ( text ="Enter number !", pos_hint = {'x': .1,'y': -0.3}, font_size = 40, color = (1,0,0,1))
                self.add_widget(self.temporary)            # it will add widget to field screen 
                Clock.schedule_once(self.eraser, 3)        # The widget will only be there for 3 seconds then the delete function will be called         
                break                                      # I added a break so I don't have an infinite loop                
            else:                                                                         
                self.temporary = Label ( text ="Number has to be between 3 and 9 ! ", pos_hint = {'x': .1,'y': -0.3}, font_size = 40, color = (1,0,0,1))
                self.add_widget(self.temporary)
                Clock.schedule_once(self.eraser, 3)
                break
            
    pass


class GameScreen(Screen):  

    def eraser_and_exit(self, *args):                     
        self.remove_widget(self.temporary2)
        self.parent.current = "HomeScreen"


    def generate (self, *args):
            
        x3 = sm.get_screen('FieldSizeScreen').ids.size_of_field.text         # this way I get to the text input: "size_of_field" from the second screen 

        x4 = int (x3) 
        
        def eraser2():                    # the function will clear the whole field - so that the old stone which was there before will be deleted 
            self.remove_widget(self.game_field)
           
        import string
        abc=list(string.ascii_lowercase)             # list of alphabet characters

               
        number_of_stones = int(sm.get_screen('SettingsScreen').ids.spinner_stones.text)  # number from settings screen 
        
                   
        def stone_rotation (z):      
            if main_list[z] == number_of_stones:
                main_list[z] = 1
                print (z)
            else:
                main_list[z]+=1

        main_list= [1] * x4*x4
           
        
        import random
        
        for g in range (6*x4):
            rand_line = random.randrange(0, x4)
            for ra_l in range (x4):
                stone_rotation (rand_line*x4-x4+ra_l)  

        for g in range (random.randrange(0, 6)):
            for ra_u in range (x4):
                stone_rotation (ra_u*x4+ra_u)              

        for g in range (random.randrange(0, 6)):
            for ra_u2 in range (x4,0,-1):
                stone_rotation (ra_u2*x4-ra_u2)

        for g in range (6*x4):
            rand_column = random.randrange(0, x4)
            for ra_s in range (x4):
                stone_rotation (rand_column+x4*ra_s)
               
              
              
        def button_is_pressed_collumn (self):
            for t in range (x4): 
                stone_rotation (abc.index(self.text)+x4*t)    # Formula for rotating the stone - columns are rotated. Text of the button is taken - order of the letters in the list 'abc' 
            eraser2()
            generate_field()
            check ()

        def button_is_pressed_line (self):
            for s in range (x4): 
                stone_rotation ((int(self.text))*x4-x4+s)      # Formula for rotating the stone, lines are rotated, Text of the button is taken - number
            eraser2()
            generate_field()
            check ()
                

        def button_is_pressed_diagonal (self):
            for v in range (x4): 
                stone_rotation (v*x4+v)      # Formula for rotating the stone, diagonal from top to bottom is rotated, Text of the button is taken '*'
            eraser2()
            generate_field()
            check ()    

        def button_is_pressed_diagonal2 (self):
            for r in range (x4,0,-1): 
                stone_rotation (r*x4-r)      # Formula for rotating the stone, diagonal from bottom to top is rotated, Text of the button is taken '+'
            eraser2()
            generate_field()
            check ()        

        def generate_field ():
            self.game_field = GridLayout (cols=x4+1,rows=x4+2)    # create a field but I had to put it at the beginning of this def to generate it again after clicking the button   
            self.add_widget (self.game_field)                     # I have to add the layout itself as a widget and not just the buttons themselves !!

            for i in range(x4):                                   # these are the lines
                if i == 0:
                    self.button = Button(text="*")                    
                    self.button.bind (on_press = button_is_pressed_diagonal)
                    self.game_field.add_widget(self.button)             
                
                    for k in range (x4):
                        self.button2 = Button(text=abc[k]) 
                        self.button2.bind (on_press = button_is_pressed_collumn)
                        self.game_field.add_widget(self.button2)       # print alphabet characters in first line 
                        
                for j in range (x4):                            # these are the columns 
                    if j == 0:
                        self.button3 = Button(text=str(i+1) ) 
                        self.button3.bind (on_press = button_is_pressed_line)
                        self.game_field.add_widget(self.button3)               # print numbers in first column
                                                              
                
                    if main_list[i*x4+j] == 1:
                        self.game_field.add_widget(Image(source = "png/1amethyst.png"))              
                    if main_list[i*x4+j] == 2:
                        self.game_field.add_widget(Image(source = "png/2gemstone.png"))
                    if main_list[i*x4+j] == 3:
                        self.game_field.add_widget(Image(source = "png/3green_stone.png"))
                    if main_list[i*x4+j] == 4:
                        self.game_field.add_widget(Image(source = "C:png/4morganite.png"))
                    if main_list[i*x4+j] == 5:
                        self.game_field.add_widget(Image(source = "C:png/5stone.png"))
                    if main_list[i*x4+j] == 6:
                        self.game_field.add_widget(Image(source = "C:png/6diamond.png"))

            self.button4 = Button(text="+") 
            self.button4.bind (on_press = button_is_pressed_diagonal2)
            self.game_field.add_widget(self.button4)

        def check ():
            ok = 0
            for ch in range (x4*x4-1):
                if main_list[ch] != main_list[ch+1]:   # it will compare numbers (stones) in the list whether all numbers are the same.  if they are then ok = 1
                    ok = 1
            if ok ==0:
                self.temporary2 = Label (text = "Victory !!!", pos_hint = {'x': .02,'y': 0.15}, font_size = 150, color = (1,0,0,1))
                self.add_widget(self.temporary2)    
                eraser2()      
                Clock.schedule_once(self.eraser_and_exit, 3) 
            
        generate_field()
                  
    pass            
          

Builder.load_file('kv/HomeScreen.kv')
Builder.load_file('kv/SettingsScreen.kv')
Builder.load_file('kv/StatisticsScreen.kv')
Builder.load_file('kv/HelpScreen.kv')
Builder.load_file('kv/FieldSizeScreen.kv')
Builder.load_file('kv/GameScreen.kv')

sm = ScreenManager(transition=WipeTransition())
sm.add_widget(HomeScreen(name="HomeScreen"))
sm.add_widget(SettingsScreen(name="SettingsScreen"))
sm.add_widget(StatisticsScreen(name="StatisticsScreen"))
sm.add_widget(HelpScreen(name="HelpScreen"))
sm.add_widget(FieldSizeScreen(name="FieldSizeScreen"))
sm.add_widget(GameScreen(name="GameScreen"))          
   

class mainApp(App):                               # this is main app 
    __version__ = "5.0.0"
    def build(self):     
        return sm
    
    
mainApp().run() 




