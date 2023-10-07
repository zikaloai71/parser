# C++ Parser

This is a Python project that uses Tkinter and Graphviz to create a simple parser for C++ programming language. It allows the user to write any simple program in C++ and click convert, which shows the scanner output and also draws a tree of all different inputs the user writes.

## Installation

To run this project, you need to have Python 3 and the following packages installed:

- Tkinter: A standard Python interface to the Tk GUI toolkit.
- Graphviz: A Python interface to the Graphviz graph layout and visualization package.

You can install them using pip:

```bash
pip install tkinter
pip install graphviz
```

## Usage

To run the project, simply execute the main.py file:

```bash
python3 program.py
```

This will open a GUI window where you can write your C++ code in the text box and click the convert button. The scanner output will be displayed in another text box, and the tree of the inputs will be rendered using Graphviz in a separate window.

![image](https://github.com/zikaloai71/parser/assets/91837017/226d08f0-f560-432b-be26-d5dab4a756a4)

You can also import the input.txt folder to have quick run.

## Note
- we haven't implemented the whole language but the basics only so some things are missed like the data type so you must write your variable directly without specify it's data type.

