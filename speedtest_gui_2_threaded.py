"""
    Name: speedtest_gui_1.py
    Author: William A Loring
    Created: 12/05/21
    Purpose: Test internet upload and download speed with Tkinter
    using Speedtest.net. This program uses threads, the GUI
    is responsive while it is testing.
    https://github.com/sivel/speedtest-cli
    https://pypi.org/project/speedtest-cli/
"""
from tkinter import *
from tkinter.ttk import *
# pip install speedtest-cli
from speedtest import Speedtest
import threading


class SpeedTestGui:
    # Define the initialize method
    def __init__(self):
        # Create speedtest object
        self.speedtest = Speedtest()

        self.root = Tk()
        self.root.title("Internet Speed Test")
        self.root.geometry("325x255")
        self.root.iconbitmap("speed.ico")
        self.root.resizable(False, False)

        # Call method to create all the widgets
        self.create_widgets()

        # Start main program loop
        mainloop()

# ---------------------------------- START --------------------------------#
    def start(self, *args):
        """Start a thread to perform the speed test
        This runs the speedtest on its own thread and doesn't affect
        the main program thread. The GUI is still responsive.
        """
        test_thread = threading.Thread(target=self.run_speedtest)
        test_thread.start()

# -------------------------- RUN SPEEDTEST --------------------------------#
    def run_speedtest(self):
        # Clear all labels
        self.lbl_server.configure(text="")
        self.lbl_download.configure(text="")
        self.lbl_upload.configure(text="")
        self.lbl_ping.configure(text="")
        self.btn_start.configure(text="Testing . . .")

        # Call methods to run speed test
        self.get_best_server()
        self.get_download_bandwidth()
        self.get_upload_bandwidth()
        self.get_ping_latency()

# ---------------------- GET DOWNLOAD BANDWIDTH ---------------------------#
    def get_download_bandwidth(self):
        """Get download bandwidth from test server."""
        self.lbl_status.configure(text="Get Download Bandwidth . . .")
        # Update the frame to show the label changes
        self.main_frame.update()
        # Get download bandwidth, returns bits per second
        download_result = self.speedtest.download()
        # Convert from bits per second to megabits per second
        self._download_result = download_result / 1000 / 1000

        self.lbl_download.configure(
            text=f" {self._download_result:.2f} Mbps")
        # Update the frame to show the label changes
        self.main_frame.update()

# ---------------------- GET UPLOAD BANDWIDTH -----------------------------#
    def get_upload_bandwidth(self):
        """Get upload bandwidth from test server."""
        # Get and print upload speed
        self.lbl_status.configure(text="Get Upload Bandwidth . . .")
        self.main_frame.update()

        # Get upload bandwidth, returns bits per second
        upload_result = self.speedtest.upload()
        # Convert from bits per second to megabits per second
        self._upload_result = upload_result / 1000 / 1000

        self.lbl_upload.configure(
            text=f" {self._upload_result:.2f} Mbps")
        # Update the frame to show the label changes
        self.main_frame.update()

# -------------------------- GET PING LATENCY -----------------------------#
    def get_ping_latency(self):
        """Get ping latency from test server."""
        # Get ping results/latency, return ms
        self._ping_result = self.speedtest.results.ping

        self.lbl_ping.configure(text=f" {self._ping_result:.2f} ms")
        self.lbl_status.configure(text="Speed Test Complete")
        # Update the frame to show the label changes
        self.main_frame.update()

# ---------------------- GET BEST SERVER --------------------------------#
    def get_best_server(self):
        # Returns the nearest server
        # Return the nearest test server and location in dictionary format
        best_server = self.speedtest.get_best_server()
        sponsor = best_server.get("sponsor")
        name = best_server.get("name")
        cc = best_server.get("cc")
        self.lbl_server.configure(text=f"{sponsor} - {name}, {cc}")

        # Update the frame to show the label changes
        self.main_frame.update()

# ---------------------- CREATE WIDGETS ----------------------------------#
    def create_widgets(self):
        self.main_frame = LabelFrame(
            self.root,
            text="Internet Speed Test",
            relief=GROOVE)

        # Fill the frame to the width of the window
        self.main_frame.pack(fill=X)
        # Keep the frame size regardless of the widget sizes
        self.main_frame.pack_propagate(False)

        self.lbl_status = Label(
            self.main_frame,
        )
        self.lbl_server = Label(
            self.main_frame,
        )

        self.lbl_download_label = Label(
            self.main_frame,
            anchor=E,
            text="Download:",
            width=13
        )
        self.lbl_upload_label = Label(
            self.main_frame,
            anchor=E,
            text="Upload:",
            width=13
        )
        self.lbl_ping_label = Label(
            self.main_frame,
            anchor=E,
            text="Ping (Latency):",
            width=13
        )

        self.lbl_download = Label(
            self.main_frame,
            width=16,
            relief=GROOVE
        )
        self.lbl_upload = Label(
            self.main_frame,
            width=16,
            relief=GROOVE
        )
        self.lbl_ping = Label(
            self.main_frame,
            width=16,
            relief=GROOVE
        )
        self.btn_start = Button(
            self.main_frame,
            text="Start Test",
            command=self.start
        )

        self.btn_start.grid(row=0, column=0, sticky=W)
        self.lbl_status.grid(row=0, column=1, sticky=W)
        self.lbl_server.grid(row=1, column=0, sticky=W, columnspan=2)

        self.lbl_download_label.grid(row=2, column=0, sticky=EW)
        self.lbl_upload_label.grid(row=3, column=0, sticky=EW)
        self.lbl_ping_label.grid(row=4, column=0)

        self.lbl_download.grid(row=2, column=1, sticky=W)
        self.lbl_upload.grid(row=3, column=1, sticky=W)
        self.lbl_ping.grid(row=4, column=1, sticky=W)

        # Set padding between frame and window
        self.main_frame.pack_configure(padx=20, pady=20)
        # Set padding for all widgets
        for child in self.main_frame.winfo_children():
            child.grid_configure(padx=5, pady=5, ipadx=4, ipady=4)
        # The enter key will activate the calculate method
        self.root.bind("<Return>", self.start)
        self.root.bind("<KP_Enter>", self.start)
        self.root.bind('<Escape>', self.quit)

# ----------------------------- QUIT PROGRAM ------------------------------#
    def quit(self, *args):
        self.destroy()


# Create object from the program class to run the program
speed_test = SpeedTestGui()
