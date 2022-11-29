from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image
from urllib.parse import urlparse, urlsplit
from datetime import datetime
from requests_html import HTMLSession
from pytube import YouTube

import os
import re
import sys
import time
import requests
import webbrowser
import tkinter as tk
import urllib.request



class VideoDownloader(object):

  def __init__(self, directory_path):

    self.progress_bar_status = Label(self, width=5, text="Video:", fg="#000000", font=("Open Sans", 14))
    self.progress_bar_status.grid(row=9, column=0, pady=10, padx=10, sticky=W)

    self.progress_bar = Label(self, width=30, text="", fg="#000000", font=("Open Sans", 14, "bold"), anchor=CENTER)
    self.progress_bar.grid(row=10, column=0, pady=10, padx=10, sticky=W)

    self.progress_bar['text'] = 'Loading...'

    self.display_downloaded_line = ttk.Separator(self, orient='horizontal')
    self.display_downloaded_line.grid(row=11, column=0, columnspan=2, pady=10, padx=10, sticky=EW)

    url = self.url_field.get()

    progress_bar = self.progress_bar

    if ("youtube.com" in url):

      get_video = YouTube(url)

      sort_video_resolutions = get_video.streams.filter(progressive=True, subtype='mp4').order_by('resolution').desc()

      get_best_resolution = sort_video_resolutions.first()

      progress_bar['text'] = 'Downloaded!'

      get_best_resolution.download(directory_path, get_video.title)

      messagebox.showinfo(title="Warning!", message='Video downloaded.')

      self.progress_bar_status.destroy()
      progress_bar.destroy()
      self.display_downloaded_line.destroy()

    else:

      self.progress_bar['text'] = 'Error! Invalid YouTube URL.'

      messagebox.showinfo(title="Warning!", message='Invalid YouTube URL.')
