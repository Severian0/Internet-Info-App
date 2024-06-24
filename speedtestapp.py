import tkinter as tk
from tkinter import ttk
import subprocess
import speedtest
import ipaddress
import requests
import json

def getPubInfo():
    urlServer = 'https://ipinfo.io/json'

    response = requests.get(urlServer,verify=True)
    if response.status_code != 200:
        return f'Status: {response.status_code} Error, Server may be down. Check connections and restart application'
    data = response.json()
    return data['ip'],data['city'],data['country'],data['timezone'],data['org']
    


def getIPConfig():
    proc = subprocess.check_output("ipconfig")
    lines = proc.decode("utf-8").splitlines()
    for line in lines:
        if "IPv4 Address" in line:
            ipv4 = line.split(":")[1].strip()
        if "IPv6 Address" in line:
            ipv6 = line.split(':')[1].strip()
        if "Subnet Mask" in line:
            SubnetMask = line.split(':')[1].strip()
    proc = subprocess.check_output("ipconfig /all")
    lines = proc.decode("utf-8").splitlines()
    for line in lines:
        if 'Host Name' in line:
            HostName = line.split(':')[1].strip()
        if 'DNS Suffix Search List' in lines:
            provider = line.split(':')[1].strip()
            
    return ipv4,ipv6,SubnetMask,HostName,
    

    

    


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # self window
        
        self.title('Internet Diagnostics by .severiano')

        window_width = 800
        window_height = 600

        # get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # find the center point
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)

        # set the position of the window to the center of the screen
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.maxsize(800,600)
        self.minsize(300,200)
        
        tabControl = ttk.Notebook(self)

        tab1 = ttk.Frame(tabControl)
        tab2 = ttk.Frame(tabControl)
        tabControl.add(tab1, text ='General Info') 
        tabControl.add(tab2, text ='Speed Test')
        tabControl.pack(expand = 1, fill ="both")  
        

        hellolabel = ttk.Label(tab1,text='Click button to see internet data').pack(ipady=5)
        showbutton = ttk.Button(tab1,text='Show Info',command=lambda: self.showinfo(tab1)).pack(ipady=5)

        speedtestlabel = ttk.Label(tab2,text='Press button to show download, upload speeds and ping to nearest server').pack(ipady=5)
        speedtestbutton = ttk.Button(tab2,text='Start Test',command=lambda: self.speedtester(tab2)).pack(ipady=5)
       
    def showinfo(self,tab):
        ip,city,country,timezone,provider = getPubInfo()
        ipv4,ipv6,SubnetMask,HostName = getIPConfig()
        pubIPLabel = ttk.Label(tab,text=ip)
        citylabel = ttk.Label(tab,text=city)
        countrylabel = ttk.Label(tab,text=country)
        timezonelabel = ttk.Label(tab,text=timezone)
        providerlabel = ttk.Label(tab,text=provider)
        ipv4label = ttk.Label(tab,text=ipv4)
        ipv6label = ttk.Label(tab,text=ipv6)
        SubnetMasklabel = ttk.Label(tab,text=SubnetMask)
        hostnamelabel = ttk.Label(tab,text=HostName)

        pubIPLabel.pack()
        citylabel.pack()
        countrylabel.pack()
        timezonelabel.pack()
        providerlabel.pack()
        ipv4label.pack()
        ipv6label.pack()
        SubnetMasklabel.pack()
        hostnamelabel.pack()

    def speedtester(self,tab):
        getserverlabel = ttk.Label(tab,text='Finding available servers')
        getserverlabel.pack()
        st = speedtest.Speedtest()
       
        
        st.get_servers()
        getbestserverlabel = ttk.Label(tab,text='Selecting best server')
        getbestserverlabel.pack()
        best = st.get_best_server()
        downloadresult = st.download()
        uploadresult = st.upload()
        ping_result = st.results.ping
        

        bestserverlabel = ttk.Label(tab,text="Found: " + best['host'] + " located in " + best['country'])
        downloadlabel = ttk.Label(tab,text=f'Download speeds = {downloadresult / 1024 / 1024: .2f} Mbit/s')
        uploadlabel = ttk.Label(tab,text=f'Upload speeds = {uploadresult / 1024 / 1024: .2f} Mbit/s')
        pinglabel = ttk.Label(tab,text="Ping to " + best['host'] + " is " + str(ping_result))

        bestserverlabel.pack()
        downloadlabel.pack()
        uploadlabel.pack()
        pinglabel.pack()





if __name__ == "__main__":
    
    app = App()
    app.mainloop()
    