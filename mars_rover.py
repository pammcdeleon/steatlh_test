import requests
import json
from datetime import datetime
import os, sys
import webbrowser

global arg_date

# date should follow this sequence ONLY --> MONTH DAY YEAR
def check_date():
    isValidDate = True
    
    if '/' in arg_date:
        month,day,year = arg_date.split('/')
    elif ',' in arg_date:
        month,day,year = arg_date.split(' ')
    elif '-' in arg_date:
        month,day,year = arg_date.split('-')

    try :
        if type(month) != int:
            if len(month) == 3:
                month = datetime.strptime(month, '%b').month
            elif len(month) > 3:
                month = datetime.strptime(month, '%B').month
                
        day = day.rstrip(',')

        datetime(int(year),int(month),int(day))
        
        print("month: " + str(month))
        print("day: " + str(day))
        print("year: " + str(year))
        new_date = year + "-" + month + "-" + day
        
    except ValueError :
        isValidDate = False

    if(isValidDate) :
        print ("Input date is valid ..")
        get_api(new_date)
    else :
        print ("Input date is not valid..")
        
def get_api(date):
    og_url = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?earth_date=DATE&api_key=DEMO_KEY"
    og_url = og_url.replace("DATE", date)

    response = requests.get(og_url)
    data = response.json()
    
    for i in range(len(data["photos"])):
        image = data["photos"][i]["img_src"]

        webbrowser.open(image)
    
        head, tail = os.path.split(image) # strip the slash from the right side
        
        download = os.path.join(os.path.expanduser('~'), 'downloads')
        full_dl = download + "\\" + tail
        
        f = open(full_dl,'wb')
        f.write(requests.get(image).content)
        f.close()

def main():
    check_date()

if __name__ == "__main__":
    global arg_date
    arg_date = input("Enter date: ")
    print("Entered date is " + arg_date)

    main()
