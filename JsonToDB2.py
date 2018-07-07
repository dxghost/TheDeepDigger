import json, sqlite3
conn = sqlite3.connect('films_info.db')
c = conn.cursor()
def split(s):
    bits=s[1:-1].splot(',')
with open('imdb.json', 'r') as json_data:
    counter=0
    try:
        films = json.load(json_data)
        counter=1
    except:pass

try:

    IDs = list(c.execute('''SELECT ID FROM Films ORDER BY ID'''))
    film_id = IDs[len(IDs) - 1][0] + 1
    IDs = list(c.execute('''SELECT ID FROM Casts ORDER BY ID'''))
    cast_id = IDs[len(IDs) - 1][0] + 1
    IDs = list(c.execute('''SELECT ID FROM Genres ORDER BY ID'''))
    genre_id = IDs[len(IDs) - 1][0] + 1
    IDs = list(c.execute('''SELECT ID FROM Countries ORDER BY ID'''))
    country_id = IDs[len(IDs) - 1][0] + 1
except:
    film_id = 0
    cast_id = 0
    genre_id = 0
    country_id = 0
finally:
    conn.commit()
    conn.close()

conn = sqlite3.connect('films_info.db')
c = conn.cursor()

for film in films:
    if type(film['FilmName']) == str:
        film_name = film['FilmName'].rstrip()
    url = film['URL']
    casts = film['Cast']
    genres = film['Genres']
    try:
        abstract = film['Story'].rstrip()
    except:
        abstract = film['Story']
    keywords = film['Keywords']
    language = film['Language']
    countries = film['Country']
    release_date = film['ReleaseDate']
    image_url = film['ImageURL']
    if not casts:
        continue


    casts_id = ''
    for cast in casts:
        try:
            CastAttrs = (cast_id, cast)
            c.execute('INSERT INTO Casts VALUES (?,?)', CastAttrs)
            casts_id += str(cast_id) + ','
            cast_id += 1
        except:
            c.execute('''SELECT ID FROM Casts WHERE Casts.Cast = ?''', (cast,))
            id = list(c.fetchone())[0]
            casts_id += str(id) + ','
    casts_id = casts_id[:len(casts_id) - 1]
    genres_id = ''
    for genre in genres:
        try:
            GenreAttrs = (genre_id, genre)
            c.execute('INSERT INTO Genres VALUES (?,?)', GenreAttrs)
            genres_id += str(genre_id) + ','
            genre_id += 1
        except:
            c.execute('''SELECT ID FROM Genres WHERE Genres.Genre = ?''', (genre,))
            id = list(c.fetchone())[0]
            genres_id += str(id) + ','
    genres_id = genres_id[:len(genres_id) - 1]
    if type(countries) == list:
        countries_id = ''
        for country in countries:
            try:
                CountryAttrs = (country_id, country)
                c.execute('INSERT INTO Countries VALUES (?,?)', CountryAttrs)
                countries_id += str(country_id) + ','
                country_id += 1
            except:
                c.execute('''SELECT ID FROM Countries WHERE Countries.Country = ?''', (country,))
                id = list(c.fetchone())[0]
                countries_id += str(id) + ','
        countries_id = countries_id[:len(countries_id) - 1]
    else:
        countries_id = ''
        try:
            CountryAttrs = (country_id, countries)
            c.execute('INSERT INTO Countries VALUES (?,?)', CountryAttrs)
            countries_id += str(country_id) + ','
            country_id += 1
        except:
            c.execute('''SELECT ID FROM Countries WHERE Countries.Country = ?''', (countries,))
            id = list(c.fetchone())[0]
            countries_id += str(id) + ','
        countries_id = countries_id[:len(countries_id) - 1]
    search_text_casts = ''
    for cast in casts:
        search_text_casts += cast

    search_text_genres = ''
    for genre in genres:
        search_text_genres += genre

    search_text_keywords = ''
    for keyword in keywords:
        search_text_keywords += keyword + ', '
    search_text_keywords = search_text_keywords[:len(search_text_keywords) -2 ]
    search_text_countries = ''
    if type(countries)==list:
        for country in countries:
            search_text_countries += country

    filmAttrs = [(film_id, film_name, casts_id, abstract, genres_id, search_text_keywords, countries_id, language, release_date, url,
                 image_url)]
    c.executemany('INSERT INTO Films VALUES (?,?,?,?,?,?,?,?,?,?,?)', filmAttrs)
    film_id += 1
    print(film_id)
conn.commit()

conn.close()
