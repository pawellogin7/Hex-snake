from pynput import keyboard


# Jako, że gra ma odbywać się w czasie przeczywistym zamiast standardowego 'input'
# do wczytywania poleceń z klawiatury użyłem Keyboard Listenera z biblioteki pynput
class KeyboardListenerThread:
    def __init__(self):
        self.listener_p1 = keyboard.Listener(
            on_press=self.on_press_p1)
        self.listener_p1.start()
        self.listener_p2 = keyboard.Listener(
            on_press=self.on_press_p2)
        self.listener_p2.start()
        self.key_pressed_p1 = ''
        self.key_pressed_p2 = ''

    def on_press_p1(self, key):
        try:
            char = key.char
            if char == 'q' or char == 'w' or char == 'e' or char == 'a' or char == 's' or char == 'd':
                self.key_pressed_p1 = char
        except AttributeError:
            pass

    def on_press_p2(self, key):
        try:
            char = key.char
            if char == 'u' or char == 'i' or char == 'o' or char == 'j' or char == 'k' or char == 'l':
                self.key_pressed_p2 = char
        except AttributeError:
            pass



