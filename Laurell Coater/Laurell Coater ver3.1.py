from Tkinter import *
import serial
import time
import tkMessageBox
import csv
import serial.tools.list_ports

######################################################################
class MyApp(object):
    """"""
    
#---------------------------------------------------------------------
    def __init__(self,Laurell):
        """initialize porgram and all"""
        self.root =  Laurell
        root.title("Laurel Coater")
        init = Text(root, height = 3, width = 30)
        init.pack()
        init.insert(END, "Welcome to the Laurell Coater Program Version 3.1"
                    + "\nPress OK to start")
        initbutton = Button(root, text="OK", command=self.transition, height = 5,
                       width = 10)
        initbutton.pack()

#---------------------------------------------------------------------
    def transition(self):
        self.hide()
        self.waferchoice()

#---------------------------------------------------------------------
    def transition2(self, parent):
        parent.destroy()
        self.waferchoice()

#---------------------------------------------------------------------
    def transition3(self, option, relaysused):
        option.destroy()
        self.constructor(relaysused)

#---------------------------------------------------------------------
    def waferchoice(self):
        """Choose wafer size 200mm/300mm"""
        option = Toplevel()
        option.title("Laurell Coater")
        option.geometry("300x75")
        labelframe = LabelFrame(option,text = "Choose wether you are running "
                                + "one or both relays:")
        labelframe.pack(fill="both", expand="yes")
        start1relay = lambda *args: self.transition3(option, 1)
        start2relay = lambda *args: self.transition3(option, 2) 
        relayone = Button(labelframe, text="Mono Relay", command = start1relay, height = 1,
                       width = 10)
        relayone.pack()
        relaytwo = Button(labelframe, text="Dual Relays", command = start2relay, height = 1,
                       width = 10)
        relaytwo.pack()

#---------------------------------------------------------------------
    def constructor(self, relaysused):
        """Constructor"""
        print (relaysused)
        parent = Toplevel()
        parent.title("Laurell Coater")
        parent.geometry("280x425")
        labelframe1 = LabelFrame(parent, text="Preperations for coating substrates:")
        labelframe1.pack(fill="both", expand="yes")
        global Process
        Process = IntVar()
        r1 = Radiobutton(labelframe1, text="Wet the lines", variable=Process,
                         value=0)
        r2 = Radiobutton(labelframe1, text="CNT flow rate check",
                         variable=Process, value=1)
        r3 = Radiobutton(labelframe1, text="Water dispense flow rate check"
                         , variable=Process, value=2)
        r4 = Radiobutton(labelframe1, text="Charge the lines", variable=Process,
                         value=3)
        r5 = Radiobutton(labelframe1, text="1x Coat", variable=Process, value=4)

        labelframe2 = LabelFrame(parent, text="Procedures for cleaning the line:")
        labelframe2.pack(fill="both", expand="yes")
        r7 = Radiobutton(labelframe2, text="1st Water rinse", variable=Process,
                         value=6)
        r8 = Radiobutton(labelframe2, text="Base rinse", variable=Process,
                         value=7)
        r9 = Radiobutton(labelframe2, text="2nd Water rinse", variable=Process,
                         value=8)
        r10 = Radiobutton(labelframe2, text="Blow Dry (only at end of the day)",
                          variable=Process, value=9)
        labelframe3 = LabelFrame(parent, text="Special procedures:")
        labelframe3.pack(fill="both", expand="yes")
        r6 = Radiobutton(labelframe3, text="1x Hand Coat", variable=Process, value=5)
        r11 = Radiobutton(labelframe3, text="3% NH4OH treatment", variable=Process,
                          value=10)
        r12 = Radiobutton(labelframe3, text="Wafer DIW rinse and spin dry",
                          variable=Process, value=11)
        r1.grid(row=1,column=1,sticky = W)
        r2.grid(row=3,column=1,sticky = W)
        r3.grid(row=2,column=1,sticky = W)
        r4.grid(row=4,column=1,sticky = W)
        r5.grid(row=5,column=1,sticky = W)
        r6.grid(row=12,column=1,sticky = W)
        r7.grid(row=6,column=1,sticky = W)
        r8.grid(row=7,column=1,sticky = W)
        r9.grid(row=8,column=1,sticky = W)
        r10.grid(row=9,column=1,sticky = W)
        r11.grid(row=10,column=1,sticky = W)
        r12.grid(row=11,column=1,sticky = W)
        gopassword = lambda *args: self.password(parent, relaysused)
        goexecute = lambda *args: self.execute(parent, relaysused)
        changerelaynumber = lambda *args: self.transition2(parent)
        master_button = Button(labelframe3,text ="Master Mode", command = gopassword,
                               height = 1, width = 12)
        submit_button = Button(labelframe3,text ="Submit",command = goexecute,
                               height = 1, width = 12)
        option_button = Button(labelframe3, text ="Relay Mode",
                               command = changerelaynumber, height = 1, width = 12)
        exit_button = Button(labelframe3, text ="Exit", fg = "red",
                             command = self.exit_program, height = 1, width = 12)
        master_button.grid(row =13, column =1,sticky = W)
        submit_button.grid(row =13, column =2,sticky = W)
        option_button.grid(row =14, column =1,sticky = W)
        exit_button.grid(row =14, column =2,sticky = W)

#----------------------------------------------------------------------
    def exit_program(self):
        """close program"""
        exit()

#----------------------------------------------------------------------
    def Exit(self, custom, relaysused):
        """close program"""
        custom.destroy()
        self.constructor(relaysused)

#----------------------------------------------------------------------
    def password(self, parent, relaysused):
        """Attempt to enter Master Mode"""
        parent.destroy()
        password = Toplevel()
        password.geometry("300x75")
        password.title("Laurell Coater")
        labelframe = LabelFrame(password,text = "Enter Master Mode's password")
        labelframe.pack(fill="both", expand="yes")
        password.PASS = Entry(labelframe, show="*")
        password.PASS.grid(row = 1, column = 1, sticky = W)
        Validate = lambda *args: self.validate(password, parent, relaysused)
        unValidate = lambda *args: self.unvalidate(password, relaysused)
        password.submit_button = Button(labelframe, text="Log in", command = Validate)
        password.submit_button.grid(row = 2, column = 2, sticky =  W)
        password.cancel = Button(labelframe, text="Cancel", command = unValidate)
        password.cancel.grid(row = 2, column = 1, sticky =  W)

#----------------------------------------------------------------------
    def unvalidate(self, password, relaysused):
        """exit master mode"""
        password.destroy()
        self.constructor(relaysused)
        
#----------------------------------------------------------------------
    def validate(self, password, parent, relaysused):
        """validate password and log in"""
        if(password.PASS.get() == "Boss"):
            password.destroy()
            tkMessageBox.showinfo("Laurell coater","Log on successful!")
            self.custom(relaysused)
        else:
            password.destroy()
            tkMessageBox.showinfo("Laurell coater","Log on Failed. Try again.")
            self.password(parent, relaysused)

#----------------------------------------------------------------------
    def custom(self, relaysused):
        """Custom Laurell Timers"""
        self.hide()
        Custom =  Toplevel()
        Custom.geometry("300x175")
        Custom.title("Laurell Coater")
        labelframe = LabelFrame(Custom, text = "Input your custom timers")
        labelframe.pack(fill="both", expand="yes")
        Custom.instruction0 = Label(labelframe,text = "Pre-Wet Delay")
        Custom.instruction0.grid(row = 1,column = 1, sticky = W)
        Custom.instruction1 = Label(labelframe,text = "Pre-Wet")
        Custom.instruction1.grid(row = 2,column = 1, sticky = W)
        Custom.instruction2 = Label(labelframe,text = "Pre-Wet/CNT Delay")
        Custom.instruction2.grid(row = 3,column = 1, sticky = W)
        Custom.instruction3 = Label(labelframe,text = "CNT Dispense")
        Custom.instruction3.grid(row = 4,column = 1, sticky = W)
        Custom.instruction4 = Label(labelframe,text = "Repetions")
        Custom.instruction4.grid(row = 5,column = 1, sticky = W)
        Custom.instruction5 = Label(labelframe,text = "Delay")
        Custom.instruction5.grid(row = 6,column = 1, sticky = W)
        Custom.Predel = Entry(labelframe)
        Custom.Predel.grid(row = 1,column = 2, sticky = W)
        Custom.Predel.insert(0,"0")
        Custom.Pre = Entry(labelframe)
        Custom.Pre.grid(row = 2,column = 2, sticky = W)
        Custom.Pre.insert(0,"5000")
        Custom.CNTdel = Entry(labelframe)
        Custom.CNTdel.grid(row = 3,column = 2, sticky = W)
        Custom.CNTdel.insert(0,"2300")
        Custom.CNT = Entry(labelframe)
        Custom.CNT.grid(row = 4,column = 2, sticky = W)
        Custom.CNT.insert(0,"4670")
        Custom.Rep = Entry(labelframe)
        Custom.Rep.grid(row = 5,column = 2, sticky = W)
        Custom.Rep.insert(0,"1")
        Custom.Delay = Entry(labelframe)
        Custom.Delay.grid(row = 6,column = 2, sticky = W)
        Custom.Delay.insert(0,"5000")
        customexecute = lambda *args: self.customaction(Custom, relaysused)
        Custom.submit_button = Button(labelframe, text="Submit", command = customexecute)
        Custom.submit_button.grid(row = 7, column = 3, columnspan = 2, sticky = W)
        exitcommand = lambda *args: self.Exit(Custom, relaysused)
        Custom.cancel = Button(labelframe, text="Cancel", command = exitcommand)
        Custom.cancel.grid(row = 7, column = 2, sticky = W)
        Custom.mainloop()

#----------------------------------------------------------------------
    def customaction(self, Custom, relaysused):
        """Custom execute Laurell Timers"""
        predel = Custom.Predel.get()
        if (int(predel) < 1000):
            predel = int(predel)*1000
        pre = Custom.Pre.get()
        if (int(pre) < 1000):
            pre = int(pre)*1000
        CNTDel = Custom.CNTdel.get()
        if (int(CNTDel) < 1000):
            CNTDel = int(CNTDel)*1000
        cnt = Custom.CNT.get()
        if (int(cnt) < 1000):
            cnt = int(cnt)*1000
        rep = Custom.Rep.get()
        delay = Custom.Delay.get()
        if (int(delay) < 1000):
            delay = int(delay)*1000
        Custom.destroy()
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if "Arduino" in p[1]:
                port = "\\\\.\\" + str(p[0])
        #open serial
        ser = serial.Serial(port,9600)
        time.sleep(2)
        string = (str(relaysused)+","+str(predel)+","+str(pre)+","+str(CNTDel)+","+str(cnt)+","+str(rep)+","+str(delay))
        print(string + "\n")
        #send data
        ser.write(string)
        Message = ("You are performing a custom run!\n\nPlease pay attention to "
                   + "the system while it is working and make sure all preperations"
                   + " are made and ready.\n\nPress Yes to continue.")
        if (tkMessageBox.askyesno("Custom",Message) == True):
            #send start
            ser.write("1\n")
            #actions
            reps = int(rep)
            while (reps>0):
                extra = Toplevel()
                extra.title("Laurell Coater")
                extra.geometry("100x50")
                text = Text(extra)
                text.insert(INSERT, "Step: " + str(int(rep)-reps+1))
                text.pack()
                print(ser.readline()) #opertaion being started
                if (pre > 0):
                    print(ser.readline()) #Prewet 1 ON
                print(ser.readline()) #CNT Dispense OFF
                print(ser.readline()) #Prewet Dispense Time (ms):
                print(ser.readline()) #Prewet 1 Off
                if (cnt > 0):
                    print(ser.readline()) #CNT Dispense ON
                    print(ser.readline()) #CNT Dispense Time (ms):
                print(ser.readline()) #CNT Dispense OFF
                reps = reps - 1
                if(reps > 1):
                    wait = int(delay)*0.001 - 0.5
                    print(str(wait) + "\n")
                    time.sleep(wait)
                extra.destroy()
            tkMessageBox.showinfo("Laurell coater",ser.readline())
            ser.close()
            self.custom(relaysused)
        
#----------------------------------------------------------------------
    def execute(self, parent, relaysused):
        parent.destroy()
        times=[]
        print("Procedure " + str(Process.get()) + " Selected")
        if (Process.get() == 0):
            filename = "Wet lines.csv"
        elif (Process.get() == 1):
            filename = "CNT Flow Rate.csv"
        elif (Process.get() == 2):
            filename = "Water Flow Rate.csv"
        elif (Process.get() == 3):
            filename = "Charge Line.csv"
        elif (Process.get() == 4):
            filename = "1x Coat.csv"
        elif (Process.get() == 5):
            filename = "1x Hand Coat.csv"
        elif (Process.get() == 6):
            filename = "Water Rinse.csv"
        elif (Process.get() == 8):
            filename = "Water Rinse.csv"
        elif (Process.get() == 7):
            filename = "Base Rinse.csv"
        elif (Process.get() == 9):
            filename = "Blow Dry.csv"
        elif (Process.get() == 10):
            filename = "NH4OH Treatment.csv"
        elif (Process.get() == 11):
            filename = "Wafer Rinse.csv"
        else:
            tkMessageBox.showinfo("Luarell coater","Incorrect Process")
        with open (filename, 'rb') as csvfile:
            reader=csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in reader:
                line = str(row)
                variables = line.split(",")[1]
                t_variables = variables.translate(None, "[']")
                if t_variables[0] == '"':
                    t_variables = t_variables[1:]
                times.append(str(t_variables))
        print(str(times))
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if "Arduino" in p[1]:
                port = "\\\\.\\" + str(p[0])
        #open serial
        ser = serial.Serial(port,9600)
        time.sleep(2)
        string = str(relaysused) + "," + str(times[0]) + "," + str(times[1]) + "," +  str(times[2]) + "," +  str(times[3]) + "," +  str(times[4] + "," + str(times[5]))
        print(string + "\n")
        #send data
        ser.write(string)
        if (filename == "1x Coat.csv" or filename == "1x Hand Coat.csv"):
            Message= ("Important Notice:\n\n 1) If running a 6-inch wafer change "
            + "the Laurell program to be 6\n 2) if running an 8-Inch wafer:\n"
            + "\t a) if OD is higher than 30 run Laurell program 13\n \t b) if OD" 
            + "is less run Laurell program 14\n 3) If Hand dispensing reduce "
            + "the time of step 4 by 1 second on Program 6, 13 and 14\n\n Press Yes to start"
            + " and No to return to the main menu")
            if (tkMessageBox.askyesno(filename[:-4],Message) == True):
                print(str(filename))
                #send Start
                ser.write("1\n")
                #actions
                extra = Toplevel()
                extra.title("Laurell Coater")
                extra.geometry("200x35")
                text = Text(extra)
                text.insert(INSERT, "Dispensing")
                text.pack()
                print(ser.readline()) #opertaion being started
                print(ser.readline()) #Prewet 1 ON
                print(ser.readline()) #CNT Dispense OFF
                print(ser.readline()) #Prewet Dispense Time (ms):
                print(ser.readline()) #Prewet 1 Off
                if (times[3] > "0"):
                    print(ser.readline()) #CNT Dispense ON
                    print(ser.readline()) #CNT Dispense Time (ms):
                print(ser.readline()) #CNT Dispense OFF
                extra.destroy()
                tkMessageBox.showinfo("Laurell coater",ser.readline())
                ser.close()
        else:
            if (filename == "Water Rinse.csv"):
                Message = ("After the first dispense remember to swap the N2 bottle "
                       + " with the 2nd DiW bottle.\nOnce the 2nd bottle is empty, "
                       + "it is prefered that you swap the empty DiW bottle with "
                       + "the previous N2 bottle to decrease water condensation "
                       + "in the lines")
                if (tkMessageBox.askyesno(filename[:-4],Message) == True):
                    print(str(filename))
                    #send Start
                    ser.write("1\n")
                    #actions
                    reps = int(times[4])
                    while (reps>0):
                        extra = Toplevel()
                        extra.title("Laurell Coater")
                        extra.geometry("100x50")
                        text = Text(extra)
                        text.insert(INSERT, "Step: " + str(int(times[4])-reps+1))
                        text.pack()
                        print(ser.readline()) #opertaion being started
                        print(ser.readline()) #CNT Dispense OFF
                        print(ser.readline()) #Prewet Dispense Time (ms):
                        print(ser.readline()) #Prewet 1 Off
                        print(ser.readline()) #CNT Dispense ON
                        print(ser.readline()) #CNT Dispense Time (ms):
                        print(ser.readline()) #CNT Dispense OFF
                        reps = reps - 1
                        if (reps > 1):
                            wait = int(times[5])*0.001 - 0.5
                            print(str(wait) + "\n")
                            time.sleep(wait)
                        extra.destroy()
                    tkMessageBox.showinfo("Laurell coater",ser.readline())
                    ser.close()
            else:
                if (tkMessageBox.askyesno(filename[:-4],"Press Yes to start") == True):
                    #send start
                    print(str(filename))
                    ser.write("1\n")
                    #actions
                    reps = int(times[4])
                    while (reps>0):
                        extra = Toplevel()
                        extra.title("Laurell Coater")
                        extra.geometry("100x50")
                        text = Text(extra)
                        text.insert(INSERT, "Step: " + str(int(times[4])-reps+1))
                        text.pack()
                        print(ser.readline()) #opertaion being started
                        if (times[1] != "0"):
                            print(ser.readline()) #Prewet 1 ON
                        print(ser.readline()) #CNT Dispense OFF
                        print(ser.readline()) #Prewet Dispense Time (ms):
                        print(ser.readline()) #Prewet 1 Off
                        if (times[3] != "0"):
                            print(ser.readline()) #CNT Dispense ON
                            print(ser.readline()) #CNT Dispense Time (ms):
                        print(ser.readline()) #CNT Dispense OFF
                        reps = reps - 1
                        if(reps > 1):
                            wait = int(times[5])*0.001 - 0.5
                            print(str(wait) + "\n")
                            time.sleep(wait)
                        extra.destroy()
                    tkMessageBox.showinfo("Laurell coater",ser.readline())
                    ser.close()
        self.constructor(relaysused)
        
#----------------------------------------------------------------------
    def hide(self):
        """Hide the main window"""
        self.root.withdraw()

#----------------------------------------------------------------------
    def show(self):
        """Reshow the main window"""
        self.root.update()
        self.root.deiconify()

        
if __name__ == "__main__":
    root = Tk()
    root.geometry("300x100")
    app = MyApp(root)
    root.mainloop()
