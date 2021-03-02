import pickle
import vk_api
import sqlite3
import os.path

vk_session = vk_api.VkApi('', '') #ввести номер телефона и пароль
vk_session.auth()
vk = vk_session.get_api()

db = sqlite3.connect('users.db')
sql = db.cursor()

myId = 225273973

def createDataBase():
    sql.execute("""DROP TABLE IF EXISTS  users""")
    sql.execute("""CREATE TABLE IF NOT EXISTS users(
                id INTEGER,
                first_name TEXT,
                last_name TEXT,
                url_to_photo TEXT,
                friends_list TEXT
     )""")
    db.commit()
    print("Data base has been created")

def pars():
    #if not os.path.isfile('users.db'):
    createDataBase()


    me = vk.users.get(user_id=myId,fields='photo_max_orig')
    sql.execute(f"INSERT INTO users VALUES(?,?,?,?,?)", (me[0]['id'], me[0]['first_name'], me[0]['last_name'], me[0]['photo_max_orig'],""))
    db.commit()
    my_friends = []
    data = vk.friends.get(user_id=myId, fields='photo_max_orig')
    for user in data['items']:
        my_friends.append(user['id'])
        sql.execute(f"INSERT INTO users VALUES(?,?,?,?,?)", (user['id'], user['first_name'], user['last_name'], user['photo_max_orig'],""))
        db.commit()
    my_friends = pickle.dumps(my_friends)
    sql.execute(f"UPDATE users SET friends_list = ? WHERE rowid = 1", (my_friends,))
    db.commit()

def createDataSet():
    pars()
    id_list = parsMyFriends()
    i=0
    while i < len(id_list) - 1:
        j = i + 1
        mutual_friends_list=[]
        hasMutual = False
        while j < len(id_list):
            k = 1
            while k < len(id_list[j]):
                if (int(id_list[i][0]) == int(id_list[j][k])):
                    hasMutual = True
                k = k + 1
            j = j + 1
        if hasMutual == True:
            mutual_friends_list = pickle.dumps(mutual_friends_list)
            sql.execute(f"UPDATE users SET friends_list = ? WHERE id = ?", (mutual_friends_list,id_list[i][0],))
            db.commit()
        i = i + 1

def parsMyFriends():
    sql.execute(f"SELECT friends_list FROM users WHERE rowid = 1")
    list_of_friends = sql.fetchall()
    list_of_friends= pickle.loads(list_of_friends[0][0])
    print(list_of_friends)

    print(len(list_of_friends))

    allUsers_friends_list = []
    i = 0
    int_max = 2147483647
    for friend in list_of_friends:
        if "deactivated" in vk.users.get(user_id=friend)[0]:  #проверка забанен/удален ли пользователь
            print(str(friend) + " deactivated")
        else:
            oneUser_friends_list = []
            data = vk.friends.get(user_id=friend, count = int_max)
            oneUser_friends_list.append(friend)
            for user in data['items']:
                oneUser_friends_list.append(user)
            print(str(i)+" len of data: "+ str(len(oneUser_friends_list)))
            allUsers_friends_list.append(oneUser_friends_list)
        i+=1
    return allUsers_friends_list

if __name__ == '__main__':
    createDataSet()
