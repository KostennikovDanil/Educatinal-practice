# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
import re
from idlelib import editor
from typing import Type

import vk_api
import string
#editor.soft.wrap.force.limit=100000

vk_session = vk_api.VkApi() #ввести номер телефона и пароль
vk_session.auth()
vk = vk_session.get_api()

def pars():
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
    #print(f)
    new_file=open('base.txt','w',encoding="utf-8")
    counter = 0
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

        if(counter == 0):
            first_name = i
        if (counter == 1):
            user_id = i
        if (counter == 2):
            second_name = i
        if(counter == 2):             #чтобы данные об одном человеке были в одной строке
            new_file.write(f"{user_id} {first_name} {second_name} \n")
            counter = 0
        else:
            counter=counter+1

    new_file.close()

def makeFile(user_id):
    #user_id = user[0]  # выбираем id
    # print(user_id)
    int_max = 2147483647
    data = vk.friends.get(user_id=user_id, fields=None, count = int_max)
    f_tmp = open("tmp.txt", 'w+', encoding="utf-8")
    f_tmp.write(json.dumps(data, indent=0, sort_keys=True, ensure_ascii=False)) # записываем id друзей друга в отдельный временный файл, чтобы было удобнее пользоваться данными
    f_tmp.close()
    f_tmp = open("tmp.txt", 'r+', encoding="utf-8")
    data = f_tmp.readlines()
    print("in func make file len of data = " + str(len(data)))
    f_tmp.close()
    return data

def getFriends(data, user_id):
    list = []
    list.append(user_id)
    i = 3
    while (i < len(data) - 3):
        id_of_friend = re.sub(r",\n", "", data[i])  # записываем id друга друга
        id_of_friend = int(id_of_friend)
        list.append(id_of_friend)
        i = i + 1
    list.append(int(data[len(data) - 3]))  # записываем последний id из файла tmp
    return list

def createDataSet():
    print()
    f = open('dataset.txt','a+',encoding="utf-8")
    f_base = open('base.txt','r',encoding="utf-8")
    data_base = f_base.readlines()
    for i in data_base:
        f.write('225273973' + ' ' + i.partition(' ')[0] + '\n')
    id_list = parsMyFriends()
    i=0
    while i < len(id_list) - 1:
        # print(str(i) + " = " + str(len(id_list[i])))
        j = i + 1
        # print(j)
        while j < len(id_list):
            k = 1
            # print("j = " + str(j) + " len(id_list[j]) = " + str(len(id_list[j])))
            while k < len(id_list[j]):
                if (int(id_list[i][0]) == int(id_list[j][k])):
                    print("bingo " + str(id_list[i][0]) + ' ' + str(id_list[j][0]))
                    f.write(str(id_list[i][0]) + " " + str(id_list[j][0]) + '\n')
                    print(id_list[i][0])
                    print(id_list[j][k])
                    print(i)
                    print(j)
                    print(k)
                k = k + 1
            j = j + 1
            # print("k = " + str(k))
        print(id_list[i])
        i = i + 1




def parsMyFriends():
    f = open('base.txt','r',encoding="utf-8")
    users = f.readlines()
    print(users)
    i = 0
    id_list = []
    list = []
    while i<len(users):
        user_id = (users[i].partition(' ')[0])
        if "deactivated" in vk.users.get(user_id=user_id)[0]:  #проверка забанен/удален ли пользователь
            print(str(i) + " deactivated")
            i = i + 1
        else:
            #print (i)

            data = makeFile(user_id)
            print(str(i)+" len of data = "  + str(len(data)))
            list = getFriends(data,user_id)
            id_list.append(list)
            i = i + 1
    #print(id_list)
    #for i in id_list:
        #print(i[0])


    #print(len(id_list))
    #print(id_list[0])

    #print(type(id_list[0][0]))
    #print(id_list[0][0])
    #print(len(id_list[1]))
    print("jopa")
    print(len(id_list))
    print("jopa")



    return id_list

# Press the green button in the gutter to run the script.
def test():
    f = open("tmp.txt" , 'w+')
    i=0
    while i<100000:
        f.write(str(i)+'\n')
        i=i+1

if __name__ == '__main__':
    pars()
    #parsMyFriends()
    createDataSet()
    #test()
    #data = open('base.txt',encoding="utf-8").read().replace('\n', '')
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
