# usr/bin/env/ python3

import tkinter as tk

class App:
	def __init__(self, master):

		# set attributes for start time, current time
		self.start_time = 0
		self.current_time = 0

		# create variable to be used by start & stop timer functions
		# stores the current call to tkinter's "after" module
		self.callback = None

		# create section for main display
		title_frame = tk.Frame(master)
		title_frame.pack(side = tk.TOP)

		# set up main display
		self.title = tk.Label(title_frame, text = "Timer", font=(None, 16))
		self.title.pack()
		self.timer_display = tk.Label(title_frame, text = "0:00", font=(None, 24))
		self.timer_display.pack()

		# create section for control buttons
		control_frame = tk.Frame(master)
		control_frame.pack(side = tk.TOP)

		# create start, stop, reset, clear buttons
		self.start_btn = tk.Button(control_frame, text="Start", command = self.start_handler)
		self.start_btn.pack(side = tk.LEFT)
		self.stop_btn = tk.Button(control_frame, text="Stop", command = self.stop_timer)
		self.stop_btn.pack(side = tk.LEFT)
		self.reset_btn = tk.Button(control_frame, text="Reset", command = self.reset_timer)
		self.reset_btn.pack(side = tk.LEFT)
		self.clear_btn = tk.Button(control_frame, text="Clear", command = self.clear_timer)
		self.clear_btn.pack(side = tk.LEFT)

		# create section for adding minutes
		minutes_frame = tk.Frame(master)
		minutes_frame.pack()

		# create buttons for adding minutes
		self.minutes_label = tk.Label(minutes_frame, text = "Add Minutes")
		self.minutes_label.pack(side = tk.TOP)
		self.minutes_minus_btn = tk.Button(minutes_frame, text = "-", command = lambda: self.change_time(-60))
		self.minutes_minus_btn.pack(side = tk.LEFT)
		self.minutes_plus_btn = tk.Button(minutes_frame, text = "+", command = lambda: self.change_time(60))
		self.minutes_plus_btn.pack(side = tk.RIGHT)

		# create section for adding seconds
		seconds_frame = tk.Frame(master)
		seconds_frame.pack()

		#create section for adding seconds
		self.seconds_label = tk.Label(seconds_frame, text = "Add Seconds")
		self.seconds_label.pack(side = tk.TOP)
		self.seconds_minus_btn = tk.Button(seconds_frame, text = "-", command = lambda: self.change_time(-1))
		self.seconds_minus_btn.pack(side = tk.LEFT)
		self.seconds_plus_btn = tk.Button(seconds_frame, text = "+", command = lambda: self.change_time(1))
		self.seconds_plus_btn.pack(side = tk.RIGHT)

	def update_display(self):
		""" Updates the timer on the app display."""
		self.timer_display["text"] = self.sec_to_min(self.current_time)

	def start_handler(self):
		""" Helper function to prevent the user from triggering "Start" more than once """
		if not self.callback:
			self.start_timer()

	def start_timer(self):
		""" Starts the timer."""
		if self.start_time > 0 and self.current_time >= 1:
			self.current_time -= 1
			self.update_display()
			if self.current_time > 0:
				self.callback = root.after(1000, lambda: self.start_timer())
			else:
				root.bell()
				self.callback = None

	def stop_timer(self):
		""" Stops the timer."""
		if self.callback:
			root.after_cancel(self.callback)
			self.callback = None

	def reset_timer(self):
		""" Stops the timer if running and resets it to the start time value."""
		self.stop_timer()
		self.current_time = self.start_time
		self.update_display()

	def clear_timer(self):
		""" Stops the timer if running and resets all time values to 0."""
		self.stop_timer()
		self.current_time = 0
		self.start_time = 0
		self.update_display()

	def change_time(self, num):
		""" Given an input in seconds, adds that value to the current time. Prevents negative time values."""
		if self.current_time + num >= 0:
			self.current_time += num
			# changes made while timer is already running won't affect saved "start time" value
			if not self.callback:
				self.start_time += num
			self.update_display()

	def sec_to_min(self, seconds):
		""" Given input in seconds, returns equivalent value in minutes (0:00 string)."""
		calculation = divmod(seconds, 60)
		if calculation[1] < 10:
			output = "0" + str(calculation[1])
		else:
			output = str(calculation[1])
		return str(calculation[0]) + ":" + output

root = tk.Tk()
root.geometry("300x200")
root.title("Timer")
app = App(root)

root.mainloop()