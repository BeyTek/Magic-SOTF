import tkinter as tk
import time
import keyboard

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
        self.previous_state = None

    def update_text(self):
        self.button.config(text=f'{self.prop_names[0]} : {self.states[self.state.get()]}')

    def toggle(self):
        self.previous_state = self.state.get()
        self.state.set((self.state.get() + 1) % 3)
        self.button.config(text=f'{self.prop_names[0]} : {self.states[self.state.get()]}')
        self.enabled = (self.state.get() in (1, 2))
        self.update_text()

        if self.command is not None:
            self.command(self.prop_names[0], self.states[self.state.get()])
            send_enabled_commands(None)

# Fonction pour simplifier l'envoi de commandes
def send_command(command):
    for line in command.split('\n'):
        time.sleep(0.5)
        keyboard.press('F1')
        time.sleep(0.1)
        keyboard.release('F1')
        time.sleep(0.5)
        keyboard.write(line)
        time.sleep(0.1)
        keyboard.press('enter')
        time.sleep(0.1)
        keyboard.release('enter')

ai_radar_enabled = False

def toggle_ai_radar():
    global ai_radar_enabled
    keyboard.press('F1')
    time.sleep(0.1)
    keyboard.release('F1')
    time.sleep(0.1)
    if ai_radar_enabled:
        keyboard.write('airadar on')
    else:
        keyboard.write('airadar off')
    time.sleep(0.1)
    keyboard.press('enter')
    time.sleep(0.1)
    keyboard.release('enter')
    ai_radar_enabled = not ai_radar_enabled

ai_dummy_enabled = False

def toggle_ai_dummy():
    global ai_dummy_enabled
    keyboard.press('F1')
    time.sleep(0.1)
    keyboard.release('F1')
    time.sleep(0.1)
    if ai_dummy_enabled:
        keyboard.write('aidummy on')
    else:
        keyboard.write('aidummy off')
    time.sleep(0.1)
    keyboard.press('enter')
    time.sleep(0.1)
    keyboard.release('enter')
    ai_dummy_enabled = not ai_dummy_enabled

is_cheatstick_pressed = False

def send_enabled_commands(event):
    global is_cheatstick_pressed
    
    if event.name == 'f1' and not is_cheatstick_pressed:
        for char in 'cheatstick':
            time.sleep(0.1)
            keyboard.press(char)
            time.sleep(0.1)
            keyboard.release(char)
        is_cheatstick_pressed = True

    if event.name == 'f7':
        toggle_ai_dummy()

    if event.name == 'f10':
        toggle_ai_radar()

    if event.name == 'f6':
        keyboard.press('F1')
        time.sleep(0.1)
        keyboard.release('F1')
        time.sleep(0.1)
        keyboard.write('igniteradius 12')
        time.sleep(0.1)
        keyboard.press('enter')
        time.sleep(0.1)
        keyboard.release('enter')

    if event.name == 'f5':
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
            for prop_name in toggle_buttons:
                toggle_buttons[prop_name].state.set(0)
                toggle_buttons[prop_name].update_text()

    if all(toggle_buttons[prop].state.get() == 0 for prop in props):
        return

# Exemple d'utilisation
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
cr1_label = tk.Label(root, text="Run the game and press F1 to activate \n \nuse toggle button and press F5\n \nincendio use F6\n \npetrifio use  F7\n \nwallahck use F10", font=('Arial', 14, 'bold'))
cr1_label.pack()

for prop_name in props:
    toggle_buttons[prop_name] = ToggleButton(root, command=on_toggle, prop_names=[prop_name, prop_values[prop_name]])
    toggle_buttons[prop_name].pack()

keyboard.on_press(send_enabled_commands)
root.mainloop()
