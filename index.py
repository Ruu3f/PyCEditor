import tkinter as tk
from tkinter import messagebox


class CodeEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Editor")
        self.linenumbers = tk.Text(
            self.root,
            width=3,
            padx=5,
            takefocus=0,
            border=0,
            background="#2f3136",
            foreground="white",
            font=("Bahnschrift", 12),
            state="disabled",
        )
        self.linenumbers.pack(side=tk.LEFT, fill=tk.Y)
        self.text_widget = tk.Text(
            self.root,
            font=("Bahnschrift", 12),
            bg="#2f3136",
            fg="white",
            insertbackground="white",
        )
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.text_widget["yscrollcommand"], self.linenumbers["yscrollcommand"] = (
            self.scroll_y,
            self.scroll_y,
        )
        self.text_widget.bind("<Configure>", self.update_linenumbers)
        self.text_widget.bind("<Key>", self.schedule_update_linenumbers)
        self.text_widget.bind("<MouseWheel>", self.scroll)
        self.linenumbers.bind("<MouseWheel>", self.scroll)
        self.update_linenumbers_id = None

    def scroll(self, event):
        current_position = self.text_widget.yview()[0]
        self.linenumbers.yview_scroll(int(-1 * (event.delta / 120)), "units")
        self.text_widget.yview_scroll(int(-1 * (event.delta / 120)), "units")
        if current_position == 1.0 and event.delta < 0:
            self.linenumbers.yview_scroll(1, "units")
            self.text_widget.yview_scroll(1, "units")

    def scroll_y(self, *args):
        current_position = self.text_widget.yview()[0]
        self.text_widget.yview("moveto", args[0])
        self.linenumbers.yview("moveto", args[0])
        if current_position == 1.0 and float(args[0]) < 1.0:
            self.linenumbers.yview_scroll(1, "units")
            self.text_widget.yview_scroll(1, "units")

    def update_linenumbers(self, *args):
        self.linenumbers.config(state="normal")
        self.linenumbers.delete("1.0", tk.END)
        lines = self.text_widget.index("end-1c").split(".")[0]
        if int(lines) > 999:
            messagebox.showerror(
                "Error",
                "Maximum number of lines exceeded. Why do you even need that much lines my guy?",
            )
            self.text_widget.delete("999.0", tk.END)
            lines = "999"
        self.linenumbers.insert(
            "1.0", "\n".join(str(i) for i in range(1, int(lines) + 1))
        )
        self.linenumbers.config(state="disabled")
        self.update_linenumbers_id = None

    def schedule_update_linenumbers(self, *args):
        if self.update_linenumbers_id is None:
            self.update_linenumbers_id = self.root.after_idle(self.update_linenumbers)


root = tk.Tk()
app = CodeEditor(root)
root.mainloop()
