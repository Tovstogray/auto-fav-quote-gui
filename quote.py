import pathlib
import proxyscrape
import tkvalidate
import tkinter as tk
import random
import re
import pandas as pd
import time
import urllib.request
from selenium import webdriver
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from tkinter import messagebox

FONT_HEADS = ('arial', 14, 'bold')
FONT_MAIN = ('arial', 8)
domains = ('@gmail.com', '@yahoo.com', '@hotmail.com', '@aol.com',
           '@hotmail.co.uk', '@hotmail.fr', '@msn.com', '@yahoo.fr',
           '@wanadoo.fr', '@orange.fr', '@comcast.net', '@yahoo.co.uk',
           '@yahoo.com.br', '@yahoo.com.in', '@live.com')


class App(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.grid()

        # TopSide Block

        self.name_label = tk.Label(text='Name', font=FONT_MAIN, justify='left')
        self.name_label.grid(row=0, column=0, sticky='w')
        self.username_label = tk.Label(text='Username', font=FONT_MAIN, justify='left')
        self.username_label.grid(row=1, column=0, sticky='w')
        self.email_label = tk.Label(text='E-mail', font=FONT_MAIN, justify='left')
        self.email_label.grid(row=2, column=0, sticky='w')

        self.name_example_label = tk.Label()
        self.name_example_label.grid(row=0, column=1, sticky='w')
        self.username_example_label = tk.Label()
        self.username_example_label.grid(row=1, column=1, sticky='w')
        self.email_example_label = tk.Label()
        self.email_example_label.grid(row=2, column=1, sticky='w')

        # Medium Space Block

        self.space_block = tk.Label(text=' ')
        self.space_block.grid(row=3, columnspan=2)

        # Bottom Side Block

        self.number_favs_label = tk.Label(text='Number of favs to add', font=FONT_MAIN, justify='left')
        self.number_favs_label.grid(row=4, column=0, sticky='w')
        self.quote_url_label = tk.Label(text='Quote URL', font=FONT_MAIN, justify='left')
        self.quote_url_label.grid(row=5, column=0, sticky='w')
        self.script_time_label = tk.Label(text='Script time', font=FONT_MAIN, justify='left')
        self.script_time_label.grid(row=6, column=0, sticky='w')

        self.entry_favs = tk.StringVar()
        self.entry_favs.trace('w', self.check)
        self.number_favs_entry = tk.Entry(width=50, textvariable=self.entry_favs)
        self.number_favs_entry.grid(row=4, column=1, sticky='w')
        tkvalidate.int_validate(self.number_favs_entry, from_=1, to=500)
        self.entry_url = tk.StringVar()
        self.entry_url.trace('w', self.check)
        self.quote_url_entry = tk.Entry(width=50, textvariable=self.entry_url)
        self.quote_url_entry.grid(row=5, column=1, sticky='w')
        self.entry_time = tk.StringVar()
        self.entry_time.trace('w', self.check)
        self.script_time_entry = tk.Entry(width=50, textvariable=self.entry_time)
        self.script_time_entry.grid(row=6, column=1, sticky='w')
        tkvalidate.int_validate(self.script_time_entry, from_=1, to=1440)

        self.btn_generate = tk.Button(text='Generate', command=self.btn_gen_on_press, height=1, width=10)
        self.btn_generate.grid(row=7, column=0, sticky='w')

        self.btn_start = tk.Button(text='Start', height=1, width=10, command=self.btn_start_on_press)
        self.btn_start.config(state='disabled')
        self.btn_start.grid(row=8, column=0, sticky='w')

        self.btn_help = tk.Button(text='Help', height=1, width=10, command=self.btn_help_on_press)
        self.btn_help.grid(row=9, column=0, sticky='w')

    def btn_gen_on_press(self):

        # First & Second name Generation

        html_page = urllib.request.urlopen('https://www.babycenter.com/top-baby-names')
        soup = BeautifulSoup(html_page, "html.parser")
        table_tag = soup.findAll('table', {'class': 'contentTable fitsOnScreen'})
        first = []
        usernames = []

        for link in table_tag:
            names = link.text
            first = (" ".join(re.findall("[a-zA-Z]+", names)))

        random_first = random.choice(list(map(str, first.split())))

        df = pd.read_excel('last.xlsx', sheet_name='RANDOMIZE THESE LAST NAMES', usecols='A', index_col=None)
        second_names = df.to_string()
        seconds = (" ".join(re.findall("[a-zA-Z]+", second_names)))
        random_second = random.choice(list(map(str, seconds.split())))

        # Username Generator

        html_name_gen = urllib.request.urlopen('http://namegenerators.org/random-username-generator/')
        soup_name_gen = BeautifulSoup(html_name_gen, 'html.parser')
        divs = soup_name_gen.find_all('div', class_='bizname')
        for div in divs:
            usernames.append(div.text)
        self.username = random.choice(usernames).lower()

        # Name & E-mail

        self.name = f'{random_first} {random_second}'
        email_name_first = f'{random_first[:3]}{random.randint(10, 100)}{random_second[-3:]}'.lower()
        email_name_second = f'{random_first}_{random_second[0]}{random.randint(1950, 2000)}'
        email_name_third = f'{random_first[0]}.{random_second}{random.randint(10, 100)}'
        email_name_fourth = f'{self.username[:3]}_{random_second}'
        email_name = [email_name_first, email_name_second, email_name_third, email_name_fourth]
        self.email = f'{random.choice(email_name)}{random.choice(domains)}'.lower()

        self.name_example_label.configure(text=self.name)
        self.username_example_label.configure(text=self.username)
        self.email_example_label.configure(text=self.email)

    def btn_start_on_press(self):
        i = 0
        while i < int(self.entry_favs.get()):

            # Web Driver + Proxy Setup

            options = webdriver.FirefoxOptions()
            useragent = UserAgent()
            options.set_preference('general.useragent.override', useragent.random)
            options.add_argument('--headless')

            collector = proxyscrape.create_collector(str(i), 'http')
            proxy = collector.get_proxy()

            ip = proxy.host
            port = proxy.port
            options.set_preference('network.proxy.type', 1)
            options.set_preference('network.proxy.http', ip)
            options.set_preference('network.proxy.http_port', port)
            options.set_preference('network.proxy.https', ip)
            options.set_preference('network.proxy.https_port', port)
            options.set_preference('network.proxy.ssl', ip)
            options.set_preference('network.proxy.ssl_port', port)

            self.btn_gen_on_press()

            i += 1
            driver = webdriver.Firefox(executable_path=str(pathlib.Path(__file__).parent.absolute()) + r'/geckodriver.exe',
                                       options=options)
            print(proxy)

            driver.get(self.entry_url.get())
            time.sleep(1)

            btn_fav = driver.find_element_by_xpath('//*[@id="author-rate-btn"]')
            btn_fav.click()

            time.sleep(2)
            name_input = driver.find_element_by_xpath('//*[@id="fld-rname"]')
            name_input.send_keys(self.name)

            email_input = driver.find_element_by_xpath('//*[@id="fld-uemail"]')
            email_input.send_keys(self.email)

            username_input = driver.find_element_by_xpath('//*[@id="fld-uname"]')
            username_input.send_keys(self.username)

            btn_join = driver.find_element_by_xpath('//*[@id="modal-signup-frm"]/div/section[4]/div/p/button')
            btn_join.click()

            high = int(self.entry_time.get()) / int(self.entry_favs.get())
            low = float(high/2)

            time_in_between_minutes = random.uniform(float(low), float(high))
            time_in_between_seconds = round(time_in_between_minutes, 2) * 60
            time.sleep(time_in_between_seconds)

            driver.close()
        messagebox.showinfo('Done', 'Successfully added the right amount of favs')

    def btn_help_on_press(self):
        messagebox.showinfo('Help', '[Generate] : Generate random example of name, username and e-mail\n\n'
                                    '[Start] : Starting script. All fields above required!\n\n'
                                    'Number of favs to add : The exact amount of favs to add, integer value '
                                    '(max = 500)\n'
                                    'Quote URL : URL which leads to the quote author\n'
                                    'Script time : The exact time of script working in minutes (max = 1440 min)\n')

    def check(self, *args):
        x = self.entry_favs.get()
        y = self.entry_url.get()
        z = self.entry_time.get()
        if x and y and z:
            self.btn_start.config(state='normal')
        else:
            self.btn_start.config(state='disabled')


root = tk.Tk()
root.title('Quotes Script')
root.resizable(False, False)
myapp = App(root)
myapp.mainloop()
