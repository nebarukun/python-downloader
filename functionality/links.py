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


class LinkDownloader(object):

  def __init__(self, directory_path):

    # FIELDS - DISPLAY DOWNLOAD INFORMATION - "AMOUNT OF AVAILABLE ANCHORS" AND "AMOUNT OF SAVED ANCHORS TEXT"
    self.display_total_amount_anchor_label = Label(self, width=12, text="Total:", fg="#000000", font=("Open Sans", 14), anchor=W)
    self.display_total_amount_anchor_label.grid(row=9, column=0, pady=10, padx=10, sticky=W)

    self.display_total_amount_anchor = Label(self, width=10, text="0", fg="#000000", font=("Open Sans", 14, "bold"), anchor=CENTER)
    self.display_total_amount_anchor.grid(row=10, column=0, pady=10, padx=10, sticky=W)

    self.display_downloaded_amount_anchor_label = Label(self, width=17, text="Downloaded:", fg="#000000", font=("Open Sans", 14), anchor=W)
    self.display_downloaded_amount_anchor_label.grid(row=9, column=0, pady=10, padx=10, sticky=E)

    self.display_downloaded_amount_anchor = Label(self, width=10, text="0", fg="#000000", font=("Open Sans", 14, "bold"), anchor=CENTER)
    self.display_downloaded_amount_anchor.grid(row=10, column=0, pady=10, padx=10, sticky=E)

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
    downloaded_anchor_counter = 0

    # ADD FIELDS TO VARIABLES
    amount_of_anchor_on_website_label = self.display_total_amount_anchor_label
    amount_of_anchor_downloaded_label = self.display_downloaded_amount_anchor_label
    amount_of_anchor_on_website = self.display_total_amount_anchor
    amount_of_anchor_downloaded = self.display_downloaded_amount_anchor

    with open(directory_path + '/file.txt', 'w') as file:

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
          messagebox.showinfo(title="Info!", message="All Links have been downloaded")
          amount_of_anchor_on_website_label.destroy()
          amount_of_anchor_downloaded_label.destroy()
          amount_of_anchor_on_website.destroy()
          amount_of_anchor_downloaded.destroy()
          self.display_downloaded_line.destroy()
        else:
          # IF FILE TYPE IS NOT AN IMAGE FILE TYPE AND IT'S NOT THE LAST FILE - SKIP THIS AND LOOP THROUGH NEXT FILE
          continue
