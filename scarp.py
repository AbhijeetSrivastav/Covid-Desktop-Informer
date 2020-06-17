import tkinter as tk
from tkinter import messagebox

import bs4
import requests
from PIL import ImageTk, Image

# Increase The DPI For High End Displays On Windows Machine
try:
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)
except Exception as e:
    pass

"""Help:
    If the app throws find_all not found error then just check out the class of the row from the scripted table ,
    it must have been updated on the website due to update of the website architecture"""

# Constant Parameters
URL = 'https://news.google.com/covid19/map?hl=en-IN&gl=IN&ceid=IN%3Aen&mid=%2Fm%2F03rk0'
DETAIL_CATEGORY = {'Confirmed': 0, 'Case Per Million': 0, 'Recovered': 0, 'Deaths': 0}

# Color Scheme For Styling"""
BACKGROUND_FRAME_SUB = '#B0BEC5'
BACKGROUND_DARK = '#000000'
BACKGROUND_FRAME_MAIN = '#00BCD4'
global FLAG


# noinspection PyAttributeOutsideInit,PyShadowingNames
class Data(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('COVID UPDATER')
        self.iconbitmap('contamination.ico')
        self.config(bg=BACKGROUND_DARK)
        self.resizable(False, False)

        # Parent Frame
        self.container = tk.Frame(self, relief='groove', borderwidth=5, background=BACKGROUND_DARK)
        self.container.grid(row=0, column=0, sticky='NSEW', padx=8, pady=8)

        # MiscImage Frame
        self.misc_image_container = tk.Frame(self, bg=BACKGROUND_FRAME_SUB, relief='raised', borderwidth=10)
        self.misc_image_container.grid(row=0, column=0, sticky='NSEW', padx=8, pady=8)

        # World Frame
        self.world_container = tk.Frame(self, relief='ridge', bg=BACKGROUND_FRAME_SUB, borderwidth=10)
        self.world_container.grid(row=0, column=1, sticky='NSEW', padx=8, pady=8)

        # India Frame
        self.india_container = tk.Frame(self, relief='ridge', bg=BACKGROUND_FRAME_SUB, borderwidth=10)
        self.india_container.grid(row=0, column=2, sticky='NSEW', padx=10, pady=10)

        # MiscOption Frame
        self.misc_option_container = tk.Frame(self, relief='ridge', bg=BACKGROUND_FRAME_SUB, borderwidth=10)
        self.misc_option_container.grid(row=1, column=1, padx=0, pady=10, columnspan=2)

        # Message Label
        self.message = tk.Label(self, text='Stay Home ! Stay Safe!', font=('Consolas', 22), relief='raised',
                                borderwidth=5, background=BACKGROUND_DARK, foreground='yellow', anchor='center')
        self.message.grid(row=1, column=0, ipadx=6, ipady=6, padx=6, pady=10)

        self.columnconfigure(0, weight=2)
        self.rowconfigure(0, weight=2)

        # Calling Methods
        self.GetStats()
        self.World()
        self.India()
        self.Miscalaneous()
        self.MiscOption()

    def Miscalaneous(self):

        self.image = Image.open('contamination_main.jpg').resize((300, 300))
        self.collected_image = ImageTk.PhotoImage(self.image)

        Center_image = tk.Label(self.misc_image_container, image=self.collected_image, justify='center')
        Center_image.grid(row=0, column=0, padx=30, pady=10, ipadx=5, ipady=5)

        self.image_tech = Image.open('logo.png').resize((150, 150))
        self.collected_image_tech = ImageTk.PhotoImage(self.image_tech)

        Center_image = tk.Label(self.misc_image_container, image=self.collected_image_tech, justify='center')
        Center_image.grid(row=0, column=1, padx=20)

    def MiscOption(self):

        def Refresh():
            self.World()
            self.India()

        def About():
            messagebox.showinfo(
                title='About', message='OWNER = x\n'
                                       'AUTHOR = ABHIJEET SRIVASTAV\n'
                                       'Youtube = xyzz\n'
                                       'LICENSE = null\n'
                                       'VERSION = 1.0\n'
            )

        def Support():
            messagebox.showinfo(title='Contact', message='In the case app doesnt run properly:\n'
                                                         'Contact us at: xyz@gmail.com\n'
                                                         'Follow us on our social media accounts:\n'
                                                         'GitHub = xyz\n'
                                                         'IG = xyz\n'
                                                         'Website = xyz\n'
                                )

        def Donate():
            messagebox.showinfo(title='Social',
                                message='Donate to make this app better and help us to grow and make more projects:\n'
                                        'Google Pay: xyz\n'
                                        'PhonePe: xyz\n')

        self.refresh_image = Image.open('refresh.png').resize((50, 50))
        self.refresh_image_cache = ImageTk.PhotoImage(self.refresh_image)
        Button_refresh = tk.Button(self.misc_option_container, image=self.refresh_image_cache, command=Refresh)
        Button_refresh.grid(column=1)

        self.about_image = Image.open('about.png').resize((50, 50))
        self.about_image_cache = ImageTk.PhotoImage(self.about_image)
        Button_about = tk.Button(self.misc_option_container, image=self.about_image_cache, command=About)
        Button_about.grid(column=2)

        self.support_image = Image.open('support.png').resize((50, 50))
        self.support_image_cache = ImageTk.PhotoImage(self.support_image)
        Button_support = tk.Button(self.misc_option_container, image=self.support_image_cache, command=Support)
        Button_support.grid(column=3)

        self.donate_image = Image.open('donate.png').resize((50, 50))
        self.donate_image_cache = ImageTk.PhotoImage(self.donate_image)
        Button_donate = tk.Button(self.misc_option_container, image=self.donate_image_cache, command=Donate)
        Button_donate.grid(column=4)

        for child in self.misc_option_container.winfo_children():
            child.grid_configure(row=0, padx=15, pady=10)
            child.config(relief='raised', justify='center')

    def GetStats(self):
        def GetHtmlData(url):
            data = requests.get(url)
            return data

        global bs
        try:
            # th2 = threading.Thread(self.Load())
            # th2.start()

            # Establishing Connection
            html_data = GetHtmlData(URL)
            bs = bs4.BeautifulSoup(html_data.text, 'html.parser')

            # Showing Connection Establishment Dialogue
            messagebox.showinfo(title='Connecting...', message='Establishing Connection...\n'
                                                               'Fetching Data...\n'
                                                               'Wait For A Minute')


        except Exception as ConnectionError:
            # Showing Connection Failure Dialogue
            error_dialogue = messagebox.showerror(title='Connection Failure!',
                                                  message='Oops! Network Connection Not Established! Please Connect To Network')

    def World(self):
        # Reaching the target element
        scraped_data = bs.find('tbody', class_='ppcUXd').find('tr', class_='sgXwHf wdLSAe Iryyw').find_all('td',
                                                                                                           class_='l3HOY')

        # Empty list to hold the data
        details = []

        # Loop to populate the details list with data
        for categorical_detail in scraped_data:
            details.append(categorical_detail.get_text())

        # Updating the values in dictionary with the data in the list
        DETAIL_CATEGORY.update(zip(DETAIL_CATEGORY, details))

        # Storing Value Into Variables
        self.world_confirmed = f"Confirmed : {DETAIL_CATEGORY['Confirmed']}"
        self.world_case_million = f"Case Per Million: {DETAIL_CATEGORY['Case Per Million']}"
        self.world_recovered = f"Recovered: {DETAIL_CATEGORY['Recovered']}"
        self.world_deaths = f"Deaths: {DETAIL_CATEGORY['Deaths']}"

        world_label = tk.Label(self.world_container, text='World :', relief='raised', font=("Times", "16"))
        world_label.grid(row=0, column=0, padx=8, pady=8, ipadx=5, ipady=5)

        world_confirmed = tk.Label(self.world_container, text=self.world_confirmed, relief='sunken')
        world_confirmed.grid(row=1, column=0)

        world_case_million = tk.Label(self.world_container, text=self.world_case_million, relief='sunken')
        world_case_million.grid(row=2, column=0)

        world_recovered = tk.Label(self.world_container, text=self.world_recovered, relief='sunken')
        world_recovered.grid(row=3, column=0)

        world_deaths = tk.Label(self.world_container, text=self.world_deaths, relief='sunken')
        world_deaths.grid(row=4, column=0)

        for child in self.world_container.winfo_children():
            child.grid_configure(ipadx=5, ipady=5, padx=8, pady=8)
            child.configure(borderwidth=5, justify='center')

    def India(self):
        # Reaching the target element
        scraped_data = bs.find('tbody', class_='ppcUXd').find('tr', class_='sgXwHf wdLSAe ROuVee').find_all('td',
                                                                                                            class_='l3HOY')

        # Empty list to hold the data
        details = []

        # Loop to populate the details list with data
        for categorical_detail in scraped_data:
            details.append(categorical_detail.get_text())

        # Updating the values in dictionary with the data in the list
        DETAIL_CATEGORY.update(zip(DETAIL_CATEGORY, details))

        self.india_confirmed = f"Confirmed : {DETAIL_CATEGORY['Confirmed']}"
        self.india_case_million = f"Case Per Million: {DETAIL_CATEGORY['Case Per Million']}"
        self.india_recovered = f"Recovered: {DETAIL_CATEGORY['Recovered']}"
        self.india_deaths = f"Deaths: {DETAIL_CATEGORY['Deaths']}"

        india_label = tk.Label(self.india_container, text='India :', relief='raised', font=("Times", "16"))
        india_label.grid(row=0, column=0)

        india_confirmed = tk.Label(self.india_container, text=self.india_confirmed, relief='sunken')
        india_confirmed.grid(row=1, column=0)

        india_case_million = tk.Label(self.india_container, text=self.india_case_million, relief='sunken')
        india_case_million.grid(row=2, column=0)

        india_recovered = tk.Label(self.india_container, text=self.india_recovered, relief='sunken')
        india_recovered.grid(row=3, column=0)

        india_deaths = tk.Label(self.india_container, text=self.india_deaths, relief='sunken')
        india_deaths.grid(row=4, column=0)

        for child in self.india_container.winfo_children():
            child.grid_configure(ipadx=5, ipady=5, padx=8, pady=8)
            child.configure(borderwidth=5, justify='center')


if __name__ == '__main__':
    data_app = Data()

    data_app.mainloop()
