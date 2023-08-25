import tkinter as tk
from tkinter import ttk
import re
import time
import requests
from bs4 import BeautifulSoup
from getNews import *
import webbrowser
import sys
from threading import Thread
sys.stdout.reconfigure(encoding='utf-8')
# methods for getting info
url = None
headlines = {}
window = None
button1 = None
button2 = None
news_headline = {}
news_link = None
index = 0
button_flag = 0
iterator = None
label3 = None

def dictionary_iterator(dictionary):
    global index
    items = list(dictionary.items()) if dictionary else []
    index = 0
    while True:
        if items:
            yield items[index]
            index = (index + 1) % len(items)
        else:
            yield None


def is_website_format(url):
    pattern = r"^(http|https)://([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})(/[a-zA-Z0-9_./-]*)?$"
    match = re.match(pattern, url)
    # If match is found, return True; otherwise, return False
    return bool(match)


def get_input():
    global headlines
    global window
    global button2
    global button_flag
    global iterator  # Define the iterator here
    url = entry.get()
    
    print(f'the url is:{url} and it is {is_website_format(url)}')
    if is_website_format(url):
        headlines = get_rss_headlines_with_links(url)  # Correctly update headlines
        print(headlines)
        button_flag += 1
        if button_flag == 1:
            # Initialize the iterator here
            iterator = dictionary_iterator(headlines)
            button2 = tk.Button(window, text='next news',
                                width=25, command=lambda: show_next_news())
            button2.pack()
            show_next_news()  # Show the first headline and link
            label2.pack()
            label3.pack()  # Place label2 and label3 under button1


def open_link(url):
    # Function to open the link in the default web browser

    webbrowser.open(url)


def show_next_news():
    global iterator  # Need to access the same iterator
    try:
        headline, link = next(iterator)
        # Display the headline and link using Text widget in label2
        label2.config(state=tk.NORMAL)
        label2.delete('1.0', tk.END)
        label2.insert(tk.END, f'{headline}:\n', 'headline')
        label2.insert(tk.END, link, 'link')
        label2.tag_config('headline', font=('Courier', 12, 'bold'))
        label2.tag_config('link', font=(
            'Courier', 12, 'underline'), foreground='blue')
        label2.config(state=tk.DISABLED)
        label2.tag_configure('center', justify='center')
        label2.tag_add('center', '1.0', 'end')

        # Bind the link click callback function
        label2.tag_bind('link', '<Button-1>', lambda event,
                        url=link: open_link(url))

    except StopIteration:
        # If the end of the dictionary is reached, restart the iterator
        iterator = dictionary_iterator(headlines)
        show_next_news()


# setting up a window
window = tk.Tk()
window.title('news app')
window.geometry("750x400")

# top labels
label = tk.Label(window, text='news reporter', font='Courier 22 bold')
label.pack()
# adding a sample loading button
custom_style = ttk.Style()
custom_style.theme_use('default')
custom_style.configure("cyan.Horizontal.TProgressbar", background='red')
progress_bar = ttk.Progressbar(
    window, mode='indeterminate', style='cyan.Horizontal.TProgressbar')
# loading_button=tk.Button(window,text='get me my news!',command=on_button_press)

# Variable to control the loading animation and label update
loading_flag = False


# input from user
entry = tk.Entry(window, width=40)
entry.focus_set()
entry.pack()
label3 = tk.Label(window, text='')


button1 = tk.Button(window, text='show news', width=25,
                    command=lambda: get_input())
button1.pack()


label2 = tk.Text(window, font=('Courier', 12),
                 wrap=tk.WORD, height=4, state=tk.DISABLED)


window.mainloop()
# https://www.bbc.com/news
