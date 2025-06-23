import tkinter as tk
import os
from pygame import mixer
from tkinter import filedialog

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.t = 0  # current song index
        self.k = 1  # 1 = default folder, 2 = user folder
        self.label = []
        self.folder_path = 'MUSIC'
        self.music = [f for f in os.listdir(self.folder_path) if f.endswith(".mp3")]

        mixer.init()

        self.root.geometry("700x550")
        self.root.title("\U0001F3B5 Music Player")
        self.root.config(bg="#1e1e1e")

        self.BTN_STYLE = {"font": ("Segoe UI", 11), "bg": "#2c3e50", "fg": "white", "activebackground": "#34495e", "bd": 0, "padx": 10, "pady": 5}
        self.LBL_STYLE = {"font": ("Segoe UI", 11), "bg": "#1e1e1e", "fg": "white", "anchor": "w", "padx": 10}

        self.setup_ui()

        if self.music:
            self.play_song(self.t)

    def setup_ui(self):
        self.frame1 = tk.Frame(self.root, bg="#1e1e1e")
        self.frame1.pack(side='top', fill='x', pady=10)

        self.frame2 = tk.Frame(self.root, bg="#1e1e1e")
        self.frame2.pack(fill='both', expand=True, padx=10)

        self.frame3 = tk.Frame(self.root, bg="#1e1e1e")
        self.frame3.pack(side='bottom', fill='x', pady=10)

        self.frame4 = tk.Frame(self.root, bg="#1e1e1e")
        self.frame4.pack(side='bottom', fill='x', padx=10, pady=5)

        tk.Label(self.frame1, text='\U0001F3B6 Music Player', font=("Segoe UI", 16, "bold"), bg="#1e1e1e", fg="white").pack(side="left", padx=10)
        self.music_playing = tk.Label(self.frame1, text='Nothing Playing', font=("Segoe UI", 12), bg="#1e1e1e", fg="lightgray")
        self.music_playing.pack(side="left", padx=20)
        tk.Button(self.frame1, text="Choose Folder", command=self.choose_folder, **self.BTN_STYLE).pack(side="right", padx=10)

        self.list_music = tk.Frame(self.frame2, bg="#1e1e1e")
        self.list_music.pack(fill='both', expand=True)

        for i, song in enumerate(self.music):
            lbl = tk.Label(self.list_music, text=f"\u266B {song}", **self.LBL_STYLE)
            lbl.pack(fill='x', pady=1)
            self.label.append(lbl)

        buttons = [
            ("Prev", self.prev),
            ("Play", lambda: self.play_song(self.t)),
            ("Pause", self.pause),
            ("Next", self.next),
            ("Vol +", self.add_v),
            ("Vol -", self.del_v)
        ]

        for text, cmd in buttons:
            tk.Button(self.frame3, text=text, command=cmd, **self.BTN_STYLE).pack(side="left", padx=5)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = tk.Scale(self.frame4, variable=self.progress_var, from_=0, to=100, orient='horizontal', showvalue=False, troughcolor='#34495e', bg="#1e1e1e", fg="white", highlightthickness=0)
        self.progress_bar.pack(fill='x')

    def choose_folder(self):
        self.k = 2
        self.folder_path = filedialog.askdirectory(title="Choose a folder")
        if not self.folder_path:
            return
        self.music = [f for f in os.listdir(self.folder_path) if f.endswith(".mp3")]
        self.t = 0
        for lbl in self.label:
            lbl.destroy()
        self.label.clear()
        for i, song in enumerate(self.music):
            lbl = tk.Label(self.list_music, text=f"\u266B {song}", **self.LBL_STYLE)
            lbl.pack(fill='x', pady=1)
            self.label.append(lbl)
        if self.music:
            self.play_song(self.t)

    def next(self):
        if self.t < len(self.music) - 1:
            self.t += 1
            self.play_song(self.t)

    def prev(self):
        if self.t > 0:
            self.t -= 1
            self.play_song(self.t)

    def pause(self):
        mixer.music.pause()
        self.highlight_current()

    def add_v(self):
        volume = mixer.music.get_volume()
        mixer.music.set_volume(min(volume + 0.1, 1.0))

    def del_v(self):
        volume = mixer.music.get_volume()
        mixer.music.set_volume(max(volume - 0.1, 0.0))

    def play_song(self, i):
        path = os.path.join(self.folder_path if self.k == 2 else "MUSIC", self.music[i])
        mixer.music.load(path)
        mixer.music.set_volume(0.5)
        mixer.music.play()
        self.highlight_current()
        self.update_progress()

    def highlight_current(self):
        self.music_playing.config(text=f"Now Playing: {self.music[self.t]}")
        for i, lbl in enumerate(self.label):
            lbl.config(bg="#1e1e1e")
        self.label[self.t].config(bg="#3498db")

    def update_progress(self):
        if mixer.music.get_busy():
            try:
                current_pos = mixer.music.get_pos() / 1000  # in seconds
                self.progress_var.set(current_pos)
                self.root.after(1000, self.update_progress)
            except:
                pass

if __name__ == '__main__':
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()
