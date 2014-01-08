from tkinter import *
from tkinter import ttk
from tkinter import font
import webbrowser

##Convert time to minutes

def convert(time):
    minutes = time[-2:]
    hours = int(float(time) / 100)
    con_time = (hours * 60) + int(minutes)
    return con_time

def revconvert(time):
    hours = int(time/60)
    minutes = time - (hours * 60)
    revcon_time = (hours * 100) + minutes
    return revcon_time

##Calculate number of Infusion/Injection

injection = []
infusion = []
a_injection = {1:[0, 0]}
a_infusion = {}
inf_inf = {}
inj_inj = {}

def calculate_drug(*args):
    start = begin.get()
    stop = end.get()
    start = convert(str(start))
    stop = convert (str(stop))
    if start > stop:
        stop += 1440                      ##For accounts that go over midnight
    time = int(stop)-int(start)
    if time < 16:                         ##Minimum infusion time (16)
        injection.append('1 injection')
        n = len(injection) + 1
        a_injection[n] = [start, stop]
        inj_inj[n] = [revconvert(start), revconvert(stop)]
        n += 1
        inj.set(inj_inj)
    else:
        p = (time - 30)/60                ##Subtract 1st 30min for the first inf
        p = int(p) + 1
        n = len(infusion) + 1
        a_infusion[n] = [start, stop]
        inf_inf[n] = [revconvert(start), revconvert(stop)]
        n += 1
        inf.set(inf_inf)
        while p > 0:
            infusion.append('1 infusion')
            p -= 1
    injamt.set(len(injection))
    infamt.set(len(infusion))

##Calculate number of Hydration

hydration = []
a_hydration = {}
hyd_hyd = {}

def calculate_hydration(*args):
    start = begin.get()
    stop = end.get()
    start = convert(start)
    stop = convert(stop)
    n = len(hydration) + 1
    a_hydration[n] = [start, stop]
    hyd_hyd[n] = [revconvert(start), revconvert(stop)]

##Check for inj overlap (probably a better way to do this)

def check_injection(*args):
    for key in a_injection:
        jfirst = a_injection[key]
        injstart = jfirst[0]
        injstop = jfirst[1]
        revjt = revconvert(injstart)
        revjp = revconvert(injstop)
        for key in a_hydration:
            hfirst = a_hydration[key]
            hydstart = hfirst[0]
            hydstop = hfirst[1]
            revhydt = revconvert(hydstart)
            revhydp = revconvert(hydstop)
            if (injstart <= hydstart < injstop) and (hydstop > injstop):
                check_hydration(*args)
            elif (injstart <= hydstop < injstop) and (hydstart < injstart):
                check_hydration(*args)
            elif (injstart <= hydstart < hydstop) and (hydstop <= injstop):
                check_hydration(*args)
            elif (hydstart <= injstart) and (hydstop >= injstop):
                check_hydration(*args)

##Check for inf overlap (probably a better way to do this)

def check_infusion(*args):
    for key in a_infusion:
        ffirst = a_infusion[key]
        infstart = ffirst[0]
        infstop = ffirst[1]
        revft = revconvert(infstart)
        revfp = revconvert(infstop)
        for key in a_hydration:
            hfirst = a_hydration[key]
            hydstart = hfirst[0]
            hydstop = hfirst[1]
            revhydt = revconvert(hydstart)
            revhydp = revconvert(hydstop)
            if (infstart <= hydstart < infstop) and (hydstop > infstop):
                check_hydration(*args)
            elif (infstart <= hydstop < infstop) and (hydstart < infstart):
                check_hydration(*args)
            elif (infstart <= hydstart < hydstop) and (hydstop <= infstop):
                check_hydration(*args)
            elif (hydstart <= infstart) and (hydstop >= infstop):
                check_hydration(*args)
      
##Check for hyd overlap

lap_inf = {}
lap_inj = {}
lap_hyd = {}

def check_hydration(*args):
    lap_inf = {}
    lap_inj = {}
    lap_hyd = {}
    hydration = []
    for key in a_hydration:
        hfirst = a_hydration[key]
        hydstart = hfirst[0]
        hydstop = hfirst[1]
        revhydt = revconvert(hydstart)
        revhydp = revconvert(hydstop)
        hydtime = hydstop - hydstart
        c = 1
        for key in a_infusion:
            ifirst = a_infusion[key]
            infstart = ifirst[0]
            infstop = ifirst[1]
            revinft = revconvert(infstart)
            revinfp = revconvert(infstop)
            if (infstart <= hydstart < infstop) and (hydstop > infstop):
                minute = int(infstop) - int(hydstart)
                hydtime -= minute
                lap_inf[c] = [infstart, infstop]
                lap_hyd[c] = [hydstart, hydstop]
                c += 1
            elif (infstart <= hydstop < infstop) and (hydstart < infstart):
                minute = int(hydstop) - int(infstart)
                hydtime -= minute
                lap_inf[c] = [infstart, infstop]
                lap_hyd[c] = [hydstart, hydstop]
                c += 1
            elif (infstart <= hydstart < hydstop) and (hydstop <= infstop):
                hydtime = 0
                lap_inf[c] = [infstart, infstop]
                lap_hyd[c] = [hydstart, hydstop]
                c += 1
            elif (hydstart <= infstart) and (hydstop >= infstop):
                minute = infstop - infstart
                hydtime -= minute
                lap_inf[c] = [infstart, infstop]
                lap_hyd[c] = [hydstart, hydstop]
                c += 1
        for key in a_injection:
            jfirst = a_injection[key]
            jstart = jfirst[0]
            jstop = jfirst[1]
            if (hydstart <= jstart < hydstop):
                hydtime -= 15
                lap_inj[c] = [jstart, jstop]
                lap_hyd[c] = [hydstart, hydstop]
                c += 1
    if hydtime != 0:
        p = (hydtime - 30)/60
        p = int(p) + 1
        if hydtime < 30:               ##Minimum hyd time (30)
          p = 0
        while p > 0:
            hydration.append("1 hydration ")
            p -= 1
    hydamt.set(len(hydration))
    
##Reset progam (clear button)

def clear(*args):
    injection = []
    infusion = []
    hydration = []
    a_injection = {}
    a_infusion = {}
    a_hydration = {}
    inf_inf = {}
    inj_inj = {}
    hyd_hyd = {}
    lap_inf = {}
    lap_inj = {}
    lap_hyd = {}
    injamt.set(len(injection))
    infamt.set(len(infusion))
    hydamt.set(len(hydration))
    inf.set('')
    inj.set('')
    hyd.set('')

##Clean up Start/Stop time lists (format to print labels)

def clean_up(*args):
    clean_inf = '\n'.join('{} {}'.format(k, d) for k, d in inf_inf.items())
    clean_inj = '\n'.join('{} {}'.format(k, d) for k, d in inj_inj.items())
    clean_hyd = '\n'.join('{} {}'.format(k, d) for k, d in hyd_hyd.items())
    inf.set(clean_inf)
    inj.set(clean_inj)
    hyd.set(clean_hyd)

##Reset entry widget

def rest(*args):
    begin.set("")
    end.set("")

##WWW Help (top level menu help)

def helps(*args):
    webbrowser.open('http://contact.infusioncalc.com/')

##Main function (calculate button)

def stype(*args):
    med = substance.get()
    if med != 'h':
        calculate_drug(*args)
        check_infusion(*args)
        check_injection(*args)
        clean_up(*args)
    else:
        calculate_hydration(*args)
        check_hydration(*args)
        clean_up(*args)
    start_entry.focus()
    rest(*args)


##GUI

root = Tk()
root.title('Infusion Calculator')

mainframe=ttk.Frame(root, padding='12 12 12 12')
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

begin = StringVar()
end = StringVar()
infamt = StringVar()
injamt = StringVar()
hydamt = StringVar()
substance = StringVar()
inf = StringVar()
inj = StringVar()
hyd = StringVar()

##Top level menu

menubar = Menu(root)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label='Close', command=root.quit)
menubar.add_cascade(label='File', menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label='Help', command=helps)
menubar.add_cascade(label='Help', menu=helpmenu)

root.config(menu=menubar)

##User Input

ttk.Label(mainframe, text='Start').grid(column=1, row=1)
ttk.Label(mainframe, text='Stop').grid(column=2, row=1)

start_entry = ttk.Entry(mainframe, textvariable = begin)
start_entry.grid(column=1, row=2, sticky=(E, W))

end_entry = ttk.Entry(mainframe, textvariable = end)
end_entry.grid(column=2, row=2, sticky=(E, W))

ttk.Button(mainframe, text='calculate', command=stype).grid(column=1, row=3, sticky=(E, W))
ttk.Button(mainframe, text='clear', command=clear).grid(column=2, row=3, sticky=(E, W))

ttk.Radiobutton(mainframe, text="Drug", variable=substance, value='d').grid(column=1, row=4)
ttk.Radiobutton(mainframe, text="Hyd", variable=substance, value='h').grid(column=2, row=4)

subframe=ttk.Frame(mainframe, padding='5 5 5 5')
subframe.grid(column=3, row=2, sticky=(N, W, E, S))
subframe.columnconfigure(0, weight=1)
subframe.rowconfigure(0, weight=1)
                       
ResultsFont = font.Font(size=12, weight='bold')

##Infusion start/stop output

ttk.Label(subframe, text='Inf Total').grid(column=1, row=1, padx=5)
ttk.Label(subframe, textvariable=infamt, font=ResultsFont).grid(column=1, row=2, padx=5)
ttk.Label(mainframe, text='Inf Start/Stop').grid(column=1, row=6, sticky=(N, W, E, S), padx=5, pady=10)
ttk.Label(mainframe, textvariable=inf).grid(column=1, row=7, sticky=(N, W, E, S))

##Injection start/stop output

ttk.Label(subframe, text='Inj Total').grid(column=2, row=1, padx=5)
ttk.Label(subframe, textvariable=injamt, font=ResultsFont).grid(column=2, row=2, padx=5)
ttk.Label(mainframe, text='Inj Start/Stop').grid(column=2, row=6, sticky=(N, W, E, S), padx=5, pady=10)
ttk.Label(mainframe, textvariable=inj).grid(column=2, row=7, sticky=(N, W, E, S))

##Hydration start/stop output

ttk.Label(subframe, text='Hyd Total').grid(column=3, row=1, padx=5)
ttk.Label(subframe, textvariable=hydamt, font=ResultsFont).grid(column=3, row=2, padx=5)
ttk.Label(mainframe, text='Hyd Start/Stop').grid(column=3, row=6, sticky=(N, W, E, S), padx=5, pady=10)
ttk.Label(mainframe, textvariable=hyd).grid(column=3, row=7, sticky=(N, W, E, S))

start_entry.focus()

root.bind('<Return>', stype)

root.mainloop()
