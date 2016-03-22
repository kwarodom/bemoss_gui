# -*- coding: utf-8 -*-
'''
Copyright (c) 2016, Virginia Tech
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
 following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following
disclaimer in the documentation and/or other materials provided with the distribution.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
The views and conclusions contained in the software and documentation are those of the authors and should not be
interpreted as representing official policies, either expressed or implied, of the FreeBSD Project.
This material was prepared as an account of work sponsored by an agency of the United States Government. Neither the
United States Government nor the United States Department of Energy, nor Virginia Tech, nor any of their employees,
nor any jurisdiction or organization that has cooperated in the development of these materials, makes any warranty,
express or implied, or assumes any legal liability or responsibility for the accuracy, completeness, or usefulness or
any information, apparatus, product, software, or process disclosed, or represents that its use would not infringe
privately owned rights.
Reference herein to any specific commercial product, process, or service by trade name, trademark, manufacturer, or
otherwise does not necessarily constitute or imply its endorsement, recommendation, favoring by the United States
Government or any agency thereof, or Virginia Tech - Advanced Research Institute. The views and opinions of authors
expressed herein do not necessarily state or reflect those of the United States Government or any agency thereof.
VIRGINIA TECH – ADVANCED RESEARCH INSTITUTE
under Contract DE-EE0006352
#__author__ = "BEMOSS Team"
#__credits__ = ""
#__version__ = "2.0"
#__maintainer__ = "BEMOSS Team"
#__email__ = "aribemoss@gmail.com"
#__website__ = "www.bemoss.org"
#__created__ = "2014-09-12 12:04:50"
#__lastUpdated__ = "2016-03-14 11:23:33"
'''


import Tkinter
import ttk
import os
import subprocess
import re
import tkMessageBox
import netifaces
from PIL import Image
import ImageTk
import shutil
import time
import volttronFunc

class GUI:
    def __init__(self):

        self.passwd = None
        self.do_update = False

        # current working directory
        self.cwd = os.getcwd()
        self.bemoss_dir = self.cwd.replace('bemoss_gui', 'bemoss_os/')

        img_path = self.find_img()
        self.logo = ImageTk.PhotoImage(Image.open(img_path).resize((350,125)))
        self.img = ttk.Label(root, image=self.logo, justify='center')
        self.img.pack(fill=Tkinter.Y, expand=True, padx=5, pady=30)
        # logoimage

        self.ip_addr = self.getIPs()
        self.ipframe = Tkinter.LabelFrame(root, text='Your IP address:')
        self.ip_label = Tkinter.Label(self.ipframe, text=self.ip_addr, font=('Courier', 12, 'bold'))
        self.ip_label.pack()
        self.ipframe.pack(fill=Tkinter.X, expand=True, padx=15)
        # IP

        self.button_quit = ttk.Button(root, text='Run BEMOSS', command=self.run_software)
        self.button_quit.pack(side=Tkinter.LEFT, fill=Tkinter.BOTH, expand=True, pady=15, padx=10)
        self.button_run = ttk.Button(root, text='Stop BEMOSS', command=self.stop_software)
        self.button_run.pack(side=Tkinter.LEFT, fill=Tkinter.BOTH, expand=True, pady=15, padx=10)
        self.button_adv = ttk.Button(root, text='Advanced Setting', command=self.adv_set)
        self.button_adv.pack(side=Tkinter.LEFT, fill=Tkinter.BOTH, expand=True, pady=15, padx=10)
        # buttons

    def find_img(self):
        cwd_path = os.getcwd()
        path = cwd_path + '/BEMOSS_logo.png'
        return path

    def getIPs(self):
        IPs = []
        ip_string = ''
        interfaces = netifaces.interfaces()
        for i in interfaces:
            if i == 'lo':
                continue
            iface = netifaces.ifaddresses(i).get(netifaces.AF_INET)
            if iface is not None:
                for j in iface:
                    IPs.append(j['addr'])
                    ip_string += str(j['addr'])
        return ip_string

    def detect_bemoss(self):
        cwd = os.getcwd()
        ui_path = cwd.replace('bemoss_gui','bemoss_web_ui')
        cassandra_path = cwd.replace('bemoss_gui','cassandra')
        env_path = cwd.replace('bemoss_gui','bemoss_os/env/bin')
        self.bemoss_installed = os.path.isdir(ui_path) and os.path.isdir(cassandra_path) and os.path.isdir(env_path)


    def run_software(self):
        self.detect_bemoss()
        if self.bemoss_installed is False:
            tmp = tkMessageBox.askokcancel(title='Please install BEMOSS at first',
                                           message='You computer does not have BEMOSS installed, do you want to install BEMOSS right now?',
                                           parent=root)
            if tmp is True:
                self.install_bemoss()
                return
            else:
                return
        self.run_bemoss()

    def stop_software(self):
        self.detect_bemoss()
        if self.bemoss_installed is False:
            tmp = tkMessageBox.askokcancel(title='Please install BEMOSS at first',
                                           message='You computer does not have BEMOSS installed, do you want to install BEMOSS right now?',
                                           parent=root)
            if tmp is True:
                self.install_bemoss()
                return
            else:
                return
        self.stop_bemoss()

    def install_bemoss(self):
        path = 'nohup x-terminal-emulator -e "bash -c \'sudo ./bemoss_install_v2.sh; bash\'"'
        subprocess.Popen(path, shell=True)

    def run_bemoss(self):
        bemoss_path = os.path.expanduser("~/workspace/bemoss_os")
        path = 'nohup x-terminal-emulator -e "bash -c \'sudo ~/workspace/bemoss_os/runBEMOSS.sh; bash\'"'
        subprocess.Popen(path, cwd=bemoss_path, shell=True)

    def stop_bemoss(self):
        pass

    def adv_set(self):
        self.detect_bemoss()
        if self.bemoss_installed is False:
            tmp = tkMessageBox.askokcancel(title='Please install BEMOSS at first',
                                           message='You computer does not have BEMOSS installed, do you want to install BEMOSS right now?',
                                           parent=root)
            if tmp is True:
                self.install_bemoss()
                return
            else:
                return
        self.new_win()

    def new_win(self):
        # advanced setting window
        window = Tkinter.Toplevel(root)
        window.title('Advanced Setting')
        x = root.winfo_rootx()
        y = root.winfo_rooty()
        window.geometry('+%d+%d' % (x+150, y+100))
        window.resizable(True, True)
        window.minsize(height=550, width=530)
        window.lift(root)

        # add 4 tabs in advanced setting window(Setting,VOLTTRON,Database,System Montior)
        notebook = ttk.Notebook(window)
        notebook.pack(fill=Tkinter.BOTH, expand=True)
        self.frame1 = ttk.Frame(notebook)
        self.frame2 = ttk.Frame(notebook)
        self.frame3 = ttk.Frame(notebook)
        self.frame4 = ttk.Frame(notebook)
        notebook.add(self.frame1, text='Setting')
        notebook.add(self.frame2, text='VOLTTRON')
        notebook.add(self.frame3, text='Database')
        notebook.add(self.frame4, text='System Monitor')
        
        # tab1 Setting
        self.frame1.config(height=550, width=530)
        disframe = Tkinter.LabelFrame(self.frame1, text='Device to be discovered:', font=('Arial', 10, 'bold'))
        disframe.pack(fill=Tkinter.BOTH, expand=True, padx=7, pady=6)
        self.Wi_Fi = Tkinter.IntVar()
        self.Hu = Tkinter.IntVar()
        self.We = Tkinter.IntVar()
        self.BACnet = Tkinter.IntVar()
        self.Modbus = Tkinter.IntVar()
        checkbutton1 = Tkinter.Checkbutton(disframe, text='Wi-Fi',
                                           variable=self.Wi_Fi, onvalue=1,
                                           offvalue=0)
        checkbutton2 = Tkinter.Checkbutton(disframe, text='Hue',
                                           variable=self.Hu, onvalue=1,
                                           offvalue=0)
        checkbutton3 = Tkinter.Checkbutton(disframe, text='WeMo',
                                           variable=self.We, onvalue=1,
                                           offvalue=0)
        checkbutton4 = Tkinter.Checkbutton(disframe, text='BACnet',
                                           variable=self.BACnet, onvalue=1,
                                           offvalue=0)
        checkbutton5 = Tkinter.Checkbutton(disframe, text='Modbus',
                                           variable=self.Modbus, onvalue=1,
                                           offvalue=0)

        disframe.rowconfigure(0, weight=1)
        disframe.rowconfigure(1, weight=1)
        disframe.rowconfigure(2, weight=1)
        disframe.rowconfigure(3, weight=1)
        disframe.columnconfigure(0, weight=3)
        disframe.columnconfigure(1, weight=3)
        disframe.columnconfigure(2, weight=3)
        disframe.columnconfigure(3, weight=3)
        disframe.columnconfigure(4, weight=1)
        checkbutton1.grid(row=0, column=1, sticky='w')
        checkbutton2.grid(row=0, column=2, sticky='w')
        checkbutton3.grid(row=0, column=3, sticky='w')
        checkbutton4.grid(row=1, column=1, sticky='w')
        checkbutton5.grid(row=1, column=2, sticky='w')

        Sub_but = ttk.Button(self.frame1, text='Submit', command=self.submit_in_setting)
        Sub_but.pack(side=Tkinter.RIGHT, padx=6,pady=10)
        GD_but = ttk.Button(self.frame1, text='Get Data',command=self.getdata_in_setting)
        GD_but.pack(side=Tkinter.RIGHT, padx=6, pady=10)
    
        #tab2 VOLTTRON
        self.frame2.config(height=550, width=530)
        textframe = ttk.Frame(self.frame2)
        textframe.pack(fill=Tkinter.BOTH, expand=True, padx=7, pady=4)
        scrollbar = ttk.Scrollbar(textframe)
        scrollbar.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)
        self.VOL_text = Tkinter.Text(textframe, bg='white',
                                yscrollcommand=scrollbar.set, wrap='word')
        self.VOL_text.pack(side=Tkinter.LEFT, expand=True, fill=Tkinter.BOTH)
        scrollbar.config(command=self.VOL_text.yview)
        view_but = ttk.Button(self.frame2, text='View Agent Status', command=self.check_agent_status)
        view_but.pack(padx=5, pady=5)
        butframe1 = ttk.Frame(self.frame2)
        butframe1.pack()
        stop_but = ttk.Button(butframe1, text='Stop Agent', command=self.agent_stop)
        stop_but.pack(side=Tkinter.RIGHT, padx=5, pady=2.5)
        start_but = ttk.Button(butframe1, text='Start Agent', command=self.agent_start)
        start_but.pack(side=Tkinter.RIGHT, padx=5, pady=2.5)
        self.agent = Tkinter.StringVar()
        VOL_entry = ttk.Entry(butframe1, width=15, textvariable=self.agent)
        VOL_entry.pack(side=Tkinter.RIGHT, padx=5, pady=2.5)
        agid = ttk.Label(butframe1, text='Agent ID:')
        agid.pack(side=Tkinter.RIGHT, padx=5, pady=2.5)
        butframe2 = ttk.Frame(self.frame2)
        butframe2.pack()
        rep_but = ttk.Button(butframe2, text='Repackage', command=self.repackage)
        rep_but.pack(side=Tkinter.RIGHT, padx=5, pady=2.5)
        self.category = Tkinter.StringVar()
        self.category.set('')
        catebox = ttk.Combobox(butframe2, textvariable=self.category)
        catebox.pack(side=Tkinter.RIGHT, padx=5, pady=2.5)
        catebox.config(values=('Thermostat', 'Plugload', 'Lighting',
                               'RTU', 'VAV', 'DeviceDiscovery', 'Network', 'MultiBuilding'))
        agcate = ttk.Label(butframe2, text='Agent category:')
        agcate.pack(side=Tkinter.RIGHT, padx=5, pady=2.5)

        #tab3 Database
        self.frame3.config(height=550, width=530)
        postframe = Tkinter.LabelFrame(self.frame3, text='Postgresql')
        postframe.pack(fill=Tkinter.BOTH, expand=True, padx=7, pady=5)
        ACS_but= ttk.Button(postframe, text='Open Configure File', command=self.open_pg_config)
        LP_but = ttk.Button(postframe, text='Launch PgAdmin3', command=self.start_pgadm)
        ACS_but.pack(fill=Tkinter.BOTH, expand=True, padx=5, pady=3)
        LP_but.pack(fill=Tkinter.BOTH, expand=True, padx=5, pady=3)
        casframe = Tkinter.LabelFrame(self.frame3, text='Cassandra')
        casframe.pack(fill=Tkinter.BOTH, expand=True, padx=7, pady=5)
        DSF_but= ttk.Button(casframe, text='Delete Setting File', command=self.del_cas)
        DD_but = ttk.Button(casframe, text='Delete Data', command=self.del_dat)
        LIT_but = ttk.Button(casframe, text='Launch in Terminal', command=self.start_cas)
        DSF_but.pack(side=Tkinter.LEFT, fill=Tkinter.BOTH, expand=True, padx=3, pady=5)
        DD_but.pack(side=Tkinter.LEFT, fill=Tkinter.BOTH, expand=True, padx=3, pady=5)
        LIT_but.pack(side=Tkinter.LEFT, fill=Tkinter.BOTH, expand=True, padx=3, pady=5)

        # tab4 System monitor
        self.frame4.config(height=550, width=530)
        self.frame4.rowconfigure(0, weight=1)
        self.frame4.rowconfigure(1, weight=1)
        self.frame4.rowconfigure(2, weight=1)
        self.frame4.rowconfigure(3, weight=1)
        self.frame4.rowconfigure(4, weight=1)
        self.frame4.rowconfigure(5, weight=1)
        self.frame4.rowconfigure(6, weight=1)
        self.frame4.rowconfigure(7, weight=1)
        self.frame4.columnconfigure(0, weight=2)
        self.frame4.columnconfigure(1, weight=1)
        self.frame4.columnconfigure(2, weight=1)
        self.frame4.columnconfigure(3, weight=1)
        self.frame4.columnconfigure(4, weight=1)
        self.frame4.columnconfigure(5, weight=1)
        LA_lab = ttk.Label(self.frame4, text='LOAD AVERAGE')
        LA_lab.grid(row=1, column=1, columnspan=2, sticky='w')
        self.var_LA = Tkinter.StringVar()
        LA_lab_Entry = Tkinter.Entry(self.frame4, width=35, state='readonly',
                                     textvariable=self.var_LA)
        LA_lab_Entry.grid(row=1, column=3, columnspan=2, sticky='w')
        CPU_UU = ttk.Label(self.frame4, text='CPU(USER USED)')
        CPU_UU.grid(row=2, column=1, columnspan=2, sticky='w')
        self.var_UU = Tkinter.StringVar()
        CPU_UU_Entry = Tkinter.Entry(self.frame4, width=35, state='readonly',
                                     textvariable=self.var_UU)
        CPU_UU_Entry.grid(row=2, column=3, columnspan=2, sticky='w')
        CPU_SU = ttk.Label(self.frame4, text='CPU(SYSTEM USED)')
        CPU_SU.grid(row=3, column=1, columnspan=2, sticky='w')
        self.var_SU = Tkinter.StringVar()
        CPU_SU_Entry = Tkinter.Entry(self.frame4, width=35, state='readonly',
                                     textvariable=self.var_SU)
        CPU_SU_Entry.grid(row=3, column=3, columnspan=2, sticky='w')
        CPU_IDLE= ttk.Label(self.frame4, text='CPU(IDLE)')
        CPU_IDLE.grid(row=4, column=1, columnspan=2, sticky='w')
        self.var_IDLE = Tkinter.StringVar()
        CPU_IDLE_Entry = Tkinter.Entry(self.frame4, width=35,state='readonly',
                                       textvariable=self.var_IDLE)
        CPU_IDLE_Entry.grid(row=4, column=3, columnspan=2, sticky='w')
        MEM_T = ttk.Label(self.frame4, text='MEMORY(TOTAL)')
        MEM_T.grid(row=5, column=1,  columnspan=2, sticky='w')
        self.var_MT = Tkinter.StringVar()
        MEM_T_Entry = Tkinter.Entry(self.frame4, width=35, state='readonly',
                                    textvariable=self.var_MT)
        MEM_T_Entry.grid(row=5, column=3, columnspan=2, sticky='w')
        MEM_F = ttk.Label(self.frame4, text='MEMORY(USED)')
        MEM_F.grid(row=6, column=1,  columnspan=2, sticky='w')
        self.var_MF = Tkinter.StringVar()
        MEM_F_Entry = Tkinter.Entry(self.frame4, width=35, state='readonly',
                                    textvariable=self.var_MF)
        MEM_F_Entry.grid(row=6, column=3, columnspan=2, sticky='w')
        Get_data = ttk.Button(self.frame4, text='Get Data', command=self.sys_monitor)
        Get_data.grid(row=7, column=4, sticky='e', padx=5)
        self.auto = Tkinter.BooleanVar()
        auto_update = Tkinter.Checkbutton(self.frame4, text='Auto-update', variable=self.auto,
                                          onvalue=True, offvalue=False, command=self.updateonoroff)
        auto_update.grid(row=7, column=4, sticky='w')

    # Frame1 functions
    def submit_in_setting(self):
        device = dict()
        device['WiFi\''] = self.Wi_Fi.get()
        device['Hue\''] = self.Hu.get()
        device['WeMo\''] = self.We.get()
        device['BACnet\''] = self.BACnet.get()
        device['Modbus\''] = self.Modbus.get()

        #print device

        new_settings = device

        f = open(self.bemoss_dir + 'settings.py', 'r')
        f_new = open(self.bemoss_dir + 'settings_new.py', 'w')

        for line in f:
            if 'find' in line:
                status = 0
                for key in new_settings.keys():
                    if key in line:
                        if new_settings[key] == 0 and 'False' not in line:
                            line = line.replace('True', 'False')
                        if new_settings[key] == 1 and 'True' not in line:
                            line = line.replace('False', 'True')
                        f_new.write(line)
                        new_settings.pop(key)
                        status = 1
                if status == 0:
                    f_new.write(line)

            else:
                f_new.write(line)

        f.close()
        f_new.close()

        os.remove(self.bemoss_dir + 'settings.py')
        os.renames(self.bemoss_dir + 'settings_new.py', self.bemoss_dir + 'settings.py')

    def getdata_in_setting(self):
        f = open(self.bemoss_dir + 'settings.py', 'r')
        device = dict()
        device['WiFi\''] = None
        device['Hue\''] = None
        device['WeMo\''] = None
        device['BACnet\''] = None
        device['Modbus\''] = None
        for line in f:
            if 'find' in line:
                for key in device.keys():
                    if key in line:
                        if 'False' in line:
                            device[key] = 0
                        else:
                            device[key] = 1
                    else:
                        continue
            else:
                continue
        f.close()
        self.Wi_Fi.set(device['WiFi\''])
        self.Hu.set(device['Hue\''])
        self.We.set(device['WeMo\''])
        self.BACnet.set(device['BACnet\''])
        self.Modbus.set(device['Modbus\''])

    # Frame2 functions
    def get_passwd(self):
        self.passwd_window = Tkinter.Toplevel(self.frame2)
        self.passwd_window.title('Log In')
        x = self.frame2.winfo_rootx()
        y = self.frame2.winfo_rooty()
        self.passwd_window.geometry('350x130+%d+%d' % (x+150, y+100))
        self.passwd_window.lift()
        self.passwd_window.columnconfigure(0, weight=1)
        self.passwd_window.columnconfigure(1, weight=1)
        self.passwd_window.columnconfigure(2, weight=1)
        self.passwd_window.columnconfigure(3, weight=2)
        self.passwd_window.columnconfigure(4, weight=2)
        self.passwd_window.columnconfigure(5, weight=1)
        self.passwd_window.rowconfigure(0, weight=1)
        self.passwd_window.rowconfigure(1, weight=2)
        self.passwd_window.rowconfigure(2, weight=2)
        self.passwd_window.rowconfigure(3, weight=2)
        self.passwd_window.rowconfigure(4, weight=1)
        self.passwd_window.resizable(False, False)
        reminder = ttk.Label(self.passwd_window, text='Please input the system password.')
        reminder.grid(row=1, column=1, columnspan=4, sticky='w')
        self.pswd = Tkinter.StringVar()
        pwentry = Tkinter.Entry(self.passwd_window, textvariable=self.pswd, width=30)
        pwentry.focus_set()
        pwentry.grid(row=2, column=3, columnspan=2, sticky='w', padx=10)
        pwentry.config(show='*')
        pswdlabel = ttk.Label(self.passwd_window, text='Password:')
        pswdlabel.grid(row=2, column=2, sticky='e', padx=10)
        confirm_but = ttk.Button(self.passwd_window, text='Confirm', command=self.pwconfirm)
        confirm_but.grid(row=3, column=4, sticky='w', padx=5)
        clear_but = ttk.Button(self.passwd_window, text='Clear',
                               command=lambda: pwentry.delete(0, Tkinter.END))
        clear_but.grid(row=3, column=3, sticky='e', padx=5)
        self.passwd_window.bind('<Return>', self.shortcut)

    def shortcut(self, event):
        self.pwconfirm()

    def pwconfirm(self):
        self.pswd
        self.passwd = self.pswd.get()
        if self.passwd is not None:
            output = volttronFunc.agent_status(self.passwd)
            try:
                if output == '':
                    # pop up a window: remind the user to check his password.
                    tkMessageBox.showerror(title="Notification", message='Sorry, the password is incorrect, please try again.', parent=self.passwd_window)
                    self.passwd = None
                    self.passwd_window.state('withdrawn')
                else:
                    self.passwd_window.state('withdrawn')
                    self.VOL_text.configure(state='normal')
                    self.VOL_text.delete('1.0', Tkinter.END)
                    self.VOL_text.insert('1.0', output)
                    self.VOL_text.configure(state='disabled')
                    self.passwd_window.withdraw()
            except Exception as er:
                print er
                print('Error @ pwconfirm.')

    def check_agent_status(self):
        if self.passwd is None:
            self.get_passwd()
        else:
            output = volttronFunc.agent_status(self.passwd)
            if output == '':
                tkMessageBox.showerror(title="Notification", message='Sorry, the password is incorrect, please try again.', parent=self.passwd_window)
                self.passwd = None
                return
            else:
                self.VOL_text.configure(state='normal')
                self.VOL_text.delete('1.0', Tkinter.END)
                self.VOL_text.insert('1.0', output)
                self.VOL_text.configure(state='disabled')

    def agent_stop(self):
        if self.passwd is None:
            self.get_passwd()
        else:
            volttronFunc.stop_agent(self.passwd, self.agent.get())
            self.VOL_text.after(3000, self.check_agent_status)

    def agent_start(self):
        if self.passwd is None:
            self.get_passwd()
        else:
            volttronFunc.start_agent(self.passwd, self.agent.get())
            self.VOL_text.after(3000, self.check_agent_status)


    def agent_remove(self):
        if self.passwd is None:
            self.get_passwd()
        else:
            volttronFunc.remove_agent(self.passwd, self.agent.get())


    def agent_clear(self):
        if self.passwd is None:
            self.get_passwd()
        else:
            volttronFunc.clear_agent(self.passwd)


    def agent_config(self):
        if self.passwd is None:
            self.get_passwd()
        else:
            agent_id = self.agent.get()
            agentType = self.category.get()+'Agent'
            volttronFunc.configure_agent(self.passwd, agent_id, agentType)


    def agent_install(self):
        if self.passwd is None:
            self.get_passwd()
        else:
            agent_id = self.agent.get()
            agentType = self.category.get()+'Agent'
            volttronFunc.install_agent(self.passwd, agent_id, agentType)

    def repackage(self):
        if self.category.get() == '':
            pass
        else:
            agentType = self.category.get()+'Agent'
            # Find running agent of this category
            running_agent, dis_agent = self.search_running_agent(self.category.get().lower())
            running_agent_vid = list()
            running_agent_id = list()
            active_running_agent_id = list()
            for item in running_agent:
                running_agent_vid.append(item[0])
                running_agent_id.append(item[2])
                try:
                    if item[3] == 'running':
                        active_running_agent_id.append(item[2])
                except:
                    print('Index out of range because no active running agent now.')
            # Stop discover agent:
            self.agent.set(dis_agent)
            self.agent_stop()
            time.sleep(1)
            # Stop these agents:
            for item in running_agent_vid:
                self.agent.set(item)
                self.agent_stop()
                time.sleep(1)
                self.agent_remove()
                time.sleep(1)
                self.agent_clear()
                print('Agent '+str(item)+' stopped')
            print ('All this type agents stopped and removed')
            # Re-package the agent code
            output = volttronFunc.repackage_agent(self.passwd, agentType)
            if 'Package created' in output:
                print ('Agent package successfully')

            # Reconfigure and Reinstall agents
            for item in running_agent_id:
                self.agent.set(item)
                self.agent_config()
                time.sleep(2)
                self.agent_install()
                print('Agent ' + str(item) + ' has been re-configrued and started.')

            self.agent_clear()

            # Restart agents
            for item in active_running_agent_id:
                print('now restarting agent ' + str(item))
                self.agent.set(item)
                volttronFunc.start_agent(self.passwd, self.agent.get(), type=2)
                time.sleep(1)

            # Time to bring back the devicediscovery agent.
            self.agent.set(dis_agent)
            self.agent_start()
            time.sleep(1)
            self.agent.set('')
            tkMessageBox.showinfo(title="Notification", message=agentType+' Repackage completed!', parent=self.frame2)

    def search_running_agent(self, target):
        output = volttronFunc.agent_status(self.passwd)
        try:
            output1 = output.split('\n')

            running_agent = list()
            dis_agent = list()
            target += 'agent'

            for item in output1:
                item_decom = item.split(' ')
                item_decom_short = [id for id in item_decom if id]
                if target in item:
                    running_agent.append(item_decom_short)
                if 'devicediscoveryagent' in item:
                    dis_agent = item_decom_short[0]
            return running_agent, dis_agent
        except Exception as er:
            print er

    # Frame3 functions
    def get_passwd_ocf(self):
        self.passwd_window_ocf = Tkinter.Toplevel(self.frame3)
        self.passwd_window_ocf.title('Postgres Auth(System Password)')
        x = self.frame3.winfo_rootx()
        y = self.frame3.winfo_rooty()
        self.passwd_window_ocf.geometry('350x130+%d+%d' % (x+150, y+100))
        self.passwd_window_ocf.lift()
        self.passwd_window_ocf.columnconfigure(0, weight=1)
        self.passwd_window_ocf.columnconfigure(1, weight=1)
        self.passwd_window_ocf.columnconfigure(2, weight=1)
        self.passwd_window_ocf.columnconfigure(3, weight=2)
        self.passwd_window_ocf.columnconfigure(4, weight=2)
        self.passwd_window_ocf.columnconfigure(5, weight=1)
        self.passwd_window_ocf.rowconfigure(0, weight=1)
        self.passwd_window_ocf.rowconfigure(1, weight=2)
        self.passwd_window_ocf.rowconfigure(2, weight=2)
        self.passwd_window_ocf.rowconfigure(3, weight=2)
        self.passwd_window_ocf.rowconfigure(4, weight=1)
        self.passwd_window_ocf.resizable(False, False)
        reminder = ttk.Label(self.passwd_window_ocf, text='Please input the system password.')
        reminder.grid(row=1, column=1, columnspan=4, sticky='w')
        self.pswd_ocf = Tkinter.StringVar()
        pwentry = Tkinter.Entry(self.passwd_window_ocf, textvariable=self.pswd_ocf, width=30)
        pwentry.focus_set()
        pwentry.grid(row=2, column=3, columnspan=2, sticky='w', padx=10)
        pwentry.config(show='*')
        pswdlabel = ttk.Label(self.passwd_window_ocf, text='Password:')
        pswdlabel.grid(row=2, column=2, sticky='e', padx=10)
        confirm_but = ttk.Button(self.passwd_window_ocf, text='Confirm', command=self.pwconfirm_ocf)
        confirm_but.grid(row=3, column=4, sticky='w', padx=5)
        clear_but = ttk.Button(self.passwd_window_ocf, text='Clear',
                               command=lambda: pwentry.delete(0, Tkinter.END))
        clear_but.grid(row=3, column=3, sticky='e', padx=5)
        self.passwd_window_ocf.bind('<Return>', self.shortcut3)

    def shortcut3(self):
        self.pwconfirm_ocf()

    def pwconfirm_ocf(self):
        password_ocf = self.pswd_ocf.get()
        self.open_pg_config_func(password_ocf)
        self.passwd_window_ocf.state('withdrawn')

    def open_pg_config(self):
        # First check postgresql version
        if self.passwd is None or self.passwd == 'nosudo':
            self.get_passwd_ocf()
        else:
            self.open_pg_config_func(self.passwd)

    def open_pg_config_func(self, sys_password):
        path = os.getcwd()
        level = path.count('/')
        back = '../'
        to_home = ''
        while level >= 0:
            to_home += back
            level -= 1
        version = os.listdir(to_home + 'etc/postgresql')
        # look for available text editors
        softwares = os.listdir(to_home + 'usr/bin')
        if 'gedit' in softwares:
            editor = 'gedit '
        elif ('leafpad' in softwares):
            editor = 'leafpad '
        # using text editor to open configure file
        try:
            cmd = 'echo \'' + str(sys_password) + '\' |sudo -S ' + editor + to_home + 'etc/postgresql/' + version[0] + '/main/postgresql.conf'
            subprocess.Popen(cmd, shell=True)
            cmd = 'echo \'' + str(sys_password) + '\' |sudo -S ' + editor + to_home + 'etc/postgresql/' + version[0] + '/main/pg_hba.conf'
            subprocess.Popen(cmd, shell=True)
        except Exception as er:
            print er
            print('No gedit or leafpad editor installed.')

    def start_pgadm(self):
        cmd = 'nohup x-terminal-emulator -e pgadmin3'
        subprocess.Popen(cmd, shell=True)

    def del_dat(self):
        cnt = tkMessageBox.askokcancel(title='Reconfirmation',
                                       message='Are you sure to delete the data?',
                                       parent=self.frame3)
        if cnt is True:
            cas_dir = self.bemoss_dir.replace('bemoss_os/', 'cassandra/')
            path = cas_dir + 'data'
            shutil.rmtree(path)
        else:
            return

    def del_cas(self):
        cnt = tkMessageBox.askokcancel(title='Reconfirmation',
                                       message='Are you sure to delete the file?',
                                       parent=self.frame3)
        if cnt is True:
            path = self.bemoss_dir + '/cassandra_settings.txt'
            os.remove(path)
        else:
            return

    def start_cas(self):
        # add log in pop up here to let the user to input the username and password. Save then in cas_usr and cas_pw
        self.login_window = Tkinter.Toplevel(root)
        self.login_window.title('Cassandra Log in')
        self.login_window.lift()
        x = self.frame3.winfo_rootx()
        y = self.frame3.winfo_rooty()
        self.login_window.geometry('300x170+%d+%d' % (x+150, y+100))
        self.login_window.rowconfigure(0, weight=1)
        self.login_window.rowconfigure(1, weight=1)
        self.login_window.rowconfigure(2, weight=1)
        self.login_window.rowconfigure(3, weight=1)
        self.login_window.rowconfigure(4, weight=1)
        self.login_window.columnconfigure(0, weight=1)
        self.login_window.columnconfigure(1, weight=1)
        self.login_window.columnconfigure(2, weight=1)
        self.login_window.columnconfigure(3, weight=1)
        self.login_window.resizable(False, False)
        unlabel = ttk.Label(self.login_window, text='Username:')
        unlabel.grid(row=1, column=1)
        pwlabel = ttk.Label(self.login_window, text='Password:')
        pwlabel.grid(row=2, column=1)
        self.username_cas = Tkinter.StringVar()
        self.password_cas = Tkinter.StringVar()
        unentry = ttk.Entry(self.login_window, textvariable=self.username_cas, width=20)
        unentry.focus_set()
        unentry.grid(row=1, column=2)
        pwentry = ttk.Entry(self.login_window, textvariable=self.password_cas, width=20)
        pwentry.grid(row=2, column=2)
        pwentry.configure(show='*')
        conf_but = ttk.Button(self.login_window, text='Confirm', command=self.checkuser)
        conf_but.grid(row=3, column=2, sticky='e')
        self.login_window.bind('<Return>', self.shortcut2)

    def shortcut2(self, event):
        self.checkuser()

    def checkuser(self):
        cas_usr = self.username_cas.get()
        cas_pw = self.password_cas.get()
        cmd = 'nohup x-terminal-emulator -e ~/workspace/cassandra/bin/cqlsh ' \
              + str(self.ip_addr) + ' -u ' + str(cas_usr) + ' -p ' + str(cas_pw)
        subprocess.Popen(cmd, shell=True)
        self.login_window.withdraw()

    # Frame4 functions
    def updateonoroff(self):
        self.do_update = self.auto.get()
        self.update()

    def update(self):
        if self.do_update == True:
            # print('test')
            self.sys_monitor()
            root.after(1000, self.update)

    def sys_monitor(self):
        cmd = ['top -b -n 2']
        result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()[0]
        reg = 'load average: (.*?)\nTasks:.*?Cpu\(s\): (.*?)us, (.*?)sy.*?ni, (.*?)id.*?Mem:   ' \
              '(.*?) total,  (.*?) used'
        pattern = re.compile(reg, re.S)
        data = re.findall(pattern, result)
        if len(data) == 2:
            idx = 1
        else:
            idx = 0
        self.var_LA.set(data[idx][0])
        self.var_UU.set(data[idx][1])
        self.var_SU.set(data[idx][2])
        self.var_IDLE.set(data[idx][3])
        self.var_MT.set(data[idx][4])
        self.var_MF.set(data[idx][5])

def main():
    global root
    root = Tkinter.Tk()
    root.geometry('380x380+500+100')
    root.resizable(True, True)
    root.minsize(width=380, height=380)
    root.title('BEMOSS (Virginia Tech)')
    app = GUI()
    root.mainloop()

if __name__ == '__main__':
    main()
