import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2

# from detector import detect_eggs  # Uncomment when you implement the detect_eggs function

class EggDetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Nhận diện trứng với YOLO")
        self.scale_factor = 1.0
        self.mode = tk.StringVar(value="image")

        self.cv_img = None
        self.detected_img = None
        self.tk_img = None
        self.image_on_canvas = None

        self.root.bind("<Configure>", self.on_resize)

        # ===== Màn hình khởi động =====
        self.start_screen = tk.Canvas(self.root)
        self.start_screen.pack(fill=tk.BOTH, expand=True)

        try:
            self.start_bg_img = Image.open("start_background.jpg")
            self.start_bg = ImageTk.PhotoImage(self.start_bg_img)
            self.start_screen_bg = self.start_screen.create_image(0, 0, anchor=tk.NW, image=self.start_bg)

            start_button = tk.Button(self.start_screen, text="Bắt đầu", command=self.show_mode_screen, 
                                     font=("Arial", 16), bg="white")
            self.start_button_window = self.start_screen.create_window(400, 500, window=start_button)
        except FileNotFoundError:
            self.start_screen.create_text(400, 300, text="Không tìm thấy ảnh nền", font=("Arial", 16))

        # Initialize other screens
        self.mode_screen = None
        self.canvas = None

        self.root.after(100, lambda: self.on_resize())

    def show_mode_screen(self):
        self.start_screen.pack_forget()

        self.mode_screen = tk.Canvas(self.root)
        self.mode_screen.pack(fill=tk.BOTH, expand=True)

        try:
            self.mode_bg_img = Image.open("mode_background.jpg")
            self.mode_bg = ImageTk.PhotoImage(self.mode_bg_img)
            self.mode_screen_bg = self.mode_screen.create_image(0, 0, anchor=tk.NW, image=self.mode_bg)
        except FileNotFoundError:
            self.mode_screen.create_text(400, 300, text="Không tìm thấy ảnh nền", font=("Arial", 16))

        self.btn_camera = tk.Button(self.mode_screen, text="CAMERA", command=self.start_camera_mode,
                                    font=("Arial", 16), relief="raised", width=20, bg="white")
        self.camera_btn_window = self.mode_screen.create_window(400, 300, window=self.btn_camera)

        self.btn_upload = tk.Button(self.mode_screen, text="UPLOAD FILE", command=self.upload_file_mode,
                                    font=("Arial", 16), relief="raised", width=20, bg="white")
        self.upload_btn_window = self.mode_screen.create_window(400, 350, window=self.btn_upload)

        self.root.after(100, lambda: self.on_resize())

    def start_camera_mode(self):
        print("Camera mode selected")
        # Add logic here for camera mode

    def upload_file_mode(self):
        print("Upload file mode selected")
        self.mode_screen.pack_forget()
        self.setup_image_display()
        self.open_image()

    def setup_image_display(self):
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        back_btn = tk.Button(self.root, text="Quay lại", command=self.back_to_mode_screen)
        back_btn.pack(side=tk.BOTTOM, pady=10)

    def back_to_mode_screen(self):
        if self.canvas:
            self.canvas.pack_forget()
        self.show_mode_screen()

    def open_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if not path:
            self.back_to_mode_screen()
            return

        self.cv_img = cv2.imread(path)
        if self.cv_img is None:
            print("Không thể đọc ảnh")
            self.back_to_mode_screen()
            return

        self.detected_img = self.cv_img.copy()
        self.scale_factor = 1.0
        self.display_image(self.cv_img)
        self.mode.set("image")

    def display_image(self, img):
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb_img)
        size = (int(pil_img.width * self.scale_factor), int(pil_img.height * self.scale_factor))
        pil_img = pil_img.resize(size, Image.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(pil_img)

        self.canvas.delete("all")
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_img)
        self.canvas.config(width=pil_img.width, height=pil_img.height)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def on_resize(self, event=None):
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        if hasattr(self, 'start_bg_img') and self.start_screen.winfo_ismapped():
            resized_start = self.start_bg_img.resize((width, height), Image.LANCZOS)
            self.start_bg = ImageTk.PhotoImage(resized_start)
            self.start_screen.itemconfig(self.start_screen_bg, image=self.start_bg)
            self.start_screen.coords(self.start_button_window, width // 2, height - 100)

        if hasattr(self, 'mode_bg_img') and self.mode_screen and self.mode_screen.winfo_ismapped():
            resized_mode = self.mode_bg_img.resize((width, height), Image.LANCZOS)
            self.mode_bg = ImageTk.PhotoImage(resized_mode)
            self.mode_screen.itemconfig(self.mode_screen_bg, image=self.mode_bg)
            self.mode_screen.coords(self.camera_btn_window, width // 2, height // 2 - 30)
            self.mode_screen.coords(self.upload_btn_window, width // 2, height // 2 + 30)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = EggDetectorApp(root)
    root.mainloop()
