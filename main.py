
from tkinter import Tk, Canvas, messagebox, IntVar, OptionMenu, Spinbox, Button, filedialog, StringVar, Label, Entry
from services import ImageService
from PIL import ImageTk
from pathlib import Path


# Create the main window
window = Tk()
window.title("Img_WM")

# Variables to choose from
font_size_var = IntVar(value=32)
position_var = StringVar(value="Bottom-Right")
wm_text_var = StringVar()


# Grid configuration
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)

# Design the main window
canvas = Canvas(window, width=500, height=500, highlightthickness=0, bg="#00b3b3")
canvas.grid(column=0, row=0, columnspan=3, padx=1, pady=1)

# Переменная состояния fullscreen
is_fullscreen = False

def toggle_fullscreen(event=None):
    global is_fullscreen
    is_fullscreen = not is_fullscreen
    window.attributes("-fullscreen", is_fullscreen)

def exit_fullscreen(event=None):
    global is_fullscreen
    is_fullscreen = False
    window.attributes("-fullscreen", False)

# Привязываем F11 для переключения
window.bind("<F11>", toggle_fullscreen)
# Привязываем Esc для выхода из fullscreen
window.bind("<Escape>", exit_fullscreen)

def create_gradient(canvas, width, height):
    """Background gradient"""
    for i in range(height):
        color = f'#{int(255 - 255 * (i / height)):02x}00{int(255 * (i / height)):02x}'
        canvas.create_line(0, i, width, i, fill=color)

def set_background_color(window):
    window.configure(bg="#00b3b3")  # Teal background color
def add_welcome_text(canvas, width, height):
    """Welcome text on background"""
    canvas.create_text(width // 2, height // 2, text="Welcome!", font=("Arial", 24, "bold"), fill="white")

create_gradient(canvas, 500, 500)   # Apply gradient
add_welcome_text(canvas, 500, 500)  # Add welcome text


# Initialize the service
service = ImageService()
displayed_img = None  # For Tkinter display

# --- UI Functions ---
# Load an image
def input_img():
    global displayed_img

    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
    )

    if not file_path:
        return

    pil_img = service.load_img(file_path)
    img_width, img_height = pil_img.size

    # Display in Tkinter
    displayed_img = ImageTk.PhotoImage(pil_img)

    canvas.config(width=img_width, height=img_height)
    canvas.delete("all")
    canvas.create_image(0, 0, image=displayed_img, anchor='nw')
    window.update_idletasks()  # Refresh layout
    window.geometry("")        # Reset to "natural" window size

# Save the image (stub)
def output_img():
    try:
        wm_text = wm_text_var.get()
        if not wm_text:
            text_path = Path("assets/default_watermark.txt")
            with open(text_path, "r", encoding="utf-8") as file_text:
                wm_text = file_text.read().strip()

        output_path = service.save_img_with_wm(
            wm_text,
            font_size=font_size_var.get(),
            position=position_var.get()
        )
        answer = messagebox.showinfo("Done!", f"Saved to:\n{output_path}")
        if answer:
            service.open_output_folder()
    except Exception as e:
        messagebox.showerror("Error!", str(e))

# --- Buttons ---
button_input = Button(window, text="Input img", command=input_img)
button_input.grid(column=0, row=1, padx=10, pady=10, sticky="ew")

button_output = Button(window, text="Output img", command=output_img)
button_output.grid(column=1, row=1, padx=10, pady=10, sticky="ew")


# Font size
spin_size = Spinbox(window, from_=8, to=100, textvariable=font_size_var, width=5)
spin_size.grid(column=0, row=2, padx=5, pady=5, sticky="ew")

# Watermark position
positions = ["Top-Left", "Top-Right", "Center", "Bottom-Left", "Bottom-Right"]
pos_menu = OptionMenu(window, position_var, *positions)
pos_menu.grid(column=2, row=1, padx=5, pady=5)
# pos_menu.config(width=12)

entry_label = Label(window, text="Enter watermark text:")
entry_label.grid(column=1, row=2, padx=5, pady=5, sticky="ew")
wm_text_entry = Entry(window, textvariable=wm_text_var)
wm_text_entry.grid(column=2, row=2, columnspan=2, padx=10, pady=10, sticky="ew")


# --- Launch ---
window.mainloop()
