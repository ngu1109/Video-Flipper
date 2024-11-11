import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
from moviepy.editor import VideoFileClip
import os

class VideoRotatorApp:
    def __init__(self, root):
        self.root = root
        self.rotation_angle = 0
        self.frame_image = None
        self.photo = None
        self.file_path = None
        self.select_file()

    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")])
        if self.file_path:
            self.extract_middle_frame()
            self.show_preview()
            self.root.focus_force()
            self.root.bind('<Left>', self.rotate_clockwise)
            self.root.bind('<Right>', self.rotate_anticlockwise)
            self.root.bind('<Return>', self.save_video)
        else:
            self.root.destroy()

    def extract_middle_frame(self):
        cap = cv2.VideoCapture(self.file_path)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count // 2)
        ret, frame = cap.read()
        cap.release()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.frame_image = Image.fromarray(frame)
        else:
            self.root.destroy()

    def show_preview(self):
        rotated_image = self.frame_image.rotate(-self.rotation_angle, expand=True)
        self.photo = ImageTk.PhotoImage(rotated_image)
        if hasattr(self, 'image_label'):
            self.image_label.configure(image=self.photo)
            self.image_label.image = self.photo
        else:
            self.image_label = tk.Label(self.root, image=self.photo)
            self.image_label.pack()

    def rotate_clockwise(self, event=None):
        self.rotation_angle = (self.rotation_angle - 90) % 360
        self.show_preview()

    def rotate_anticlockwise(self, event=None):
        self.rotation_angle = (self.rotation_angle + 90) % 360
        self.show_preview()

    def save_video(self, event=None):
        clip = VideoFileClip(self.file_path)
        rotated_clip = clip.rotate(-self.rotation_angle)
        dirname, basename = os.path.split(self.file_path)
        name, ext = os.path.splitext(basename)
        save_name = f"{name}_flipped{ext}"
        save_path = os.path.join(dirname, save_name)
        rotated_clip.write_videofile(save_path, codec="libx264")
        self.root.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Video Rotator")
    app = VideoRotatorApp(root)
    root.mainloop()
