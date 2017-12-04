# -*- coding: utf-8 -*-
import pymysql
from passwords import * 

class DBconn:
    def __init__(self):
        self.conn = pymysql.connect(host, conntype, password, database)
        #self.conn = pymysql.connect('localhost','root','Welcome123','hitchhiking')#w razie potrzeby dopisać 3 przy nazwie bazy danych            
        #self.conn=conn
        self.cursor = self.conn.cursor()
        print('You are connected with database')
        
        while(True):
            choice = input('What do you want to do? (L)Login (R)Register (Q)Quit: ')
            if (choice.upper() == 'L'):
                self.log_in()
                break
            elif (choice.upper() == 'R'):
                self.register() 
                break
            elif (choice.upper() == 'Q'):
                print('Bye!')
                self.conn.close()
                break
            else:
                print('You have entered wrong letter. Try again.')            
            
            
    def log_in(self):

        while(True):
            user_login = input('Enter your login: ')
            user_password = input('Enter your password: ')
            user_access = input('Enter your access type (D)Driver (H)Hiker (A)Admin: ')                        
            if (user_access.upper() == 'D'):
                self.cursor.execute( 'select id_d, login_d, password_d from drivers_logins where login_d = "'+ user_login +'" and password_d = "'+ user_password +'";')
                results = self.cursor.fetchall() 
                if(results):
                    for row in results:
                        sql_user_id = row[0]
                        sql_user_login = row[1]
                        sql_user_password = row[2]
                        print(sql_user_id) # zostawione do testów
                        l1 = Driver(sql_user_id)
                        l1.menu_driver()
                else:
                    print('Incorrect credentials. Try again.')             
            elif (user_access.upper() == 'H'):
                self.cursor.execute( 'select id_h, login_h, password_h from hikers_logins where login_h = "'+ user_login +'" and password_h = "'+ user_password +'";')
                results = self.cursor.fetchall()
                if(results):
                    for row in results:
                        sql_user_id = row[0]
                        sql_user_login = row[1]
                        sql_user_password = row[2]
                        print(sql_user_id) # zostawione do testów
                    l1 = Hiker(sql_user_id)
                    l1.menu_hiker()
                else:
                    print('Incorrect credentials. Try again.')                        
            elif (user_access.upper() == 'A'):
                self.cursor.execute( 'select id_a, login_a, password_a from admins_logins where login_a = "'+ user_login +'" and password_a = "'+ user_password +'";')
                results = self.cursor.fetchall()                
                if(results):
                    for row in results:
                        sql_user_id = row[0]
                        sql_user_login = row[1]
                        sql_user_password = row[2]
                        print(sql_user_id)
                    l1 = Admin(sql_user_id)
                    l1.menu_admin()
                else:
                    print('Incorrect credentials. Try again.')                                
            elif (user_access.upper() == 'Q'):
                print('Bye!')
                self.conn.close()
                break 
            else:
                print('You have entered wrong letter for access type. Try again.')
                
                
    def register(self):
        user_access = input('Enter your requested access type (D)Driver (H)Hiker (A)Admin: ')
        if (user_access.upper() == 'D'):
            name_d = input('Enter your name: ')
            surname_d = input('Enter your surname: ')
            sex_d = input('Enter your sex(man/woman): ')
            town_d = input('Enter your town: ')
            birth_date_d = input('Enter your birth date(yyyy-mm-dd): ')
            mail_d = input('Enter your mail: ')
            car_brand_d = input('Enter your car brand: ')
            user_login = input('Enter your login: ')
            user_password = input('Enter your password: ') 
            #print('insert into drivers (name_d, surname_d, sex_d, town_d, birth_date_d, mail_d, car_brand_d) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s");'%(name_d, surname_d, sex_d, town_d, birth_date_d, mail_d, car_brand_d)) # do testów
            self.cursor.execute('insert into drivers (name_d, surname_d, sex_d, town_d, birth_date_d, mail_d, car_brand_d) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s");',(name_d, surname_d, sex_d, town_d, birth_date_d, mail_d, car_brand_d)) # błąd który chyba dotyczy tej linijki: pymysql.err.DataError: (1265, "Data truncated for column 'sex_d' at row 1")
            self.conn.commit
            self.cursor.execute('select max(id_d) from drivers_logins;')
            id_d = self.cursor.fetchall()
            print(id_d)
            self.cursor.execute('update drivers_logins set login_d = "%s", password_d = "%s" where id_d = %i;',(user_login, user_password, id_d))
            
        elif (user_access.upper() == 'H'):
            pass # analogicznie do drivera
        elif (user_access.upper() == 'A'):
            pass # analogicznie do drivera
        else:
            print('Value selected is incorrect.')
            
        
class Hiker: 
    def __init__ (self, sql_user_id):
        self.user_id = sql_user_id
        print(self.user_id) # zostawione do testów
        self.conn = pymysql.connect(host, conntype, password, database)    
    def menu_hiker(self):    
        self.cursor = self.conn.cursor()
        print('Welcome!\nYou are connected with database.')
        while(True):
            i = input('What do you want to do? \n(S)Search for any free car\t(SS)Special search requirements\t(B)Book trip\t(C)Cancel booking\tD)Delete account\t(Q)Quit ')
            if(i.upper() == 'S'):
                self.search()
            elif(i.upper() == 'SS'):
                self.specialsearch()
            elif(i.upper() == 'B'):
                self.book()            
            elif(i.upper() == 'C'):
                self.cancel()    
            elif(i.upper() == 'D'):
                self.deleteaccount()    
            elif(i.upper() == 'Q'):
                self.quit() 
                
    def search(self):
        self.cursor.execute('SELECT trips.*, drivers.*  FROM trips left join trips_drivers_hikers on (trips.id_t=trips_drivers_hikers.id_t) left join drivers on (trips_drivers_hikers.id_d=drivers.id_d) where trips.id_t = (SELECT trips.id_t where trips.free_place = "1");')
        results = self.cursor.fetchall()
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
    def specialsearch(self):
        town_start = input('Leaving from: ')
        town_finish = input('Going to: ')
        date_start = input('Start date (yyyy-mm-dd): ')
        self.cursor.execute('SELECT trips.*, drivers.*  FROM trips left join trips_drivers_hikers on (trips.id_t=trips_drivers_hikers.id_t) left join drivers on (trips_drivers_hikers.id_d=drivers.id_d) where trips.id_t = (SELECT trips.id_t where trips.free_place = "1" and trips.town_start = "%s" and trips.town_finish = "%s" and trips.date_start = "%s");',(town_start, town_finish, date_start)) # błąd: C:\Users\Ania\AppData\Local\Programs\Python\Python36-32\lib\site-packages\pymysql\cursors.py:166: Warning: (1292, "Incorrect date value: ''2017-12-02'' for column 'date_start' at row 1") result = self._query(query)
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
            print('%-5.5s|%-12.12s|%-12.12s|%-12.12s|%-12.12s|%-12.12s|%-12.12s|%-5.5s|%-12.12s|%-12.12s|%-12.12s|%-12.12s|%-12.12s|%-12.12s|%-12.12s'%('ID_T','TOWN_START','TOWN_FINISH','DATE_START','DATE_FINISH','FREE_PLACE','POINTS_IN_KM','ID_D','NAME_D','SURNAME_D','SEX_D','TOWN_D','BIRTH_DATE_D','MAIL_D','CAR_BRAND_D'))
    def book(self):
        id_t = int(input('What is the id of trip to be booked? '))
        self.user_id = int(self.user_id)
        self.cursor.execute('update trips_drivers_hikers set id_h=%i where id_t=%i;'%(self.user_id, id_t)) # BŁĄD CHYBA USUNIĘTY, PRZETESTOWAĆ
    def cancel(self):
        id_t = int(input('What is the id of trip to be cancelled? '))
        self.cursor.execute('update trips_drivers_hikers set id_h=null where id_t=%i and id_h=%i;'%(id_t, self.user_id))
    def deleteaccount(self):
        id_h = input('Confirm the hiker id to be deleted: ')
        if(self.user_id == id_h):
            self.cursor.execute('delete from hikers_logins where id_h=%i;'%(self.user_id)) # BŁĄD CHYBA USUNIĘTY, PRZETESTOWAĆ
        else:
            print('This is not your id. Try again.')
    def quit(self):
        print('Connection ended. Changes have been saved.')
        self.conn.commit()
        self.conn.close()
                

class Driver:
    def __init__ (self, sql_user_id):        
        self.user_id = sql_user_id
        print(self.user_id) # zostawione do testów        
        self.conn = pymysql.connect(host, conntype, password, database)

    def menu_driver(self):      
        self.cursor = self.conn.cursor()
        print('Welcome!\nYou are connected with database.')
        while(True):
            i = input('What do you want to do? \n(A)Add a new trip\t(R)Reject hiker\'s application\t(C)Cancel trip\t(D)Delete account\t(Q)Quit ')
            if(i.upper() == 'A'):
                self.add()
            elif(i.upper() == 'R'):
                self.reject()           
            elif(i.upper() == 'C'):
                self.cancel()    
            elif(i.upper() == 'D'):
                self.deleteaccount()    
            elif(i.upper() == 'Q'):
                self.quit() 
    def add(self):
        town_start = input('Leaving from: ')
        town_finish = input('Going to: ')
        date_start = input('Start date: ')
        date_finish = input('Finish date: ')
        points_in_km = int(input('Points = kilometers: '))
        self.cursor.execute('insert into trips (town_start, town_finish, date_start, date_finish, free_place, points_in_km) values (%s, %s, %s, %s, "1", %i);', (town_start, town_finish, date_start, date_finish, points_in_km))
    def reject(self):
        id_t = int(input('What is the id of trip in which you want to reject hiker\'s application? '))
        self.cursor.execute('update trips_drivers_hikers set id_h = NULL where id_t = %i;'%(id_t)) 
    def cancel(self):
        id_t = int(input('What is the id of trip which you want to cancel? '))
        self.cursor.execute('delete from trips_drivers_hikers where id_t = %i and id_d = %i;'%(id_t, self.user_id)) # BŁĄD CHYBA USUNIĘTY, PRZETESTOWAĆ
    def deleteaccount(self):
        id_d = int(input('What is the driver id to be deleted? ')) 
        self.cursor.execute('delete from drivers_logins where id_d = %i;'%(self.user_id)) # BŁĄD CHYBA USUNIĘTY, PRZETESTOWAĆ
    def quit(self):
        print('Connection ended. Changes have been saved.')
        self.conn.commit()
        self.conn.close()        
                
                
db = DBconn()
# TO DO:
# usunąć błędy pokazujące sie przy wszystkich zapytaniach co do formatu
# ascii art generator
# dodać opis i informację z linkiem do bazy danych