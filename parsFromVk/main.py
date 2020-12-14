# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
import vk_api
import re
import string

def pars():
    vk_session = vk_api.VkApi('','') #ввести номер телефона и пароль
    vk_session.auth()
    vk = vk_session.get_api()

    nameOfFile = 'base.txt'
    f = open(nameOfFile, 'w',encoding="utf-8")
    data = vk.friends.get(user_id=225273973,fields='nickname')
    dataTxt = json.dumps(data, indent=4, sort_keys=True,ensure_ascii=False)
    f.write(dataTxt)
    f.close()
    f = open(nameOfFile, 'r',encoding="utf-8")

    f_new = f.readlines()
    filter_base = open('filter_base.txt','w',encoding="utf-8")
    #print(f_new)
    for i in f_new:
        if re.search(r"\"id\":",i):          # запись строки с id
            filter_base.write(i)
        elif re.search(r"\"last_name\":",i): # запись строки с last name
            filter_base.write(i)
        elif re.search(r"\"first_name\":",i):# запись строки с first name
            filter_base.write(i)
    filter_base.close()
    f.close()
    removingUnnecessary('filter_base.txt')


def removingUnnecessary(nameOfFile):
    file = open(nameOfFile,'r',encoding="utf-8")
    f=file.readlines()
    print(f)
    new_file=open('base.txt','w',encoding="utf-8")
    #counter = 1
    for i in f:
        i = i.lstrip()  # удалить все пробелы в начале строки
        i = i.rstrip()  # удалить все пробелы в конце строки
        if(i[1]=='f'): # удаление "first_name": ".....",
            for j in "\"first_name\": \"":
                i = i.replace(i[0], "", 1)
            i = i.replace(i[len(i) - 1], "", 1)  # удаление последного символа (,)
            i = i.replace(i[len(i) - 1], "", 1)  # удаление предпоследного символа (")
        elif(i[1]=='l'):  # удаление "last_name": ".....",
            for j in "\"last_name\": \"":
                i = i.replace(i[0], "", 1)
            i = i.replace(i[len(i) - 1], "", 1)  # удаление последного символа (,)
            i = i.replace(i[len(i) - 1], "", 1)  # удаление предпоследного символа (")
        elif(i[1]=='i'): #удаление "id": ....,
            for j in "\"id\": ":
                i = i.replace(i[0], "", 1)
            i = i.replace(i[len(i) - 1], "", 1)  # удаление последного символа (,)
        #if(counter%3==0):             чтобы данные об одном человеке были в одной строке
        new_file.write(i + '\n')
        #else:
        #    new_file.write(i+' ')
        #counter=counter+1

    new_file.close()




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pars()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
