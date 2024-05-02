import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
import os
from tabulate import tabulate
from datetime import datetime
import json
from rich import print
import subprocess

genai.configure(api_key=os.getenv('GOOGLE_GEMINI_API'))

model=genai.GenerativeModel("gemini-pro")


def ai(query):
    response=model.generate_content(query)
    return response.text

def todo():
    cntrl=True
    date=datetime.now()
    filename=date.strftime('%d%m%y')+'.json'
    filepath='history/'+filename

    data={'task':["Tasks"],'dscrpt':["Short description"],'stn':["Situation"]}
    def commit():
        with open (filepath,'w',encoding='utf-8') as f:
            json.dump(data,f,ensure_ascii=False,indent=4)
    if os.path.isfile(filepath):
        with open(filepath,'r',encoding='utf-8') as f:
            data=json.load(f)
    else:
        commit()
    while cntrl:
        print("Type 'add;' for Add new task.\nType 'view;' for View Tasks.\nType 'mark;' Update situation.\nType 'bot;' for ChatBot\nType 'exit;' for exit programme.\n '$' ",end='')
        prmnt=input()
        try:
            match (prmnt.lower()):
                case 'add;':
                    try:
                        task=input("Enter Task $ ")
                        dscrpt=ai('Write short description in 15 word about that how can I comlete task '+task+'in a day')
                        data['task'].append(task)
                        data['dscrpt'].append(dscrpt)
                        data['stn'].append('Not Yet')
                        print("Task added seccesfully.")
                    except:
                        print("Check your network connection!")
                    commit()
                case 'view;':
                    if data['task']==[]:
                        print("No task available ! ")
                    print(tabulate(data,headers='firstrow',tablefmt='grid'))
                case 'exit;':
                    print("\nExiting.")
                    commit()
                    cntrl=False
                case 'mark;':
                    updt=True
                    while updt:
                        tsknm=input("Enter Task name. $ ")
                        tasks=data['task']
                        if tsknm not in tasks:
                            print("Inputed task not matched,try typing valid task.")
                        i=0
                        for task in tasks:
                            if task==tsknm:
                                data['stn'][i]="Completed."
                                print("Marked as comleted.")
                                updt=False
                            else: 
                                i+=1
                                continue                
                    commit()
                case 'bot;':
                    bot()
                    cntrl=False
                case _:
                    print("\nInvalid Input ! Please Try Again,\n")
        except:
            print("\nInvalid Input ! Please Try Again,\n")



def bot():
    content=[["Query","Response"]]
    cntrl=True
    while cntrl:
    
        print("Put your query after '$' .\nType 'help;' for instructions\nType 'todo;' for go in to ToAIDo.\nType 'exit;' for exit programme.\n'$' ",end='')
    
        query=input()    
        
        match (query.lower()):
            case 'help;':
                print("Put your query after '$' .\nType 'help;' for instructions\nType 'exit;' for exit programme.")
                
            case 'exit;':
                cntrl=False
            case 'todo;':
                todo()
                cntrl=False
            case _:
                response=ai(query)
                cnt=[query,response]
                content.append(cnt)
                print(tabulate(content,headers='firstrow',tablefmt='grid'))
                # return tabulate(content,headers='firstrow',tablefmt='grid')  

def main():
    ch=int(input("1.Run in browser\n2.ToDo\n3.ChatBot\n4.Exit [any-key/enter]\n $ "))
    match (ch):
        case 1:
            # subprocess.run(['streamlit','run','main.py'], capture_output=False, text=True)
            pass
        case 2:
            todo()
        case 3:
            bot()
        case 4:
            # subprocess.run(['exit();'])                
            pass
        case _:
            print("Type valid command!")            
        
        
if __name__ =='__main__':

    main()