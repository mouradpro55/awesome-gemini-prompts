import customtkinter as ctk
import threading
from core import test_speed, save_to_history

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window settings
        self.title("Test de Débit Internet - DTN El Menia")
        self.geometry("600x500")
        self.resizable(False, False)

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # Header
        self.title_label = ctk.CTkLabel(self, text="Test de Vitesse Internet", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=20)

        self.subtitle_label = ctk.CTkLabel(self, text="Direction des Transmissions Nationales (DTN) - Wilaya d'El Menia", font=ctk.CTkFont(size=14))
        self.subtitle_label.pack(pady=5)

        # Results Frame
        self.results_frame = ctk.CTkFrame(self)
        self.results_frame.pack(pady=30, padx=40, fill="both", expand=True)

        self.ping_label = ctk.CTkLabel(self.results_frame, text="Ping : -- ms", font=ctk.CTkFont(size=18))
        self.ping_label.pack(pady=10)

        self.download_label = ctk.CTkLabel(self.results_frame, text="Téléchargement : -- Mbps", font=ctk.CTkFont(size=18))
        self.download_label.pack(pady=10)

        self.upload_label = ctk.CTkLabel(self.results_frame, text="Envoi : -- Mbps", font=ctk.CTkFont(size=18))
        self.upload_label.pack(pady=10)

        self.server_label = ctk.CTkLabel(self.results_frame, text="Serveur : --", font=ctk.CTkFont(size=14))
        self.server_label.pack(pady=10)

        # Start Button
        self.start_button = ctk.CTkButton(self, text="Démarrer le Test", font=ctk.CTkFont(size=16, weight="bold"), command=self.start_test_thread)
        self.start_button.pack(pady=10)

        # Footer (Credits)
        self.footer_label = ctk.CTkLabel(self, text="Idée et Supervision : Mr. Mesbah Mourad", font=ctk.CTkFont(size=12))
        self.footer_label.pack(side="bottom", pady=10)

    def start_test_thread(self):
        self.start_button.configure(state="disabled", text="Test en cours...")
        self.ping_label.configure(text="Ping : -- ms")
        self.download_label.configure(text="Téléchargement : -- Mbps")
        self.upload_label.configure(text="Envoi : -- Mbps")
        self.server_label.configure(text="Serveur : --")

        # Run in a separate thread to not freeze the GUI
        threading.Thread(target=self.run_test).start()

    def run_test(self):
        result = test_speed()
        self.after(0, self.update_gui_results, result)

    def update_gui_results(self, result):
        if result["success"]:
            self.ping_label.configure(text=f"Ping : {result['ping_ms']} ms")
            self.download_label.configure(text=f"Téléchargement : {result['download_mbps']} Mbps")
            self.upload_label.configure(text=f"Envoi : {result['upload_mbps']} Mbps")
            self.server_label.configure(text=f"Serveur : {result['server_sponsor']} ({result['server_name']})")

            # Save to history
            save_to_history(result)
        else:
            self.ping_label.configure(text="Erreur de Connexion")
            self.download_label.configure(text=result["error"])

        self.start_button.configure(state="normal", text="Recommencer le Test")

if __name__ == "__main__":
    app = App()
    app.mainloop()