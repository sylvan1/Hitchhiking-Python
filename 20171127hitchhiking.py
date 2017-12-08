# -*- coding: utf-8 -*-
import pymysql
from passwords import * 

class DBconn:
    def __init__(self):
        self.conn = pymysql.connect(host, conntype, password, database)
        #self.conn = pymysql.connect('localhost','root','Welcome123','hitchhiking')#w razie potrzeby dopisać 3 przy nazwie bazy danych            
        #self.conn=conn
        self.cursor = self.conn.cursor()
        print('''
 __      __   _                    _         _  _ _ _      _    _    _ _   _           
 \ \    / /__| |__ ___ _ __  ___  | |_ ___  | || (_) |_ __| |_ | |_ (_) |_(_)_ _  __ _ 
  \ \/\/ / -_) / _/ _ \ '  \/ -_) |  _/ _ \ | __ | |  _/ _| ' \| ' \| | / / | ' \/ _` |
   \_/\_/\___|_\__\___/_|_|_\___|  \__\___/ |_||_|_|\__\__|_||_|_||_|_|_\_\_|_||_\__, |
                                                                                 |___/ 
     
        ''')

        print('You are connected with database')        
        
        while True:
            choice = input('What do you want to do? (L)Login (R)Register (Q)Quit: ')
            if choice.upper() == 'L':
                self.log_in()
                break
            elif (choice.upper() == 'R'):
                self.register() 
                break
            elif choice.upper() == 'Q':
                print('See you soon again!')
                self.conn.close()
                break
            else:
                print('You have entered wrong letter. Try again.')            
            
            
    def log_in(self):

        while True:
            user_access = input('Enter your access type (D)Driver (H)Hiker or enter (Q) to quit: ')                 
            if user_access.upper() == 'Q':
                print ('See you soon again!')
                self.conn.close()
                break 
            elif user_access.upper() != 'Q' and user_access.upper() != 'D' and user_access.upper() != 'H': 
                print('You have entered wrong letter for access type. Try again.')
            else:
                user_login = input('Enter your login: ')
                user_password = input('Enter your password: ')
                if user_access.upper() == 'D':
                    self.cursor.execute('select id_d, login_d, password_d from drivers_logins where login_d = "'+ user_login +'" and password_d = "'+ user_password +'";')
                    results = self.cursor.fetchall()  # You can use fetchone because login is unique. 
                    if results:
                        for row in results:
                            sql_user_id = row[0]
                            sql_user_login = row[1]  # You don't use it anywhere.
                            sql_user_password = row[2]  # You don't use it anywhere.
                        l1 = Driver(sql_user_id)
                        l1.menu_driver()
                        break
                    else:
                        print('You gave incorrect credentials. Try again')
                elif user_access.upper() == 'H':
                    self.cursor.execute( 'select id_h, login_h, password_h from hikers_logins where login_h = "'+ user_login +'" and password_h = "'+ user_password +'";')
                    results = self.cursor.fetchall()  # You can use fetchone because login is unique.
                    if results:
                        for row in results:
                            sql_user_id = row[0]
                            sql_user_login = row[1]  # You don't use it anywhere.
                            sql_user_password = row[2]  # You don't use it anywhere.
                        l1 = Hiker(sql_user_id)
                        l1.menu_hiker()
                        break
                    else:
                        print('You gave incorrect credentials. Try again.')                     
             
                
    def register(self):
        
        while True:
            user_access = input('Enter your requested access type (D)Driver (H)Hiker or enter (Q) to quit: ')
            if user_access.upper() == 'D':
                name_d = input('Enter your name: ')
                surname_d = input('Enter your surname: ')
                sex_d = input('Enter your sex(man/woman): ')
                town_d = input('Enter your town: ')
                birth_date_d = input('Enter your birth date(yyyy-mm-dd): ')
                mail_d = input('Enter your mail: ')
                car_brand_d = input('Enter your car brand: ')
                while True:
                    user_login = input('Enter your login: ')
                    results = self.cursor.execute('select login_d from drivers_logins where login_d = %s;',(user_login))
                    if results:
                        print('This login already exists. Please select another one.')
                    else:
                        while True:
                            user_password = input('Enter your password: ')
                            user_password2 = input('Enter your password again: ')
                            if user_password != user_password2:
                                print('You entered 2 different passwords. Try again')
                            else:
                                self.cursor.execute('insert into drivers (name_d, surname_d, sex_d, town_d, birth_date_d, mail_d, car_brand_d) values (%s, %s, %s, %s, %s, %s, %s);',(name_d, surname_d, sex_d, town_d, birth_date_d, mail_d, car_brand_d))
                                self.conn.commit()
                                self.cursor.execute('select max(id_d) from drivers_logins;')
                                id_d = self.cursor.fetchall() # You can use fetchone.
                                self.cursor.execute('update drivers_logins set login_d = %s, password_d = %s where id_d = %s;',(user_login, user_password, id_d))
                                self.conn.commit()
                                print('Your account has been created. Your id is ' + id_d)
                                l1 = Driver(id_d)
                                l1.menu_driver()                                
                                        
            elif user_access.upper() == 'H':
                name_h = input('Enter your name: ')
                surname_h = input('Enter your surname: ')
                sex_h = input('Enter your sex(man/woman): ')
                town_h = input('Enter your town: ')
                birth_date_h = input('Enter your birth date(yyyy-mm-dd): ')
                mail_h = input('Enter your mail: ')
                while True:
                    user_login = input('Enter your login: ')
                    results = self.cursor.execute('select login_h from hikers_logins where login_h = %s;',(user_login))
                    if results:
                        print('This login already exists. Please select another one.')
                    else:
                        while True:
                            user_password = input('Enter your password: ')
                            user_password2 = input('Enter your password again: ')
                            if user_password != user_password2:
                                print('You entered 2 different passwords. Try again')
                            else:
                                self.cursor.execute('insert into hikers (name_h, surname_h, sex_h, town_h, birth_date_h, mail_h) values (%s, %s, %s, %s, %s, %s);',(name_h, surname_h, sex_h, town_h, birth_date_h, mail_h))
                                self.conn.commit()
                                self.cursor.execute('select max(id_h) from hikers_logins;')
                                id_h = self.cursor.fetchall()  # You can use fetchone
                                self.cursor.execute('update hikers_logins set login_h = %s, password_h = %s where id_h = %s;',(user_login, user_password, id_h))
                                self.conn.commit()
                                print('Your account has been created. Your id is ' + id_h)
                                l1 = Hiker(id_h)
                                l1.menu_hiker() 
                  
            elif user_access.upper() == 'Q':
                print ('See you soon again!')
                self.conn.close()
                break             
            else:
                print('Value selected is incorrect.')
                      
class Hiker: 
    def __init__ (self, sql_user_id):
        self.user_id = sql_user_id
        print('''
 __      __   _                    _         _  _ _ _           _                    _      _     _ 
 \ \    / /__| |__ ___ _ __  ___  | |_ ___  | || (_) |_____ _ _( )___  _ __  ___  __| |_  _| |___| |
  \ \/\/ / -_) / _/ _ \ '  \/ -_) |  _/ _ \ | __ | | / / -_) '_|/(_-< | '  \/ _ \/ _` | || | / -_)_|
   \_/\_/\___|_\__\___/_|_|_\___|  \__\___/ |_||_|_|_\_\___|_|   /__/ |_|_|_\___/\__,_|\_,_|_\___(_)
                                                                                                    
        ''')
        self.conn = pymysql.connect(host, conntype, password, database)  
        self.cursor = self.conn.cursor()  

    def menu_hiker(self):    
        print('You are connected with database.') # zostawione do testów
        while True:          
            i = input('\nWhat do you want to do? \n(S)Search for any free car\t(SS)Special search requirements\t(B)Book trip\t(C)Cancel booking\t(D)Delete account\t(Q)Quit: ')
            if i.upper() == 'S':
                self.search()
            elif i.upper() == 'SS':
                self.specialsearch()
            elif i.upper() == 'B':
                self.book()            
            elif i.upper() == 'C':
                self.cancel()    
            elif i.upper() == 'D':
                self.deleteaccount()    
            elif i.upper() == 'Q':
                self.quit()
                break
                
    def search(self):
        print()
        print('%-5.5s|%-12.12s|%-12.12s|%-12.12s|%-12.12s|%-12.12s|%-12.12s|%-5.5s|%-12.12s|%-12.12s|%-12.12s|%-12.12s|%-12.12s|%-12.12s|%-12.12s'%('ID_T','TOWN_START','TOWN_FINISH','DATE_START','DATE_FINISH','FREE_PLACE','POINTS_IN_KM','ID_D','NAME_D','SURNAME_D','SEX_D','TOWN_D','BIRTH_DATE_D','MAIL_D','CAR_BRAND_D'))
        self.cursor.execute('SELECT trips.*, drivers.*  FROM trips left join trips_drivers_hikers on (trips.id_t=trips_drivers_hikers.id_t) left join drivers on (trips_drivers_hikers.id_d=drivers.id_d) where trips.id_t = (SELECT trips.id_t where trips.free_place = "1");')
        results = self.cursor.fetchall()
        for row in results:
            id_t = row[0]
            town_start = row[1]
            town_finish = row[2]
            date_start = row[3]
            date_finish = row[4]
            free_place = row[5]
            points_in_km = row[6]
            id_d = row[7]
            name_d = row[8]
            surname_d = row[9]
            sex_d = row[10]
            town_d = row[11]
            birth_date_d = row[12]
            mail_d = row[13]
            car_brand_d  = row[14]           
            print('%-5.5s|%-12.12s|%-12.12s|%-12.12s|%-12.12s|%-12.12s|%-12.12s|%-5.5s|%-12.12s|%-12.12s|%-12.12s|%-12.12s|%-12.12s|%-12.12s|%-12.12s'%(id_t,town_start,town_finish,date_start,date_finish,free_place,points_in_km,id_d,name_d,surname_d,sex_d,town_d,birth_date_d,mail_d,car_brand_d))

    def specialsearch(self):
        town_start = input('Leaving from: ')
        town_finish = input('Going to: ')
        date_start = input('Start date (yyyy-mm-dd): ')
        self.cursor.execute('SELECT trips.*, drivers.*  FROM trips left join trips_drivers_hikers on (trips.id_t=trips_drivers_hikers.id_t) left join drivers on (trips_drivers_hikers.id_d=drivers.id_d) where trips.id_t = (SELECT trips.id_t where trips.free_place = "1" and trips.town_start = %s and trips.town_finish = %s and trips.date_start = %s);',(town_start, town_finish, date_start))
        results = self.cursor.fetchall()
        if results:
            print('%-5.5s|%-12.12s|%-12.12s|%-12.12s|%-12.12s|%-12.12s|%-12.12s|%-5.5s|%-12.12s|%-12.12s|%-12.12s|%-12.12s|%-12.12s|%-12.12s|%-12.12s'%('ID_T','TOWN_START','TOWN_FINISH','DATE_START','DATE_FINISH','FREE_PLACE','POINTS_IN_KM','ID_D','NAME_D','SURNAME_D','SEX_D','TOWN_D','BIRTH_DATE_D','MAIL_D','CAR_BRAND_D'))
            for row in results:
                id_t = row[0]
                town_start = row[1]
                town_finish = row[2]
                date_start = row[3]
                date_finish = row[4]
                free_place = row[5]
                points_in_km = row[6]
                id_d = row[7]
                name_d = row[8]
                surname_d = row[9]
                sex_d = row[10]
                town_d = row[11]
                birth_date_d = row[12]
                mail_d = row[13]
                car_brand_d  = row[14]         
                print('%-5.5s|%-12.12s|%-12.12s|%-12.12s|%-12.12s|%-12.12s|%-12.12s|%-5.5s|%-12.12s|%-12.12s|%-12.12s|%-12.12s|%-12.12s|%-12.12s|%-12.12s'%(id_t,town_start,town_finish,date_start,date_finish,free_place,points_in_km,id_d,name_d,surname_d,sex_d,town_d,birth_date_d,mail_d,car_brand_d))
        else:
            print('Sorry, no trips match your requirements. Please select (S) to see available trips.')

    def book(self):
        id_t = input('\nWhat is the id of trip to be booked? ')        
        self.cursor.execute('select id_t from trips_drivers_hikers where id_t=%s and id_h is null;',(id_t))
        print(type(self.user_id))        
        results = self.cursor.fetchall()
        if results:
            self.cursor.execute('update trips_drivers_hikers set id_h=%s where id_t=%s;',(self.user_id, id_t))
            self.conn.commit()
            print('The trip has been booked successfully')
        else:
            print('You can\'t book this trip or you have entered incorrect trip id.')        
        
    def cancel(self):
        id_t = input('\nWhat is the id of trip to be cancelled? ')
        self.cursor.execute('select id_t from trips_drivers_hikers where id_t=%s and id_h = %s;',(id_t, self.user_id))
        results = self.cursor.fetchall()
        if results:            
            self.cursor.execute('update trips_drivers_hikers set id_h=null where id_t=%s and id_h=%s;',(id_t, self.user_id))
            self.conn.commit()
            print('Your booking for this trip has been cancelled')
        else:
            print('We couldn\'t cancel this trip. Try again.')

    def deleteaccount(self):
        id_h = input('\nConfirm your id in order to be deleted: ')
        if str(self.user_id) == id_h:
            self.cursor.execute('delete from hikers_logins where id_h=%i;',(id_h)) 
            self.conn.commit()
            print('Your account has been deleted successfully')
            self.quit()
        else:
            print('This is not your id. Try again.')

    def quit(self):
        print('\nConnection ended. Changes have been saved.')
        self.conn.commit()
        self.conn.close() 
        exit()
                

class Driver:
    def __init__ (self, sql_user_id):        
        self.user_id = sql_user_id
        print('''       
 __      __   _                    _         ___      _             _                    _      _     _ 
 \ \    / /__| |__ ___ _ __  ___  | |_ ___  |   \ _ _(_)_ _____ _ _( )___  _ __  ___  __| |_  _| |___| |
  \ \/\/ / -_) / _/ _ \ '  \/ -_) |  _/ _ \ | |) | '_| \ V / -_) '_|/(_-< | '  \/ _ \/ _` | || | / -_)_|
   \_/\_/\___|_\__\___/_|_|_\___|  \__\___/ |___/|_| |_|\_/\___|_|   /__/ |_|_|_\___/\__,_|\_,_|_\___(_)

        ''')
        
        self.conn = pymysql.connect(host, conntype, password, database)

    def menu_driver(self):      
        self.cursor = self.conn.cursor()
        print('You are connected with database.') # zostawione do testów
        while(True):
            i = input('\nWhat do you want to do? \n(A)Add a new trip\t(R)Reject hiker\'s application\t(C)Cancel trip\t(D)Delete account\t(Q)Quit: ')
            if i.upper() == 'A':
                self.add()
            elif i.upper() == 'R':
                self.reject()           
            elif i.upper() == 'C':
                self.cancel()    
            elif i.upper() == 'D':
                self.deleteaccount()    
            elif i.upper() == 'Q':
                self.quit() 
                break
                
    def add(self):
        print()
        town_start = input('Leaving from: ')
        town_finish = input('Going to: ')
        date_start = input('Start date: ')
        date_finish = input('Finish date: ')
        points_in_km = input('Points = kilometers: ')
        self.cursor.execute('insert into trips (town_start, town_finish, date_start, date_finish, free_place, points_in_km) values (%s, %s, %s, %s, "1", %s);', (town_start, town_finish, date_start, date_finish, points_in_km))
        self.conn.commit()
        self.cursor.execute('select max(id_t) from trips')
        id_t = self.cursor.fetchall()  # You can use fetchone
        self.cursor.execute('insert into trips_drivers_hikers (id_t, id_d) values (%s, %s)', (id_t, self.user_id))
        self.conn.commit()
        print('\nTrip has been added.')
    def reject(self):
        id_t = input('\nWhat is the id of trip in which you want to reject hiker\'s application? ')
        self.cursor.execute('select id_t from trips_drivers_hikers where id_t = %s and id_d = %s and id_h is not null',(id_t, self.user_id))
        results = self.cursor.fetchall()
        if results:
            self.cursor.execute('update trips_drivers_hikers set id_h = null where id_t = %s;',(id_t)) 
            self.conn.commit()
            print('Hiker\'s application has been rejected for this trip.')
        else:
            print('We couldn\'t reject this application. Try again.')

    def cancel(self):
        id_t = input('\nWhat is the id of trip which you want to cancel? ')
        self.cursor.execute('select id_t from trips_drivers_hikers where id_t = %s and id_d = %s;',(id_t, self.user_id))
        results = self.cursor.fetchall()
        if results: 
            self.cursor.execute('delete from trips_drivers_hikers where id_t = %s and id_d = %s;',(id_t, self.user_id)) 
            print('Trip has been cancelled.') 
            self.conn.commit()                        
        else:
            print('We couldn\'t cancel this trip. Try again.')
        
    def deleteaccount(self):
        id_d = input('What is the driver id to be deleted? ')
        if str(self.user_id) == id_d:
            self.cursor.execute('delete from drivers_logins where id_d = %s;',(self.user_id))
            self.conn.commit()
            print('Your account has been deleted successfully')
            self.quit()
        else:
            print('This is not your id. Try again.')
        
    def quit(self):
        print('Connection ended. Changes have been saved.')
        self.conn.commit()
        self.conn.close() 
        exit()
                                
db = DBconn()

# TO DO:

