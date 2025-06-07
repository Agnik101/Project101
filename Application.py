from PIL import Image, ImageTk
import tkinter as tk
import cv2
import os
import numpy as np
from keras.models import model_from_json
import operator
from string import ascii_uppercase

class Application:
    def __init__(self):
        self.directory = r'D:\python\NewPRJ\model'
        self.vs = cv2.VideoCapture(0)
        self.current_image = None
        self.current_image2 = None
        
        # Load only the primary bw model
        self.loaded_model = self.load_model("model-bw.json", "model-bw.weights.h5")

        self.ct = {}
        self.ct['blank'] = 0
        self.blank_flag = 0

        for i in ascii_uppercase:
            self.ct[i] = 0
        
        # For timing persistence tracking if needed elsewhere
        self.symbol_start_time = {}
        for i in ascii_uppercase:
            self.symbol_start_time[i] = None

        self.symbol_start_time['blank'] = None

        print("Loaded model from disk")
        self.root = tk.Tk()
        self.root.title("Sign Language to Text Converter")
        self.root.protocol('WM_DELETE_WINDOW', self.destructor)
        self.root.geometry("900x1150")
        self.root.configure(bg="#ffffff")  # Light background from guidelines

        # Bind Enter key to capture current word
        self.root.bind('<Return>', self.on_enter_key)
        # Bind 'z' key to capture current symbol
        self.root.bind('z', self.on_z_key)
        
        # Typography styles following guidelines
        header_font = ("Courier", 40, "bold")
        label_font = ("Courier", 40, "bold")
        char_font = ("Courier", 50, "bold")

        self.panel = tk.Label(self.root, bg="#ffffff")
        self.panel.place(x=135, y=10, width=640, height=640)
        
        self.panel2 = tk.Label(self.root, bg="#ffffff")
        self.panel2.place(x=460, y=95, width=310, height=310)
        
        self.T = tk.Label(self.root, bg="#ffffff", fg="#111111", text="Sign Language to Text", font=("Inter", 48, "bold"))
        self.T.place(x=31, y=17)
        
        self.panel3 = tk.Label(self.root, bg="#ffffff", fg="#111111")  # Current Symbol
        self.panel3.place(x=500, y=640)
        
        self.T1 = tk.Label(self.root, bg="#ffffff", fg="#6b7280", text="Character :", font=label_font)
        self.T1.place(x=10, y=640)
        
        self.panel4 = tk.Label(self.root, bg="#ffffff", fg="#111111")  # Word output
        self.panel4.place(x=220, y=700)
        
        self.T2 = tk.Label(self.root, bg="#ffffff", fg="#6b7280", text="Word :", font=label_font)
        self.T2.place(x=10, y=700)
        
        self.panel5 = tk.Label(self.root, bg="#ffffff", fg="#111111")  # Sentence output
        self.panel5.place(x=350, y=760)
        
        self.T3 = tk.Label(self.root, bg="#ffffff", fg="#6b7280", text="Sentence :", font=label_font)
        self.T3.place(x=10, y=760)

        self.T4 = tk.Label(self.root, bg="#ffffff", fg="red", text="Suggestions", font=label_font)
        self.T4.place(x=250, y=820)

        # Suggestion buttons placeholders with enhanced visibility and size
        self.bt1 = tk.Button(self.root, command=self.action1, height=2, width=10)
        self.bt1.place(x=26, y=890)

        self.bt2 = tk.Button(self.root, command=self.action2, height=2, width=10)
        self.bt2.place(x=325, y=890)

        self.bt3 = tk.Button(self.root, command=self.action3, height=2, width=10)
        self.bt3.place(x=625, y=890)

        self.bt4 = tk.Button(self.root, command=self.action4, height=2, width=10)
        self.bt4.place(x=125, y=950)

        self.bt5 = tk.Button(self.root, command=self.action5, height=2, width=10)
        self.bt5.place(x=425, y=950)

        # Button to capture current word
        self.bt_capture_word = tk.Button(self.root, text="Capture Word", command=self.action_capture_word, height=2, width=15, bg="#111111", fg="#ffffff", font=("Inter", 16, "bold"))
        self.bt_capture_word.place(x=325, y=1010)

        # Button to delete last character from the word, styled and visible
        self.bt_delete_char = tk.Button(self.root, text="X", command=self.delete_last_char, height=2, width=5, bg="#ff4444", fg="#ffffff", font=("Inter", 18, "bold"))
        self.bt_delete_char.place(x=500, y=700)

        self.str = ""
        self.word = ""
        self.current_symbol = "Empty"
        self.photo = "Empty"

        self.video_loop()

    def load_model(self, json_file, weights_file):
        with open(os.path.join(self.directory, json_file), "r") as f:
            model_json = f.read()
        model = model_from_json(model_json)
        model.load_weights(os.path.join(self.directory, weights_file))
        return model

    def video_loop(self):
        ok, frame = self.vs.read()
        if ok:
            cv2image = cv2.flip(frame, 1)
            x1 = int(0.5 * frame.shape[1])
            y1 = 10
            x2 = frame.shape[1] - 10
            y2 = int(0.5 * frame.shape[1])

            # Create a blurred version of the frame
            blurred_frame = cv2.GaussianBlur(cv2image, (35, 35), 0)

            # Replace the ROI area in blurred frame with the non-blurred ROI (sharp)
            blurred_frame[y1:y2, x1:x2] = cv2image[y1:y2, x1:x2]

            # Use this composed frame for display and processing
            display_frame = blurred_frame

            # Draw rectangle around ROI
            cv2.rectangle(display_frame, (x1 - 1, y1 - 1), (x2 + 1, y2 + 1), (255, 0, 0), 2)

            # Convert to RGBA for tkinter display
            cv2image_rgba = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGBA)
            self.current_image = Image.fromarray(cv2image_rgba)
            imgtk = ImageTk.PhotoImage(image=self.current_image)
            self.panel.imgtk = imgtk
            self.panel.config(image=imgtk)

            # Extract ROI and preprocess for prediction
            roi = cv2image_rgba[y1:y2, x1:x2]
            roi_gray = cv2.cvtColor(roi, cv2.COLOR_RGBA2GRAY)
            blur = cv2.GaussianBlur(roi_gray, (5, 5), 2)
            th3 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY_INV, 11, 2)
            _, res = cv2.threshold(th3, 70, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

            self.predict(res)

            self.current_image2 = Image.fromarray(res)
            imgtk2 = ImageTk.PhotoImage(image=self.current_image2)

            self.panel2.imgtk = imgtk2
            self.panel2.config(image=imgtk2)

            self.panel3.config(text=self.current_symbol, font=("Courier", 50), fg="#111111", bg="#ffffff")
            self.panel4.config(text=self.word, font=("Courier", 40), fg="#111111", bg="#ffffff")
            self.panel5.config(text=self.str, font=("Courier", 40), fg="#111111", bg="#ffffff")

        self.root.after(30, self.video_loop)

    def predict(self, test_image):
        test_image = cv2.resize(test_image, (128, 128), interpolation=cv2.INTER_AREA)

        result = self.loaded_model.predict(test_image.reshape(1, 128, 128, 1))

        prediction = {}
        prediction['blank'] = result[0][0]
        inde = 1
        for i in ascii_uppercase:
            prediction[i] = result[0][inde]
            inde += 1
        prediction = sorted(prediction.items(), key=operator.itemgetter(1), reverse=True)
        self.current_symbol = prediction[0][0]

        if self.current_symbol == 'blank':
            for i in ascii_uppercase:
                self.ct[i] = 0
        self.ct[self.current_symbol] += 1

        if self.ct[self.current_symbol] > 60:
            for i in ascii_uppercase:
                if i == self.current_symbol:
                    continue
                tmp = abs(self.ct[self.current_symbol] - self.ct[i])
                if tmp <= 20:
                    self.ct['blank'] = 0
                    for i in ascii_uppercase:
                        self.ct[i] = 0
                    return
            self.ct['blank'] = 0
            for i in ascii_uppercase:
                self.ct[i] = 0
            if self.current_symbol == 'blank':
                if self.blank_flag == 0:
                    self.blank_flag = 1
                    if len(self.str) > 0:
                        self.str += " "
                    self.str += self.word
                    self.word = ""
            else:
                if len(self.str) > 16:
                    self.str = ""
                self.blank_flag = 0
                self.word += self.current_symbol

    def action_capture_word(self):
        # Capture current word into sentence
        if self.word.strip():
            if len(self.str) > 0 and not self.str.endswith(" "):
                self.str += " "
            self.str += self.word.strip()
            self.word = ""
            self.panel4.config(text=self.word, font=("Courier", 40))
            self.panel5.config(text=self.str, font=("Courier", 40))

    def delete_last_char(self):
        # Delete the last character from the current word
        if self.word:
            self.word = self.word[:-1]
            self.panel4.config(text=self.word, font=("Courier", 40))

    def on_enter_key(self, event):
        # Handler for Enter key
        self.action_capture_word()

    def on_z_key(self, event):
        # Handler for 'z' key to capture current predicted character
        if self.current_symbol and self.current_symbol != 'blank' and self.current_symbol != "Empty":
            self.word += self.current_symbol
            self.panel4.config(text=self.word, font=("Courier", 40))

    def action1(self):
        pass
    def action2(self):
        pass
    def action3(self):
        pass
    def action4(self):
        pass
    def action5(self):
        pass

    def destructor(self):
        print("Closing Application...")
        self.root.destroy()
        self.vs.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    print("Starting Application...")
    app = Application()
    # Bind Enter key to capture word
    app.root.bind('<Return>', app.on_enter_key)
    # Bind 'z' key to capture predicted character
    app.root.bind('z', app.on_z_key)
    app.root.mainloop()

