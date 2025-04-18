#####################################################
#                                                   #
# Source code belongs to group 12 of Linear Algebra #
# Developed by Tran Anh Huy and YdtTran             #
# Mã nguồn thuộc về nhóm 12 môn Đại Số Tuyến Tính   #
# Được lập trình bởi Trần Anh Huy                   #
#                                                   #
#####################################################

import tkinter as tk
from tkinter import *
import customtkinter as ctk
from dataclasses import dataclass
from PIL import Image, ImageTk
import math
import solvingLU

# Declarations
global matrixSize
global previousSize
global matrixItem
previousSize = 0
outputWidgets = []
changes = []
matrixItem = []

# Settings
frameSize = 250
matrixSize = 0
maxMatrixSize = 10
outputMatrixSize = 150
padding = 10
linePadding = 50
outerPadding = 150
outputPointer = [outerPadding, 500]
arrowImage = Image.open("arrow.png")
arrowImage = arrowImage.resize((150, 50))
bracketsImage = Image.open("brackets.png")
bracketsImage = bracketsImage.resize((156, 156))
# bracketsImage = bracketsImage.resize((100,100))
windowDimension = (
    str(outerPadding * 2 + padding * 4 + outputMatrixSize * 3 + 150 * 2) + "x600"
)

# 2nd declarations
originalPointer = [outerPadding, 500]


@dataclass
class BDSC:
    row: int
    operation: str
    multiplier: float
    targetRow: int


def convertToFloat(value):
    try:
        result = float(value)
        return result
    except ValueError:
        print("Cannot convert to float, returning 0.")
        return 0


def convertToInt(value):
    try:
        result = int(value)
        return result
    except ValueError:
        print("Cannot convert to int, returning 0.")
        return 0


def createMatrixInput(a, b, c):
    global matrixSize
    global previousSize
    matrixSize = convertToInt(app.scrollable_frame.sizeEntry.get())
    if matrixSize <= 0:
        matrixSize = 1
    if matrixSize > maxMatrixSize:
        matrixSize = maxMatrixSize
        app.scrollable_frame.sizeEntry.delete(0, tk.END)
        app.scrollable_frame.sizeEntry.insert(0, str(maxMatrixSize))
        print("Matrix size too large, set to max size")

    app.scrollable_frame.matrixADeclaration.config(text="A = ")

    matrixFrame = app.scrollable_frame.matrixInput
    matrixFrame.configure(height=frameSize)
    matrixFrame.configure(width=frameSize)

    # Remove extra matrixes if size is smaller than before
    top = previousSize
    if previousSize > matrixSize:
        top = matrixSize
        newMatrix = []
        counter = 0
        rowCounter = 0
        removingCounter = 0
        for i in range(0, len(matrixFrame.matrix)):
            if rowCounter >= matrixSize:
                matrixFrame.matrix[i].destroy()
                continue
            if counter < matrixSize:
                counter += 1
                newMatrix.append(matrixFrame.matrix[i])
            elif removingCounter < previousSize - matrixSize:
                removingCounter += 1
                matrixFrame.matrix[i].destroy()
            if removingCounter >= previousSize - matrixSize:
                removingCounter = 0
                counter = 0
                rowCounter += 1
        matrixFrame.matrix = newMatrix

    cellSize = math.ceil(frameSize / matrixSize)
    fontSize = int(frameSize / (matrixSize * 2))
    for i in range(0, matrixSize):
        matrixFrame.grid_rowconfigure(
            i, minsize=math.ceil(frameSize / matrixSize), weight=1
        )
        matrixFrame.grid_columnconfigure(
            i, minsize=math.ceil(frameSize / matrixSize), weight=1
        )

    for i in range(0, matrixSize):
        for j in range(0, matrixSize):
            if i >= previousSize or j >= previousSize:
                entry = ctk.CTkEntry(
                    matrixFrame,
                    placeholder_text="0",
                    border_width=2,
                    corner_radius=0,
                    justify="center",
                )
                matrixFrame.matrix.insert(i * matrixSize + j, entry)
                entry.bind("<Return>", FocusNext)
                entry.bind("<Right>", FocusNext)
                entry.bind("<Up>", FocusNext)
                entry.bind("<Left>", FocusNext)
                entry.bind("<Down>", FocusNext)

    for i in range(0, matrixSize):
        for j in range(0, matrixSize):
            matrixFrame.matrix[i * matrixSize + j].configure(
                width=cellSize + 1, height=cellSize + 1
            )
            matrixFrame.matrix[i * matrixSize + j].cget("font").configure(size=fontSize)
            matrixFrame.matrix[i * matrixSize + j].place(
                x=j * cellSize, y=i * cellSize, anchor="nw"
            )

    previousSize = matrixSize


def FocusNext(event):
    list = app.scrollable_frame.matrixInput.matrix
    widget = event.widget.master
    keyPressed = event.keysym
    nextIndex = list.index(widget)
    if keyPressed == "Return" and nextIndex == len(list) - 1:
        return
    elif keyPressed == "Return":
        nextIndex = (nextIndex + 1) % len(list)
    elif keyPressed == "Right" and widget.index(ctk.END) == widget.index(ctk.INSERT):
        nextIndex = (nextIndex + 1) % len(list)
    elif keyPressed == "Left" and widget.index(ctk.INSERT) == 0:
        nextIndex -= 1
    elif keyPressed == "Down":
        nextIndex = (nextIndex + matrixSize) % len(list)
    elif keyPressed == "Up":
        nextIndex -= matrixSize
    if nextIndex == list.index(widget):
        # Cancel
        return
    nextWidget = list[nextIndex]
    nextWidget.focus_set()


def getMatrix():
    matrix = []
    for i in range(0, matrixSize):
        row = []
        for j in range(0, matrixSize):
            entry = app.scrollable_frame.matrixInput.matrix[i * matrixSize + j]
            value = convertToFloat(entry.get())
            row.append(value)
        matrix.append(row)
    return matrix


def calculateMatrix():
    # Get the matrix and perform LU decomposition
    matrix = getMatrix()
    print(matrix)
    matrixL, matrixU, matrixStore, condition = solvingLU.LUDecomposition(
        matrix, matrixSize
    )
    print("Matrix L:")
    print(matrixL)
    print("Matrix U:")
    print(matrixU)
    print("Matrix Store:")
    print(matrixStore)
    global outputPointer
    global outputWidgets
    global matrixItem

    # Display "A ="
    textA = ctk.CTkLabel(
        app.scrollable_frame.frame,
        text="A = ",
        width=50,
        font=("Helvetica", 25),
        text_color="black",
        anchor="w",
    )
    textA.place(x=outputPointer[0], y=outputPointer[1], anchor="e")
    outputPointer[0] += outputMatrixSize + padding

    clearMatrixItems()

    # Store the PhotoImage object as a persistent reference
    for i in range(len(matrixStore)):
        isArrow = True
        if i == len(matrixStore) - 1:
            isArrow = False
        else:
            isArrow = True
        newBox = n_(app.scrollable_frame.frame, matrixStore[i], isArrow)
        newBox.place(
            x=outputPointer[0] + outputMatrixSize / 2,
            y=outputPointer[1],
            anchor="center",
        )
        matrixItem.append(newBox)

    # newBox = n_(app.scrollable_frame.frame, matrixStore[0])
    # newBox.place(
    #     x=outputPointer[0] + outputMatrixSize / 2,
    #     y=outputPointer[1],
    #     anchor="center",
    # )

    outputPointer[0] = originalPointer[0]
    outputPointer[1] = outputPointer[1] + outputMatrixSize + linePadding

    #
    if condition == False:
        print("Không thể phân tích ma trận này thành LU!!!")
        # Invalid matrix
        text = ctk.CTkLabel(
            app.scrollable_frame.frame,
            text="Ma trận không phân tích LU được",
            width=50,
            font=("Helvetica", 25),
            text_color="black",
            anchor="center",
        )
        text.place(
            relx=0.5, y=outputPointer[1] - linePadding + padding, anchor="center"
        )
        matrixItem.append(text)
        return
    else:
        textL = ctk.CTkLabel(
            app.scrollable_frame.frame,
            text="L = ",
            width=50,
            font=("Helvetica", 25),
            text_color="black",
            anchor="w",
        )
        textL.place(x=outputPointer[0], y=outputPointer[1], anchor="e")
        boxL = n_(app.scrollable_frame.frame, matrixL, False)
        boxL.place(
            x=outputPointer[0] + outputMatrixSize / 2,
            y=outputPointer[1],
            anchor="center",
        )
        outputPointer[0] = originalPointer[0]
        outputPointer[1] = outputPointer[1] + outputMatrixSize + linePadding
        textU = ctk.CTkLabel(
            app.scrollable_frame.frame,
            text="U = ",
            width=50,
            font=("Helvetica", 25),
            text_color="black",
            anchor="w",
        )
        textU.place(x=outputPointer[0], y=outputPointer[1], anchor="e")
        boxU = n_(app.scrollable_frame.frame, matrixU, False)
        boxU.place(
            x=outputPointer[0] + outputMatrixSize / 2,
            y=outputPointer[1],
            anchor="center",
        )
        matrixItem.append(textL)
        matrixItem.append(boxL)
        matrixItem.append(textU)
        matrixItem.append(boxU)
    print(matrixItem)


def clearMatrixItems():
    global matrixItem
    if len(matrixItem) >= 1:
        for widget in matrixItem:
            widget.destroy()
    matrixItem = []
    outputPointer[0] = originalPointer[0]
    outputPointer[1] = originalPointer[1]


# frame
class n_(ctk.CTkFrame):
    def __init__(self, master, matrix, isArrow):
        super().__init__(master, fg_color="transparent")
        global outputPointer
        global matrixItem

        # Brackets
        photo = ImageTk.PhotoImage(bracketsImage)
        brackets = tk.Label(app.scrollable_frame.frame, image=photo)
        brackets.image = photo
        brackets.place(
            x=outputPointer[0] + outputMatrixSize / 2,
            y=outputPointer[1],
            width=156,
            height=156,
            anchor=tk.CENTER,
        )
        parent = tk.Canvas(app.scrollable_frame.frame)
        parent.place(
            x=outputPointer[0],
            y=outputPointer[1],
            width=outputMatrixSize,
            height=outputMatrixSize,
            anchor="w",
        )
        outputPointer[0] += outputMatrixSize + padding

        matrixItem.append(brackets)
        matrixItem.append(parent)

        # Add matrix cells
        cellSize = int(outputMatrixSize / len(matrix))
        for i in range(0, len(matrix)):
            parent.grid_rowconfigure(i, minsize=cellSize, weight=1)
            parent.grid_columnconfigure(i, minsize=cellSize, weight=1)
        for i in range(0, len(matrix)):
            for j in range(0, len(matrix[i])):
                output = "{:.2f}".format(matrix[i][j])
                if int(matrix[i][j]) == matrix[i][j]:
                    output = int(matrix[i][j])
                parent.create_text(
                    cellSize / 2 + cellSize * j,
                    cellSize / 2 + cellSize * i,
                    width=cellSize,
                    text=output,
                    font=("Helvetica", int(cellSize / 4)),
                    fill="black",
                    anchor="center",
                )

        # Add arrow if needed
        if isArrow:
            photo = ImageTk.PhotoImage(arrowImage)
            arrow = ctk.CTkLabel(
                app.scrollable_frame.frame,
                text="",
                image=photo,
                width=150,
                font=("Helvetica", 15),
                text_color="black",
                anchor="w",
            )
            if (
                outputPointer[0]
                >= outerPadding + padding * 4 + outputMatrixSize * 2 + 150 * 2
            ):
                outputPointer[0] = outerPadding
                outputPointer[1] += outputMatrixSize + linePadding

            if outputPointer[
                1
            ] + outputMatrixSize + outerPadding > app.scrollable_frame.frame.cget(
                "height"
            ):
                app.scrollable_frame.frame.configure(
                    height=outputPointer[1] + outputMatrixSize + outerPadding
                )
            arrow.image = photo
            arrow.place(x=outputPointer[0], y=outputPointer[1], anchor="w")
            outputPointer[0] += 150 + padding


# def matrixResultBox(S, matrix):
#     global outputPointer
#     global matrixItem

#     # Update outputPointer for the new row
#     outputPointer[0] = originalPointer[0]
#     outputPointer[1] += outputMatrixSize + linePadding

#     print(f"Displaying {S} at {outputPointer}")

#     # Display the label
#     textA = ctk.CTkLabel(
#         app.scrollable_frame.frame,
#         text=f"{S}",
#         width=50,
#         font=("Helvetica", 25),
#         text_color="black",
#         anchor="w",
#     )
#     textA.place(x=outputPointer[0], y=outputPointer[1], anchor="e")
# outputPointer[0] += outputMatrixSize + padding

# # Display the matrix
# newBox = n_(app.scrollable_frame.frame, matrix, False)
# newBox.place(
#     x=outputPointer[0] + outputMatrixSize / 2,
#     y=outputPointer[1],
#     anchor="center",
# )
# matrixItem.append(newBox)


class MyScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.canvas = ctk.CTkCanvas(self)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.frame = ctk.CTkFrame(
            self.canvas, fg_color="transparent", corner_radius=0, height=1200
        )
        self.frame.pack(side="left", fill="both", expand=True)

        # Size input
        label = ctk.CTkLabel(
            self.frame,
            text=f"Nhập cấp của ma trận vuông:\n(Tối đa là {maxMatrixSize})",
            width=300,
            height=25,
            fg_color="transparent",
            text_color="black",
            font=("Helvetica", 20),
            anchor="n",
        )
        label.place(x=175, y=50, anchor="n")
        size_var = ctk.StringVar()
        size_var.trace_add("write", createMatrixInput)
        self.sizeEntry = ctk.CTkEntry(
            self.frame,
            textvariable=size_var,
            width=100,
            height=100,
            border_width=2,
            corner_radius=10,
            font=("Helvetica", 50),
            justify="center",
        )
        self.sizeEntry.place(x=175, y=50 * 2 + 25 + 100 / 2, anchor="center")

        # Matrix input
        self.matrixADeclaration = tk.Label(
            self.frame, text="", foreground="black", font=("Helvetica", 50), anchor="e"
        )
        self.matrixADeclaration.place(x=500, y=160, width=200, height=150, anchor="e")
        self.matrixInput = tk.Frame(self.frame)
        self.matrixInput.place(
            x=500, y=160, width=frameSize, height=frameSize, anchor="w"
        )
        self.matrixInput.matrix = []

        # Buttons
        button = ctk.CTkButton(
            self.frame,
            width=200,
            height=50,
            border_width=0,
            corner_radius=10,
            text="Calculate",
            font=("Helvetica", 30),
            command=calculateMatrix,
        )
        button.place(relx=0.45, y=325, anchor="ne")
        button = ctk.CTkButton(
            self.frame,
            width=200,
            height=50,
            border_width=0,
            corner_radius=10,
            text="Reset",
            font=("Helvetica", 30),
            fg_color="#666666",
            hover_color="#444444",
            # command=ResetMatrix,
        )
        button.place(relx=0.55, y=325, anchor="nw")

        # Credits
        credits = tk.Label(
            self.frame,
            text="Sản phẩm của nhóm 12\nmôn Đại Số Tuyến Tính",
            foreground="black",
            font=("Helvetica", 15),
            anchor="ne",
        )
        credits.place(relx=0.98, rely=0.02, width=250, height=200, anchor="ne")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry(windowDimension)
        self.title("BTL Nhóm 12")
        self.resizable(False, False)

        self.scrollable_frame = MyScrollableFrame(
            self, fg_color="transparent", corner_radius=0
        )
        self.scrollable_frame.pack(side="left", fill="both", expand=True)


class matrixInputField(ctk.CTkFrame):
    def __init__(self, master, row, column):
        super().__init__(master)


if __name__ == "__main__":
    app = App()
    app.mainloop()
