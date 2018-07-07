class Searcher:
    def __init__(self):
        import sqlite3
        self.conn = sqlite3.connect('films_info.db')
        self.cursor = self.conn.cursor()

    def general_search(self,search_input):
        
        result = []
        counter = 0
        if '[' in search_input:
            query = search_input.split('[')[1][0:-1]
            counter = 1
            search_input = search_input.split('[')[0].rstrip()
        name_result = self.search_by_name(search_input)
        cast_result = self.search_by_cast(search_input)
        abstract_result = self.search_by_abstract(search_input)
        country_result = self.search_by_country(search_input)
        genre_result = self.search_by_genre(search_input)
        keyword_result = self.search_by_keyword(search_input)
        language_result = self.search_by_language(search_input)

        for item in name_result:
            if item not in result:
                result.append(item)
        for item in cast_result:
            if item not in result:
                result.append(item)
        for item in abstract_result:
            if item not in result:
                result.append(item)
        for item in country_result:
            if item not in result:
                result.append(item)
        for item in genre_result:
            if item not in result:
                result.append(item)
        for item in keyword_result:
            if item not in result:
                result.append(item)
        for item in language_result:
            if item not in result:
                result.append(item)

        if len(result[0]) >=1:
            for i in range(len(result)):
                if type(result[i][0])== list:
                    result[i] = result[i][0]
            if counter == 1:

                f = query.split('|')
                query=[]
                for i in f:
                    query.append(i)
                print(query)
                notcounter=0
                #NOOOOOOOOOOOT :D
                for i in query:
                    if 'NOT' in i:
                        notcounter=1
                        i=i[4:-1].split(',')
                        nots=i
                        #print(i)
                if notcounter==1:
                    temp = []
                    for i in result:
                        a = ''
                        for j in i:
                            a += str(j)
                            a +='@'
                        temp.append(a)
                    temp2=[]
                    for j in temp:
                        rmcounter=0
                        for i in nots:
                            if i in j:
                                rmcounter=1
                        if rmcounter==0:
                            temp2.append(j)
                    temp3=[]
                    for j in temp2:
                        j=j[0:j.index('@')]
                        self.cursor.execute('''SELECT * FROM Films WHERE ID = ?''', (j,))
                        films = list(map(list, self.cursor.fetchall()))
                        temp3.append(self.replace_information(films))
                    #print(temp3)
                    temp4=[]
                    for i in temp3:
                        temp4.append(i[0])
                    result=temp4
                
                orcounter=0
                #OOOOOORR :D
                for i in query:
                    
                    if 'OR' in i:
                        orcounter=1
                        i=i[4:-1].split(',')
                        ors=i
                        #print(i)
                if orcounter==1:
                    temp = []
                    for i in result:
                        a = ''
                        for j in i:
                            a += str(j)
                            a +='@'
                        temp.append(a)
                    temp2=[]
                    for j in temp:
                        rmcounter=0
                        for i in ors:
                            if i in j:
                                rmcounter=1
                        if rmcounter==1:
                            temp2.append(j)
                    temp3=[]
                    for j in temp2:
                        j=j[0:j.index('@')]
                        self.cursor.execute('''SELECT * FROM Films WHERE ID = ?''', (j,))
                        films = list(map(list, self.cursor.fetchall()))
                        temp3.append(self.replace_information(films))
                    #print(temp3)
                    temp4=[]
                    for i in temp3:
                        temp4.append(i[0])
                    result=temp4

                andcounter=0
                #and:D
                for i in query:     
                    if 'AND' in i:
                        andcounter=1
                        i=i[4:-1].split(',')
                        ands=i
                        #print(i)

                if andcounter==1:
                    temp = []
                    for i in result:
                        a = ''
                        for j in i:
                            a += str(j)
                            a +='@'
                        temp.append(a)
                    temp2=[]
                    for j in temp:
                        rmcounter=0
                        for i in ands:
                            if i not in j:
                                rmcounter=1
                        if rmcounter==0:
                            temp2.append(j)
                    temp3=[]
                    for j in temp2:
                        j=j[0:j.index('@')]
                        self.cursor.execute('''SELECT * FROM Films WHERE ID = ?''', (j,))
                        films = list(map(list, self.cursor.fetchall()))
                        temp3.append(self.replace_information(films))
                    #print(temp3)
                    temp4=[]
                    for i in temp3:
                        temp4.append(i[0])
                    result=temp4
        return result


    

    def search_by_name(self,name):
        self.cursor.execute('''SELECT * FROM Films WHERE Film_Name LIKE ?''', ("%" + name + "%",))
        films = list(map(list, self.cursor.fetchall()))
        return self.replace_information(films)

    def search_by_cast(self,cast):
        casts_id = list(map(list, self.cursor.execute('''SELECT ID FROM Casts WHERE Casts.Cast LIKE ?''',("%" + cast + "%",)).fetchall()))
        films = []
        for item in casts_id:
            cast_id = str(item[0])
            self.cursor.execute('''SELECT * FROM Films WHERE Casts_ID LIKE ?''', ("%" + cast_id + "%",))
            cast_films = list(map(list, self.cursor.fetchall()))
            films.append(self.replace_information(cast_films))
        return films
    def search_by_id(self,id):
        films = []
        self.cursor.execute('''SELECT * FROM Films WHERE ID = ?''', (str(id),))
        keyword_films = list(map(list, self.cursor.fetchall()))
        films.append(self.replace_information(keyword_films))
        return films
    def search_by_abstract(self,keyword):
        films = []
        #for item in keywords:
        #keyword = str(item[0])
        self.cursor.execute('''SELECT * FROM Films WHERE Abstract LIKE ?''', ("%" + keyword + "%",))
        keyword_films = list(map(list, self.cursor.fetchall()))
        films.append(self.replace_information(keyword_films))
        return films

    def search_by_genre(self,genre):
        genres_id = list(map(list, self.cursor.execute('''SELECT ID FROM Genres WHERE Genre LIKE ?''',
                                                      ("%" + genre + "%",)).fetchall()))

        films = []
        for item in genres_id:
            genre_id = str(item[0])
            self.cursor.execute('''SELECT * FROM Films WHERE Genres_ID LIKE ?''', ("%" + genre_id + "%",))
            genre_films = list(map(list, self.cursor.fetchall()))
            films.append(self.replace_information(genre_films))
        return films

    def search_by_keyword(self, keyword):
        self.cursor.execute('''SELECT * FROM Films WHERE Keywords LIKE ?''', ("%" + keyword + "%",))
        films = list(map(list, self.cursor.fetchall()))
        return self.replace_information(films)

    def search_by_country(self,country):
        countries_id = list(map(list, self.cursor.execute('''SELECT ID FROM Countries WHERE Country LIKE ?''',
                                                      ("%" + country + "%",)).fetchall()))

        films = []
        for item in countries_id:
            country_id = str(item[0])
            self.cursor.execute('''SELECT * FROM Films WHERE Countries_ID LIKE ?''', ("%" + country_id + "%",))
            country_films = list(map(list, self.cursor.fetchall()))
            films.append(self.replace_information(country_films))
        return films

    def search_by_language(self,language):
        self.cursor.execute('''SELECT * FROM Films WHERE Language LIKE ?''', ("%" + language + "%",))
        films = list(map(list, self.cursor.fetchall()))
        return self.replace_information(films)

    def replace_information(self, films):
        for film in films:
            casts_id = list(map(int, film[2].split(',')))
            try:
                genres_id = list(map(int, film[4].split(',')))
            except:
                genres_id = []
            countries_id = list(map(int, film[6].split(',')))

            casts = []
            for id in casts_id:
                execute_text = 'SELECT "Cast" FROM Casts INNER JOIN films ON Casts.ID = ' + str(id)
                self.cursor.execute(execute_text)
                casts.append(self.cursor.fetchone()[0])

            casts_str = ''
            for i in casts:
                casts_str += i + ','
            casts_str = casts_str[:len(casts_str) - 1]

            film[2] = casts_str

            genres = []
            for id in genres_id:
                self.cursor.execute('''SELECT Genre FROM Genres INNER JOIN Films ON Genres.ID =? ''',(id,))
                genres.append(self.cursor.fetchone()[0])

            genres_str = ''
            for i in genres:
                genres_str += i + ','
            genres_str = genres_str[:len(genres_str) - 1]

            film[4] = genres_str

            countries = []
            for id in countries_id:
                execute_text = 'SELECT Country FROM Countries INNER JOIN Films ON Countries.ID = ' + str(id)
                self.cursor.execute(execute_text)
                countries.append(self.cursor.fetchone()[0])

            countries_str = ''
            for i in countries:
                if type(i) == str:
                    countries_str += i + ','
            countries_str = countries_str[:len(countries_str) - 1]

            film[6] = countries_str

        return films

s = Searcher()
print(s.search_by_id(16))
