#!/usr/bin/python3
from os import system as shell
import re
from time import sleep as delay
try:
    import pyufw as ufw
    from colorama import Fore
except ImportError:
    shell('./graphicSetup.sh')
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from requests import get

class ShowStatus:
    def __init__(self,master):
        masterSS = tk.Toplevel(master)
        masterSS.title('Show Status - FireFlower')
        a = True
        i = 0
        while a or i<10:
            try:
                i+=1
                masterSS.iconbitmap('icon.ico')
                a = False
            except Exception:
                f = get('https://www.masteradon.altervista.org/img/fireflower.ico')
                open('icon.ico','wb').write(f.content)
        masterSS.configure(background='black')
        masterSS.geometry("700x400+100+100")
        masterSS.resizable(False,False)
        Subname = tk.Label(masterSS,text="Show Status",bg='black',fg='orange',anchor='n',font=('Algerian',20)).pack(pady=20)
        def refreshPage():
            masterSS.destroy()
            ShowStatus(master)
        tk.Button(masterSS,text='Refresh',fg='white',bg='blue',font=('ArialBlack',10,'bold'),command=lambda:refreshPage()).pack(pady=5)
        totS = ufw.status()
        able = totS['status']
        if able == 'active':
            defaul = totS['default']
            rules = totS['rules']
            tk.Label(masterSS,text="STATUS => ACTIVE",bg='black',fg='green',anchor='n',font=('Arial',12)).pack(pady=0)
            tk.Label(masterSS,text="DEFAULT RULES => {\n"+"| INCOMING: "+defaul['incoming']+"\n | OUTGOING: "+defaul['outgoing']+"\n| ROUTED: "+defaul['routed']+" }",bg='black',fg='cyan',anchor='n',font=('Arial',12)).pack(pady=3)
            tk.Label(masterSS,text="ACTIVE RULES => {",bg='black',fg='yellow',anchor='n',font=('Arial',12)).pack(pady=3)
            widget = tk.Text(masterSS,fg='yellow',width=75,height=12,bg='black',font=('Arial',12))
            def getRule(StRule):
                rule = ""
                spec = False
                prot = False
                ip = False
                if 'allow' in StRule:
                    rule += "ALLOW "
                elif 'deny' in StRule:
                    rule += "DENY "
                elif 'limit' in StRule:
                    rule += "LIMIT "
                elif 'reject' in StRule:
                    rule += "REJECT "
                elif 'route' in StRule:
                    rule += "ROUTE "
                if 'in' in StRule:
                    rule += "incoming "
                elif 'out' in StRule:
                    rule += "outgoing "
                else:
                    spec = True
                    rule += "every "
                rule += "connection "
                if '/t' in StRule:
                    prot = True		
                elif '/u' in StRule:
                    prot = True
                elif bool(re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', StRule)):
                    ip = true
                if prot == False and ip == False:
                    rule += "on port "
                    if spec == True:
                        rule += StRule.split(" ")[1]
                    else:
                        rule += StRule.split(" ")[2]
                elif prot == True and ip == False:
                    rule += "on port "
                    if spec == True:
                        rule += StRule.split(" ")[1].split("/")[0]
                        rule += StRule.split(" ")[1].split("/")[1]
                    else:
                        rule += StRule.split(" ")[2].split("/")[0]
                        rule +="for protocol "+StRule.split(" ")[2].split("/")[1]
                elif prot == False and ip == True:
                    if spec == True:
                        rule += " for the IP addresses from "+StRule.split(" ")[2]+" to "+StRule.split(" ")[4]
                        rule += " on port "
                        rule += StRule.split(" ")[6]
                    else:
                        rule+=" for the IP addresses from "+StRule.split(" ")[3]+" to "+StRule.split(" ")[5]
                        rule += " on port "
                        rule+=StRule.split(" ")[7]
                elif prot == True and ip == True:
                    if spec == True:
                        rule += " for the IP addresses from "+StRule.split(" ")[2]+" to "+StRule.split(" ")[4]
                        rule+=" on port "
                        rule+=StRule.split(" ")[6]
                        rule+=" for protocol "+StRule.split(" ")[6].split("/")[1]
                    else:
                        prule+=" for the IP addresses from "+StRule.split(" ")[3]+" to "+StRule.split(" ")[5]
                        rule+=" on port "
                        rule+=StRule.split(" ")[7]
                        rule+=" for protocol "+StRule.split(" ")[7].split("/")[1]
                return rule
            for r in range(len(rules)):
                ru = getRule(rules[r+1])
                st = f""+str(r+1)+") "+ru+'\n'
                if r+1==len(rules)/2:
                    widget.insert(tk.INSERT,st+'\n')
                else:
                    widget.insert(tk.INSERT,st)
            widget.pack(side=tk.LEFT,fill=tk.BOTH,pady=3)
            widget.config(state=tk.DISABLED)
            scrollbar = ttk.Scrollbar(masterSS,orient='vertical', command=widget.yview)
            scrollbar.pack(side=tk.RIGHT,fill=tk.BOTH)
            widget['yscrollcommand'] = scrollbar.set      
        else:
            tk.Label(masterSS,text="STATUS => INACTIVE",bg='black',fg='red',anchor='n',font=('Arial',12)).pack(pady=0)

class EditR:
    def __init__(self,master):
        masterSS = tk.Toplevel(master)
        masterSS.title('Edit the Rules - FireFlower')
        a = True
        i = 0
        while a or i<10:
            try:
                i+=1
                masterSS.iconbitmap('icon.ico')
                a = False
            except Exception:
                f = get('https://www.masteradon.altervista.org/img/fireflower.ico')
                open('icon.ico','wb').write(f.content)
        masterSS.configure(background='black')
        masterSS.geometry("230x200+100+100")
        masterSS.resizable(False,False)
        Subname = tk.Label(masterSS,text="Edit the Rules",bg='black',fg='orange',anchor='n',font=('Algerian',20)).pack(pady=20)
        class AddRule:
            def __init__(self,master):
                masterSSA = tk.Toplevel(masterSS)
                masterSSA.title('Add New Rules - FireFlower')
                masterSSA.geometry("600x400+100+100")
                masterSSA.configure(background='black')
                masterSSA.resizable(False,False)
                Subname = tk.Label(masterSSA,text="Add a New Rule",bg='black',fg='orange',anchor='n',font=('Algerian',20)).pack(pady=20)
                at = 0
                ac = 0
                def upd():
                    nonlocal at
                    nonlocal tipe
                    if at == 0:
                        tipe['text']='outgoing'
                        tipe['bg']='red'
                        at = 1
                    elif at == 1:
                        tipe['text']='every'
                        tipe['bg']='orange'
                        at = 2
                    else:
                        tipe['text']='incoming'
                        tipe['bg']='green'
                        at = 0
                def upc():
                    nonlocal ac
                    nonlocal conne
                    if ac == 0:
                        conne['text']='deny'
                        conne['bg']='red'
                        ac = 2
                    elif ac == 2:
                        conne['text']='reject'
                        conne['bg']='orange'
                        ac = 5
                    elif ac == 3:
                        conne['text']='route'
                        conne['bg']='orange'
                        ac = 5
                    elif ac == 5:
                        conne['text']='limit'
                        conne['bg']='orange'
                        ac = 6
                    else:
                        conne['text']='allow'
                        conne['bg']='green'
                        ac = 0
                tipe = tk.Button(masterSSA,text='incoming',fg='white',bg='green',font=('ArialBlack',10,'bold'),command=lambda:upd())
                tipe.pack(pady=5)
                conne = tk.Button(masterSSA,text='allow',fg='white',bg='green',font=('ArialBlack',10,'bold'),command=lambda:upc())
                conne.pack(pady=5)
                tk.Label(masterSSA,text="Insert the port number:",bg='black',fg='white',anchor='n',font=('Arial',10)).pack(pady=5)
                ports = tk.Text(masterSSA,width=10,height=1)
                ports.pack(pady=5)
                rule = ''
                def chk():
                    nonlocal tipe
                    nonlocal conne
                    nonlocal ports
                    nonlocal recap
                    nonlocal rule
                    try:
                        if int(ports.get('1.0',tk.END)) > 0 and int(ports.get('1.0',tk.END)) < 65535:
                            pass
                        else:
                            raise ValueError
                        recap['text']=conne['text']+' '+tipe['text']+' connections on port '+str(int(ports.get('1.0',tk.END)))
                        rule = conne['text']
                        if tipe['text'] == 'incoming':
                            rule += ' in '
                        if tipe['text'] == 'outgoing':
                            rule += ' out '
                        else:
                            rule += ' '
                        rule += str(int(ports.get('1.0',tk.END)))
                        if rule in ufw.status()['rules']:
                            messagebox.showinfo('HEY!','Your rule already exists!')
                    except ValueError:
                        messagebox.showerror('ERROR!','Port can only be an integer from 0 to 65535')
                        recap['text']='ERROR!'
                check = tk.Button(masterSSA,text='Check the Rule',fg='cyan',bg='black',font=('ArialBlack',10,'bold'),command=lambda:chk())
                check.pack(pady=5)
                recap = tk.Label(masterSSA,text="Allow incoming connections on port -",bg='black',fg='white',anchor='n',font=('Arial',10))
                recap.pack(pady=5)
                def submitt():
                    nonlocal rule
                    print(rule)
                    if rule in ufw.status()['rules']:
                        messagebox.showinfo('HEY!','Your rule already exists!')
                    else:
                        ufw.add(rule)
                        inf=tk.Label(masterSSA,text="Rule Successfully Added!",bg='black',fg='cyan',anchor='n',font=('Arial',10))
                        inf.pack(pady=5)
                        masterSSA.after(2000, lambda: inf.destroy())
                
                submitB = tk.Button(masterSSA,text='Submit the Rule',fg='cyan',bg='black',font=('ArialBlack',10,'bold'),command=lambda:submitt())
                submitB.pack(pady=5)
                
        class RmRule:
            def __init__(self,master):
                masterSSA = tk.Toplevel(masterSS)
                masterSSA.title('Delete an Existing Rules - FireFlower')
                masterSSA.geometry("600x400+100+100")
                masterSSA.configure(background='black')
                masterSSA.resizable(False,False)
                Subname = tk.Label(masterSSA,text="Delete an Existing Rule",bg='black',fg='orange',anchor='n',font=('Algerian',20)).pack(pady=20)
                tk.Label(masterSSA,text="insert the number of the rule you want to delete:\n(You can see the list of rules in section 'Show Status'\n[remember to click refresh after every delete])",bg='black',fg='white',anchor='n',font=('Arial',10)).pack(pady=5)
                ports = tk.Text(masterSSA,width=10,height=1)
                ports.pack(pady=5)
                rule = ''
                def chk():
                    nonlocal ports
                    try:
                        if int(s) > len(ufw.status()['rules']) and int(s) <= 0:
                            ufw.delete(int(ports.get('1.0',tk.END)))
                            recap = tk.Label(masterSSA,text="Rule Successfully Deleted!",bg='black',fg='white',anchor='n',font=('Arial',10))
                            recap.pack(pady=5)
                            masterSSA.after(2000, lambda: recap.destroy())
                        else:
                            raise ValueError
                    except ValueError:
                        messagebox.showerror('ERROR!','Rule Not Found...')
                        recap = tk.Label(masterSSA,text="Error!",bg='black',fg='white',anchor='n',font=('Arial',10))
                        recap.pack(pady=5)
                        masterSSA.after(2000, lambda: recap.destroy())
                dell = tk.Button(masterSSA,text='Delete the Rule',fg='red',bg='black',font=('ArialBlack',10,'bold'),command=lambda:chk())
                dell.pack(pady=5)
        
        class DefRule:
            def __init__(self,master):
                masterSSA = tk.Toplevel(master)
                masterSSA.title('Change Default Rules - FireFlower')
                masterSSA.geometry("600x300+100+100")
                masterSSA.configure(background='black')
                masterSSA.resizable(False,False)
                Subname = tk.Label(masterSSA,text="Change Default Rules",bg='black',fg='orange',anchor='n',font=('Algerian',20)).pack(pady=20)
                def refreshPage():
                    masterSSA.destroy()
                    DefRule(master)
                tk.Button(masterSSA,text='Refresh',fg='white',bg='blue',font=('ArialBlack',10,'bold'),command=lambda:refreshPage()).pack(pady=10)
                if ufw.status()['default']['incoming'].lower() == 'allow':
                    incomingColor = 'green'
                    incomingText = 'incoming connections: ALLOWED!'
                elif ufw.status()['default']['incoming'].lower() == 'deny':
                    incomingColor = 'red'
                    incomingText = 'incoming connections: DENY!'
                elif ufw.status()['default']['incoming'].lower() == 'route':
                    incomingColor = 'orange'
                    incomingText = 'incoming connections: ROUTED!'
                elif ufw.status()['default']['incoming'].lower() == 'reject':
                    incomingColor = 'orange'
                    incomingText = 'incoming connections: REJECTED!'
                elif ufw.status()['default']['incoming'].lower() == 'limit':
                    incomingColor = 'orange'
                    incomingText = 'incoming connections: LIMITED!'
                if ufw.status()['default']['outgoing'].lower() == 'allow':
                    outgoingColor = 'green'
                    outgoingText = 'outgoing connections: ALLOWED!'
                elif ufw.status()['default']['outgoing'].lower() == 'deny':
                    outgoingColor = 'red'
                    outgoingText = 'outgoing connections: DENY!'
                elif ufw.status()['default']['outgoing'].lower() == 'route':
                    outgoingColor = 'orange'
                    outgoingText = 'outgoing connections: ROUTED!'
                elif ufw.status()['default']['outgoing'].lower() == 'reject':
                    outgoingColor = 'orange'
                    outgoingText = 'outgoing connections: REJECTED!'
                elif ufw.status()['default']['outgoing'].lower() == 'limit':
                    outgoingColor = 'orange'
                    outgoingText = 'outgoing connections: LIMITED!'
                if ufw.status()['default']['routed'].lower() == 'allow':
                    routedColor = 'green'
                    routedText = 'routed connections: ALLOWED!'
                elif ufw.status()['default']['routed'].lower() == 'deny':
                    routedColor = 'red'
                    routedText = 'routed connections: DENY!'
                elif ufw.status()['default']['routed'].lower() == 'route':
                    routedColor = 'orange'
                    routedText = 'routed connections: ROUTED!'
                elif ufw.status()['default']['routed'].lower() == 'reject':
                    routedColor = 'orange'
                    routedText = 'routed connections: REJECTED!'
                elif ufw.status()['default']['routed'].lower() == 'limit':
                    routedColor = 'orange'
                    routedText = 'routed connections: LIMITED!'
                def updateIn(par=' ',masterSSAB=''):
                    global incomingColor
                    global incomingText
                    if par == ' ':
                        masterSSAI = tk.Toplevel(masterSSA)
                        masterSSAI.title('Default Incoming Connections - FireFlower')
                        masterSSAI.geometry("200x350+100+100")
                        masterSSAI.configure(background='black')
                        masterSSAI.resizable(False,False)
                        SubnameI = tk.Label(masterSSAI,text="Incoming\nConnections",bg='black',fg='orange',anchor='n',font=('Algerian',20))
                        SubnameI.pack(pady=20)
                        allowB = tk.Button(masterSSAI,text='Allow',fg='white',bg='green',font=('ArialBlack',10,'bold'),command=lambda:updateIn('allow',masterSSAI))
                        allowB.pack(pady=5)
                        denyB = tk.Button(masterSSAI,text='Deny',fg='white',bg='red',font=('ArialBlack',10,'bold'),command=lambda:updateIn('deny',masterSSAI))
                        denyB.pack(pady=5)
                        rejectB = tk.Button(masterSSAI,text='Reject',fg='white',bg='orange',font=('ArialBlack',10,'bold'),command=lambda:updateIn('reject',masterSSAI))
                        rejectB.pack(pady=5)
                        routeB = tk.Button(masterSSAI,text='Route',fg='white',bg='orange',font=('ArialBlack',10,'bold'),command=lambda:updateIn('route',masterSSAI))
                        routeB.pack(pady=5)
                        limitB = tk.Button(masterSSAI,text='Limit',fg='white',bg='orange',font=('ArialBlack',10,'bold'),command=lambda:updateIn('limit',masterSSAI))
                        limitB.pack(pady=5)
                    else:
                        if par == 'allow':
                            incomingColor = 'green'
                            incomingText = 'incoming connections: ALLOWED!'
                        if par == 'deny':
                            incomingColor = 'red'
                            incomingText = 'incoming connections: DENY!'
                        if par == 'reject':
                            incomingColor = 'orange'
                            incomingText = 'incoming connections: ROUTED!'
                        if par == 'route':
                            incomingColor = 'orange'
                            incomingText = 'incoming connections: REJECT!'
                        if par == 'limit':
                            incomingColor = 'orange'
                            incomingText = 'incoming connections: LIMITED!'
                        ufw.default(incoming=par,outgoing=ufw.status()['default']['outgoing'],routed=ufw.status()['default']['routed'])
                        warnlabel = tk.Label(masterSSA,text="Incoming Connections Updated!",bg='black',fg='cyan',anchor='n',font=('Arial',10))
                        warnlabel.pack(pady=5)
                        masterSSAB.destroy()
                        masterSSA.after(2000, lambda: warnlabel.destroy())
                upin = tk.Button(masterSSA,text='incomingText',fg='white',bg='green',font=('ArialBlack',10,'bold'),command=lambda:updateIn())
                upin.pack(pady=5)
                def updateOut(par=' ',masterSSAB=''):
                    global outgoingColor
                    global outgoingText
                    if par == ' ':
                        masterSSAI = tk.Toplevel(masterSSA)
                        masterSSAI.title('Default Outgoing Connections - FireFlower')
                        masterSSAI.geometry("200x350+100+100")
                        masterSSAI.configure(background='black')
                        masterSSAI.resizable(False,False)
                        SubnameI = tk.Label(masterSSAI,text="Outgoing\nConnections",bg='black',fg='orange',anchor='n',font=('Algerian',20))
                        SubnameI.pack(pady=20)
                        allowB = tk.Button(masterSSAI,text='Allow',fg='white',bg='green',font=('ArialBlack',10,'bold'),command=lambda:updateOut('allow',masterSSAI))
                        allowB.pack(pady=5)
                        denyB = tk.Button(masterSSAI,text='Deny',fg='white',bg='red',font=('ArialBlack',10,'bold'),command=lambda:updateOut('deny',masterSSAI))
                        denyB.pack(pady=5)
                        rejectB = tk.Button(masterSSAI,text='Reject',fg='white',bg='orange',font=('ArialBlack',10,'bold'),command=lambda:updateOut('reject',masterSSAI))
                        rejectB.pack(pady=5)
                        routeB = tk.Button(masterSSAI,text='Route',fg='white',bg='orange',font=('ArialBlack',10,'bold'),command=lambda:updateOut('route',masterSSAI))
                        routeB.pack(pady=5)
                        limitB = tk.Button(masterSSAI,text='Limit',fg='white',bg='orange',font=('ArialBlack',10,'bold'),command=lambda:updateOut('limit',masterSSAI))
                        limitB.pack(pady=5)
                    else:
                        if par == 'allow':
                            outgoingColor = 'green'
                            outgoingText = 'incoming connections: ALLOWED!'
                        if par == 'deny':
                            outgoingColor = 'red'
                            outgoingText = 'incoming connections: DENY!'
                        if par == 'reject':
                            outgoingColor = 'orange'
                            outgoingText = 'incoming connections: ROUTED!'
                        if par == 'route':
                            outgoingColor = 'orange'
                            outgoingText = 'incoming connections: REJECT!'
                        if par == 'limit':
                            outgoingColor = 'orange'
                            outgoingText = 'incoming connections: LIMITED!'
                        ufw.default(incoming=ufw.status()['default']['incoming'],outgoing=par,routed=ufw.status()['default']['routed'])
                        warnlabel2 = tk.Label(masterSSA,text="Outgoing Connections Updated!",bg='black',fg='cyan',anchor='n',font=('Arial',10))
                        warnlabel2.pack(pady=5)
                        masterSSA.after(2000, lambda: warnlabel2.destroy())
                upout = tk.Button(masterSSA,text='outgoingText',fg='white',bg='red',font=('ArialBlack',10,'bold'),command=lambda:updateOut())
                upout.pack(pady=5)
                def updateRou(par=' ',masterSSAB=''):
                    global routedColor
                    global routedText
                    if par == ' ':
                        masterSSAI = tk.Toplevel(masterSSA)
                        masterSSAI.title('Default Routed Connections - FireFlower')
                        masterSSAI.geometry("200x350+100+100")
                        masterSSAI.configure(background='black')
                        masterSSAI.resizable(False,False)
                        SubnameI = tk.Label(masterSSAI,text="Routed\nConnections",bg='black',fg='orange',anchor='n',font=('Algerian',20))
                        SubnameI.pack(pady=20)
                        allowB = tk.Button(masterSSAI,text='Allow',fg='white',bg='green',font=('ArialBlack',10,'bold'),command=lambda:updateRou('allow',masterSSAI))
                        allowB.pack(pady=5)
                        denyB = tk.Button(masterSSAI,text='Deny',fg='white',bg='red',font=('ArialBlack',10,'bold'),command=lambda:updateRou('deny',masterSSAI))
                        denyB.pack(pady=5)
                        rejectB = tk.Button(masterSSAI,text='Reject',fg='white',bg='orange',font=('ArialBlack',10,'bold'),command=lambda:updateRou('reject',masterSSAI))
                        rejectB.pack(pady=5)
                        routeB = tk.Button(masterSSAI,text='Route',fg='white',bg='orange',font=('ArialBlack',10,'bold'),command=lambda:updateRou('route',masterSSAI))
                        routeB.pack(pady=5)
                        limitB = tk.Button(masterSSAI,text='Limit',fg='white',bg='orange',font=('ArialBlack',10,'bold'),command=lambda:updateRou('limit',masterSSAI))
                        limitB.pack(pady=5)
                    else:
                        if par == 'allow':
                            routedColor = 'green'
                            routedText = 'incoming connections: ALLOWED!'
                        if par == 'deny':
                            routedColor = 'red'
                            routedText = 'incoming connections: DENY!'
                        if par == 'reject':
                            routedColor = 'orange'
                            routedText = 'incoming connections: ROUTED!'
                        if par == 'route':
                            routedColor = 'orange'
                            routedText = 'incoming connections: REJECT!'
                        if par == 'limit':
                            routedColor = 'orange'
                            routedText = 'incoming connections: LIMITED!'
                        ufw.default(incoming=ufw.status()['default']['incoming'],outgoing=ufw.status()['default']['routed'],routed=par)
                    warnlabel3 = tk.Label(masterSSA,text="Routed Connections Updated!",bg='black',fg='cyan',anchor='n',font=('Arial',10))
                    warnlabel3.pack(pady=5)
                    masterSSA.after(2000, lambda: warnlabel3.destroy())
                uprou = tk.Button(masterSSA,text='routedText',fg='white',bg='orange',font=('ArialBlack',10,'bold'),command=lambda:updateRou())
                uprou.pack(pady=5)
        tk.Button(masterSS,text='Add a New Rule',fg='white',bg='green',font=('ArialBlack',10,'bold'),command=lambda:AddRule(master)).pack(pady=5)
        tk.Button(masterSS,text='Remove an Existing Rule',fg='white',bg='red',font=('ArialBlack',10,'bold'),command=lambda:RmRule(master)).pack(pady=5)
        tk.Button(masterSS,text='Change Default Rules',fg='white',bg='orange',font=('ArialBlack',10,'bold'),command=lambda:DefRule(master)).pack(pady=5)

class ResetFirewall:
    def __init__(self,master):
        masterSS = tk.Toplevel(master)
        masterSS.title('Reset Firewall - FireFlower')
        a = True
        i = 0
        while a or i<10:
            try:
                i+=1
                masterSS.iconbitmap('icon.ico')
                a = False
            except Exception:
                f = get('https://www.masteradon.altervista.org/img/fireflower.ico')
                open('icon.ico','wb').write(f.content)
        masterSS.configure(background='black')
        masterSS.geometry("650x400+100+100")
        masterSS.resizable(False,False)
        Subname = tk.Label(masterSS,text="Reset the Firewall",bg='black',fg='orange',anchor='n',font=('Algerian',20)).pack(pady=20)
        def totalFirewallReset():
            ufw.enable()
            ufw.reset()
            ufw.disable()
            ufw.enable()
            ufw.default(incoming='deny', outgoing='allow', routed='reject')
            tk.Label(masterSS,text="Total Reset Completed!",bg='black',fg='cyan',anchor='n',font=('Arial',10)).pack(pady=5)
        tk.Button(masterSS,text='Total Reset\n(erase every rule, also the default ones)',fg="white",bg="red",font=('ArialBlack',10,'bold'),command=lambda:totalFirewallReset()).pack(pady=10)
        def limFirewallReset():
            rules = ufw.status()['rules']
            for r in range(len(rules)):
                ufw.delete('*')
            tk.Label(masterSS,text="Every Rule Deleted!",bg='black',fg='cyan',anchor='n',font=('Arial',10)).pack(pady=5)
        tk.Button(masterSS,text='Delete every madeup rule\n(erase every rule except the default ones)',fg="white",bg="orange",font=('ArialBlack',10,'bold'),command=lambda:limFirewallReset()).pack(pady=10)
        def baseFirewallReset():
            rules = ufw.status()['rules']
            for r in range(len(rules)):
                if '80' in rules[r] or '8080' in rules[r] or '23' in rules[r] or '443' in rules[r] or '20' in rules[r] or '110' in rules[r] or '143' in rules[r] or '465' in rules[r] or '995' in rules[r] or '666' in rules[r]:
                    pass
                else:
                    ufw.delete(r)
            tk.Label(masterSS,text="Base Reset Completed!",bg='black',fg='cyan',anchor='n',font=('Arial',10)).pack(pady=5)
        tk.Button(masterSS,text='Base Reset\n(erase every rule except the ones for base services\n(80-8080,443,23 etc.) and the default ones)',fg="white",bg="green",font=('ArialBlack',10,'bold'),command=lambda:baseFirewallReset()).pack(pady=10)

class EnableDisable:
    def __init__(self,master):
        masterSS = tk.Toplevel(master)
        masterSS.title('Enable/Disable - FireFlower')
        a = True
        i = 0
        while a or i<10:
            try:
                i+=1
                masterSS.iconbitmap('icon.ico')
                a = False
            except Exception:
                f = get('https://www.masteradon.altervista.org/img/fireflower.ico')
                open('icon.ico','wb').write(f.content)
        masterSS.configure(background='black')
        masterSS.geometry("450x300+100+100")
        masterSS.resizable(False,False)
        Subname = tk.Label(masterSS,text="Enable/Disable Firewall",bg='black',fg='orange',anchor='n',font=('Algerian',20)).pack(pady=20)
        def refreshPage():
            masterSS.destroy()
            EnableDisable(master)
        tk.Button(masterSS,text='Refresh',fg='white',bg='blue',font=('ArialBlack',10,'bold'),command=lambda:refreshPage()).pack(pady=20)
        valid = ufw.status()['status']
        if valid == 'inactive':
            descr = tk.Label(masterSS,text="The Firewall is currenctly INACTIVE",bg='black',fg='magenta',anchor='n',font=('Arial',10)).pack(pady=10)
            def enable():
                ufw.enable()
                masterSS.destroy()
                EnableDisable(master)
            tk.Button(masterSS,text='Enable the Firewall',fg="white",bg="green",font=('ArialBlack',10,'bold'),command=lambda:enable()).pack(pady=10)
        else:
            descr = tk.Label(masterSS,text="The Firewall is ACTIVE",bg='black',fg='magenta',anchor='n',font=('Arial',10)).pack(pady=10)
            def disable():
                ufw.disable()
                masterSS.destroy()
                EnableDisable(master)
            tk.Button(masterSS,text='Disable the Firewall',fg="white",bg="red",font=('ArialBlack',10,'bold'),command=lambda:disable()).pack(pady=10)
        
class Main:
    def __init__(self, master):
        msg = "Hi User!\nThis is an easy software to manage your Linux's Firewall. It allows you to create new rules, delete old ones, check the current status and lots of other features! It's still in beta, so some error may occours, but you can signal them to me and i'll fix that. It works only on Linux! based on UFW and iptables;\nNB: This is a tool very easy to use, so it doesn't have every options of iptables. Soon i'll add the rules for IP address and group of ports and protocols. This is still a beta!\n"
        tst = "How does it works?"
        master.title("FireFlower - Firewall Manager")
        master.configure(background='black')
        master.geometry("500x400+200+200")
        master.resizable(False,False)
        self.master = master

        name = tk.Label(master,text="FireFlower",bg='black',fg='orange',anchor='n',font=('Algerian',30)).pack(pady=20)

        showS = tk.Button(master,text="Show Status",fg='white',bg='red',font=('ArialBlack',10,'bold'),command=lambda:ShowStatus(master)).pack(pady=10)

        editR = tk.Button(master,text="Edit the Rules",fg='white',bg='green',font=('ArialBlack',10,'bold'),command=lambda:EditR(master)).pack(pady=10)

        resetB = tk.Button(master,text="Reset Firewall",fg='white',bg='red',font=('ArialBlack',10,'bold'),command=lambda:ResetFirewall(master)).pack(pady=10)

        endis = tk.Button(master,text="Enable/Disable Firewall",fg='white',bg='green',font=('ArialBlack',10,'bold'),command=lambda:EnableDisable(master)).pack(pady=10)

        hdiw = tk.Button(master,text="How does it works?",fg='white',bg='red',font=('ArialBlack',10,'bold'),command=lambda:messagebox.showinfo(tst,msg)).pack(pady=10)

        exitB = tk.Button(master,text="   Exit   ",fg='white',bg='green',font=('ArialBlack',10,'bold'),command=lambda:exit(0)).pack(pady=10)

master = tk.Tk()
a = True
i = 0
while a or i<10:
    try:
        i+=1
        master.iconbitmap('icon.ico')
        a = False
    except Exception:
        f = get('https://www.masteradon.altervista.org/img/fireflower.ico')
        open('icon.ico','wb').write(f.content)
mt = Main(master)
master.mainloop()
