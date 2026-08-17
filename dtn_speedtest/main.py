import customtkinter as ctk
import threading
from core import test_speed, save_to_history

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window settings
        self.title("DTN Speedtest - Édition 2026")
        self.geometry("800x500")
        self.resizable(False, False)

        # Modern Appearance
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar ---
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="DTN\nSpeedtest", font=ctk.CTkFont(size=28, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(40, 10))

        self.subtitle_label = ctk.CTkLabel(self.sidebar_frame, text="Wilaya d'El Menia", font=ctk.CTkFont(size=14, slant="italic"), text_color="gray")
        self.subtitle_label.grid(row=1, column=0, padx=20, pady=(0, 30))

        self.start_button = ctk.CTkButton(self.sidebar_frame, text="DÉMARRER", font=ctk.CTkFont(size=16, weight="bold"), height=45, command=self.start_test_thread)
        self.start_button.grid(row=2, column=0, padx=20, pady=10)

        self.status_label = ctk.CTkLabel(self.sidebar_frame, text="Prêt", font=ctk.CTkFont(size=14))
        self.status_label.grid(row=3, column=0, padx=20, pady=10)

        self.footer_label = ctk.CTkLabel(self.sidebar_frame, text="Dirigé par:\nM. Mesbah Mourad", justify="center", font=ctk.CTkFont(size=12))
        self.footer_label.grid(row=4, column=0, padx=20, pady=20, sticky="s")

        # --- Main Content ---
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.main_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        # Title
        self.header_label = ctk.CTkLabel(self.main_frame, text="Tableau de Bord", font=ctk.CTkFont(size=32, weight="bold"))
        self.header_label.grid(row=0, column=0, columnspan=3, pady=(10, 30), sticky="w")

        # Cards Frame (Ping, Download, Upload)
        # Ping Card
        self.ping_card = ctk.CTkFrame(self.main_frame, corner_radius=15, fg_color="#2b2b2b")
        self.ping_card.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.ping_title = ctk.CTkLabel(self.ping_card, text="PING", font=ctk.CTkFont(size=16, weight="bold"), text_color="gray")
        self.ping_title.pack(pady=(30, 5))
        self.ping_value = ctk.CTkLabel(self.ping_card, text="--", font=ctk.CTkFont(size=40, weight="bold"), text_color="#00a8ff")
        self.ping_value.pack(pady=5)
        self.ping_unit = ctk.CTkLabel(self.ping_card, text="ms", font=ctk.CTkFont(size=14), text_color="gray")
        self.ping_unit.pack(pady=(0, 20))

        # Download Card
        self.dl_card = ctk.CTkFrame(self.main_frame, corner_radius=15, fg_color="#2b2b2b")
        self.dl_card.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.dl_title = ctk.CTkLabel(self.dl_card, text="TÉLÉCHARGEMENT", font=ctk.CTkFont(size=14, weight="bold"), text_color="gray")
        self.dl_title.pack(pady=(30, 5))
        self.dl_value = ctk.CTkLabel(self.dl_card, text="--", font=ctk.CTkFont(size=40, weight="bold"), text_color="#4cd137")
        self.dl_value.pack(pady=5)
        self.dl_unit = ctk.CTkLabel(self.dl_card, text="Mbps", font=ctk.CTkFont(size=14), text_color="gray")
        self.dl_unit.pack(pady=(0, 20))

        # Upload Card
        self.ul_card = ctk.CTkFrame(self.main_frame, corner_radius=15, fg_color="#2b2b2b")
        self.ul_card.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
        self.ul_title = ctk.CTkLabel(self.ul_card, text="ENVOI", font=ctk.CTkFont(size=16, weight="bold"), text_color="gray")
        self.ul_title.pack(pady=(30, 5))
        self.ul_value = ctk.CTkLabel(self.ul_card, text="--", font=ctk.CTkFont(size=40, weight="bold"), text_color="#9c88ff")
        self.ul_value.pack(pady=5)
        self.ul_unit = ctk.CTkLabel(self.ul_card, text="Mbps", font=ctk.CTkFont(size=14), text_color="gray")
        self.ul_unit.pack(pady=(0, 20))

        # Server Info & Progress Bar
        self.bottom_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.bottom_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(30, 0))

        self.server_label = ctk.CTkLabel(self.bottom_frame, text="Serveur : En attente...", font=ctk.CTkFont(size=16))
        self.server_label.pack(anchor="w", pady=(0, 10))

        self.progress_bar = ctk.CTkProgressBar(self.bottom_frame, mode="indeterminate", height=10, corner_radius=5)
        self.progress_bar.pack(fill="x", pady=10)
        self.progress_bar.set(0)

    def start_test_thread(self):
        self.start_button.configure(state="disabled")
        self.status_label.configure(text="Test en cours...", text_color="#fbc531")

        self.ping_value.configure(text="--")
        self.dl_value.configure(text="--")
        self.ul_value.configure(text="--")
        self.server_label.configure(text="Serveur : Recherche en cours...")

        self.progress_bar.start()

        # Run in a separate thread
        threading.Thread(target=self.run_test, daemon=True).start()

    def run_test(self):
        result = test_speed()
        self.after(0, self.update_gui_results, result)

    def update_gui_results(self, result):
        self.progress_bar.stop()
        self.progress_bar.set(1)

        if result["success"]:
            self.ping_value.configure(text=f"{result['ping_ms']}")
            self.dl_value.configure(text=f"{result['download_mbps']}")
            self.ul_value.configure(text=f"{result['upload_mbps']}")
            self.server_label.configure(text=f"Serveur : {result['server_sponsor']} ({result['server_name']})")

            self.status_label.configure(text="Terminé", text_color="#4cd137")
            save_to_history(result)
        else:
            self.status_label.configure(text="Erreur", text_color="#e84118")
            self.server_label.configure(text=f"Erreur : {result['error']}")

        self.start_button.configure(state="normal", text="RECOMMENCER")

if __name__ == "__main__":
    app = App()
    app.mainloop()