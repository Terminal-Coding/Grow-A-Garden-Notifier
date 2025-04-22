import threading
import colorsys
import customtkinter as ctk
from plyer import notification
import time
import pygame  # Import pygame for audio handling

NOTIFY_INTERVAL = 5  # 5 minutes

# Initialize pygame mixer for sound
pygame.mixer.init()

def send_notification():
    # Play the notification sound
    pygame.mixer.music.load("notify.wav")  # Make sure 'notify.wav' is in the correct directory
    pygame.mixer.music.play()

    # Send system notification
    notification.notify(
        title='GROW A GARDEN',
        message='SHOP HAS RESET',
        timeout=5
    )

class NotificationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Grow-A-Garden")
        self.root.geometry("440x240")
        self.root.resizable(False, False)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Rainbow title
        self.rainbow_label = ctk.CTkLabel(
            root,
            text="NOTIFIER",
            font=("Poppins", 28, "bold", "underline"),
            text_color="white"
        )
        self.rainbow_label.pack(pady=(15, 5))

        # Countdown label (initially hidden)
        self.label = ctk.CTkLabel(
            root,
            text="05:00",
            font=("Poppins", 36, "bold"),
            text_color="white"
        )

        # Start button
        self.start_button = ctk.CTkButton(
            root,
            text="Start",
            font=("Poppins", 20, "bold"),
            command=self.start_app,
            fg_color="#1f6aa5",
            hover_color="#155a8a",
            text_color="white",
            width=120,
            height=40,
            corner_radius=12
        )
        self.start_button.pack(pady=40)

        self.remaining = NOTIFY_INTERVAL
        self.animate_rainbow()

    def start_app(self):
        self.start_button.pack_forget()
        self.label.pack(expand=True)
        self.update_timer()
        self.start_notification_thread()

    def update_timer(self):
        minutes = self.remaining // 60
        seconds = self.remaining % 60
        self.label.configure(text=f"{minutes:02d}:{seconds:02d}")
        if self.remaining > 0:
            self.remaining -= 1
            self.root.after(1000, self.update_timer)
        else:
            self.remaining = NOTIFY_INTERVAL
            self.update_timer()

    def animate_rainbow(self, hue=0.0):
        r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        hex_color = "#{:02x}{:02x}{:02x}".format(int(r*255), int(g*255), int(b*255))
        self.rainbow_label.configure(text_color=hex_color)
        self.root.after(50, lambda: self.animate_rainbow((hue + 0.01) % 1.0))

    def start_notification_thread(self):
        def loop_notifications():
            while True:
                time.sleep(NOTIFY_INTERVAL)
                send_notification()

        threading.Thread(target=loop_notifications, daemon=True).start()


if __name__ == "__main__":
    app = ctk.CTk()
    NotificationApp(app)
    app.mainloop()
