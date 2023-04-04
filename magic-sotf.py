import tkinter as tk
import time
from pynput.keyboard import Key, Controller
import keyboard

keyboard_controller = Controller()

class ToggleButton(tk.Frame):
    def __init__(self, parent, command=None, prop_names=[], **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.command = command
        self.state = tk.IntVar(value=0)
        self.states = ['ignore', 'on', 'off']
        self.button = tk.Button(self, text=f'{prop_names[0]} : {self.states[self.state.get()]}', command=self.toggle)
        self.button.pack()
        self.prop_names = prop_names
        self.enabled = False
        self.previous_state = None # Initialize the previous_state attribute to None.
    def update_text(self):
        self.button.config(text=f'{self.prop_names[0]} : {self.states[self.state.get()]}')
    def toggle(self):
        self.previous_state = self.state.get() # Store the current state in the previous_state attribute.
        self.state.set((self.state.get() + 1) % 3)
        self.button.config(text=f'{self.prop_names[0]} : {self.states[self.state.get()]}')
        self.enabled = (self.state.get() in (1, 2))
        self.update_text()
        if self.command is not None:
            self.command(self.prop_names[0], self.states[self.state.get()])
            send_enabled_commands(None)  # appel à la fonction send_enabled_commands


# fonction pour simplifier l'envoi de commandes
def send_command(command):
     for line in command.split('\n'):
        time.sleep(0.5)
        keyboard_controller.press(Key.f1)
        time.sleep(0.1)
        keyboard_controller.release(Key.f1)
        time.sleep(0.5)
        keyboard_controller.type(line)
        time.sleep(0.1)
        keyboard_controller.press(Key.enter)
        time.sleep(0.1)
        keyboard_controller.release(Key.enter)





ai_radar_enabled = False
def toggle_ai_radar():
    global ai_radar_enabled
    ai_radar_enabled = not ai_radar_enabled
    keyboard_controller.press(Key.f1)
    time.sleep(0.1)
    keyboard_controller.release(Key.f1)
    time.sleep(0.1)
    if ai_radar_enabled:
        keyboard_controller.type('airadar on')
    else:
        keyboard_controller.type('airadar off')
    time.sleep(0.1)
    keyboard_controller.press(Key.enter)
    time.sleep(0.1)
    keyboard_controller.release(Key.enter)


ai_dummy_enabled = False
def toggle_ai_dummy():
    global ai_dummy_enabled
    ai_dummy_enabled = not ai_dummy_enabled
    keyboard_controller.press(Key.f1)
    time.sleep(0.1)
    keyboard_controller.release(Key.f1)
    time.sleep(0.1)
    if ai_dummy_enabled:
        keyboard_controller.type('aipause on')
    else:
        keyboard_controller.type('aipause off')
    time.sleep(0.1)
    keyboard_controller.press(Key.enter)
    time.sleep(0.1)
    keyboard_controller.release(Key.enter)


is_cheatstick_pressed = False

def send_enabled_commands(event):
    if event.name == 'f1':
        global is_cheatstick_pressed
        if not is_cheatstick_pressed:
            for char in 'cheatstick':
                time.sleep(0.1)
                keyboard_controller.press(char)
                time.sleep(0.1)
                keyboard_controller.release(char)
        is_cheatstick_pressed = True
    
    if event.name == 'f7':
        toggle_ai_dummy()            
    
    if event.name == 'f10':
        toggle_ai_radar()
    
    if event.name == 'f6':
        keyboard_controller.press(Key.f1)
        time.sleep(0.1)
        keyboard_controller.release(Key.f1)
        time.sleep(0.1)
        keyboard_controller.type('igniteradius 12')
        time.sleep(0.1)
        keyboard_controller.press(Key.enter)
        time.sleep(0.1)
        keyboard_controller.release(Key.enter)
    
    
    if event.name == 'f5':
        sticks_quantity = quantities['sticks'].get()
        rock_quantity = quantities['rock'].get()
        drink_quantity = quantities['drink'].get()
        fish_quantity = quantities['fish'].get()
        meds_quantity = quantities['meds'].get()

        # création de la commande avec les quantités
        command_parts_qty = []
        if sticks_quantity:
            command_parts_qty.append(f'spawnitem stick {sticks_quantity}\n')
        if rock_quantity:
            command_parts_qty.append(f'spawnitem rock {rock_quantity}\n')
        if drink_quantity:
            command_parts_qty.append(f'spawnitem energydrink {drink_quantity}\n')
        if fish_quantity:
            command_parts_qty.append(f'spawnitem fish {fish_quantity}\n')
        if meds_quantity:
            command_parts_qty.append(f'spawnitem 437 {meds_quantity}\n')

        if command_parts_qty:
            command_qty = ''.join(command_parts_qty)
            send_command(command_qty)
              # Supprimer les valeurs de tous les champs de texte
            for quantity in quantities.values():
                quantity.set('')
        enabled_props = [prop_name for prop_name in props if toggle_buttons[prop_name].enabled]
        if not enabled_props:
            return
        command_parts = []
        for prop_name in enabled_props:
            if toggle_buttons[prop_name].state.get() == 1:
                command_parts.append(prop_values[prop_name] + ' on\n')
            elif toggle_buttons[prop_name].state.get() == 2:
                command_parts.append(prop_values[prop_name] + ' off\n')
        if command_parts:
            command = ' '.join(command_parts)
            send_command(command)
            # Réinitialiser les boutons à leur état initial
            for prop_name in toggle_buttons:
                toggle_buttons[prop_name].state.set(0)
                toggle_buttons[prop_name].update_text()

                
    if all(not quantities[var].get() for var in quantities) and all(toggle_buttons[prop].state.get() == 0 for prop in props):
        return      
    

# exemple d'utilisation
props = [
    'God Mode',
    'Instant Book Build',
    'Unlimited Logs',
    'Add All Items',
    'Speedy Run'
]

prop_values = {
    'God Mode': 'godmode',
    'Instant Book Build': 'instantbookbuild',
    'Unlimited Logs': 'loghack',
    'Add All Items': 'addallitems',
    'Speedy Run': 'speedyrun'
}

toggle_buttons = {}

def on_toggle(prop_name, value):
    toggle_buttons[prop_name].enabled = (value == 'on' or 'off')



root = tk.Tk()
root.title('SOTF plus')
cr_label = tk.Label(root, text="HOW TO USE: ", font=('Arial', 14, 'bold'))
cr_label.pack()
cr1_label = tk.Label(root, text="Run the game and press F1 to ativate \n \nadd quantity and/or use toggle button and press F5\n \nincendio use F6\n \npetrifio use  F7\n \nwallahck use F10", font=('Arial', 14, 'bold'))
cr1_label.pack()
# création des variables pour stocker les quantités entrées
quantities = {
    'sticks': tk.StringVar(),
    'rock': tk.StringVar(),
    'drink': tk.StringVar(),
    'fish': tk.StringVar(),
    'meds': tk.StringVar(),
}

# création des labels et champs de texte pour entrer les quantités
label_sticks = tk.Label(root, text="Sticks quantity:")
label_sticks.pack()
entry_sticks = tk.Entry(root, textvariable=quantities['sticks'])
entry_sticks.pack()

label_rock = tk.Label(root, text="Rock quantity:")
label_rock.pack()
entry_rock = tk.Entry(root, textvariable=quantities['rock'])
entry_rock.pack()

label_drink = tk.Label(root, text="Drink quantity:")
label_drink.pack()
entry_drink = tk.Entry(root, textvariable=quantities['drink'])
entry_drink.pack()

label_fish = tk.Label(root, text="Fish quantity:")
label_fish.pack()
entry_fish = tk.Entry(root, textvariable=quantities['fish'])
entry_fish.pack()

label_meds = tk.Label(root, text="Meds quantity:")
label_meds.pack()
entry_meds = tk.Entry(root, textvariable=quantities['meds'])
entry_meds.pack()

root.geometry("450x550")
for prop_name in props:
    toggle_buttons[prop_name] = ToggleButton(root, command=on_toggle, prop_names=[prop_name, prop_values[prop_name]])
    toggle_buttons[prop_name].pack()

keyboard.on_press(send_enabled_commands)
root.mainloop()
