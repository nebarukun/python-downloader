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



class FileDownloader(object):


  def __init__(self, directory_path):


    # FIELDS - DISPLAY DOWNLOAD INFORMATION - "AMOUNT OF AVAILABLE FILES" AND "AMOUNT OF DOWNLOADED FILES"
    self.display_total_amount_files_label = Label(self, width=12, text="Total:", fg="#000000", font=("Open Sans", 14), anchor=W)
    self.display_total_amount_files_label.grid(row=9, column=0, pady=10, padx=10, sticky=W)

    self.display_total_amount_files = Label(self, width=10, text="0", fg="#000000", font=("Open Sans", 14, "bold"), anchor=CENTER)
    self.display_total_amount_files.grid(row=10, column=0, pady=10, padx=10, sticky=W)

    self.display_downloaded_amount_files_label = Label(self, width=17, text="Downloaded:", fg="#000000", font=("Open Sans", 14), anchor=W)
    self.display_downloaded_amount_files_label.grid(row=9, column=0, pady=10, padx=10, sticky=E)

    self.display_downloaded_amount_files = Label(self, width=10, text="0", fg="#000000", font=("Open Sans", 14, "bold"), anchor=CENTER)
    self.display_downloaded_amount_files.grid(row=10, column=0, pady=10, padx=10, sticky=E)

    self.display_downloaded_line = ttk.Separator(self, orient='horizontal')
    self.display_downloaded_line.grid(row=11, column=0, columnspan=2, pady=10, padx=10, sticky=EW)


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
