#!/usr/bin/env python3
"""
Name: speedtest_gui_4.py
Author: William A Loring
Created: 09/13/23
Purpose: Use a random close speedtest server
using Speedtest.net
https://github.com/sivel/speedtest-cli
https://pypi.org/project/speedtest-cli/
"""
# pip install customtkinter
import customtkinter as ct

# pip install speedtest-cli
from speedtest import Speedtest
import random
import threading


class SpeedTestGui(ct.CTk):
    # Define the initialize method
    def __init__(self):
        super().__init__()
        self.title("Internet Speed Test")
        self.geometry("375x275")
        self.iconbitmap("speedtest_logo.ico")
        self.resizable(False, False)

        # Modes: system (default), light, dark
        ct.set_appearance_mode("dark")
        # Themes: blue (default), dark-blue, green
        ct.set_default_color_theme("blue")

        # Bind the closing event to the on_closing function
        self.protocol("WM_DELETE_WINDOW", self.quit)

        # Create speedtest object
        self.speedtest = Speedtest()

        # Call method to create all the widgets
        self.create_widgets()

    # ---------------------------------- START ------------------------------- #
    def start(self, *args):
        """Start a thread to perform the speed test
        This runs the speedtest on its own thread and doesn't affect
        the main program thread. The GUI is still responsive.
        """
        test_thread = threading.Thread(target=self.run_speedtest)
        test_thread.start()

    # -------------------------- RUN SPEEDTEST ------------------------------- #
    def run_speedtest(self):
        # Clear all labels
        self.lbl_server.configure(text="")
        self.lbl_download.configure(text="")
        self.lbl_upload.configure(text="")
        self.lbl_ping.configure(text="")
        self.btn_start.configure(text="Testing . . .")
        self.progress_bar.set(0)

        # Call methods to run speed test
        self.get_random_server()
        self.get_download_bandwidth()
        self.get_upload_bandwidth()
        self.get_ping_latency()

    # ---------------------- GET DOWNLOAD BANDWIDTH -------------------------- #
    def get_download_bandwidth(self):
        """Get download bandwidth from test server"""
        self.progress_bar.set(0.33)
        self.lbl_status.configure(text="Get Download Bandwidth . . .")

        # Update the frame to show the label changes
        self.main_frame.update()

        # Get download bandwidth, returns bits per second
        download_result = self.speedtest.download()
        # Convert from bits per second to megabits per second
        self._download_result = download_result / 1000 / 1000

        self.lbl_download.configure(text=f" {self._download_result:.2f} Mbps")
        # Update the frame to show the label changes
        self.main_frame.update()

    # ---------------------- GET UPLOAD BANDWIDTH ---------------------------- #
    def get_upload_bandwidth(self):
        """Get upload bandwidth from test server"""
        self.progress_bar.set(0.66)
        # Get and print upload speed
        self.lbl_status.configure(text="Get Upload Bandwidth . . .")
        self.main_frame.update()

        # Get upload bandwidth, returns bits per second
        upload_result = self.speedtest.upload()
        # Convert from bits per second to megabits per second
        self._upload_result = upload_result / 1000 / 1000

        self.lbl_upload.configure(text=f" {self._upload_result:.2f} Mbps")
        # Update the frame to show the label changes
        self.main_frame.update()

    # -------------------------- GET PING LATENCY ---------------------------- #
    def get_ping_latency(self):
        """Get ping latency from test server"""
        self.progress_bar.set(1)
        # Get ping results/latency, return ms
        self._ping_result = self.speedtest.results.ping

        self.lbl_ping.configure(text=f" {self._ping_result:.2f} ms")
        self.lbl_status.configure(text="Speed Test Complete")
        self.btn_start.configure(text="Start Test")
        # Update the frame to show the label changes
        self.main_frame.update()

    # -------------------------- GET RANDOM SERVER --------------------------- #
    def get_random_server(self):
        """Get random servers from speedtest"""
        servers = self.speedtest.get_servers()

        # Print server list for debugging
        # print(servers)

        # Get a random distance key from the dictionary
        random_distance_key = random.choice(list(servers.keys()))

        # Get the list of servers for the selected distance key
        random_servers = servers[random_distance_key]

        # Select a random server from the list
        random_server = random.choice(random_servers)

        name = random_server.get("name")
        # print("URL:", random_server['url'])

        sponsor = random_server.get("sponsor")
        location = random_server.get("cc")
        km = float(random_distance_key)
        miles = km * 0.621371

        self.lbl_server.configure(
            text=f"{sponsor} - {name}, {location}, {miles:.0f} miles"
        )

        # Update the frame to show the label changes
        self.main_frame.update()

    # ------------------------ GET BEST SERVER ------------------------------- #
    def get_best_server(self):
        """Return the nearest test server and location
        in dictionary format"""
        best_server = self.speedtest.get_best_server()
        sponsor = best_server.get("sponsor")
        name = best_server.get("name")
        location = best_server.get("cc")
        self.lbl_server.configure(text=f"{sponsor} - {name}, {location}")

        # Update the frame to show the label changes
        self.main_frame.update()

    # ------------------------- CREATE WIDGETS ------------------------------- #
    def create_widgets(self):
        self.main_frame = ct.CTkFrame(master=self)

        # Fill the frame to the width of the window
        self.main_frame.pack(fill=ct.X)
        # Keep the frame size regardless of the widget sizes
        self.main_frame.pack_propagate(False)

        self.status_bar = ct.CTkFrame(master=self)

        # Fill the frame to the width of the window
        self.status_bar.pack(fill=ct.X)
        # Keep the frame size regardless of the widget sizes
        self.status_bar.pack_propagate(False)

        self.lbl_status = ct.CTkLabel(self.main_frame, text="")
        self.lbl_server = ct.CTkLabel(self.main_frame, text="")

        self.lbl_download_label = ct.CTkLabel(
            self.main_frame, anchor=ct.E, text="Download:", width=13
        )
        self.lbl_upload_label = ct.CTkLabel(
            self.main_frame, anchor=ct.E, text="Upload:", width=13
        )
        self.lbl_ping_label = ct.CTkLabel(
            self.main_frame, anchor=ct.E, text="Ping (Latency):", width=13
        )

        self.lbl_download = ct.CTkLabel(self.main_frame, width=16, text="")
        self.lbl_upload = ct.CTkLabel(self.main_frame, width=16, text="")
        self.lbl_ping = ct.CTkLabel(self.main_frame, width=16, text="")
        self.btn_start = ct.CTkButton(
            self.main_frame, text="Start Test", command=self.start
        )
        self.progress_bar = ct.CTkProgressBar(
            self.status_bar, mode="determinate", width=375
        )
        self.progress_bar.set(0)
        self.progress_bar.grid(row=0, column=0, columnspan=2, sticky=ct.W)

        self.btn_start.grid(row=0, column=0, sticky=ct.W)
        self.lbl_status.grid(row=0, column=1, sticky=ct.W)
        self.lbl_server.grid(row=1, column=0, sticky=ct.W, columnspan=2)

        self.lbl_download_label.grid(row=2, column=0, sticky=ct.EW)
        self.lbl_upload_label.grid(row=3, column=0, sticky=ct.EW)
        self.lbl_ping_label.grid(row=4, column=0, sticky=ct.EW)

        self.lbl_download.grid(row=2, column=1, sticky=ct.W)
        self.lbl_upload.grid(row=3, column=1, sticky=ct.W)
        self.lbl_ping.grid(row=4, column=1, sticky=ct.W)

        # Set padding between frame and window
        self.main_frame.pack_configure(padx=20, pady=20)
        # Set padding for all widgets
        for child in self.main_frame.winfo_children():
            child.grid_configure(padx=4, pady=4, ipadx=3, ipady=3)

        # The enter key will activate the start method
        self.bind("<Return>", self.start)
        self.bind("<KP_Enter>", self.start)
        self.bind("<Escape>", self.quit)

    # ----------------------------- QUIT PROGRAM ----------------------------- #
    def quit(self, *args):
        self.destroy()


def main():
    # Create object from the program class
    speed_test = SpeedTestGui()
    speed_test.mainloop()


if __name__ == "__main__":
    main()
