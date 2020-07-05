"""
Name of file - hello_world.py

Purpose of file - This file is an stripped-down example of how Flask renders HTML

Date of most recent revision - 5/30/20

Author(s) - Ethan Bradway

Dependencies and Modules - Flask
"""

from flask import Flask

# from flask import render_template

app = Flask(__name__)


@app.route("/")
def main():
    """
        Parameters - N/A

        Return Data - The string "hello world"

        Purpose - This example renders "hello world" onto the localhost URL.

        Pre-conditions and post-conditions - N/A
    """
    return "hello world"
    # return render_template(
    #     "**/path/to/html/template/file.html"
    # )  # ideally in the templates folder of a Flask project


if __name__ == "__main__":
    app.run()
