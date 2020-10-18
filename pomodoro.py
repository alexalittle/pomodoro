# usr/bin/env/ python3

import tkinter as tk

class App:
	def __init__(self, master):

		# pomodoro settings
		self.work_time = 25 * 60
		self.short_break_time = 5 * 60
		self.long_break_time = 25 * 60
		self.pomodoro_status = 1

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
		self.title = tk.Label(title_frame, text = "Pomodoro Timer", font=(None, 16))
		self.title.pack()
		self.timer_display = tk.Label(title_frame, text = "25:00", font=(None, 24))
		self.timer_display.pack()

		# create section for control buttons
		control_frame = tk.Frame(master)
		control_frame.pack(side = tk.TOP)

		# create start, stop, skip, reset, clear buttons
		self.start_btn = tk.Button(control_frame, text="Start", command = self.do_pomodoro)
		self.start_btn.pack(side = tk.LEFT)
		self.stop_btn = tk.Button(control_frame, text="Stop", command = self.stop_timer)
		self.stop_btn.pack(side = tk.LEFT)
		self.skip_btn = tk.Button(control_frame, text="Skip", command = self.skip_session)
		self.skip_btn.pack(side = tk.LEFT)
		self.reset_btn = tk.Button(control_frame, text="Reset", command = self.restart_timer)
		self.reset_btn.pack(side = tk.LEFT)
		self.clear_btn = tk.Button(control_frame, text="Clear", command = self.clear_timer)
		self.clear_btn.pack(side = tk.LEFT)

		# other controls will go here

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
				self.pomodoro_status += 1
				self.callback = None
				self.do_pomodoro()

	def stop_timer(self):
		""" Stops the timer."""
		if self.callback:
			root.after_cancel(self.callback)
			self.callback = None
			self.start_btn["text"] = "Resume"

	def skip_session(self):
		root.after_cancel(self.callback)
		self.callback = None
		self.pomodoro_status += 1
		self.do_pomodoro()

	def restart_timer(self):
		""" Stops the timer if running and resets it to the start time value."""
		self.stop_timer()
		self.current_time = self.start_time
		self.start_btn["text"] = "Start"
		self.update_display()

	def clear_timer(self):
		""" Stops the timer if running and resets all time values to 0."""
		self.stop_timer()
		self.current_time = 0
		self.start_time = 0
		self.start_btn["text"] = "Start"
		self.update_display()

	def sec_to_min(self, seconds):
		""" Given input in seconds, returns equivalent value in minutes (0:00 string)."""
		calculation = divmod(seconds, 60)
		if calculation[1] < 10:
			output = "0" + str(calculation[1])
		else:
			output = str(calculation[1])
		return str(calculation[0]) + ":" + output

	def do_pomodoro(self):
		if self.pomodoro_status % 2 == 1:
			# odd numbers = do pomodoro work time
			timer_len = self.work_time
			title_value = "Work Session"
		elif self.pomodoro_status % 8 == 0:
			# after 4 work sessions and 3 breaks, take a long break
			timer_len = self.long_break_time
			title_value = "Long Break"
		else:
			# even numbers = do pomodoro break time
			timer_len = self.short_break_time
			title_value = "Short Break"
			# do long break
		self.start_time = timer_len
		self.current_time = timer_len
		self.title["text"] = title_value
		self.update_display()
		self.start_handler()

root = tk.Tk()
root.geometry("300x200")
root.title("Pomodoro Timer")
app = App(root)

root.mainloop()