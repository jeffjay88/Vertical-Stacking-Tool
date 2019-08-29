#!/usr/bin/env python3

# -*- coding: utf-8 -*-
"""
Created on Monday August 19, 2019 20:50:00
@author: Jeffrey N. A. Aryee 
@email: jeff.jay8845@gmail.com
@package_name: 
@version:  1.0.0
"""

''' --> the # sign represents comment lines, and though are part of the program, they aren't executed.
        Those are just useful for the user. Also, to comment long sections, you use 3 opening and closing 
        inverted commas or quotation marks, as used for this part and the part above.


'''

import numpy as np         #Import Numerical Python Recipe
import numpy.random.common
import numpy.random.bounded_integers
import numpy.random.entropy


import os
import os.path            #To trace the path to our current directory
from os.path import basename   #Used to assess file name from its working directory, without including its directory and subdirectory names.
import glob               #used to access subdirectories
from datetime import date, datetime
from tkinter import *
from PIL import ImageTk, Image
import tkinter.messagebox as tkm
from tkinter import filedialog
import time





class VStack:
    ################################################################
    ###########  Simply Tweek Function on Date for Check    ######## 
    ################################################################        
    def coerce(b,x,a):
        try:
            if len(x)==a:
                return 'True'
            else:
                return 'False'
            
        except:
            raise ValueError("Wrong length of ",b,'. Must be length of ',a,'characters')


    def CheckOutFolder(file, out):
        global in_file, start_year, end_year
        file = file; out = out
        out_folder=in_file.get()+'/Output_'+str(date.today().strftime('%Y%m%d'))
        if not os.path.exists(out_folder):
            os.makedirs(out_folder)
        out[:,1:3]=np.int_(out[:,1:3])
        np.savetxt(out_folder+'/out_'+start_year.get()+'-'+end_year.get()+'_'+basename(file),out,fmt=['%s','%s','%s','%s','%s'],delimiter=',')
        #np.savetxt(out_folder+'/out_'+basename(file),out,fmt=['%s','%4.4d','%2.2d','%2.2d','%.1f'],delimiter=',')
        # Save the output to the output file contained in the Out folder, with the year, month and days formated as 
        #integers, and the data as real with 1 decimal place.                 
                

    
    def sort_stacked_data(s,app_file,yr_start,yr_end,miss_val):
        global out_code, list1
        y_m_d_data = np.asarray(app_file).T
        #print(np.shape(y_m_d_data))
        #print(y_m_d_data)
        station = str(s)[2:-1]    #save Station data from pp to variable "station"
        #variable=np.transpose(pp)[1]   #save parameter name from pp to variable "var"
        year=np.int_( y_m_d_data[0])       #save years [column 3] saved in pp to variable "year"
        month=np.int_( y_m_d_data[1])       #save month [column 4] saved in pp to variable "month"
        day=np.int_( y_m_d_data[2])        #save day [column 5] saved in pp to variable "day"
        
        
        count=0; out=[]
        for yy in range(yr_start,yr_end+1):     #loop through the years you want to vertically stack.
            print('Kindly Wait Patiently..... It will be completed soon.\n')
            print
            if (len(np.shape(y_m_d_data))>1):
                years=y_m_d_data[0]
                fin_data = y_m_d_data[:,years==yy]
            else:
                fin_data = y_m_d_data
            year=fin_data[0]; month=fin_data[1]; day=fin_data[2]; value=fin_data[3]

            for mm in range(1,13):              #loop through months 1 to 12.  (The 13 here limits it to 12.)
                if (mm==1 or mm==3 or mm==5 or mm==7 or mm==8 or mm==10 or mm==12):  # Condition for identifying number of days in a month.
                    days=31
                elif (mm==4 or mm==6 or mm==9 or mm==11):
                    days=30
                elif (mm==2):           # Condition for identifying number of days in February for both Ordinary and Leap years.
                    if (yy%4==0):       #  The % sign used here represents the modulos.
                        days=29
                    else:
                        days=28
     

                pr=[]                   #create empty arrays for appending data
                pr1=[]                  #create empty arrays for appending data
                for dd in range(1,days+1):      #After completing the condition for days in a month, you now loop through the days, from day 1 to the final day of each month.                    
                    if (year.size>0):
                        count+=1; inner_count=0   #count is to identify Null arrays, and inner_count is to avoid duplicating values which have been parsed under a meeting condition.
                        for i in range(year.size):      #Set an iterator for your data, and loop through the data   
                            if (year[i]==yy and month[i]==mm and day[i]==dd):   # Condition to retrieve data for looped years that tallies years within the data
                                p1=station,yy,mm,dd,value[i]                            #Assign those to p1 and append to pr
                                #print(p1)
                                #pr.append(p1)
                                out.append(p1)
                            else:
                                if (inner_count==year.size-1):
                                    p2=station,yy,mm,dd,miss_val                            #If there's no match, assign to p2 and append to pr1
                                    #print(p2)
                                    #pr1.append(p2)
                                    out.append(p2)
                                inner_count+=1
                    else:
                        if (count>=0):
                            p2=station,yy,mm,dd,miss_val
                            #print(p2)
                            #pr1.append(p2)
                            out.append(p2)
                                   
            print('Year '+np.str(yy)+' Completed for '+str(station))
            out_code='Year '+np.str(yy)+' Completed for '+str(station+'\n')
            VStack_GUI.TextUpdate(out_code)
        out=np.copy(out)
        return out




    def stacking(self):
        global start_year, end_year, missing_val, sta_column, year_col, in_file, num_hdr, out_code
        try:
            VStack.coerce('Start Year',start_year.get(),4)      #Check that start date is 4 characters long
            VStack.coerce('Start Year',end_year.get(),4)      #Check that end date is 4 characters long
            yr_start = np.int(start_year.get())
            yr_end = np.int(end_year.get())
            ### Check Missing Value
            try:
                miss_val = np.float(missing_val.get())
            except:
                miss_val = np.nan
            ### Check number of headers
            try:
                num_header = np.int(num_hdr.get())
            except:
                num_header=0
            y_col = np.int(year_col.get())
            sta_col = np.int(sta_column.get())
            path=in_file.get()
        except:
            out_code='One or more input arguments is/are wrong.\n'
            VStack_GUI.TextUpdate(out_code)
            
            pass
        else:
            out_code='Kindly Wait Patiently..... \nIt will be completed soon.\n'
            VStack_GUI.TextUpdate(out_code)
        ### First thing is to echo out the input of the user.
        print('Start-Year:',yr_start,'\n','End-Year:',yr_end,'\n','Year Column:',y_col)
        all_files=glob.glob(os.path.join(path, "*.csv"))    #Store all files ending in '.csv' to the variable all_files
        fin_out=[]   #Final Output
        for file in all_files:          #Loop through all selected files
            try:
                data = np.genfromtxt(file, delimiter=',', skip_header=num_header, missing_values=miss_val, filling_values=miss_val)  #import data, skipping the first line and indicating that each column is separated by commas
                string_input = np.genfromtxt(file, delimiter=',', skip_header=num_header, dtype=None, defaultfmt='%s', usecols=sta_col-1) 
                data=data[:,y_col-1:y_col+32]
                Station_Name=string_input[:]; #Var_Name=string_input[:,1]
                station=sorted(list(set(Station_Name)))         #Find the unique strings (stations) in the dataset.
                    
                #print(station)
                for s in station:
                    station_data=data[Station_Name==s,:]
                    
                    
                    #print(np.shape(station_data))
                    [i,j]=np.shape(station_data)   #Assign number of rows and columns to i and j respectively.
                    pp=[]               #create empty arrays for appending data
                    
                    for ii in range(i):     #loop through the rows
                         for jj in range(2,j):  #loop through the columns
                             p=station_data[ii,0],station_data[ii,1],jj-1, station_data[ii,jj]     #save found data as p and append to pp.
                             pp.append(p)
                             
                    p=VStack.sort_stacked_data(s,pp,yr_start,yr_end,miss_val)      #Call the sort_stacked function on the station name and the appended data.
                    col_fin=np.shape(p)[1]
                    fin_out.append(np.ravel(p))
                fin_out=np.copy(fin_out)
                
                final_output=[]
                for i in range(fin_out.shape[0]):
                    for j in range(np.size(fin_out[i])):
                        final_output.append((fin_out[i])[j]) 
                        
                final_output=np.copy(final_output)
                final_output=np.reshape(final_output, newshape=(final_output.size//col_fin,col_fin))
                VStack.CheckOutFolder(file,final_output)
                
                #os.system("clear") 
                
                 
            except ImportError:
                out_code='Check the data structure in the input file "'+file+'" \n'
                VStack_GUI.TextUpdate(out_code)
            else:
                out_code='Programme run successfully. \n'
                VStack_GUI.TextUpdate(out_code)
              
                
        print('\n\nStacking Completed.... Thanks For Using The GyerphStack Timeseries Stacking Tool. Looking forward to your kind Reviews and Sharing of The Tool.')
        print("Protected by Copyright Law. Do not reproduce or use for commercial purpose without author's consent.")
        out_code="Stacking Completed.... Thanks For Using The GyerphStack Timeseries Stacking Tool. Looking forward to your kind Reviews and Sharing of The Tool. \n\nProtected by Copyright Law. Do not reproduce or use for commercial purpose without author's consent."        
        VStack_GUI.TextUpdate(out_code)







     
#############################################################################################            
#############################################################################################            
#################                                            ################################
#################               MAIN SCRIPT                  ################################
#################                                            ################################
#############################################################################################        
#############################################################################################
def StackTool(event):
    print('\nVStack Tool | Designed and Maintained by Jeffrey N. A. Aryee. \nContact via mail at jeff.jay8845@gmail.com. \n\n' )
    VStack.stacking()    
    
    


#############################################################################################            
#############################################################################################            
#################                                            ################################
#################                   THE GUI                  ################################
#################                                            ################################
#############################################################################################        
#############################################################################################

class VStack_GUI:
    global update_time        
    def update_time():
        # get current date & time as text
        current = datetime.now().strftime('%A, %d-%B-%Y\n%H:%M:%S')
        # update label with current date and time
        label['text'] = '\t\t\t\t\t\t\t  '+current
        # run update_time again after 200ms (0.2s)
        try:
            root.after(200, update_time)
        except:
            pass

    
    ################################################################
    ###########         Software Interface                  ######## 
    ################################################################       
    def __init__(self, master):
        global start_year, end_year, missing_val, sta_column, year_col, in_file, num_hdr, label, out_code, list1
        
        self.s1=None
        menuframe = Frame(master)
        menuframe.pack()
        dateframe = Frame(master)
        dateframe.pack()
        topframe = Frame(master)
        topframe.pack()
        bottomframe = Frame(master)
        bottomframe.pack()
        extraframe = Frame(master)
        extraframe.pack()
        
        
        #Create Topmenu
        menu = Menu(menuframe)
        root.config(menu=menu)
        
        subMenu1 = Menu(menu)
        menu.add_cascade(label="File", menu=subMenu1)
        subMenu1.add_command(label="Input Folder", command=self.file_found_menu)
        #subMenu1.add_separator() 
        #subMenu1.add_command(label="Refresh", command=Actions.restart)
        subMenu1.add_separator() 
        menu.config(font=("Sans", 11, "bold"))
        
        menu.add_command(label="Help", command=self.help)
        menu.add_command(label="Exit", command=self.onExit)
        
        #Clock Area
        label = Label(dateframe, fg='white', bg='black', width=137, justify='right')
        label.grid(row=1, column=1, sticky='e,w')  
        update_time()
        label.config(font=("Sans", 11, "bold"))
        
        #Display Image on Foreground
        img = Image.open("banner.jpg")
        img= ImageTk.PhotoImage(img.resize((615,375), resample=0))
        imglabel = Label(topframe, image=img, fg='white', text="\n\n\n\n\n\n\n\n\n\n\n ...stack meteorological data with ease", compound='center', width=650, height=255)
        imglabel.image = img
        imglabel.grid(row=2, column=0, columnspan=4, rowspan=7)
        imglabel.config(font=("Sans", 12, "bold italic"))
        
        #Define ListBox
        #list=scrolledtext.ScrolledText(window, width=40,height=10)
        text_var="Glad you chose to use the Vertical Stacking Tool v1.0.0 \nAll items in red are necessary. Others are optional. Default missing values (if not stated) is \nNaN, and default number of headers is 0. Have a great time data-stacking. \n\n"
        list1=Text(topframe, height=3, width=77)
        list1.grid(row=9, column=0, columnspan=4, rowspan=1)  
        list1.insert(INSERT, text_var)
        
        list1.tag_add("here", "1.0", "1.70")
        list1.tag_add("start", "2.0", "5.0")
        list1.tag_config("here", background="white", foreground="red",font=("Sans", 13, "bold"))
        list1.tag_config("start", background="white", foreground="black",font=("Times", 11, "bold"))
        sb1=Scrollbar(topframe, width=22)
        sb1.grid(row=9, column=3, rowspan=1, sticky='n,e')        
        list1.configure(yscrollcommand=sb1.set)
        sb1.configure(command=list1.yview)
        list1.config(font=("Times", 11, "bold"))
        
        #400
        
        '''termf = Label(topframe, height=5, width=100)
        termf.grid(row=7, column=1, columnspan=5, rowspan=2, sticky='w') 
        #termf.pack(fill=BOTH, expand=YES)
        wid = termf.winfo_id()
        print(wid)
        os.system('xterm -into %d -geometry 100x20 -sb &' % wid)
        '''
        
        #Right side Information Required
        l1=Label(topframe, text="  Input Folder: ", fg='red', justify='right')
        l1.grid(row=2, column=6, sticky='w')          
        l1.config(font=("Sans", 11, "bold"))
        l1=Label(topframe, text="  Start Year: ", fg='red')
        l1.grid(row=3, column=6, sticky='w')                  
        l1.config(font=("Sans", 11, "bold"))
        l1=Label(topframe, text="  End Year: ", fg='red')
        l1.grid(row=4, column=6, sticky='w')                   
        l1.config(font=("Sans", 11, "bold"))
        l1=Label(topframe, text="  Year Column: ", fg='red')
        l1.grid(row=5, column=6, sticky='w')                
        l1.config(font=("Sans", 11, "bold"))
        l1=Label(topframe, text="  Station Column: ", fg='red')
        l1.grid(row=6, column=6, sticky='w')               
        l1.config(font=("Sans", 11, "bold"))    
        '''l1=Label(topframe, text="  Station Type Column: ", fg='red')
        l1.grid(row=6, column=6, sticky='w')               
        l1.config(font=("Sans", 11, "bold"))       '''
        l1=Label(topframe, text="  Missing Values: ")
        l1.grid(row=7, column=6, sticky='w')                 
        l1.config(font=("Sans", 11, "bold")) 
        l1=Label(topframe, text="  # of Headers: ")
        l1.grid(row=8, column=6, sticky='w')                
        l1.config(font=("Sans", 11, "bold"))
        
        
        l1=Label(topframe, text="", fg='red', justify='right')
        l1.grid(row=1, column=8, sticky='w')          
        l1.config(font=("Sans", 11, "bold"))

        #Define Right-Side Entries
        in_file=StringVar()         #### Input Folder Variable
        in_file.set("select folder...")
        e1=Entry(topframe,textvariable=in_file, width=18)
        e1.grid(row=2, column=7, sticky='w')#
        e1.bind("<Button-1>", self.file_found)
        
        start_year=StringVar()
        start_year.set(datetime.now().strftime('%Y'))
        spin = Spinbox(topframe, textvariable=start_year, from_=1900, to=datetime.now().strftime('%Y'), width=4).grid(row=3, column=7, sticky='w')
        end_year=StringVar()
        end_year.set(datetime.now().strftime('%Y'))
        spin = Spinbox(topframe, textvariable=end_year, from_=1900, to=datetime.now().strftime('%Y'), width=4).grid(row=4, column=7, sticky='w')
        year_col=StringVar()
        Entry(topframe,textvariable=year_col, width=6).grid(row=5, column=7, sticky='w')        
        sta_column=StringVar()
        Entry(topframe,textvariable=sta_column, width=6).grid(row=6, column=7, sticky='w')         
        '''type_column=StringVar()
        Entry(topframe,textvariable=type_column, width=6).grid(row=6, column=7, sticky='w')         '''
        missing_val=StringVar()
        Entry(topframe,textvariable=missing_val, width=6).grid(row=7, column=7, sticky='w')         
        num_hdr=StringVar()
        Entry(topframe,textvariable=num_hdr, width=6).grid(row=8, column=7, sticky='w') 
        b1=Button(topframe, text="Stack Data", fg='blue', width=20, padx=10,activebackground='red',activeforeground='white', relief='raised')
        b1.grid(row=9, column=6,  columnspan=2)   
        b1.bind("<Button-1>", VStack.stacking) 
        #b1.bind("<Leave>", self.status)         #To fix Status Bar
        #b1.bind("<Enter>", self.displayValidity) 
        b1.config(font=("Sans", 12, "bold"))
        
        #l1=Label(topframe, text="\t All items in red are necessary. Others are optional", fg='blue')
        #l1.grid(row=9, column=0,  columnspan=6,  sticky='w')   
        #l1.config(font=("Sans", 10, "bold"))


        l1=Label(bottomframe, text=" (c) 2019 Gyerph Technologies Inc.    |    Developed by Jeffrey N. A. Aryee \nAll Rights Reserved.", bg='black', fg='white', width=150)
        l1.pack(side=BOTTOM, fill=X)  
        l1.config(font=("Sans", 10, "bold"))
        





    def status(event, self):
        var=StringVar()
        var.set("Close")
        s1=Label(root, textvariable=var, bd=1, relief=SUNKEN, anchor=W).pack(side=BOTTOM, fill=X)
        var.set('')
        
    def clear_status(event, self):
        var=StringVar()
        var.set("Open")
        s1=Label(root, textvariable=var, bd=1, relief=SUNKEN, anchor=W).pack(side=BOTTOM, fill=X)
        var.set('')
        
        
    def TextUpdate(text_var):
        #self.text_var = text_var
        list1.insert(END, ' >> '+text_var)
        list1.see("end")
        
        
        
  
    ################################################################
    ###########         Exit Function                       ########
    ################################################################
    def onExit(self):
            answer=tkm.askquestion('Exit Vertical Stacking Tool', 'Do you want to close the application?')
            if answer == 'yes':
                root.destroy()
                
                
    ################################################################
    ###########         Help Function                       ######## 
    ################################################################
    def help(self):
        tkm.showinfo('Help!','Need assistance with any aspect of the Vertical Stacking Tool. Contact us via email at jeff.jay8845@gmail.com')


    ################################################################
    ###########         Input Folder Function               ######## 
    ################################################################
    def file_found(self, event):
        global in_file
        in_file.set(filedialog.askdirectory(title='Select Input Data Directory'))
     
    def file_found_menu(self):
        global in_file
        in_file.set(filedialog.askdirectory(title='Select Input Data Directory'))
                    



class Actions:
    def restart():
        #CloseWindow()
        Actions.RefreshAction()
    
    def RefreshAction():
        os.execl(sys.executable, *([sys.executable]+sys.argv))
        
        
    #if __name__ == '__main__':
    def refresh():
        root.destroy()
        VStack_GUI(root)


    
    
if __name__ == '__main__':
    root = Tk()
    root.title('Vertical Stacking Tool v1.0.0')
    root.resizable(width=False, height=False)
    root.configure(background='#c98')
    jay = VStack_GUI(root)
    root.geometry("1000x422+80+20")
    root.iconbitmap('py-VStack.ico')
    root.mainloop()

