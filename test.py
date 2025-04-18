import customtkinter
import solvingLU
from PIL import Image, ImageTk

N = 0
image = Image.open("arrow.png")


def subscript(number):
    # Define the mapping from regular digits to subscript digits
    list = {
        "0": "₀",
        "1": "₁",
        "2": "₂",
        "3": "₃",
        "4": "₄",
        "5": "₅",
        "6": "₆",
        "7": "₇",
        "8": "₈",
        "9": "₉",
    }
    return list[str(number)]


# Tạo khung chứa tiêu đề
class titleFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.text_title = customtkinter.CTkLabel(
            self, text="Phân tích LU - BTL DSTT - Nhóm 12", font=("Arial", 36)
        )
        self.text_title.grid(row=0, column=0, padx=5, pady=5, sticky="")


# Tạo khung chứa kích thước ma trận
class sizeInputFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.N = 0
        self.grid_columnconfigure(0, weight=1)
        # Tạo và hiển thị nhãn nhập kích thước ma trận lên ứng dụng
        self.text_input = customtkinter.CTkLabel(
            self, text="Nhập kích thước ma trận:\n(1<=N<=10) ", font=("Arial", 20)
        )
        self.text_input.grid(row=0, column=0, padx=5, pady=5, sticky="")
        self.entry_field = customtkinter.CTkEntry(
            self, placeholder_text="N", font=("Arial", 24), width=50, height=50
        )
        self.entry_field.grid(row=0, column=1, padx=5, pady=5, sticky="")
        self.entry_field.bind("<Return>", self.delay_call)

        self.label = customtkinter.CTkLabel(self, text=", A = ", font=("Arial", 32))
        self.label.grid(row=0, column=2, padx=5, pady=5, sticky="")

        self.input_field = matrixInputField(self, 1)
        self.input_field.grid(row=0, column=3, padx=5, pady=5, sticky="")

        self.operation_field = option(self)
        self.operation_field.grid(row=0, column=4, padx=5, pady=5, sticky="")

    def get_entry(self, event):
        try:
            if self.entry_field.get().isnumeric() == False:
                self.N = 1
                self.entry_field.delete(0, "end")
                self.entry_field.insert(0, self.N)
                # self.error_box("Nhập số nguyên dương từ 1 đến 10")

            elif (int(self.entry_field.get()) > 10) or (
                int(self.entry_field.get()) <= 0
            ):
                self.N = int(self.entry_field.get())
                print("N từ 0 đến 10")
                if self.N > 10:
                    self.N = 10

                else:
                    self.N = 1
                self.entry_field.delete(0, "end")
                self.entry_field.insert(0, self.N)
            else:
                self.N = int(self.entry_field.get())
                try:
                    self.error_title.destroy()
                    self.error_title.grid_forget()
                except:
                    pass
            print(f"self.N1={self.N}")
        except:
            print("Lỗi cmnr")

    def create_input_field(self, master, event):
        try:
            self.input_field.destroy()
            self.input_field.grid.forget()
        except:
            pass
        self.input_field = matrixInputField(self, self.N)
        self.input_field.grid(row=0, column=3, padx=5, pady=5, sticky="w")

    def solve(self):
        try:
            self.input_field.get_matrix_value()
        except:
            pass

    def delay_call(self, event):
        self.after(10, lambda: self.get_entry(event))
        self.after(10, lambda: self.create_input_field(self.master, event))
        self.after(10, lambda: self.input_field.matrix[0].focus_set())


# Tạo khung chứa ma trận
class matrixInputField(customtkinter.CTkFrame):
    def __init__(self, master, N):
        super().__init__(master, width=256, height=256)
        self.grid_propagate(False)
        self.N = N
        self.matrix = []
        self.matrix_val = []
        self.w = 2520
        self.h = 2520
        self.create_matrix()

    def create_matrix(self):
        for i in range(self.N):
            for j in range(self.N):
                # print(f"a[{i}][{j}]")
                entry = customtkinter.CTkEntry(
                    self,
                    placeholder_text="0",
                    width=(self.w // (self.N)) * 0.1,
                    height=(self.h // (self.N)) * 0.1,
                    corner_radius=0,
                    justify="center",
                    font=("Arial", (self.w // (self.N)) * 0.04),
                )
                entry.grid(row=i, column=j, padx=0, pady=0)
                entry.bind("<Return>", lambda e, i=i, j=j: self.move_focus(i + 1, j))
                entry.bind("<Right>", lambda e, i=i, j=j: self.move_focus(i, j + 1))
                entry.bind("<Left>", lambda e, i=i, j=j: self.move_focus(i, j - 1))
                entry.bind("<Down>", lambda e, i=i, j=j: self.move_focus(i + 1, j))
                entry.bind("<Up>", lambda e, i=i, j=j: self.move_focus(i - 1, j))
                self.matrix.append(entry)

    def move_focus(self, i, j):
        if i < self.N and j < self.N:
            self.matrix[i * self.N + j].focus_set()

    def get_matrix_value(self):
        matrix_val = []
        for i in range(self.N):
            row = []
            for j in range(self.N):
                try:
                    value = float(self.matrix[i * self.N + j].get())
                    row.append(value)
                except ValueError:
                    row.append(0.0)
            matrix_val.append(row)
        self.matrix = solvingLU.LUDecomposition(matrix_val, self.N)
        self.matrixL = self.matrix[0]
        self.matrixU = self.matrix[1]
        self.matrixStore = self.matrix[2]

        print(self.matrixL)
        print(self.matrixU)
        print(self.matrixStore)

        self.master.master.opration_field = operation_fieldLU(
            self.master.master, self.matrixStore
        )
        self.master.master.opration_field.grid(
            row=2, column=0, padx=5, pady=5, sticky="nswe"
        )


class option(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.config_checkbox = customtkinter.CTkCheckBox(
            self,
            text="PLU",
            font=("Arial", 20),
        )
        self.config_checkbox.grid(row=0, column=0, padx=5, pady=5, sticky="")
        self.calculate_button = customtkinter.CTkButton(
            self,
            text="Phân tích",
            command=self.master.solve,
            font=("Arial", 20),
        )
        self.calculate_button.grid(row=1, column=0, padx=5, pady=5, sticky="")


class operation_fieldLU(customtkinter.CTkFrame):
    def __init__(self, master, matrixStore):
        super().__init__(master, bg_color="transparent")

        # Create a canvas for scrolling
        self.canvas = customtkinter.CTkCanvas(self, highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Add a scrollbar
        self.scrollbar = customtkinter.CTkScrollbar(
            self, orientation="vertical", command=self.canvas.yview
        )
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # Configure the canvas to use the scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a frame inside the canvas
        self.scrollable_frame = customtkinter.CTkFrame(
            self.canvas, fg_color="transparent"
        )
        self.scrollable_frame_id = self.canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw"
        )

        # Configure resizing behavior
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.scrollable_frame.bind("<Configure>", self.update_scroll_region)
        self.canvas.bind("<Configure>", self.adjust_frame_width)

        # Add content to the scrollable frame
        self.populate_matrix_store(matrixStore)

    def update_scroll_region(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def adjust_frame_width(self, event):
        self.canvas.itemconfig(self.scrollable_frame_id, width=event.width)

    def populate_matrix_store(self, matrixStore):
        r = 0
        self.label = customtkinter.CTkLabel(
            self.scrollable_frame,
            text="A = ",
            font=("Arial", 48),
        )
        self.label.grid(row=r, column=0, padx=5, pady=5, sticky="")
        counter = 1
        for i in range(len(matrixStore)):
            print(i)
            n_box = box(self.scrollable_frame, matrixStore[i])
            n_box.grid(row=r, column=counter, padx=0, pady=0, sticky="")
            counter = counter + 1
            if counter >= 6:
                counter = 0
                r += 1
            if i != len(matrixStore) - 1:
                img_label = customtkinter.CTkLabel(
                    self.scrollable_frame,
                    text="",
                    image=customtkinter.CTkImage(
                        light_image=image, dark_image=image, size=(150, 50)
                    ),
                )
                img_label.grid(row=r, column=counter, padx=0, pady=0, sticky="nsew")
            counter = counter + 1


class box(customtkinter.CTkFrame):
    def __init__(self, master, matrix):
        super().__init__(
            master, width=300, height=300, corner_radius=0, bg_color="transparent"
        )

        # Load the image
        self.grid_propagate(False)
        brackets_image = Image.open("brackets.png")
        brackets_label = customtkinter.CTkLabel(
            self,
            text="",
            image=customtkinter.CTkImage(
                light_image=brackets_image, dark_image=brackets_image, size=(300, 300)
            ),
        )
        # Use .place to position the image as a background
        brackets_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Configure the grid for the CTkEntry widgets

        self.w = 2520
        self.h = 2520

        # Add CTkEntry widgets on top of the image
        newBox = n_(self, matrix)
        newBox.grid(row=0, column=0, padx=0, pady=0, sticky="")


class n_(customtkinter.CTkFrame):
    def __init__(self, master, matrix):
        super().__init__(master)
        self.h = 2520
        self.w = 2520
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        # Add CTkEntry widgets on top of the image
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                print(f"matrix[{i}][{j}]")
                n_label = customtkinter.CTkEntry(
                    self,
                    font=("Arial", (self.w // len(matrix)) * 0.03),
                    width=(self.w // (len(matrix))) * 0.1,
                    height=(self.h // (len(matrix))) * 0.1,
                    # border_width=0,
                    corner_radius=0,
                    justify="center",
                    # fg_color="transparent",
                    # bg_color="transparent",
                )
                n_label.insert(0, f"{matrix[i][j]}")  # Insert the value into the entry
                n_label.grid(row=i, column=j, padx=0, pady=0)
                n_label.configure(state="readonly")


# Tạo khung chung cho ứng dụng
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("BTL DSTT - Phương pháp LU")
        self.geometry("1280x720")
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)

        self.title_frame = titleFrame(self)
        self.title_frame.grid(row=0, column=0, sticky="n")

        self.input_frame = sizeInputFrame(self)
        self.input_frame.grid(row=1, column=0, padx=5, pady=5, sticky="")


app = App()
app.mainloop()
