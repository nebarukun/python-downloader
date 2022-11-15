# -----------------------------------------------------------
# Python · Downloader
# Version: 2.0.0
# Developer: nebaru
# Website: WDTools.org
# E-Mail: hello@wdtools.org
# Copyright © 2021 · WDTools.org
# -----------------------------------------------------------

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image
from urllib.parse import urlparse, urlsplit
from datetime import datetime
from requests_html import HTMLSession



import os
import sys
import time
import requests
import webbrowser
import tkinter as tk
import urllib.request



from functionality.images import *
from functionality.links import *
from functionality.files import *
from functionality.video import *




class MainWindow(tk.Frame):

  def __init__(self, master=None):
    super().__init__(master)
    self.master = master
    self.grid()
    self.create_widgets()



  def create_widgets(self):

    self.save_link_int_var = tk.IntVar()
    self.int_var_widget = tk.IntVar()

    self.link_visible = False

    self.url_label = Label(self, width=5, text="URL:", fg="#000000", font=("Open Sans", 14))
    self.url_label.grid(row=1, column=0, pady=10, sticky=W)

    self.url_field = Entry(self, width=40, font=("Open Sans", 14, "bold"))
    self.url_field.grid(row=2, column=0, pady=10, padx=10, sticky=W)
    self.url_field.focus()

    self.clear_url_field_btn = Button(self, width=15, text="Clear", font=("Open Sans", 14), command=self.clear_url_field)
    self.clear_url_field_btn.grid(row=2, column=1, pady=10, padx=10, sticky=W)

    self.download_line = ttk.Separator(self, orient='horizontal')
    self.download_line.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky=EW)

    self.download_radio_label = Label(self, width=10, text="Download:", fg="#000000", font=("Open Sans", 14))
    self.download_radio_label.grid(row=4, column=0, pady=10, sticky=W)

    self.radio_images = Radiobutton(self, width=10, text="Images", font=("Open Sans", 14), pady=10, variable=self.int_var_widget, value=1, command=self.adv_image)
    self.radio_images.grid(row=5, column=0, pady=10, sticky=W)

    self.radio_links = Radiobutton(self, width=10, text="Links", font=("Open Sans", 14), pady=10, variable=self.int_var_widget, value=2, command=self.adv_link)
    self.radio_links.grid(row=5, column=0, pady=10, sticky=S)

    self.radio_files = Radiobutton(self, width=10, text="All Files", font=("Open Sans", 14), pady=10, variable=self.int_var_widget, value=3, command=self.adv_files)
    self.radio_files.grid(row=5, column=0, pady=10, sticky=E)

    self.radio_files = Radiobutton(self, width=10, text="YouTube Video", font=("Open Sans", 14), pady=10, variable=self.int_var_widget, value=4, command=self.adv_video)
    self.radio_files.grid(row=5, column=1, pady=10, sticky=EW)

    self.pre_settings_line = ttk.Separator(self, orient='horizontal')
    self.pre_settings_line.grid(row=6, column=0, columnspan=2, pady=10, padx=10, sticky=EW)

    self.download_btn = Button(self, text="Download", width=15, bg="#909090", font=("Open Sans", 14), command=self.start_download)
    self.download_btn.grid(row=12, column=0, pady=10, padx=10, sticky=E)

    self.cancel_btn = Button(self, text="Close", width=15, font=("Open Sans", 14), command=self.close_application) # Destroy (remove) all window
    self.cancel_btn.grid(row=12, column=1, pady=10, padx=10, sticky=W)

    self.config_first_line = ttk.Separator(self, orient='horizontal')
    self.config_first_line.grid(row=13, column=0, columnspan=2, pady=10, padx=10, sticky=EW)

    self.license_info = Button(self, text="Terms and Conditions", width=18, font=("Open Sans", 10), command=lambda: webbrowser.open("https://wdtools.org/terms_and_conditions.php"))
    self.license_info.grid(row=14, column=0, pady=10, padx=10, sticky=E)

    self.about_info = Button(self, text="About", width=10, font=("Open Sans", 10), command=self.about_software)
    self.about_info.grid(row=14, column=1, pady=10, padx=10, sticky=E)




  def adv_image(self):

    if (self.link_visible == True):
      self.save_link.destroy()
      self.save_link_list.destroy()
      self.save_link_array.destroy()
      self.end_link_line.destroy()
      self.link_visible = False



  def adv_link(self):

    self.link_visible = True

    self.save_link = Label(self, width=10, text="Save as:", fg="#000000", font=("Open Sans", 14))
    self.save_link.grid(row=7, column=0, pady=10, sticky=W)

    self.save_link_list = Radiobutton(self, width=8, text="List", font=("Open Sans", 14), pady=10, variable=self.save_link_int_var, value=1)
    self.save_link_list.grid(row=7, column=0, pady=10, sticky=S)
    self.save_link_list.select()

    self.save_link_array = Radiobutton(self, width=8, text="Array", font=("Open Sans", 14), pady=10, variable=self.save_link_int_var, value=2)
    self.save_link_array.grid(row=7, column=0, pady=10, sticky=E)

    self.end_link_line = ttk.Separator(self, orient='horizontal')
    self.end_link_line.grid(row=8, column=0, columnspan=2, pady=10, padx=10, sticky=EW)



  def adv_files(self):

    if (self.link_visible == True):
      self.save_link.destroy()
      self.save_link_list.destroy()
      self.save_link_array.destroy()
      self.end_link_line.destroy()
      self.link_visible = False



  def adv_video(self):

    if (self.link_visible == True):
      self.save_link.destroy()
      self.save_link_list.destroy()
      self.save_link_array.destroy()
      self.end_link_line.destroy()
      self.link_visible = False



  def start_download(self):

    if (self.int_var_widget.get() == 0):
      messagebox.showinfo(title="Warning!", message="Select what you want to download: Images or Links.")

    else:

      if (len(self.url_field.get()) == 0):
        messagebox.showinfo(title="Warning!", message="URL Field ist Empty!\nPlease add an URL:\nhttps://...\nor\nhttp://...")

      else:
        self.check_settings_and_url()



  def check_settings_and_url(self):

    check_string = urlparse(self.url_field.get())

    if ((check_string.scheme == 'http') or (check_string.scheme == 'https')):
      self.create_download_folder()

    else:
      messagebox.showinfo(title="Warning!", message="URL is wrong\nPlease write the URL correctly:\nhttps://...\nor\nhttp://...")




  def create_download_folder(self):
    current_datetime = datetime.now()
    directory_datetime = current_datetime.strftime("Date_%m-%d-%Y_Time_%H-%M-%S")

    # GET PATH TO CURRENT DIRECTORY
    get_directory = os.getcwd()
    create_download_folder = get_directory + "/Download_Data_" + directory_datetime

    try:
      # CREATE DOWNLOAD FOLDER
      os.mkdir(create_download_folder)

    except OSError:
      print("Creation of the directory %s failed" % create_download_folder)

    else:
      print("Successfully created the directory %s " % create_download_folder)

      if (self.int_var_widget.get() == 1):

        ImageDownloader.__init__(self, create_download_folder)

      elif (self.int_var_widget.get() == 2):

        LinkDownloader.__init__(self, create_download_folder)

      else:

        VideoDownloader.__init__(self, create_download_folder)









  def about_software(self):
    messagebox.showinfo(title="About", message='Version: 2.0.0\n\nDeveloper: nebaru\nWebsite: wdtools.org\nContact: hello@wdtools.org')



  def clear_url_field(self):
    self.url_field.delete(0, 'end')



  def close_application(self):
    self.master.quit()
    sys.exit(1)



  def close_window(self):
    root.quit()
    sys.exit(1)






root = tk.Tk()
root.title("Python · Downloader")

# PREVENT WINDOW FROM BEING RESIZED
root.resizable(width=False, height=False)

# ROOT WINDOW - RUN AND ON WINDOW CLOSE EXECUTE "close_window" FUNCTION
root.protocol('WM_DELETE_WINDOW', MainWindow(master=root).close_window)

root.mainloop()
