# -----------------------------------------------------------
# Python · Downloader
# Version: 1.0.0
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

    self.application_title = Label(self, text="Python · Downloader",  width=40, fg="#000000", font=("Open Sans", 16, "bold"))
    self.application_title.grid(row=1, column=0, pady=10, sticky=EW)

    self.url_label = Label(self, text="URL:", fg="#000000", font=("Open Sans", 14))
    self.url_label.grid(row=2, column=0, pady=10, padx=10, sticky=W)

    self.url_field = Entry(self, width=27, font=("Open Sans", 14, "bold"))
    self.url_field.grid(row=2, column=0, pady=10, padx=60, sticky=S)
    self.url_field.focus()

    self.clear_url_field_btn = Button(self, text="Clear", font=("Open Sans", 12), command=self.clear_url_field)
    self.clear_url_field_btn.grid(row=2, column=0, pady=10, padx=10, sticky=E)

    self.download_line = ttk.Separator(self, orient='horizontal')
    self.download_line.grid(row=3, pady=10, padx=10, sticky=EW)

    self.download_radio_label = Label(self, width=10, text="Download:", fg="#000000", font=("Open Sans", 14))
    self.download_radio_label.grid(row=4, column=0, pady=10, sticky=W)

    self.radio_images = Radiobutton(self, width=8, text="Images", font=("Open Sans", 14), pady=10, variable=self.int_var_widget, value=1, command=self.adv_image)
    self.radio_images.grid(row=5, column=0, pady=10, sticky=W)

    self.radio_links = Radiobutton(self, width=8, text="Links", font=("Open Sans", 14), pady=10, variable=self.int_var_widget, value=2, command=self.adv_link)
    self.radio_links.grid(row=5, column=0, pady=10, sticky=S)

    self.radio_all_files = Radiobutton(self, width=8, text="All Files", font=("Open Sans", 14), pady=10, variable=self.int_var_widget, value=3, command=self.adv_all_files)
    self.radio_all_files.grid(row=5, column=0, pady=10, sticky=E)

    self.pre_settings_line = ttk.Separator(self, orient='horizontal')
    self.pre_settings_line.grid(row=6, pady=10, padx=10, sticky=EW)

    self.download_btn = Button(self, text="Download", width=15, bg="#909090", font=("Open Sans", 14), command=self.start_download)
    self.download_btn.grid(row=12, column=0, pady=10, padx=10, sticky=W)

    self.cancel_btn = Button(self, text="Close", width=15, font=("Open Sans", 14), command=self.close_application) # Destroy (remove) all window
    self.cancel_btn.grid(row=12, column=0, pady=10, padx=10, sticky=E)

    self.config_first_line = ttk.Separator(self, orient='horizontal')
    self.config_first_line.grid(row=13, pady=10, padx=10, sticky=EW)

    self.about_info = Button(self, text="About", width=10, font=("Open Sans", 10), command=self.about_software)
    self.about_info.grid(row=14, column=0, pady=10, padx=10, sticky=S)

    self.license_info = Button(self, text="T&C", width=10, font=("Open Sans", 10), command=lambda: webbrowser.open("https://wdtools.org/terms_and_conditions.php"))
    self.license_info.grid(row=14, column=0, pady=10, padx=10, sticky=E)



  def adv_image(self):

    if (self.link_visible == True):
      self.save_as_link.destroy()
      self.file_type_txt.destroy()
      self.file_type_json.destroy()
      self.link_end_line.destroy()
      self.link_visible = False



  def adv_link(self):

    self.link_visible = True

    self.save_as_link = Label(self, width=10, text="Save as:", fg="#000000", font=("Open Sans", 14))
    self.save_as_link.grid(row=7, column=0, pady=10, sticky=W)

    self.file_type_txt = Radiobutton(self, width=8, text="txt", font=("Open Sans", 14), pady=10, variable=self.save_link_int_var, value=1)
    self.file_type_txt.grid(row=7, column=0, pady=10, sticky=S)
    self.file_type_txt.select()

    self.file_type_json = Radiobutton(self, width=8, text="Array", font=("Open Sans", 14), pady=10, variable=self.save_link_int_var, value=2)
    self.file_type_json.grid(row=7, column=0, pady=10, sticky=E)

    self.link_end_line = ttk.Separator(self, orient='horizontal')
    self.link_end_line.grid(row=8, pady=10, padx=10, sticky=EW)



  def adv_all_files(self):

    if (self.link_visible == True):
      self.save_as_link.destroy()
      self.file_type_txt.destroy()
      self.file_type_json.destroy()
      self.link_end_line.destroy()
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
        self.download_images(create_download_folder)

      elif (self.int_var_widget.get() == 2):
        self.download_links(create_download_folder)

      else:
        self.download_all_files(create_download_folder)



  def download_images(self, directory_path):

    # FIELDS - DISPLAY DOWNLOAD INFORMATION - "AMOUNT OF AVAILABLE IMAGES" AND "AMOUNT OF DOWNLOADED IMAGES"
    self.display_total_amount_images_label = Label(self, width=12, text="Total image sources:", fg="#000000", font=("Open Sans", 14), anchor=W)
    self.display_total_amount_images_label.grid(row=9, column=0, pady=10, padx=10, sticky=W)

    self.display_total_amount_images = Label(self, width=10, text="0", fg="#000000", font=("Open Sans", 14, "bold"), anchor=CENTER)
    self.display_total_amount_images.grid(row=10, column=0, pady=10, padx=10, sticky=W)

    self.display_downloaded_amount_images_label = Label(self, width=17, text="Downloaded images:", fg="#000000", font=("Open Sans", 14), anchor=W)
    self.display_downloaded_amount_images_label.grid(row=9, column=0, pady=10, padx=10, sticky=E)

    self.display_downloaded_amount_images = Label(self, width=10, text="0", fg="#000000", font=("Open Sans", 14, "bold"), anchor=CENTER)
    self.display_downloaded_amount_images.grid(row=10, column=0, pady=10, padx=10, sticky=E)

    self.display_downloaded_line = ttk.Separator(self, orient='horizontal')
    self.display_downloaded_line.grid(row=11, pady=10, padx=10, sticky=EW)


    # GET FIELD URL VALUE
    url = self.url_field.get()

    # SPLIT URL
    get_base_url = urlsplit(url)

    session = HTMLSession()

    get_url_session = session.get(url)

    # GET HTML "BODY" OF WEBSITE
    get_html_body = get_url_session.html.find('body', first=True)

    # FIND "IMG" TAG
    get_img_tags = get_html_body.find('img')

    # DOWNLOADED IMAGES COUNTER - FOR "display_downloaded_amount_images" FIELD
    downloaded_images_counter = 0

    # ADD FIELDS TO VARIABLES
    amount_of_images_on_website_label = self.display_total_amount_images_label
    amount_of_images_downloaded_label = self.display_downloaded_amount_images_label
    amount_of_images_on_website = self.display_total_amount_images
    amount_of_images_downloaded = self.display_downloaded_amount_images


    # LOOP THROUGH ALL IMAGES
    for ids in range(len(get_img_tags)):

      if ("src" in get_img_tags[ids].attrs):
        get_data_src = get_img_tags[ids].attrs["src"]
      elif ( ("src" in get_img_tags[ids].attrs) and ("data-src" in get_img_tags[ids].attrs) ):
        get_data_src = get_img_tags[ids].attrs["src"]
      else:
        get_data_src = get_img_tags[ids].attrs["data-src"]


      # GET FILE NAME AND FILE TYPE - EXAMPLE ".jpg"
      get_end_of_file = get_data_src.split('/')[-1]

      ## IF PARAM AFTER IMAGE TAG - REMOVE ? AND EVERYTHING AFTER IT
      if ("?" in get_end_of_file):
        file_name = get_end_of_file.split("?")[0]
      else:
        file_name = get_end_of_file


      # SPLIT FILE PATH - AND FILE TYPE
      file_path, file_type = os.path.splitext(file_name)

      # CHECK IF FILE TYPE EQUALS AN IMAGE FILE TYPE
      a_string = file_name
      matches = [".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp", ".gif", ".svg", ".eps", ".raw"]

      # CHECK IF FILE TYPE EQUALS AN IMAGE FILE TYPE
      if any(x in a_string for x in matches):

        # INCREASE COUNTER BY ONE - AFTER EACH LOOP
        downloaded_images_counter += 1

        # -----------------------------------------------------------
        # CHECK IF "IMG SRC" URL IS AN EXTERNAL OR AN INTERNAL URL
        # -----------------------------------------------------------

        # CHECK IF URL IS EXTERNAL
        if (("https://" or "http://") in get_data_src):

          # COMBINE "DOWNLOAD PATH" AND "FILE NAME" - TO "download_destination"
          download_destination = os.path.join(directory_path, "Image_" + str(ids) + "_" + file_name)


          if ((" ") in get_data_src):
            remove_whitespace_url = get_data_src.replace(" ", "%20")
          else:
            remove_whitespace_url = get_data_src


          # TRY TO DOWNLOAD THE IMAGE FILE
          try:
            urllib.request.urlretrieve(remove_whitespace_url, download_destination)

            # GET REQUEST CODE LIKE: 200 (OK) - 404 (PAGE NOT FOUND) - AND MORE
            # print("Get Code ", urllib.request.urlopen(get_data_src).getcode())

          except: # IF FILE COULDN'T BE DOWNLOADED - TRY NEXT ONE
            print("Error - File has not been downloaded! ", urllib.request.urlopen(get_data_src).getcode())

        else: # ELSE IS INTERNAL

          # CHECK PATH OF URL
          internal_file_img_src = ""

          if (get_data_src[:1] == "/"):
            get_data_src = get_data_src[1:]


          if ((" ") in get_data_src):
            remove_whitespace_url = get_data_src.replace(" ", "%20")
          else:
            remove_whitespace_url = get_data_src

          internal_file_img_src = get_base_url.scheme + "://" + get_base_url.netloc + "/" + remove_whitespace_url

          # COMBINE "DOWNLOAD PATH" AND "FILE NAME" - TO "download_destination"
          download_destination = os.path.join(directory_path, "Image_" + str(ids) + "_" + file_name)

          # TRY TO DOWNLOAD THE IMAGE FILE
          try:
            urllib.request.urlretrieve(internal_file_img_src, download_destination)

            # GET REQUEST CODE LIKE: 200 (OK) - 404 (PAGE NOT FOUND) - AND MORE
            # print("Get Code ", urllib.request.urlopen(get_data_src).getcode())

          except: # IF FILE COULDN'T BE DOWNLOADED - TRY NEXT ONE
            print("Error - File has not been downloaded! ", urllib.request.urlopen(get_data_src).getcode())

        # -----------------------------------------------------------
        # END CHECK
        # -----------------------------------------------------------


        if (ids == 0):
          amount_of_images_on_website['text'] = 0 # ADD VALUE 0 TO "TEXT"
          amount_of_images_on_website.update_idletasks() # UPDATE LABEL "TEXT" VALUE

          amount_of_images_downloaded['text'] = 0 # ADD VALUE 0 TO "TEXT"
          amount_of_images_downloaded.update_idletasks() # UPDATE LABEL "TEXT" VALUE

          time.sleep(0.2) # WAIT FOR 2 MILLISECOND
        # END IF 0

        amount_of_images_on_website['text'] = len(get_img_tags) # ADD AMOUNT OF AVAILABLE IMAGES TO "TEXT"
        amount_of_images_on_website.update_idletasks() # UPDATE LABEL "TEXT" VALUE

        amount_of_images_downloaded['text'] = downloaded_images_counter # ADD AMOUNT OF DOWNLOADED IMAGES TO "TEXT"
        amount_of_images_downloaded.update_idletasks() # UPDATE LABEL "TEXT" VALUE

        time.sleep(0.2) # WAIT FOR 2 MILLISECOND

        # IF ALL POSSIBLE IMAGES HAVE BEEN DOWNLOADED DISPLAY MESSAGE
        if (ids == (len(get_img_tags) - 1)):
          messagebox.showinfo(title="Info!", message="ALL FILES HAVE BEEN DOWNLOADED")
          amount_of_images_on_website_label.destroy()
          amount_of_images_downloaded_label.destroy()
          amount_of_images_on_website.destroy()
          amount_of_images_downloaded.destroy()
          self.display_downloaded_line.destroy()
        else:
          # IF FILE TYPE IS NOT AN IMAGE FILE TYPE AND IT'S NOT THE LAST FILE - SKIP THIS AND LOOP THROUGH NEXT FILE
          continue



      elif (("base64") in file_name): # IMPORTANT - IF IMAGE FILE EQUALS "base64" SKIP IT

        if (ids == (len(get_img_tags) - 1)):
          messagebox.showinfo(title="Info!", message="ALL FILES HAVE BEEN DOWNLOADED")
          amount_of_images_on_website_label.destroy()
          amount_of_images_downloaded_label.destroy()
          amount_of_images_on_website.destroy()
          amount_of_images_downloaded.destroy()
          self.display_downloaded_line.destroy()
        else:
          # IF FILE TYPE IS NOT AN FILE TYPE AND IT'S NOT THE LAST FILE - SKIP THIS AND LOOP THROUGH NEXT FILE
          continue



      else: # IMPORTANT - URL HAS IMAGE FILE TYPE EXTENSION

        # GET FILE TYPE
        get_type_of_unknown_file = Image.open(requests.get(get_data_src, stream=True).raw).format

        # INCREASE COUNTER BY ONE - AFTER EACH LOOP
        downloaded_images_counter += 1

        # -----------------------------------------------------------
        # CHECK IF "IMG SRC" URL IS AN EXTERNAL OR AN INTERNAL URL
        # -----------------------------------------------------------

        # CHECK IF URL IS EXTERNAL
        if (("https://" or "http://") in get_data_src):

          # COMBINE "DOWNLOAD PATH" AND "FILE NAME" - TO "download_destination"
          download_destination = os.path.join(directory_path, "Image_" + str(ids) + "_" + file_name + "." + get_type_of_unknown_file.lower())


          if ((" ") in get_data_src):
            remove_whitespace_url = get_data_src.replace(" ", "%20")
          else:
            remove_whitespace_url = get_data_src


          # TRY TO DOWNLOAD THE IMAGE FILE
          try:
            urllib.request.urlretrieve(remove_whitespace_url, download_destination)

            # GET REQUEST CODE LIKE: 200 (OK) - 404 (PAGE NOT FOUND) - AND MORE
            # print("Get Code ", urllib.request.urlopen(get_data_src).getcode())

          except: # IF FILE COULDN'T BE DOWNLOADED - TRY NEXT ONE
            print("Error - File has not been downloaded! ", urllib.request.urlopen(get_data_src).getcode())

        else: # ELSE IS INTERNAL

          # CHECK PATH OF URL
          internal_file_img_src = ""

          if (get_data_src[:1] == "/"):
            get_data_src = get_data_src[1:]


          if ((" ") in get_data_src):
            remove_whitespace_url = get_data_src.replace(" ", "%20")
          else:
            remove_whitespace_url = get_data_src

          internal_file_img_src = get_base_url.scheme + "://" + get_base_url.netloc + "/" + remove_whitespace_url

          # COMBINE "DOWNLOAD PATH" AND "FILE NAME" - TO "download_destination"
          download_destination = os.path.join(directory_path, "Image_" + str(ids) + "_" + file_name + "." + get_type_of_unknown_file.lower())

          # TRY TO DOWNLOAD THE IMAGE FILE
          try:
            urllib.request.urlretrieve(internal_file_img_src, download_destination)

            # GET REQUEST CODE LIKE: 200 (OK) - 404 (PAGE NOT FOUND) - AND MORE
            # print("Get Code ", urllib.request.urlopen(get_data_src).getcode())

          except: # IF FILE COULDN'T BE DOWNLOADED - TRY NEXT ONE
            print("Error - File has not been downloaded! ", urllib.request.urlopen(get_data_src).getcode())

        # -----------------------------------------------------------
        # END CHECK
        # -----------------------------------------------------------


        if (ids == 0):
          amount_of_images_on_website['text'] = 0 # ADD VALUE 0 TO "TEXT"
          amount_of_images_on_website.update_idletasks() # UPDATE LABEL "TEXT" VALUE

          amount_of_images_downloaded['text'] = 0 # ADD VALUE 0 TO "TEXT"
          amount_of_images_downloaded.update_idletasks() # UPDATE LABEL "TEXT" VALUE

          time.sleep(0.2) # WAIT FOR 2 MILLISECOND
        # END IF 0

        amount_of_images_on_website['text'] = len(get_img_tags) # ADD AMOUNT OF AVAILABLE IMAGES TO "TEXT"
        amount_of_images_on_website.update_idletasks() # UPDATE LABEL "TEXT" VALUE

        amount_of_images_downloaded['text'] = downloaded_images_counter # ADD AMOUNT OF DOWNLOADED IMAGES TO "TEXT"
        amount_of_images_downloaded.update_idletasks() # UPDATE LABEL "TEXT" VALUE

        time.sleep(0.2) # WAIT FOR 2 MILLISECOND

        # IF FILE TYPE IS NOT AN IMAGE FILE TYPE - AND IT'S THE LAST FILE - DISPLAY MESSAGEBOX - ALL FILES HAVE BEEN DOWNLOADED
        if (ids == (len(get_img_tags) - 1)):
          messagebox.showinfo(title="Info!", message="ALL FILES HAVE BEEN DOWNLOADED")
          amount_of_images_on_website_label.destroy()
          amount_of_images_downloaded_label.destroy()
          amount_of_images_on_website.destroy()
          amount_of_images_downloaded.destroy()
          self.display_downloaded_line.destroy()



  def download_links(self, directory_path):

    # FIELDS - DISPLAY DOWNLOAD INFORMATION - "AMOUNT OF AVAILABLE ANCHORS" AND "AMOUNT OF SAVED ANCHORS TEXT"
    self.display_total_amount_anchor_label = Label(self, width=12, text="Total anchor:", fg="#000000", font=("Open Sans", 14), anchor=W)
    self.display_total_amount_anchor_label.grid(row=9, column=0, pady=10, padx=10, sticky=W)

    self.display_total_amount_anchor = Label(self, width=10, text="0", fg="#000000", font=("Open Sans", 14, "bold"), anchor=CENTER)
    self.display_total_amount_anchor.grid(row=10, column=0, pady=10, padx=10, sticky=W)

    self.display_downloaded_amount_anchor_label = Label(self, width=17, text="Downloaded href:", fg="#000000", font=("Open Sans", 14), anchor=W)
    self.display_downloaded_amount_anchor_label.grid(row=9, column=0, pady=10, padx=10, sticky=E)

    self.display_downloaded_amount_anchor = Label(self, width=10, text="0", fg="#000000", font=("Open Sans", 14, "bold"), anchor=CENTER)
    self.display_downloaded_amount_anchor.grid(row=10, column=0, pady=10, padx=10, sticky=E)

    self.display_downloaded_line = ttk.Separator(self, orient='horizontal')
    self.display_downloaded_line.grid(row=11, pady=10, padx=10, sticky=EW)


    # GET FIELD URL VALUE
    url = self.url_field.get()

    # SPLIT URL
    get_base_url = urlsplit(url)

    session = HTMLSession()

    get_url_session = session.get(url)

    # GET HTML "BODY" OF WEBSITE
    get_html_body = get_url_session.html.find('body', first=True)

    # FIND "ANCHOR" TAG
    get_files_tags = get_html_body.find('a')

    # DOWNLOADED IMAGES COUNTER - FOR "display_downloaded_amount_images" FIELD
    downloaded_anchor_counter = 0

    # ADD FIELDS TO VARIABLES
    amount_of_anchor_on_website_label = self.display_total_amount_anchor_label
    amount_of_anchor_downloaded_label = self.display_downloaded_amount_anchor_label
    amount_of_anchor_on_website = self.display_total_amount_anchor
    amount_of_anchor_downloaded = self.display_downloaded_amount_anchor

    with open(directory_path + "/" + 'file_path.txt', 'w') as file:

      # LOOP THROUGH ALL IMAGES
      for ids in range(len(get_files_tags)):

        if ("href" in get_files_tags[ids].attrs):
          get_data_src = get_files_tags[ids].attrs["href"]

          # INCREASE COUNTER BY ONE - AFTER EACH LOOP
          downloaded_anchor_counter += 1
        else:
          print("skip - no href")
          continue


        if (self.save_link_int_var.get() == 1):
          file.write(get_data_src + "\n")
        else:
          if (ids == 0):
            file.write('["' + get_data_src + '", ')
          elif (ids == (len(get_files_tags) - 1)):
            file.write('"' + get_data_src + '"]')
          else:
            file.write('"' + get_data_src + '", ')


        if (ids == 0):
          amount_of_anchor_on_website['text'] = 0 # ADD VALUE 0 TO "TEXT"
          amount_of_anchor_on_website.update_idletasks() # UPDATE LABEL "TEXT" VALUE

          amount_of_anchor_downloaded['text'] = 0 # ADD VALUE 0 TO "TEXT"
          amount_of_anchor_downloaded.update_idletasks() # UPDATE LABEL "TEXT" VALUE

          time.sleep(0.2) # WAIT FOR 2 MILLISECOND
        # END IF 0

        amount_of_anchor_on_website['text'] = len(get_files_tags) # ADD AMOUNT OF AVAILABLE IMAGES TO "TEXT"
        amount_of_anchor_on_website.update_idletasks() # UPDATE LABEL "TEXT" VALUE

        amount_of_anchor_downloaded['text'] = downloaded_anchor_counter # ADD AMOUNT OF DOWNLOADED IMAGES TO "TEXT"
        amount_of_anchor_downloaded.update_idletasks() # UPDATE LABEL "TEXT" VALUE

        time.sleep(0.2) # WAIT FOR 2 MILLISECOND

        # IF ALL POSSIBLE IMAGES HAVE BEEN DOWNLOADED DISPLAY MESSAGE
        if (ids == (len(get_files_tags) - 1)):
          messagebox.showinfo(title="Info!", message="ALL ANCHOR HAVE BEEN DOWNLOADED")
          amount_of_anchor_on_website_label.destroy()
          amount_of_anchor_downloaded_label.destroy()
          amount_of_anchor_on_website.destroy()
          amount_of_anchor_downloaded.destroy()
          self.display_downloaded_line.destroy()
        else:
          # IF FILE TYPE IS NOT AN IMAGE FILE TYPE AND IT'S NOT THE LAST FILE - SKIP THIS AND LOOP THROUGH NEXT FILE
          continue



  def download_all_files(self, directory_path):

    # FIELDS - DISPLAY DOWNLOAD INFORMATION - "AMOUNT OF AVAILABLE FILES" AND "AMOUNT OF DOWNLOADED FILES"
    self.display_total_amount_files_label = Label(self, width=12, text="Total hrefs:", fg="#000000", font=("Open Sans", 14), anchor=W)
    self.display_total_amount_files_label.grid(row=9, column=0, pady=10, padx=10, sticky=W)

    self.display_total_amount_files = Label(self, width=10, text="0", fg="#000000", font=("Open Sans", 14, "bold"), anchor=CENTER)
    self.display_total_amount_files.grid(row=10, column=0, pady=10, padx=10, sticky=W)

    self.display_downloaded_amount_files_label = Label(self, width=17, text="Downloaded files:", fg="#000000", font=("Open Sans", 14), anchor=W)
    self.display_downloaded_amount_files_label.grid(row=9, column=0, pady=10, padx=10, sticky=E)

    self.display_downloaded_amount_files = Label(self, width=10, text="0", fg="#000000", font=("Open Sans", 14, "bold"), anchor=CENTER)
    self.display_downloaded_amount_files.grid(row=10, column=0, pady=10, padx=10, sticky=E)

    self.display_downloaded_line = ttk.Separator(self, orient='horizontal')
    self.display_downloaded_line.grid(row=11, pady=10, padx=10, sticky=EW)


    # GET FIELD URL VALUE
    url = self.url_field.get()

    # SPLIT URL
    get_base_url = urlsplit(url)

    session = HTMLSession()

    get_url_session = session.get(url)

    # GET HTML "BODY" OF WEBSITE
    get_html_body = get_url_session.html.find('body', first=True)

    # FIND "ANCHOR" TAG
    get_files_tags = get_html_body.find('a')

    # DOWNLOADED IMAGES COUNTER - FOR "display_downloaded_amount_images" FIELD
    downloaded_files_counter = 0

    # ADD FIELDS TO VARIABLES
    amount_of_files_on_website_label = self.display_total_amount_files_label
    amount_of_files_downloaded_label = self.display_downloaded_amount_files_label
    amount_of_files_on_website = self.display_total_amount_files
    amount_of_files_downloaded = self.display_downloaded_amount_files


    # LOOP THROUGH ALL IMAGES
    for ids in range(len(get_files_tags)):

      if ("href" in get_files_tags[ids].attrs):
        get_data_src = get_files_tags[ids].attrs["href"]
      else:
        print("skip - no href")
        continue


      if (get_data_src.split('/')[-1]):
        # GET FILE NAME AND FILE TYPE - EXAMPLE ".jpg"
        get_end_of_file = get_data_src.split('/')[-1]
      else:
        get_end_of_file = get_data_src


      ## IF PARAM AFTER IMAGE TAG - REMOVE ? AND EVERYTHING AFTER IT
      if ("?" in get_end_of_file):
        file_name = get_end_of_file.split("?")[0]
      else:
        file_name = get_end_of_file


      # SPLIT FILE PATH - AND FILE TYPE
      file_path, file_type = os.path.splitext(file_name)

      # CHECK IF FILE TYPE EQUALS AN IMAGE FILE TYPE
      a_string = file_name
      matches = [".pdf", ".doc", ".docx", ".odt", ".rtf", ".tex", ".txt", ".wpd", ".xls", ".ods", ".xlsm", ".xlsx", ".key", ".odp", ".pps", ".ppt", ".pptx", ".ai", ".psd", ".zip", ".tar", ".7z", ".rar", ".tar.gz"]

      # CHECK IF FILE TYPE EQUALS AN IMAGE FILE TYPE
      if any(x in a_string for x in matches):

        # INCREASE COUNTER BY ONE - AFTER EACH LOOP
        downloaded_files_counter += 1


        # -----------------------------------------------------------
        # CHECK IF "IMG SRC" URL IS AN EXTERNAL OR AN INTERNAL URL
        # -----------------------------------------------------------

        # CHECK IF URL IS EXTERNAL
        if (("https://" or "http://") in get_data_src):

          # COMBINE "DOWNLOAD PATH" AND "FILE NAME" - TO "download_destination"
          download_destination = os.path.join(directory_path, "File_" + str(ids) + "_" + file_name)


          if ((" ") in get_data_src):
            remove_whitespace_url = get_data_src.replace(" ", "%20")
          else:
            remove_whitespace_url = get_data_src


          # TRY TO DOWNLOAD THE IMAGE FILE
          try:
            # GET REQUEST CODE LIKE: 200 (OK) - 404 (PAGE NOT FOUND) - AND MORE
            #print("Get Code ", urllib.request.urlopen(get_data_src).getcode())

            urllib.request.urlretrieve(remove_whitespace_url, download_destination)

          except: # IF FILE COULDN'T BE DOWNLOADED - TRY NEXT ONE
            print("Error - File has not been downloaded! ", urllib.request.urlopen(get_data_src).getcode())

        else: # ELSE IS INTERNAL

          # CHECK PATH OF URL
          internal_file_src = ""

          if (get_data_src[:1] == "/"):
            get_data_src = get_data_src[1:]


          if ((" ") in get_data_src):
            remove_whitespace_url = get_data_src.replace(" ", "%20")
          else:
            remove_whitespace_url = get_data_src


          internal_file_src = get_base_url.scheme + "://" + get_base_url.netloc + "/" + remove_whitespace_url

          # COMBINE "DOWNLOAD PATH" AND "FILE NAME" - TO "download_destination"
          download_destination = os.path.join(directory_path, "Image_" + str(ids) + "_" + file_name)

          # TRY TO DOWNLOAD THE IMAGE FILE
          try:
            # GET REQUEST CODE LIKE: 200 (OK) - 404 (PAGE NOT FOUND) - AND MORE
            #print("Get Code ", urllib.request.urlopen(get_data_src).getcode())

            urllib.request.urlretrieve(internal_file_src, download_destination)

          except: # IF FILE COULDN'T BE DOWNLOADED - TRY NEXT ONE
            print("Error - File has not been downloaded! ", urllib.request.urlopen(get_data_src).getcode())

        # -----------------------------------------------------------
        # END CHECK
        # -----------------------------------------------------------


        if (ids == 0):
          amount_of_files_on_website['text'] = 0 # ADD VALUE 0 TO "TEXT"
          amount_of_files_on_website.update_idletasks() # UPDATE LABEL "TEXT" VALUE

          amount_of_files_downloaded['text'] = 0 # ADD VALUE 0 TO "TEXT"
          amount_of_files_downloaded.update_idletasks() # UPDATE LABEL "TEXT" VALUE

          time.sleep(0.2) # WAIT FOR 2 MILLISECOND
        # END IF 0

        amount_of_files_on_website['text'] = len(get_files_tags) # ADD AMOUNT OF AVAILABLE IMAGES TO "TEXT"
        amount_of_files_on_website.update_idletasks() # UPDATE LABEL "TEXT" VALUE

        amount_of_files_downloaded['text'] = downloaded_files_counter # ADD AMOUNT OF DOWNLOADED IMAGES TO "TEXT"
        amount_of_files_downloaded.update_idletasks() # UPDATE LABEL "TEXT" VALUE

        time.sleep(0.2) # WAIT FOR 2 MILLISECOND

        # IF ALL POSSIBLE IMAGES HAVE BEEN DOWNLOADED DISPLAY MESSAGE
        if (ids == (len(get_files_tags) - 1)):
          messagebox.showinfo(title="Info!", message="ALL FILES HAVE BEEN DOWNLOADED")
          amount_of_files_on_website_label.destroy()
          amount_of_files_downloaded_label.destroy()
          amount_of_files_on_website.destroy()
          amount_of_files_downloaded.destroy()
          self.display_downloaded_line.destroy()
        else:
          # IF FILE TYPE IS NOT AN FILE TYPE AND IT'S NOT THE LAST FILE - SKIP THIS AND LOOP THROUGH NEXT FILE
          continue
#
#

      elif (("base64") in file_name): # IMPORTANT - IF IMAGE FILE EQUALS "base64" SKIP IT

        if (ids == (len(get_files_tags) - 1)):
          messagebox.showinfo(title="Info!", message="ALL FILES HAVE BEEN DOWNLOADED")
          amount_of_files_on_website_label.destroy()
          amount_of_files_downloaded_label.destroy()
          amount_of_files_on_website.destroy()
          amount_of_files_downloaded.destroy()
          self.display_downloaded_line.destroy()
        else:
          # IF FILE TYPE IS NOT AN FILE TYPE AND IT'S NOT THE LAST FILE - SKIP THIS AND LOOP THROUGH NEXT FILE
          continue



      elif ((".html") in file_name): # IMPORTANT - IF FILE EQUALS "html" SKIP IT

        if (ids == (len(get_files_tags) - 1)):
          messagebox.showinfo(title="Info!", message="ALL FILES HAVE BEEN DOWNLOADED")
          amount_of_files_on_website_label.destroy()
          amount_of_files_downloaded_label.destroy()
          amount_of_files_on_website.destroy()
          amount_of_files_downloaded.destroy()
          self.display_downloaded_line.destroy()
        else:
          # IF FILE TYPE IS NOT AN FILE TYPE AND IT'S NOT THE LAST FILE - SKIP THIS AND LOOP THROUGH NEXT FILE
          continue


      else:

        if (ids == (len(get_files_tags) - 1)):
          messagebox.showinfo(title="Info!", message="ALL FILES HAVE BEEN DOWNLOADED")
          amount_of_files_on_website_label.destroy()
          amount_of_files_downloaded_label.destroy()
          amount_of_files_on_website.destroy()
          amount_of_files_downloaded.destroy()
          self.display_downloaded_line.destroy()
        else:
          # IF FILE TYPE IS NOT AN FILE TYPE AND IT'S NOT THE LAST FILE - SKIP THIS AND LOOP THROUGH NEXT FILE
          continue



  def about_software(self):
    messagebox.showinfo(title="About", message='Version: 1.0.0\n\nDeveloper: nebaru\nWebsite: wdtools.org\nContact: hello@wdtools.org')



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
