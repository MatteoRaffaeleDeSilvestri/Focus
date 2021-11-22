import logging
import webbrowser
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import font as tkFont
import cv2
from cv2 import dnn_superres


class GUI:

    def __init__(self):

        # Set window propriety
        self.root = tk.Tk()
        self.root.title('Focus')
        self.root.resizable(False, False)

        # Set font style
        self.lato15 = tkFont.Font(family='Lato', size=15)
        self.lato15italic = tkFont.Font(family='Lato', size=15, slant='italic')
        
        self.open_file_path = tuple
        self.dest_folder = tuple
        self.model = tuple

        # UI structure
        tk.Label(self.root, font=self.lato15italic, fg='#242424', text='This program is mean to provide\na simple and easy-to-use tool for\nupscaling low quality ".png" file.\nPick up a photo, chose a folder\nand select an upscaling model\nand you are ready to go!\nNeed help?').grid(row=0, column=0, rowspan=4, padx=10, pady=0)
        tk.Button(self.root, font=self.lato15italic, fg='#242424', text='Documentation', width=10, command=lambda: webbrowser.open('https://github.com/MatteoRaffaeleDeSilvestri/Focus', new=0, autoraise=True)).grid(row=4, column=0, padx=10, pady=10)
        
        ttk.Separator(self.root, orient='vertical').grid(row=0, column=1, rowspan=5, pady=10, sticky='ns')

        tk.Button(self.root, font=self.lato15, fg='#242424', text='Select an image file', width=15, command=lambda: GUI.get_file(self)).grid(row=1, column=2, padx=10, pady=10)
        tk.Button(self.root, font=self.lato15, fg='#242424', text='Select a destination folder', width=19, command=lambda: GUI.get_folder(self)).grid(row=2, column=2, padx=10, pady=10)

        sources = ['EDSR x2', 'EDSR x3', 'EDSR x4',
                   'ESPCN x2', 'ESPCN x3', 'ESPCN x4',
                   'FSRCNN x2', 'FSRCNN x3', 'FSRCNN x4',
                   'LapSRN x2', 'LapSRN x4', 'LapSRN x8']

        self.model = tk.StringVar(self.root)
        self.model.set(sources[0])
        
        self.dropdown_menu = tk.OptionMenu(self.root, self.model, *sources)
        self.dropdown_menu.config(font=self.lato15, fg='#242424', width=15)
        self.dropdown_menu.grid(row=3, column=2, padx=10, pady=10)
        
        tk.Button(self.root, font=self.lato15, fg='#242424', text='Upscale', width=10, state='disabled', command=lambda: GUI.upscaler(self)).grid(row=4, column=2, padx=10, pady=10)

        # Start main loop (GUI)
        self.root.mainloop()

    def get_file(self):
        self.open_file_path = tk.filedialog.askopenfilename(filetypes=[("PNG file", '*.png')])
        GUI.abilitate(self)

    def get_folder(self):
        self.dest_folder = tk.filedialog.askdirectory()
        GUI.abilitate(self)

    def abilitate(self):
        
        tk.Button(self.root, font=self.lato15italic, fg='#242424', text='Documentation', width=10, command=lambda: webbrowser.open('https://github.com/MatteoRaffaeleDeSilvestri/Focus', new=0, autoraise=True)).grid(row=4, column=0, padx=10, pady=10)
            
        if type(self.open_file_path) == str and len(self.open_file_path) != 0:
            tk.Button(self.root, font=self.lato15, fg='#1f9100', activeforeground='#1f9100', text='Image selected', width=15, command=lambda: GUI.get_file(self)).grid(row=1, column=2, padx=10, pady=10)
            if type(self.dest_folder) == str and len(self.dest_folder) != 0:
                tk.Button(self.root, font=self.lato15, fg='#1f9100', activeforeground='#1f9100', text='Folder selected', width=19, command=lambda: GUI.get_folder(self)).grid(row=2, column=2, padx=10, pady=10)
                tk.Button(self.root, font=self.lato15, activebackground='#8fdb69', activeforeground='#242424', bg='#67cf34', fg='#242424', text='Upscale', width=10, state='normal', command=lambda: GUI.upscaler(self)).grid(row=4, column=2, padx=10, pady=10)
            else:
                tk.Button(self.root, font=self.lato15, fg='#242424', text='Select a destination folder', width=19, command=lambda: GUI.get_folder(self)).grid(row=2, column=2, padx=10, pady=10)
                tk.Button(self.root, font=self.lato15, fg='#242424', text='Upscale', width=10, state='disabled').grid(row=4, column=2, padx=10, pady=10)

        elif type(self.dest_folder) == str and len(self.dest_folder) != 0:
            tk.Button(self.root, font=self.lato15, fg='#1f9100', activeforeground='#1f9100', text='Folder selected', width=19, command=lambda: GUI.get_folder(self)).grid(row=2, column=2, padx=10, pady=10)
            if type(self.open_file_path) == str and len(self.open_file_path) != 0:
                tk.Button(self.root, font=self.lato15, fg='#1f9100', text='Image selcted', width=15, command=lambda: GUI.get_file(self)).grid(row=1, column=2, padx=10, pady=10)
                tk.Button(self.root, font=self.lato15, activebackground='#8fdb69', activeforeground='#242424', bg='#67cf34', fg='#242424', text='Upscale', width=10, state='normal', command=lambda: GUI.upscaler(self)).grid(row=4, column=2, padx=10, pady=10)
            else:
                tk.Button(self.root, font=self.lato15, fg='#242424', text='Select an image file', width=15, command=lambda: GUI.get_file(self)).grid(row=1, column=2, padx=10, pady=10)
                tk.Button(self.root, font=self.lato15, fg='#242424', text='Upscale', width=10, state='disabled').grid(row=4, column=2, padx=10, pady=10)

        else:
            tk.Button(self.root, font=self.lato15, fg='#242424', text='Select an image file', width=15, command=lambda: GUI.get_file(self)).grid(row=1, column=2, padx=10, pady=10)    
            tk.Button(self.root, font=self.lato15, fg='#242424', text='Select a destination folder', width=19, command=lambda: GUI.get_folder(self)).grid(row=2, column=2, padx=10, pady=10)
            tk.Button(self.root, font=self.lato15, fg='#242424', text='Upscale', width=10, state='disabled').grid(row=4, column=2, padx=10, pady=10)
        
        self.root.update()

    def upscaler(self):
        
        # Read selected model
        mod = self.model.get()

        # Freeze buttons
        tk.Button(self.root, font=self.lato15, fg='#242424', text='Image selected', width=15, state='disabled').grid(row=1, column=2, padx=10, pady=10)    
        tk.Button(self.root, font=self.lato15, fg='#242424', text='Folder selected', width=19, state='disabled').grid(row=2, column=2, padx=10, pady=10)
        self.dropdown_menu.configure(state='disabled')
        tk.Button(self.root, font=self.lato15italic, fg='#242424', text='Documentation', width=10, state='disabled').grid(row=4, column=0, padx=10, pady=10)        
        tk.Button(self.root, font=self.lato15, background='#ffffb3', fg='#242424', text='Upscaling...', width=10, state='disabled').grid(row=4, column=2, padx=10, pady=10)
        self.root.update()
        
        try:
        
            # Create an SR object
            sr = dnn_superres.DnnSuperResImpl_create()

            # Read image
            image = cv2.imread(self.open_file_path)

            # Read the desired model
            path = 'models/{}.pb'.format(mod.replace(' ', '_'))
            sr.readModel(path)

            # Set the desired model and scale to get correct pre and post processing
            selected_model = mod.lower().replace('-', ' ').split(' ')[0]
            for char in mod:
                if char.isnumeric():
                    factor = char
                    break

            sr.setModel(selected_model, int(factor))

            # Upscale the image
            result = sr.upsample(image)

            # Save the image
            cv2.imwrite('{}/{}'.format(self.dest_folder, selected_model + '_x' + factor + '_' + self.open_file_path.split(self.open_file_path[0])[len(self.open_file_path.split(self.open_file_path[0])) - 1]), result)

            # GUI reset
            self.open_file_path = None
            self.dest_folder = None
            self.dropdown_menu.configure(state='active')
            GUI.abilitate(self)

        except Exception as e:

            logging.basicConfig(filename='{}/{}'.format(self.dest_folder, 'error.log'), filemode='w', format='%(levelname)s - %(asctime)s\n%(message)s')
            logging.warning(e)

            print('ATTENTION: an error occurred. Check out the "error.log" file for more information.')

if __name__ == '__main__':

    GUI()
