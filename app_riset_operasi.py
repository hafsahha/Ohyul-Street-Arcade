import os
import sys
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from PIL import Image, ImageTk
from scipy.optimize import linprog

ctk.set_appearance_mode("Light")

class OhyulStreetArcadeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("► COFFEE_OPTIMIZER // STREET_ARCADE_EDITION ◄")
        self.geometry("1150x700")
        self.resizable(False, False)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # State kontrol alur dan mekanik teks
        self.current_step = 0
        self.is_typing = False
        self.skip_typing = False  # Flag untuk memotong/skip animasi mengetik
        
        # --- RETRO BOYISH BRANDING THEME ---
        self.FONT_MONO = "Consolas"
        self.COLOR_STREET_CREAM = "#F5F2EB"  
        self.COLOR_WHITE = "#FFFFFF"
        self.COLOR_INK_BLACK = "#111111"    
        self.COLOR_VANDAL_RED = "#D32F2F"   
        
        # --- MASTER LAYOUT CONFIGURATION ---
        self.grid_columnconfigure(0, weight=1) 
        self.grid_columnconfigure(1, weight=0, minsize=520) # Diperlebar sedikit agar console lega            
        self.grid_rowconfigure(0, weight=1)

        # ==================== SISI KIRI: MATRIX MONITOR (GRAFIK) ====================
        self.left_graph_panel = ctk.CTkFrame(
            self, fg_color=self.COLOR_WHITE, border_width=4, border_color=self.COLOR_INK_BLACK, corner_radius=0
        )
        self.left_graph_panel.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.monitor_header = ctk.CTkLabel(
            self.left_graph_panel,
            text="▼ ANALOG MATRIX REALTIME MONITOR // PLAYER_01",
            font=ctk.CTkFont(family=self.FONT_MONO, size=12, weight="bold"),
            text_color=self.COLOR_INK_BLACK, anchor="w"
        )
        self.monitor_header.pack(fill="x", padx=15, pady=(10, 0))

        self.fig, self.ax = plt.subplots(figsize=(6, 5))
        self.canvas_graph = FigureCanvasTkAgg(self.fig, master=self.left_graph_panel)
        self.canvas_graph.get_tk_widget().pack(expand=True, fill="both", padx=15, pady=15)
        self.reset_grafik()

        # ==================== SISI KANAN: CONTROL & DIALOG ZONE ====================
        self.right_control_panel = ctk.CTkFrame(self, fg_color=self.COLOR_STREET_CREAM, corner_radius=0)
        self.right_control_panel.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="nsew")
        
        self.right_control_panel.grid_rowconfigure(0, weight=0, minsize=230) # Ditambah tinggi minimalnya
        self.right_control_panel.grid_rowconfigure(1, weight=1)              
        self.right_control_panel.grid_columnconfigure(0, weight=1)

        # --- PANEL ATAS KANAN: INPUT DASHBOARD (LEBIH LONGGAR & RAPI) ---
        self.input_frame = ctk.CTkFrame(
            self.right_control_panel, fg_color=self.COLOR_WHITE, border_width=3, border_color=self.COLOR_INK_BLACK, corner_radius=0
        )
        self.input_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="nsew")
        self.setup_input_fields()

        # --- PANEL BAWAH KANAN: DIALOGUE CUTSCENE ROOM ---
        self.dialogue_room_frame = ctk.CTkFrame(self.right_control_panel, fg_color="transparent", corner_radius=0)
        self.dialogue_room_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")

        # Box Bubble Chat (Tempat Utama Teks + Ohyul Menyatu)
        self.bubble_chat_box = ctk.CTkFrame(
            self.dialogue_room_frame, fg_color=self.COLOR_WHITE, border_width=3, border_color=self.COLOR_INK_BLACK, corner_radius=0
        )
        self.bubble_chat_box.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=0.78) # Dipertinggi agar teks tidak buntung
        self.bubble_chat_box.pack_propagate(False)

        self.bubble_tag = ctk.CTkLabel(
            self.bubble_chat_box, text="[ OHYUL_CORE.LOG ]---------------------------",
            font=ctk.CTkFont(family=self.FONT_MONO, size=11, weight="bold"), text_color=self.COLOR_INK_BLACK, anchor="w"
        )
        self.bubble_tag.pack(fill="x", padx=15, pady=(8, 0))

        # Teks Utama (wraplength dikunci di 230 agar tidak menabrak Ohyul di kanan)
        self.lbl_mocha_talk = ctk.CTkLabel(
            self.bubble_chat_box, 
            text="Sistem Siap hulu. Masukkan variabel kontrol di atas, lalu tekan [RUN] untuk memulai kalkulasi linear programming. 🕹️",
            font=ctk.CTkFont(family=self.FONT_MONO, size=12, weight="bold"),
            text_color=self.COLOR_INK_BLACK, wraplength=230, justify="left", anchor="nw"
        )
        self.lbl_mocha_talk.pack(padx=15, pady=10, fill="both", expand=True, side="left")

        # FOTO OHYUL MASUK KE DALAM BOX DIALOG (Pojok Kanan Bawah Box, Ukuran Diperbesar)
        self.avatar_label = tk.Label(self.bubble_chat_box, bg=self.COLOR_WHITE)
        self.avatar_label.place(relx=1.0, rely=1.0, anchor="se", x=-5, y=-5) 

        # Tombol Next Step (Selalu Aktif untuk Fitur Skip)
        self.btn_next_step = ctk.CTkButton(
            self.dialogue_room_frame, text="► NEXT_INTERATION_PHASE()", 
            command=self.next_step,
            font=ctk.CTkFont(family=self.FONT_MONO, size=12, weight="bold"),
            fg_color=self.COLOR_VANDAL_RED, text_color=self.COLOR_WHITE, hover_color="#991B1B", corner_radius=0
        )
        self.btn_next_step.place(relx=0.0, rely=0.82, relwidth=1.0, relheight=0.14)

        # Muat Aset Gambar
        self.loaded_images = {}
        self.load_avatar_assets()

        if "ohyul1" in self.loaded_images:
            self.avatar_label.configure(image=self.loaded_images["ohyul1"])

    # ==================== LOGIKA MANAGEMENT FOTO AVATAR ====================
    def load_avatar_assets(self):
        # Loop sampai gambar 9 (Ohyul9 angkat alis)
        for i in range(1, 10):
            filename = f"ohyul{i}.png"
            if os.path.exists(filename):
                try:
                    img = Image.open(filename)
                    # Diperbesar ukurannya dari 200 ke 225 agar terlihat jelas di dalam box
                    base_width = 225
                    w_percent = (base_width / float(img.size[0]))
                    h_size = int((float(img.size[1]) * float(w_percent)))
                    img = img.resize((base_width, h_size), Image.Resampling.LANCZOS)
                    self.loaded_images[f"ohyul{i}"] = ImageTk.PhotoImage(img)
                except Exception as e:
                    print(f"Gagal memproses gambar {filename}: {e}")

    def efek_mengetIK(self, teks, index=0, play_mode="pov1"):
        if not self.winfo_exists(): return
        
        # JIKA USER MENEKAN SKIP (NEXT STEP): Hentikan animasi, muntahkan semua teks
        if self.skip_typing:
            self.lbl_mocha_talk.configure(text=teks)
            self.is_typing = False
            self.skip_typing = False
            self.set_pose_selesai(play_mode)
            return

        if index < len(teks):
            self.is_typing = True
            self.lbl_mocha_talk.configure(text=teks[:index+1])
            
            animation_tick = index // 4
            if play_mode == "pov1":
                frame_key = f"ohyul{2 if animation_tick % 2 == 0 else 3}"
            elif play_mode == "pov2":
                mouth_loop = ["ohyul4", "ohyul5", "ohyul6", "ohyul7"]
                frame_key = mouth_loop[animation_tick % 4]
            else:
                frame_key = "ohyul8"

            if frame_key in self.loaded_images:
                self.avatar_label.configure(image=self.loaded_images[frame_key])
            
            self.after(45, lambda: self.efek_mengetIK(teks, index+1, play_mode))
        else:
            self.is_typing = False
            self.set_pose_selesai(play_mode)

    def set_pose_selesai(self, play_mode):
        """ Mengunci pose diam ketika teks kelar diketik """
        if play_mode == "pov1" and "ohyul1" in self.loaded_images:
            self.avatar_label.configure(image=self.loaded_images["ohyul1"])
        elif play_mode == "pov2" and "ohyul5" in self.loaded_images:
            self.avatar_label.configure(image=self.loaded_images["ohyul5"])
        elif play_mode == "happy":
            # Mulai looping bolak-balik ohyul 8 dan 9
            self.loop_animasi_finish(toggle=True)

    def loop_animasi_finish(self, toggle=True):
        """ Loop animasi dinamis bolak balik angkat alis (8 <-> 9) """
        # Berhenti jika user me-restart perhitungan atau menekan langkah lain
        if not self.winfo_exists() or self.current_step != 5 or self.is_typing:
            return
        
        frame_key = "ohyul8" if toggle else "ohyul9"
        if frame_key in self.loaded_images:
            self.avatar_label.configure(image=self.loaded_images[frame_key])
            
        # Kecepatan ganti alis setiap 400 milidetik
        self.after(400, lambda: self.loop_animasi_finish(not toggle))

    # ==================== RAPIH & LONGGAR: DASHBOARD CONTROL INPUT ====================
    def setup_input_fields(self):
        lbl = ctk.CTkLabel(
            self.input_frame, text="► CONSOLE_CORE_VARIABLES_OVERRIDE", 
            font=ctk.CTkFont(family=self.FONT_MONO, size=12, weight="bold"), text_color=self.COLOR_INK_BLACK
        )
        lbl.grid(row=0, column=0, columnspan=4, pady=(12, 10))

        # Kotak isian dinaikkan ke width=100 agar longgar dan proporsional
        box_style = {
            "width": 100, "corner_radius": 0, 
            "border_color": self.COLOR_INK_BLACK, "border_width": 2,
            "fg_color": self.COLOR_WHITE, "text_color": self.COLOR_INK_BLACK, 
            "font": (self.FONT_MONO, 12, "bold")
        }

        # Menggunakan grid ber-padding renggang (padx=8, pady=6) agar tidak berhimpitan kaku
        ctk.CTkLabel(self.input_frame, text="PROFIT_X1:", font=(self.FONT_MONO, 10, "bold"), text_color=self.COLOR_INK_BLACK).grid(row=1, column=0, padx=8, pady=6, sticky="e")
        self.ent_u_kopi = ctk.CTkEntry(self.input_frame, **box_style); self.ent_u_kopi.insert(0, "15000"); self.ent_u_kopi.grid(row=1, column=1, pady=6, sticky="w")

        ctk.CTkLabel(self.input_frame, text="PROFIT_X2:", font=(self.FONT_MONO, 10, "bold"), text_color=self.COLOR_INK_BLACK).grid(row=1, column=2, padx=8, pady=6, sticky="e")
        self.ent_u_matcha = ctk.CTkEntry(self.input_frame, **box_style); self.ent_u_matcha.insert(0, "20000"); self.ent_u_matcha.grid(row=1, column=3, pady=6, sticky="w")

        ctk.CTkLabel(self.input_frame, text="MAX_MILK:", font=(self.FONT_MONO, 10, "bold"), text_color=self.COLOR_INK_BLACK).grid(row=2, column=0, padx=8, pady=6, sticky="e")
        self.ent_max_susu = ctk.CTkEntry(self.input_frame, **box_style); self.ent_max_susu.insert(0, "10000"); self.ent_max_susu.grid(row=2, column=1, pady=6, sticky="w")

        ctk.CTkLabel(self.input_frame, text="MAX_TIME:", font=(self.FONT_MONO, 10, "bold"), text_color=self.COLOR_INK_BLACK).grid(row=2, column=2, padx=8, pady=6, sticky="e")
        self.ent_max_waktu = ctk.CTkEntry(self.input_frame, **box_style); self.ent_max_waktu.insert(0, "400"); self.ent_max_waktu.grid(row=2, column=3, pady=6, sticky="w")

        self.btn_start = ctk.CTkButton(
            self.input_frame, text="⚙️ [ RUN_GRAPHIC_COMPUTATION ]", 
            command=self.mulai_proses, fg_color=self.COLOR_INK_BLACK, text_color=self.COLOR_WHITE, 
            hover_color="#2A2A2A", corner_radius=0, font=(self.FONT_MONO, 12, "bold")
        )
        self.btn_start.grid(row=3, column=0, columnspan=4, pady=15, padx=15, sticky="ew")

    def reset_grafik(self):
        self.ax.clear()
        self.ax.set_title("OPTIMIZATION MATRIX GRAPH", fontsize=12, fontweight="bold", fontname=self.FONT_MONO, color=self.COLOR_INK_BLACK, pad=10)
        self.ax.set_xlabel("Kopi Susu (X1) -> Cup", fontname=self.FONT_MONO, fontsize=10, fontweight="bold")
        self.ax.set_ylabel("Matcha Latte (X2) -> Cup", fontname=self.FONT_MONO, fontsize=10, fontweight="bold")
        
        self.ax.grid(True, linestyle="-", alpha=0.9, color="#222222", linewidth=1.2)
        self.ax.set_facecolor(self.COLOR_STREET_CREAM)
        self.fig.patch.set_facecolor(self.COLOR_WHITE)
        self.canvas_graph.draw()

    # ==================== RETRO PROCESSING CORE ENGINE ====================
    def mulai_proses(self):
        try:
            self.u1 = float(self.ent_u_kopi.get())
            self.u2 = float(self.ent_u_matcha.get())
            self.s_max = float(self.ent_max_susu.get())
            self.w_max = float(self.ent_max_waktu.get())
            
            c = [-self.u1, -self.u2]
            A = [[100, 200], [5, 5]]
            b = [self.s_max, self.w_max]
            res = linprog(c, A_ub=A, b_ub=b, bounds=[(0, None), (0, None)], method='highs')
            
            if not res.success:
                messagebox.showerror("Error", "Komputasi gagal! Batasan ruang solusi ilegal.")
                return
                
            self.x1_opt, self.x2_opt = res.x
            self.max_p = -res.fun
            
            self.current_step = 1
            self.run_current_step()

        except ValueError:
            messagebox.showwarning("Input Error", "Gunakan input data angka bulat valid!")

    def next_step(self):
        # JIKA SEDANG MENGETIK: Set flag skip ke True (Biar langsung reveal full teks)
        if self.is_typing: 
            self.skip_typing = True
        else:
            # JIKA SUDAH SELESAI MENGETIK: Baru maju ke langkah berikutnya
            self.current_step += 1
            self.run_current_step()

    def run_current_step(self):
        limit_max = max(self.s_max/100, self.w_max/5) * 1.15
        x_vals = np.linspace(0, limit_max, 250)

        for spine in self.ax.spines.values():
            spine.set_linewidth(3)
            spine.set_color(self.COLOR_INK_BLACK)

        if self.current_step == 1:
            self.reset_grafik()
            msg = (
                ">> MODEL MATRIX...\n\n"
                f"• MAX Z = {int(self.u1)}X1 + {int(self.u2)}X2\n"
                f"• L1 (MILK): 100X1 + 200X2 <= {int(self.s_max)} ml\n"
                f"• L2 (TIME): 5X1 + 5X2 <= {int(self.w_max)} min\n\n"
                "[READY FOR PLOT]"
            )
            self.efek_mengetIK(msg, play_mode="pov1")

        elif self.current_step == 2:
            y_inter = self.s_max / 200
            x_inter = self.s_max / 100
            
            g_susu = (self.s_max - 100 * x_vals) / 200
            self.ax.plot(x_vals, g_susu, label='[L1] MILK BOUNDARY', color=self.COLOR_INK_BLACK, linewidth=4)
            self.ax.set_xlim(0, limit_max); self.ax.set_ylim(0, limit_max)
            self.ax.legend(prop={'family': self.FONT_MONO, 'size': 9, 'weight': 'bold'}, loc='upper right')
            self.canvas_graph.draw()

            msg = (
                ">> PLOTTING LINE 01 (MILK)\n\n"
                f"Equation: 100X1 + 200X2 = {int(self.s_max)}\n"
                f"• Sumbu X2 -> (0, {int(y_inter)})\n"
                f"• Sumbu X1 -> ({int(x_inter)}, 0)\n\n"
                "Sektor batas susu berhasil di-render."
            )
            self.efek_mengetIK(msg, play_mode="pov2")

        elif self.current_step == 3:
            y_inter2 = self.w_max / 5
            x_inter2 = self.w_max / 5
            
            g_waktu = (self.w_max - 5 * x_vals) / 5
            self.ax.plot(x_vals, g_waktu, label='[L2] TIME BOUNDARY', color=self.COLOR_VANDAL_RED, linewidth=4, linestyle='--')
            self.ax.legend(prop={'family': self.FONT_MONO, 'size': 9, 'weight': 'bold'}, loc='upper right')
            self.canvas_graph.draw()

            msg = (
                ">> PLOTTING LINE 02 (TIME)\n\n"
                f"Equation: 5X1 + 5X2 = {int(self.w_max)}\n"
                f"• Sumbu X2 -> (0, {int(y_inter2)})\n"
                f"• Sumbu X1 -> ({int(x_inter2)}, 0)\n\n"
                "Garis batas jam kerja barista berhasil ditumpuk."
            )
            self.efek_mengetIK(msg, play_mode="pov2")

        elif self.current_step == 4:
            g_susu = (self.s_max - 100 * x_vals) / 200
            g_waktu = (self.w_max - 5 * x_vals) / 5
            area_layak = np.minimum(g_susu, g_waktu)
            area_layak = np.maximum(area_layak, 0)
            
            self.ax.fill_between(
                x_vals, 0, area_layak, facecolor='none', edgecolor=self.COLOR_INK_BLACK, hatch='\\\\\\', linewidth=0, label='FEASIBLE_ZONE'
            )
            self.ax.legend(prop={'family': self.FONT_MONO, 'size': 9, 'weight': 'bold'}, loc='upper right')
            self.canvas_graph.draw()

            msg = (
                ">> FEASIBLE SPACE LAYER GENERATED...\n\n"
                "Zonasi kelayakan aman terdeteksi di koordinat dalam.\n"
                "Diarsir tebal menggunakan pattern retro hatching silang miring."
            )
            self.efek_mengetIK(msg, play_mode="pov2")

        elif self.current_step == 5:
            self.ax.scatter(self.x1_opt, self.x2_opt, color=self.COLOR_VANDAL_RED, s=200, marker='s', zorder=5, label='OPTIMUM_TARGET')
            self.ax.annotate(
                f' [TARGET FIXED]\n ({round(self.x1_opt)} X1, {round(self.x2_opt)} X2)', 
                xy=(self.x1_opt, self.x2_opt), xytext=(self.x1_opt + (limit_max*0.08), self.x2_opt + (limit_max*0.08)),
                fontname=self.FONT_MONO, weight="bold", color=self.COLOR_VANDAL_RED, fontsize=10,
                arrowprops=dict(facecolor=self.COLOR_INK_BLACK, shrink=0.05, width=2.5, headwidth=7)
            )
            self.ax.legend(prop={'family': self.FONT_MONO, 'size': 9, 'weight': 'bold'}, loc='upper right')
            self.canvas_graph.draw()

            msg = (
                ">> SYSTEM COMPLETION! ⭐\n\n"
                "Kombinasi output produksi paling eksploitatif & untung:\n"
                f"► KOPI SUSU (X1) = {round(self.x1_opt)} CUP\n"
                f"► MATCHA LATE (X2) = {round(self.x2_opt)} CUP\n\n"
                f"💸 EST. PROFIT = Rp {round(self.max_p):,}\n"
                "Mission successful! Selesai kak."
            )
            self.efek_mengetIK(msg, play_mode="happy") 

    def on_closing(self):
        self.destroy()
        sys.exit(0)

if __name__ == "__main__":
    try:
        app = OhyulStreetArcadeApp()
        app.mainloop()
    except KeyboardInterrupt:
        sys.exit(0)