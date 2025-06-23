import tkinter as tk
import time
import random

class TimeGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Time Game 🎯")
        self.geometry("800x600")
        self.configure(bg="#1e1e2f")
        self.resizable(False, False)

        self.font_large = ("Segoe UI", 28, "bold")
        self.font_medium = ("Segoe UI", 20)
        self.font_small = ("Segoe UI", 16)

        self.title_label = tk.Label(self, text="⏱️ ZAMAN TAHMİN OYUNU", font=self.font_large, bg="#1e1e2f", fg="#ffffff")
        self.title_label.pack(pady=(40, 10))

        self.instruction_label = tk.Label(self, text="Hedef süreyi yaz veya kaydır:", font=self.font_medium, bg="#1e1e2f", fg="#dddddd")
        self.instruction_label.pack()

        self.time_entry = tk.Entry(self, font=self.font_medium, justify="center", width=10)
        self.time_entry.pack(pady=10)
        self.time_entry.insert(0, "10")

        self.slider = tk.Scale(self, from_=1, to=300, orient="horizontal", length=400,
                               font=self.font_small, bg="#1e1e2f", fg="white",
                               troughcolor="#444", highlightthickness=0,
                               command=self.sync_entry)
        self.slider.set(10)
        self.slider.pack()

        self.buttons_frame = tk.Frame(self, bg="#1e1e2f")
        self.buttons_frame.pack(pady=20)

        self.start_btn = tk.Button(self.buttons_frame, text="🚀 BAŞLAT", font=self.font_medium,
                                   bg="#4CAF50", fg="white", width=12, command=self.start_timer)
        self.start_btn.grid(row=0, column=0, padx=10)
        self.start_btn.bind("<Enter>", lambda e: self.animate_button(self.start_btn, "#45d166"))
        self.start_btn.bind("<Leave>", lambda e: self.animate_button(self.start_btn, "#4CAF50"))

        self.stop_btn = tk.Button(self.buttons_frame, text="🛑 DURDUR", font=self.font_medium,
                                  bg="#f44336", fg="white", width=12, command=self.stop_timer, state="disabled")
        self.stop_btn.grid(row=0, column=1, padx=10)
        self.stop_btn.bind("<Enter>", lambda e: self.animate_button(self.stop_btn, "#ff6666"))
        self.stop_btn.bind("<Leave>", lambda e: self.animate_button(self.stop_btn, "#f44336"))

        self.elapsed_label = tk.Label(self, text="Geçen süre: 0.00 sn", font=self.font_medium, bg="#1e1e2f", fg="#00ffff")
        self.elapsed_label.pack(pady=10)

        self.result_label = tk.Label(self, text="", font=self.font_medium, bg="#1e1e2f", fg="#ffffff", justify="center")
        self.result_label.pack(pady=10)

        self.time_entry.bind("<FocusIn>", self.clear_result)
        self.running = False

    def animate_button(self, btn, color):
        btn.config(bg=color)

    def clear_result(self, event):
        self.result_label.config(text="")
        self.elapsed_label.config(text="Geçen süre: 0.00 sn")
        self.configure(bg="#1e1e2f")

    def sync_entry(self, val):
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, str(int(float(val))))

    def parse_time(self):
        text = self.time_entry.get().strip()
        if ":" in text:
            parts = text.split(":")
            if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                return int(parts[0]) * 60 + int(parts[1])
        if text.isdigit():
            return int(text)
        return self.slider.get()

    def start_timer(self):
        parsed = self.parse_time()
        self.target_time = parsed
        self.start_time = time.time()
        self.running = True
        self.update_elapsed_time()
        self.result_label.config(text="Sayaç başladı...")
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")

    def update_elapsed_time(self):
        if self.running:
            elapsed = time.time() - self.start_time
            self.elapsed_label.config(text=f"Geçen süre: {elapsed:.2f} sn")
            self.animate_elapsed_label()
            self.after(100, self.update_elapsed_time)

    def animate_elapsed_label(self):
        color = random.choice(["#00ffff", "#00e5ff", "#00ccff", "#00bfff"])
        self.elapsed_label.config(fg=color)

    def stop_timer(self):
        self.running = False
        elapsed = time.time() - self.start_time
        self.elapsed_label.config(text=f"Geçen süre: {elapsed:.2f} sn")
        self.elapsed_label.config(fg="#00ffff")

        difference = elapsed - self.target_time
        diff_display = f"{difference:+.2f}"

        if difference == 0:
            self.result_label.config(text="🎯 TAM ZAMANINDA! KAZANDIN!", fg="#00ff88")
            self.configure(bg="#003f2e")
            self.blink_label(self.result_label)
        else:
            self.result_label.config(
                text=f"🛑 Kaybettin!\nHedef: {self.target_time:.2f} sn\nGeçen: {elapsed:.2f} sn\nFark: {diff_display} sn",
                fg="#ff4444")
            self.configure(bg="#501818")
            self.shake_result()

        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")

    def blink_label(self, label, count=6):
        if count == 0:
            return
        current = label.cget("fg")
        label.config(fg="#ffffff" if current != "#ffffff" else "#00ff88")
        self.after(200, lambda: self.blink_label(label, count - 1))

    def shake_result(self, count=10):
        if count == 0:
            self.result_label.place_forget()
            self.result_label.pack(pady=10)
            return
        x = random.randint(-5, 5)
        y = random.randint(-5, 5)
        self.result_label.place(relx=0.5, rely=0.75, anchor="center", x=x, y=y)
        self.after(50, lambda: self.shake_result(count - 1))

if __name__ == "__main__":
    app = TimeGame()
    app.mainloop()
