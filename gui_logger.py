import tkinter as tk
from tkinter import ttk, messagebox
import time
import json
import os
from datetime import datetime

class LocalLoggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Focus-Restricted Key Event Recorder")
        self.root.geometry("680x520")
        self.root.configure(bg="#1e1e2e")
        self.root.resizable(False, False)

        self.is_logging = False
        self.log_data = []
        self.key_counter = 0
        self.session_start_time = None

        self.setup_styles()
        self.create_widgets()
        self.root.bind("<Key>", self.handle_key_event)

    def setup_styles(self):
        self.bg_color = "#1e1e2e"
        self.card_color = "#252538"
        self.text_color = "#cdd6f4"
        self.text_dim = "#a6adc8"
        self.accent_green = "#a6e3a1"
        self.accent_red = "#f38ba8"
        self.accent_blue = "#89b4fa"

    def create_widgets(self):
        header = tk.Frame(self.root, bg=self.card_color, height=60)
        header.pack(fill="x", padx=0, pady=0)
        header.pack_propagate(False)

        title_lbl = tk.Label(
            header,
            text="Local Keyboard Event Recorder",
            font=("Segoe UI", 14, "bold"),
            fg=self.text_color,
            bg=self.card_color
        )
        title_lbl.pack(side="left", padx=20, pady=15)

        self.status_indicator = tk.Canvas(header, width=16, height=16, bg=self.card_color, highlightthickness=0)
        self.status_indicator.pack(side="right", padx=(0, 20), pady=22)
        self.draw_status_indicator(self.accent_red)

        self.status_lbl = tk.Label(
            header,
            text="INACTIVE",
            font=("Segoe UI", 10, "bold"),
            fg=self.accent_red,
            bg=self.card_color
        )
        self.status_lbl.pack(side="right", padx=10, pady=15)

        controls_frame = tk.Frame(self.root, bg=self.bg_color)
        controls_frame.pack(fill="x", padx=20, pady=15)

        self.start_btn = tk.Button(
            controls_frame,
            text="▶ Start Logging",
            font=("Segoe UI", 10, "bold"),
            bg=self.accent_green,
            fg="#11111b",
            activebackground="#89dceb",
            activeforeground="#11111b",
            relief="flat",
            padx=15,
            pady=6,
            command=self.start_logging
        )
        self.start_btn.pack(side="left", padx=(0, 10))

        self.stop_btn = tk.Button(
            controls_frame,
            text="■ Stop Logging",
            font=("Segoe UI", 10, "bold"),
            bg=self.accent_red,
            fg="#11111b",
            activebackground="#eba0ac",
            activeforeground="#11111b",
            relief="flat",
            padx=15,
            pady=6,
            command=self.stop_logging,
            state="disabled"
        )
        self.stop_btn.pack(side="left", padx=10)

        self.save_btn = tk.Button(
            controls_frame,
            text="💾 Save Log",
            font=("Segoe UI", 10, "bold"),
            bg=self.accent_blue,
            fg="#11111b",
            activebackground="#b4befe",
            activeforeground="#11111b",
            relief="flat",
            padx=15,
            pady=6,
            command=self.save_logs
        )
        self.save_btn.pack(side="right")

        stats_frame = tk.Frame(self.root, bg=self.bg_color)
        stats_frame.pack(fill="x", padx=20, pady=(0, 15))

        self.card1 = tk.Frame(stats_frame, bg=self.card_color, padx=15, pady=10)
        self.card1.pack(side="left", expand=True, fill="both", padx=(0, 10))
        self.kpm_lbl = tk.Label(self.card1, text="Total Keystrokes", font=("Segoe UI", 9), fg=self.text_dim, bg=self.card_color)
        self.kpm_lbl.pack(anchor="w")
        self.kpm_val = tk.Label(self.card1, text="0", font=("Segoe UI", 18, "bold"), fg=self.accent_blue, bg=self.card_color)
        self.kpm_val.pack(anchor="w")

        self.card2 = tk.Frame(stats_frame, bg=self.card_color, padx=15, pady=10)
        self.card2.pack(side="left", expand=True, fill="both", padx=10)
        self.time_lbl = tk.Label(self.card2, text="Focus Status", font=("Segoe UI", 9), fg=self.text_dim, bg=self.card_color)
        self.time_lbl.pack(anchor="w")
        self.time_val = tk.Label(self.card2, text="Local Window Only", font=("Segoe UI", 12, "bold"), fg=self.accent_green, bg=self.card_color)
        self.time_val.pack(anchor="w", pady=(5, 0))

        log_container = tk.Frame(self.root, bg=self.card_color, padx=10, pady=10)
        log_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        log_header = tk.Label(
            log_container,
            text="Live Keyboard Event Stream (Focus restricted):",
            font=("Segoe UI", 10, "bold"),
            fg=self.text_color,
            bg=self.card_color
        )
        log_header.pack(anchor="w", pady=(0, 5))

        scrollbar = tk.Scrollbar(log_container)
        scrollbar.pack(side="right", fill="y")

        self.text_area = tk.Text(
            log_container,
            bg="#11111b",
            fg=self.accent_green,
            insertbackground=self.text_color,
            relief="flat",
            font=("Consolas", 10),
            yscrollcommand=scrollbar.set,
            state="disabled"
        )
        self.text_area.pack(fill="both", expand=True)
        scrollbar.config(command=self.text_area.yview)

    def draw_status_indicator(self, color):
        self.status_indicator.delete("all")
        self.status_indicator.create_oval(2, 2, 14, 14, fill=color, outline="")

    def start_logging(self):
        self.is_logging = True
        self.session_start_time = time.time()
        self.status_lbl.config(text="ACTIVE & RECORDING", fg=self.accent_green)
        self.draw_status_indicator(self.accent_green)
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.log_message("[System Message] Logging session started. Focused keypresses will be logged.")

    def stop_logging(self):
        self.is_logging = False
        self.status_lbl.config(text="INACTIVE", fg=self.accent_red)
        self.draw_status_indicator(self.accent_red)
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.log_message("[System Message] Logging session stopped.")

    def handle_key_event(self, event):
        if not self.is_logging:
            return

        focused_widget = self.root.focus_get()
        if focused_widget is None:
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        
        key_repr = event.char
        if not key_repr or ord(event.char) < 32:
            key_repr = f"[{event.keysym}]"

        log_entry = {
            "timestamp": timestamp,
            "key": event.keysym,
            "char": event.char if event.char.isprintable() else "",
            "keycode": event.keycode
        }

        self.log_data.append(log_entry)
        self.key_counter += 1
        self.kpm_val.config(text=str(self.key_counter))

        display_text = f"[{timestamp}] Key Pressed: {key_repr:<15} | KeyCode: {event.keycode:<5}\n"
        self.log_message(display_text)

    def log_message(self, message):
        self.text_area.config(state="normal")
        self.text_area.insert(tk.END, message)
        self.text_area.see(tk.END)
        self.text_area.config(state="disabled")

    def save_logs(self):
        if not self.log_data:
            messagebox.showinfo("Save Log", "No keystroke events have been recorded in this session.")
            return

        file_name = f"keystroke_log_{int(time.time())}.json"
        try:
            with open(file_name, "w") as f:
                json.dump(self.log_data, f, indent=4)
            messagebox.showinfo("Save Success", f"Logs successfully saved to:\n{os.path.abspath(file_name)}")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save log file: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = LocalLoggerApp(root)
    root.mainloop()
