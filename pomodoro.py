# usr/bin/env/ python3

import tkinter as tk


class App:
    def __init__(self, master):

        super().__init__()
        self.master = master

        # pomodoro settings
        self.work_time = 25 * 60
        self.short_break_time = 5 * 60
        self.long_break_time = 25 * 60
        self.pomodoro_status = 1

        # default display attributes - background color, window size, icon
        self.color = "black"
        master["bg"] = self.color
        master.geometry("300x200")

        # set attributes for start time, current time
        self.start_time = 0
        self.current_time = 0
        self.user_paused = False

        # create variable to be used by start & stop timer functions
        # stores the current call to tkinter's "after" module
        self.callback = None

        # create section for main display
        self.title_frame = tk.Frame(master)
        self.title_frame.pack(side=tk.TOP)
        self.title_frame["bg"] = self.color

        # set up main display
        self.title = tk.Label(self.title_frame,
        					  text="Pomodoro Timer", 
        					  font=(None, 16), 
        					  bg=self.color, 
        					  fg="white")
        self.title.pack()
        self.timer_display = tk.Label(self.title_frame, 
        							  text=self.sec_to_min(self.work_time),
        							  font=(None, 24), 
        							  bg=self.color, 
        							  fg="white")
        self.timer_display.pack()

        # create section for control buttons
        control_frame = tk.Frame(master)
        control_frame.pack(side=tk.TOP)

        # create start, stop, skip, reset, clear buttons
        self.start_btn = tk.Button(control_frame, 
        						   text="Start", 
        						   command=self.start_handler)

        self.stop_btn = tk.Button(control_frame, 
        						  text="Stop", 
        						  command=self.stop_timer)

        self.skip_btn = tk.Button(control_frame, 
        						  text="Skip", 
        						  command=self.skip_session)

        self.reset_btn = tk.Button(control_frame, 
        						   text="Reset", 
        						   command=self.restart_timer)

        self.clear_btn = tk.Button(control_frame, 
        						   text="Clear", 
        						   command=self.clear_timer)

        self.start_btn.pack(side=tk.LEFT)
        self.stop_btn.pack(side=tk.LEFT)
        self.skip_btn.pack(side=tk.LEFT)
        self.reset_btn.pack(side=tk.LEFT)
        self.clear_btn.pack(side=tk.LEFT)

    def update_timer(self):
        """ Updates the timer on the app display."""
        self.timer_display["text"] = self.sec_to_min(self.current_time)

    def update_colors(self, master, color):
        """ Updates the background color of the app window."""
        self.color = color
        self.master["bg"] = self.color
        self.title_frame["bg"] = self.color
        self.title["bg"] = self.color
        self.timer_display["bg"] = self.color

    def start_handler(self):
        """ Helper function.
                Prevents the user from triggering "Start" more than once.
                Differentiates between a fresh start and a start after the user paused.
        """
        if not self.callback:
            if self.user_paused:
                self.user_paused = False
                self.start_btn["text"] = "Start"
                self.start_timer()
            else:
                self.set_pomodoro()
                self.start_timer()

    def start_timer(self):
        """ Starts the timer."""
        if self.start_time > 0 and self.current_time >= 1:
            self.current_time -= 1
            self.update_timer()
            if self.current_time > 0:
                self.callback = root.after(1000, lambda: self.start_timer())
            else:
                root.bell()
                self.pomodoro_status += 1
                self.callback = None
                self.start_handler()

    def stop_timer(self):
        """ Stops the timer."""
        if self.callback:
            root.after_cancel(self.callback)
            self.callback = None
            self.user_paused = True
            self.start_btn["text"] = "Resume"

    def skip_session(self):
        """ Advances to the next session. (Timer is stopped at full value.)"""
        if self.callback:
            root.after_cancel(self.callback)
            self.callback = None
        self.start_btn["text"] = "Start"
        self.pomodoro_status += 1
        self.set_pomodoro()

    def restart_timer(self):
        """ Stops the timer if running and resets it to the start time value."""
        self.stop_timer()
        self.current_time = self.start_time
        self.start_btn["text"] = "Start"
        self.update_timer()

    def clear_timer(self):
        """ Resets all pomodoro values to initial states."""
        self.stop_timer()
        self.user_paused = False
        self.pomodoro_status = 1
        self.start_btn["text"] = "Start"
        self.start_time = self.work_time
        self.update_display(self.start_time, "Pomodoro Timer", "black")

    def sec_to_min(self, seconds):
        """ Given input in seconds, returns equivalent value as a 0:00 string."""
        result = divmod(seconds, 60)
        return str(result[0]) + ":" + "{:02d}".format(result[1])

    def set_pomodoro(self):
        """ Sets up the timer and display for a pomodoro session. """
        if self.pomodoro_status % 2 == 1:
            # odd numbers = do pomodoro work time
            timer_len = self.work_time
            title_value = "Work Session"
            color = "#b30000"  # brick red
        elif self.pomodoro_status % 8 == 0:
            # after 4 work sessions and 3 breaks, take a long break
            timer_len = self.long_break_time
            title_value = "Long Break"
            color = "green"
        else:
            # even numbers = do pomodoro break time
            timer_len = self.short_break_time
            title_value = "Short Break"
            color = "green"
        self.start_time = timer_len
        self.update_display(timer_len, title_value, color)

    def update_display(self, timer_len, title_value, color):
        """ Helper function to update the app window:
        	current time, title label, timer, background color. """
        self.current_time = timer_len
        self.title["text"] = title_value
        self.update_timer()
        self.update_colors(self.master, color)


root = tk.Tk()
root.title("Pomodoro Timer")
root.iconphoto(False, tk.PhotoImage(file="tomato.png"))
app = App(root)

root.mainloop()
