from pathlib import Path
from tkinter import *
from tkinter import messagebox 
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import re
import string
import random
import requests

def random_string(n):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(n))

s = requests.session()
hstorypage = False
def random_data(dta):
    data_send = {}
    global hstorypage
    for key, value in dta.items():
        if "year" in key:
            value = int(random.randint(1890, 2077))
        elif "month" in key:
            value = int(random.randint(1, 12))
        elif "day" in key:
            value = int(random.randint(1, 28))
        elif "minute" in key:
            value = int(random.randint(1, 59))
        elif "hour" in key:
            value = int(random.randint(1, 24))
        elif value != "No information!":
            value = random.choice(value) # khả năng tỷ lệ sẽ làm ở bước này
        data_send[key] = value
    if hstorypage:
        data_send['pageHistory'] = hstorypage
    return data_send

def attack(url_link, times, progress_bar, window):
    total_runs = 0
    url_in = url_link
    url = s.get(url_in).url.split('/')[-2]
    url_rsp = 'https://docs.google.com/forms/u/0/d/e/'+url+'/formResponse'

    contentext = s.get(url_rsp).text
    pram = "<title>(.*?)</title>"
    try:
        titlee = re.findall(pram, contentext, re.DOTALL)[0]
    except Exception as e:
        print(f"Lỗi: {e}")
    if titlee:
        print("FROM SPAM - TÊN FORM VỪA NHẬP:")
        print('--------------------------------------------------')
        print(titlee.center(50, '|'))
        print('--------------------------------------------------\n')
    else:
        print("link lỗi !!!")
    max_spam = times
    messagebox.showinfo(title="Tiêu đề", message=titlee)
    print(f'Spamming "{titlee}" for {times} times')
    
    pattern = r',null,8,'
    numpage = re.findall(pattern, contentext)
    hstorypage = False
    if len(numpage):
        hstorypage = "0"
        for i in range(1, len(numpage) + 1):
            hstorypage += ',' + str(i)

    pattern = f'FB_PUBLIC_LOAD_DATA(.*?){url}'
    dulieu = re.findall(pattern, contentext, re.DOTALL)[0]
    pattern = r"\[\d+,\"(.*?)\",null,(\d+)"
    cauhoii = re.findall(pattern, dulieu, re.DOTALL)

    pattern_Get_id = r'\[\[(\d+),'
    pattern_get_cau_tl = r'\[\"(.*?)\"'
    

    
    # input()
    dta = {}
    for (y, z) in cauhoii:
        if int(z) != 8:
            tltracno = dulieu.split(y)[1]
            # id_q = re.findall(pattern_Get_id, tltracno)[0]
            result = re.findall(pattern_Get_id, tltracno)

            if result:
                id_q = result[0]
            else:
                # Xử lý khi không tìm thấy chuỗi khớp
                print(" không tìm thấy chuỗi khớp")
                continue  # Skip to the next iteration

            if int(z) == 9:
                ngay_thang_nam = True
                dta['entry.' + id_q + '_year'] = "year"
                dta['entry.' + id_q + '_month'] = "month"
                dta['entry.' + id_q + '_day'] = "day"
            elif int(z) == 10:
                ngay_gio = True
                dta['entry.' + id_q + '_hour'] = "hour"
                dta['entry.' + id_q + '_minute'] = "minute"
            elif int(z) == 0:
                dta['entry.' + id_q] = "No information!"
            else:
                cautraloi = re.findall(pattern_get_cau_tl, tltracno.split(']]')[0])
                dta['entry.' + id_q] = cautraloi
    
    
    if total_runs >= times:
        return
    
    for _ in range(times):
        try:           
            if total_runs >= max_spam:
                return
            s.post(url_rsp,data=random_data(dta))
            print(f"Sending: {total_runs + 1}".center(50, '-'))
            total_runs += 1
            # Update progress bar value
            progress_value = (total_runs / max_spam) * 100
            progress_bar['value'] = progress_value
            window.update_idletasks()  # Update the window to show changes
            if total_runs >= max_spam:
                messagebox.showinfo(title="Done", message=f"Done! Spamed {times} times")
                return
            if total_runs <= max_spam:
                continue

        except Exception as e:
            print(f"Lỗi: {e}")
            messagebox.showerror(title="Error", message=f"Error: {e}")
            break

    return
            

#############################################################################
def gui():
    def relative_to_assets(path: str) -> Path:
            return Path(__file__).parent / "assets" / path
    
    global url_link
    global times

    window = Tk()
    window.title("Spam Google Form")
    icon_path = relative_to_assets("spam_ico.ico")
    icon = Image.open(icon_path)
    icon = ImageTk.PhotoImage(icon)
    window.iconbitmap(icon_path) 
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = 375
    window_height = 639
    x = int(screen_width/2 - window_width/2)  
    y = int(screen_height/2 - window_height/2)
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    window.configure(bg = "#E8E8E8")
    canvas = Canvas(window,bg = "#FFE1CC",height = 639,width = 375,bd = 0,highlightthickness = 0,relief = "ridge")
    canvas.place(x = 0, y = 0)
    canvas.create_rectangle(0.0,0.0,780.0,1444.0,fill="#E8E8E8",outline="")
    background_img = PhotoImage(file=relative_to_assets("background.png"))
    background = canvas.create_image(0.0,0.0,image=background_img,anchor="nw")
    padding_top = 0
    
    
    progress_bar = ttk.Progressbar(window, orient='horizontal', length=200, mode='determinate')
    progress_bar.place(x=87, y=540)
    
    url_entry = f"url_entry"
    globals()[url_entry] = Entry(bd=0,bg="#EDEDED",fg="#000716",highlightthickness=0)
    globals()[url_entry].place(x=24,y=230 + padding_top,width=323,height=50)
    globals()[url_entry].config(borderwidth=5, relief="groove")
    
    
    times_entry = f"times_entry"
    globals()[times_entry] = Entry(bd=0,bg="#EDEDED",fg="#000716",highlightthickness=0)
    globals()[times_entry].place(x=24,y=323 + padding_top,width=323,height=50)
    globals()[times_entry].config(borderwidth=5, relief="groove")
    
    spam_img = PhotoImage(file=relative_to_assets("spam.png"))
    spam_btn = f"spam_btn"
    globals()[spam_btn] = Button(image=spam_img,borderwidth=0,highlightthickness=0,
        command=lambda url_link=globals()[url_entry], times=globals()[times_entry]: threading.Thread(target=runNow, args=(url_link.get(), times.get(), window)).start(),
        relief="flat"
    )
    globals()[spam_btn].place(x=90,y=473 + padding_top,width=198,height=37.0)
    
    def runNow(url_link, times, window):
        """Handles the click event of the spam button"""
        try:
            # Validate and process URL input
            if not url_link:
                raise ValueError("URL cannot be empty")

            # URL format validation using regular expressions
            url_regex = r"^https?://[\w\.-]+/\S*$"  # Basic URL format with protocol (http/https)
            if not re.match(url_regex, url_link):
                raise ValueError("Invalid URL format")
            
            # Ensure URL starts with "https://docs.google.com/forms"
            if not url_link.startswith("https://docs.google.com/forms"):
                raise ValueError("URL must start with 'https://docs.google.com/forms'")
                
            # Validate and process times input
            try:
                times = int(times)
                if times <= 0:
                    raise ValueError("Times must be a positive integer")
            except ValueError as e:            
                raise ValueError("Times must be a valid number")

            # Perform spam action (using the provided URL and times)
            # Create and start a new thread for the attack
            threading.Thread(target=attack, args=(url_link, times, progress_bar, window)).start()
            # ... Implement your spam logic here ...
            
        except ValueError as e:
            # Display error message to the user
            error_message = f"Error: {e}"
            print(error_message)
            # Display error message using a popup
            messagebox.showerror(title="Error", message=f"Error: {e}")

    pass
    window.resizable(False, False)
    window.mainloop()
 
if __name__ == '__main__':
    gui()