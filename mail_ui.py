from calendar import Calendar
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
from turtle import bgcolor, onclick
from tkcalendar import DateEntry
from datetime import date


from mail_setup import *
from mail_functions import StartDriver, AccessMail, AccessMailFolder, CollectExcelList
tooltips = Objects.data["tooltips"]

'''
    Reference: 
        https://www.delftstack.com/tutorial/tkinter-tutorial/tkinter-message-box/
        https://www.delftstack.com/tutorial/tkinter-tutorial/tkinter-scrollbar/

'''

def StartFunction():
    # >>> Data for log in <<<
    domain_name = domain_text.get()
    id = id_text.get()
    pw = pw_text.get()

    # >>> List of folders can be selected for running test <<<
    #               type = bool
    all_folders_value = all_folders.get()
    inbox_value = inbox.get()
    folders_value = folders.get()
    shared_value = shared.get()
    spam_value = spam.get()
    fetching_value = fetching.get()
    
    folder_dict = {
        "Inbox": inbox_value,
        "Folders": folders_value,
        "Shared": shared_value,
        "Spam": spam_value,
        "Fetching": fetching_value
    }

    # >>> List of folders can be selected for running test <<<
    selected_folders = []
    for folder_name in folder_dict.keys():
        if folder_dict[folder_name] == True:
            selected_folders.append(folder_name)

    # >>> This function is under development <<<
    #               type = int 
    options_value = options_var.get()

    page_unread_dict = {}

    # >>>>> Groupware function at Mail menu <<<<<
    domain = "https://%s/ngw/app/#" % domain_name
    driver = StartDriver()
    AccessMail(domain, id, pw)
    
    global folder_page_unread
    folder_page_unread = {}
	
    for selected_folder in selected_folders:
        folder_page_unread.update({selected_folder: {}})
        page_unread_dict = AccessMailFolder(selected_folder)
        folder_page_unread[selected_folder] = page_unread_dict

    # >>>> Handler - After mail execution finished, list of result data will be shown in this module <<<<
    HandlerBar()

    #InsertLog() 

    driver.close()

def Messages(status):
    if status == "pass":
        msg = "Execution is executed successfully."
    else:
        #Logs.CreateFailLog()
        msg = "There is an error while executing. Please run again or report your issue."

    showinfo(title='Information', message=msg)    

def RemoveTextDomain(event):
    domain_value_text = domain_text.get()
    if domain_value_text == tooltips["domain"]:
        domain_value.delete(0, END)
        domain_value.config(foreground="#000000")

def RemoveTextId(event):
    id_value_text =  id_text.get()
    if id_value_text == tooltips["id"]:
        id_value.delete(0, END)
        id_value.config(foreground="#000000")

def RemoveTextPw(event):
    pw_value_text = pw_text.get()
    if pw_value_text == tooltips["pw"]:
        pw_value.delete(0, END)
        pw_value.config(foreground="#000000")

def ShowTextDomain(event):
    domain_value.config(state=NORMAL)
    domain_value_text = domain_text.get()

    if bool(domain_value_text) == False:
        domain_value.insert(0, "Domain name")
        domain_value.config(foreground="#d3d3d3")

def ShowTextId(event):
    id_value.config(state=NORMAL)
    id_value_text =  id_text.get()

    if bool(id_value_text) == False:
        id_value.insert(0, "User id for login")
        id_value.config(foreground="#d3d3d3")

def ShowTextPw(event):
    pw_value.config(state=NORMAL)
    pw_value_text = pw_text.get()

    if bool(pw_value_text) == False:
        pw_value.insert(0, "User pw for login")
        pw_value.config(foreground="#d3d3d3")

def CheckboxAll():
    checkbox_list = [inbox_checkbox, folders_checkbox, shared_checkbox, fetching_checkbox, spam_checkbox]
    for checkbox in checkbox_list:
        if all_folders.get() == True:
            checkbox.select()
        else:
            checkbox.deselect()

def CheckFolders():
    folder_dict = {
        "inbox": {
            "value": inbox.get(),
            "button": inbox_checkbox
        },
        "folders": {
            "value": folders.get(),
            "button": folders_checkbox
        },
        "shared": {
            "value": shared.get(),
            "button": shared_checkbox
        },
        "fetching": {
            "value": fetching.get(),
            "button": fetching_checkbox
        },
        "spam": {
            "value": spam.get(),
            "button": spam_checkbox
        }
    }

    for folder_name in folder_dict.keys():
        if folder_dict[folder_name]["value"] == False and all_folders.get() == True:
            all_checkbox.deselect()

def MarkAsReadFunction():
    global suspected_dict, important_dict, groupware_dict, other_dict

    selected_mails = {
        "suspected_dict": suspected_dict,
        "important_dict": important_dict,
        "groupware_dict": groupware_dict,
        "other_dict": other_dict
    }

    selected_mails_text = []

    for dict_name in selected_mails.keys():
        for item_index in selected_mails[dict_name].keys():
            selected_mail = selected_mails[dict_name][item_index]
            if bool(selected_mail["var"].get()) == True:
                selected_mails_text.append(selected_mail["text"])
    
    msg = "\n".join(selected_mails_text)
    showinfo("Info", msg)


def CheckDateSelect():
    if options_var.get() == 2:
        start_cal.configure(state=NORMAL)
        end_cal.configure(state=NORMAL)
    else:
        start_cal.configure(state=DISABLED)
        end_cal.configure(state=DISABLED)

def SelectDate():
    start_date = start_cal.get_date()
    end_date = end_cal.get_date()

    selected_date = (start_date, end_date)
    # Date format: yyyy-mm-dd

    return selected_date

def QuitExecution():
    root.destroy()
    try:
        driver.quit()
    except:
        pass

def ConfigDomain(row_number):
    global domain_value, domain_text
    domain_text = tk.StringVar()
    
    domain_label = ttk.Label(signin, text="(*) Domain")
    domain_label.grid(column=0, row=row_number, columnspan=2, ipadx=6, ipady=5, sticky="W")

    placeholder_domain = tooltips["domain"]
    domain_value = ttk.Entry(signin, textvariable=domain_text, width=60)
    domain_value.insert(0, placeholder_domain)
    domain_value.config(foreground="#d3d3d3")
    domain_value.bind("<FocusIn>", RemoveTextDomain)
    domain_value.bind("<FocusOut>", ShowTextDomain)
    domain_value.grid(column=2, row=row_number, columnspan=4, ipadx=10, ipady=2, sticky="W")








  




def back_to(row_number):
    global back_to_label
    #domain_text = tk.StringVar()

    #back_to_label = ttk.Label(signin, text="Back to main page",width=30)
    #back_to_label.grid(column=0, row=row_number, columnspan=2, ipadx=6, ipady=5, sticky="W")
    

    #container_luu = tk.Frame(signin)
    #container_luu.pack(side="top",fill="both", expand=True)



    back_to_btn = Button(signin,text="Back to main page",width=30,borderwidth=0)
    back_to_btn.grid(column=0, row=row_number, columnspan=2, ipadx=6, ipady=5, sticky="W")
    placeholder_domain = tooltips["domain"]
    


    move_to_spam_button = ttk.Button(signin, text="Move To Spam", width=15)
    move_to_spam_button.grid(column=3, row=row_number, columnspan=2, ipadx=6, ipady=3, sticky="W")
    

    mark_as_read_button = ttk.Button(signin, text="Mark as Read", width=15)
    mark_as_read_button.grid(column=5, row=row_number, columnspan=2, ipadx=6, ipady=3, sticky="W")

def suspected_mails(row_number):
    global suspected_mails_label
    back_to_label = ttk.Label(signin, text="You have [1] suspected mails",width=35)
    back_to_label.grid(column=0, row=row_number+1, columnspan=2, ipadx=6, ipady=5, sticky="W")


    #view_list_label = ttk.Button(signin, text="View list",width=10)
    #view_list_label.grid(column=3, row=row_number+1, columnspan=2, ipadx=6, ipady=5, sticky="W")

    view_list_btn=Button(signin,text="View list",width=10,borderwidth=0)
    view_list_btn.grid(column=3, row=row_number+1, columnspan=2, ipadx=6, ipady=5, sticky="W")
  
    
    back_to_label2 = ttk.Label(signin, text="You have [1] important mails",width=35)
    back_to_label2.grid(column=0, row=row_number+2, columnspan=2, ipadx=6, ipady=5, sticky="W")

    view_list_btn2=Button(signin,text="View list",width=10,borderwidth=0)
    view_list_btn2.grid(column=3, row=row_number+2, columnspan=2, ipadx=6, ipady=5, sticky="W")

    back_to_label3 = ttk.Label(signin, text="You have [1] groupware mails",width=35)
    back_to_label3.grid(column=0, row=row_number+3, columnspan=2, ipadx=6, ipady=5, sticky="W")

    view_list_btn3=Button(signin,text="View list",width=10,borderwidth=0)
    view_list_btn3.grid(column=3, row=row_number+3, columnspan=2, ipadx=6, ipady=5, sticky="W")

    back_to_label4 = ttk.Label(signin, text="You have [1] others mails",width=35)
    back_to_label4.grid(column=0, row=row_number+4, columnspan=2, ipadx=6, ipady=5, sticky="W")

    view_list_btn4=Button(signin,text="View list",width=10,borderwidth=0)
    view_list_btn4.grid(column=3, row=row_number+4, columnspan=2, ipadx=6, ipady=5, sticky="W")



def ConfigID(row_number):
    global id_value, id_text
    id_text = tk.StringVar()

    id_label = ttk.Label(signin, text="(*) ID")
    id_label.grid(column=0, row=row_number, columnspan=2, ipadx=4, ipady=5, sticky="W")

    placeholder_id = tooltips["id"]
    id_value = ttk.Entry(signin, textvariable=id_text, width=60)
    id_value.insert(0, placeholder_id)
    id_value.config(foreground="#d3d3d3")
    id_value.bind("<FocusIn>", RemoveTextId)
    id_value.bind("<FocusOut>", ShowTextId)
    id_value.grid(column=2, row=row_number, columnspan=4, ipadx=8, ipady=2, sticky="W")

def ConfigPassword(row_number):
    global pw_value, pw_text
    pw_text = tk.StringVar()

    pw_label = ttk.Label(signin, text="(*) Password")
    pw_label.grid(column=0, row=row_number, columnspan=2, ipadx=4, ipady=5, sticky="W")

    placeholder_pw = tooltips["pw"]
    pw_value = ttk.Entry(signin, textvariable=pw_text, width=60)
    pw_value.insert(0, placeholder_pw)
    pw_value.config(foreground="#d3d3d3")
    pw_value.bind("<FocusIn>", RemoveTextPw)
    pw_value.bind("<FocusOut>", ShowTextPw)
    pw_value.grid(column=2, row=row_number, columnspan=4, ipadx=8, ipady=2, sticky="W")

def ConfigFolders(row_number1, row_number2):
    global all_checkbox, inbox_checkbox, folders_checkbox, shared_checkbox, fetching_checkbox, spam_checkbox
    global all_folders, inbox, folders, shared, fetching, spam
    
    all_folders = tk.BooleanVar()
    inbox = tk.BooleanVar()
    folders = tk.BooleanVar()
    shared = tk.BooleanVar()
    spam = tk.BooleanVar()
    fetching = tk.BooleanVar()
    #trash = tk.BooleanVar()

    folders_label = ttk.Label(signin, text="Folders")
    folders_label.grid(column=0, row=row_number1, ipadx=4, ipady=5, sticky="W")
    
    all_checkbox = tk.Checkbutton(signin, text="All", var=all_folders, command=CheckboxAll)
    all_checkbox.grid(column=2, row=row_number1, ipadx=2, ipady=5, sticky="W")

    inbox_checkbox = tk.Checkbutton(signin, text="Inbox", var=inbox, command=CheckFolders)
    inbox_checkbox.grid(column=3, row=row_number1, ipadx=2, ipady=5, sticky="W")

    folders_checkbox = tk.Checkbutton(signin, text="Folders", var=folders, command=CheckFolders)
    folders_checkbox.grid(column=4, row=row_number1, ipadx=2, ipady=5, sticky="W")

    shared_checkbox = tk.Checkbutton(signin, text="Shared", var=shared, command=CheckFolders)
    shared_checkbox.grid(column=2, row=row_number2, ipadx=2, ipady=5, sticky="W")

    fetching_checkbox = tk.Checkbutton(signin, text="Fetching", var=fetching, command=CheckFolders)
    fetching_checkbox.grid(column=3, row=row_number2, ipadx=2, ipady=5, sticky="W")

    spam_checkbox = tk.Checkbutton(signin, text="Spam", var=spam, command=CheckFolders)
    spam_checkbox.grid(column=4, row=row_number2, ipadx=2, ipady=5, sticky="W")

def ConfigOptions(row_number):
    global options_var
    options_var = tk.IntVar()

    year = int(Objects.year)
    month = int(Objects.month)
    day = int(Objects.day)
    default_date = date(year, month, day)

    options_label = ttk.Label(signin, text="Options")
    options_label.grid(column=0, row=row_number, ipadx=4, ipady=5, sticky="W")

    auto = ttk.Radiobutton(signin, text="Auto", variable=options_var, value=1, command=CheckDateSelect)
    auto.grid(column=2, row=row_number, ipadx=6, ipady=5, sticky="W")
    
    custom = ttk.Radiobutton(signin, text="Custom", variable=options_var, value=2, command=CheckDateSelect)
    custom.grid(column=3, row=row_number, ipadx=6, ipady=5, sticky="W")

    global start_cal, end_cal
    start_cal = DateEntry(signin, selectmode='day', width=8)
    start_cal.set_date(default_date)
    start_cal.configure(state=DISABLED)
    start_cal.grid(column=4, row=row_number, ipady=2, columnspan=4, sticky="W")

    end_cal = DateEntry(signin, selectmode='day', width=8)
    end_cal.set_date(default_date)
    end_cal.configure(state=DISABLED)
    end_cal.grid(column=5, row=row_number, ipady=2, columnspan=2, sticky="W")

    options_var.set(1)

def ConfigButtons(row_number):
    start_button = ttk.Button(signin, text="Start", width=20, command=StartFunction)
    start_button.grid(column=2, row=row_number, columnspan=3, ipadx=6, ipady=2, sticky="W")
 
    quit_button = ttk.Button(signin, text="Quit", width=20, command=QuitExecution)
    quit_button.grid(column=4, row=row_number, columnspan=3, ipadx=6, ipady=2, sticky="W")

def ConfigEmptyLabel(frame, row_number):
    empty_label = ttk.Label(frame, text="")
    empty_label.grid(column=0, row=row_number, ipadx=4, ipady=2, sticky="W")

def ConfigSeparator(frame, row_number):
    separator = ttk.Separator(frame, orient='horizontal')
    separator.grid(column=0, row=row_number, columnspan=6, ipadx=4, ipady=2, sticky="W")

def ConFigLogFrame(frame, row_number):
    log_labelframe = LabelFrame(frame, width=460, height=200)
    log_labelframe.grid(row=row_number, columnspan=6, padx=15, ipadx=90, ipady=20, sticky="W")
    
    log_empty = Label(log_labelframe, text="Log is empty")
    log_empty.grid(row=row_number+1, columnspan=6, padx=15, ipadx=90, ipady=20, sticky="W")

    log_empty1 = Label(log_labelframe, text="Log is empty")
    log_empty1.grid(row=row_number+2, columnspan=6, padx=15, ipadx=90, ipady=20, sticky="W")

    log_empty2 = Label(log_labelframe, text="Log is empty")
    log_empty2.grid(row=row_number+3, columnspan=6, padx=15, ipadx=90, ipady=20, sticky="W")

def InsertLog():
    print("")

def ShowSuspectedMails():
    global suspected_dict
    #suspected_dict = {}
    # item_index = {
    #       "var": "",
    #       "text": ""
    # }

    if len(suspected_mails) > 0:
        for item in suspected_mails:
            item_var = tk.BooleanVar()
            
            row_number = handler_start_row + int(suspected_mails.index(item)) + 1
            item_checkbox = tk.Checkbutton(signin, text=item, var=item_var, command="")
            item_checkbox.grid(column=0, row=row_number, columnspan=6, ipadx=6, ipady=2, sticky="W")

            item_index = str(suspected_mails.index(item))
            suspected_dict.update({item_index: {}})
            suspected_dict[item_index]["checkbox"] = item_checkbox
            suspected_dict[item_index]["var"] = item_var
            suspected_dict[item_index]["text"] = item
    
    return suspected_dict

def ShowImportantMails():
    global important_dict
    #important_dict = {}

    if len(important_mails) > 0:
        for item in important_mails:
            item_var = tk.BooleanVar()
            
            current_row = suspected_row + 1
            item_position = int(important_mails.index(item)) + 1
            row_number = current_row + item_position

            item_checkbox = tk.Checkbutton(signin, text=item, var=item_var, command="")
            item_checkbox.grid(column=0, row=row_number, columnspan=6, ipadx=6, ipady=2, sticky="W")

            item_index = str(important_mails.index(item))
            important_dict.update({item_index: {}})
            important_dict[item_index]["checkbox"] = item_checkbox
            important_dict[item_index]["var"] = item_var
            important_dict[item_index]["text"] = item
    
    return important_dict

def ShowGroupwareMails():
    global groupware_dict
    #groupware_dict = {}

    if len(groupware_mails) > 0:
        for item in groupware_mails:
            item_var = tk.BooleanVar()
            
            current_row = important_row + 1
            item_position = int(groupware_mails.index(item)) + 1
            row_number = current_row + item_position

            item_checkbox = tk.Checkbutton(signin, text=item, var=item_var, command="")
            item_checkbox.grid(column=0, row=row_number, columnspan=6, ipadx=6, ipady=2, sticky="W")

            item_index = str(groupware_mails.index(item))
            groupware_dict.update({item_index: {}})
            groupware_dict[item_index]["checkbox"] = item_checkbox
            groupware_dict[item_index]["var"] = item_var
            groupware_dict[item_index]["text"] = item
    
    return groupware_dict

def ShowOtherMails():
    global other_dict
    #other_dict = {}

    if len(other_mails) > 0:
        for item in other_mails:
            item_var = tk.BooleanVar()
            
            current_row = groupware_row + 1
            item_position = int(other_mails.index(item)) + 1
            row_number = current_row + item_position

            item_checkbox = tk.Checkbutton(signin, text=item, var=item_var, command="")
            item_checkbox.grid(column=0, row=row_number, columnspan=6, ipadx=6, ipady=2, sticky="W")

            item_index = str(other_mails.index(item))
            other_dict.update({item_index: {}})
            other_dict[item_index]["checkbox"] = item_checkbox
            other_dict[item_index]["var"] = item_var
            other_dict[item_index]["text"] = item
    
    return other_dict

def ConfigSuspectedHandler(current_row):
    global suspected_mails, suspected_dict, suspected_view
    suspected_dict = {}
    suspected_mails = CollectExcelList("suspected_mails")

    if len(suspected_mails) > 0:
        suspected_msg = "You have [%s] suspected mails." % str(len(suspected_mails))
        suspected_label = ttk.Label(signin, text=suspected_msg)
        suspected_label.grid(column=0, row=current_row, columnspan=3, ipadx=6, ipady=2, sticky="W")

        suspected_view = ttk.Button(signin, text="View List", width=5, command=ShowSuspectedMails)
        suspected_view.grid(column=4, row=current_row, columnspan=3, ipadx=6, ipady=2, sticky="W")
    
    end_row = current_row + int(len(suspected_mails))

    ''' 🚩To-Do: 
                + suspected_mails collect from excel log []
                + if suspected_mails > 0 => show ok btn
                + suspected_mails: make it empty first => If 0 elif > 0 '''
    
    return end_row

def ConfigImportantHandler(current_row):
    global important_mails, important_dict, important_view
    important_dict = {}
    important_mails = CollectExcelList("important_mails")

    if len(important_mails) > 0:
        important_msg = "You have [%s] important mails."  % str(len(important_mails))
        important_label = ttk.Label(signin, text=important_msg)
        important_label.grid(column=0, row=current_row, columnspan=3, ipadx=6, ipady=2, sticky="W")

        important_view = ttk.Button(signin, text="View List", width=5, command=ShowImportantMails)
        important_view.grid(column=4, row=current_row, columnspan=3, ipadx=6, ipady=2, sticky="W")

    end_row = current_row + int(len(important_mails))

    return end_row

def ConfigGroupwareHandler(current_row):
    global groupware_mails, groupware_dict
    groupware_dict = {}
    groupware_mails = CollectExcelList("groupware_mails")

    if len(groupware_mails) > 0:
        groupware_msg = "You have [%s] groupware mails." % str(len(groupware_mails))
        groupware_label = ttk.Label(signin, text=groupware_msg)
        groupware_label.grid(column=0, row=current_row, columnspan=3, ipadx=6, ipady=2, sticky="W")

        groupware_view = ttk.Button(signin, text="View List", width=5, command=ShowGroupwareMails)
        groupware_view.grid(column=4, row=current_row, columnspan=3, ipadx=6, ipady=2, sticky="W")

    end_row = current_row + int(len(groupware_mails))

    return end_row

def ConfigOtherHandler(current_row):
    global other_mails, other_dict
    other_dict = {}
    other_mails = CollectExcelList("other_mails")

    if len(other_mails) > 0:
        other_msg = "You have [%s] other mails." % str(len(other_mails))
        other_label = ttk.Label(signin, text=other_msg)
        other_label.grid(column=0, row=current_row, columnspan=3, ipadx=6, ipady=2, sticky="W")

        other_view = ttk.Button(signin, text="View List", width=5, command=ShowOtherMails)
        other_view.grid(column=4, row=current_row, columnspan=3, ipadx=6, ipady=2, sticky="W")

    end_row = current_row + int(len(other_mails))

    return end_row

def ConfigHandlerButtons(current_row):
    mail_list = [suspected_mails, important_mails, groupware_mails, other_mails]
    for picked_list in mail_list:
        picked_index = mail_list.index(picked_list)
        if bool(picked_list) == True:
            mail_list[picked_index] = True
        else:
            mail_list[picked_index] = False
    
    if True in mail_list:
        move_spam_btn = ttk.Button(signin, text="Move to Spam", width=20, command="")
        move_spam_btn.grid(column=2, row=current_row, columnspan=2, ipadx=6, ipady=2, sticky="W")

        mark_read_btn = ttk.Button(signin, text="Mark as read", width=20, command=MarkAsReadFunction)
        mark_read_btn.grid(column=4, row=current_row, columnspan=2, ipadx=6, ipady=2, sticky="W")

def HandlerBar():
    # Handler - Suspected handler moving mails to Spam 
    global handler_start_row, suspected_row, important_row, groupware_row, other_row

    handler_start_row = signin_start_row+10
    # Start row of fie
    
    # Handler - Suspected mails
    suspected_row = ConfigSuspectedHandler(handler_start_row)

    # Handler - Important mails
    important_row = ConfigImportantHandler(suspected_row+1)

    # Handler - Groupware mails
    groupware_row = ConfigGroupwareHandler(important_row+1)

    # Handler - Other mails
    other_row = ConfigOtherHandler(groupware_row+1)

    # Handler - Empty Row
    ConfigEmptyLabel(signin, other_row+1)

    # Handler - Buttons 'Mark as Read' and 'Move to Spam'
    ConfigHandlerButtons(other_row+2)


def MainUI():
    global root, signin

    # Root frame
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = 800
    height = 500
    x = (screen_width/3) - (width/2)
    y = (screen_height/3) - (height/2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))
    root.resizable(True, True)
    root.title('Mail Analysis')

    # Signin frame
    signin = ttk.Frame(root)
    signin.config(height=200)
    signin.pack(padx=2, pady=10, fill='x', expand=True)

    # Login data
    global signin_start_row
    signin_start_row = 0

    back_to(row_number=signin_start_row)
    suspected_mails(row_number=signin_start_row+1)


    

    '''

    ConfigDomain(row_number=signin_start_row)
    ConfigID(row_number=signin_start_row+1)
    ConfigPassword(row_number=signin_start_row+2)

    # Select folders to inspect
    ConfigFolders(row_number1=signin_start_row+3, row_number2=signin_start_row+4)
    
    # Auto run or inspect mails on selected date
    ConfigOptions(row_number=signin_start_row+5)
    
    # Add an empty space
    #ConfigEmptyLabel(signin, row_number=signin_start_row+6)
    
    # Start and Quit button
    ConfigButtons(row_number=signin_start_row+7)

    # Generate a space
    ConfigEmptyLabel(signin, row_number=signin_start_row+8)

    # Separate content frame
    ConfigSeparator(signin, row_number=signin_start_row+9)

    '''



   
    root.mainloop()

MainUI()