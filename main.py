import vk
import webbrowser
import time
from  geopy.geocoders import Nominatim
import os
import geopandas
import folium
from selenium import webdriver
keyword_city = "Москва"
geolocator = Nominatim()
location = geolocator.geocode(keyword_city)
#print((location.latitude,location.longitude))
m=folium.Map(
            location=[location.latitude, location.longitude]
        )
keywords_groups = ['новости', 'происшествия', 'события']
print('Войдите и дайте приложению необходимые разрешения.\n')
print('------------------\n')
#webbrowser.open('https://oauth.vk.com/authorize?client_id=6998450&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends%2Cphotos%20%2Caudio%2Cvideo%2Cdocs%2Cnotes%2Cpages%2Cstatus%2Cwall%2Cgroups%2Cnotifications%2Coffline&response_type=token')
driver = webdriver.Firefox()
driver.get('https://oauth.vk.com/authorize?client_id=6998450&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends%2Cphotos%20%2Caudio%2Cvideo%2Cdocs%2Cnotes%2Cpages%2Cstatus%2Cwall%2Cgroups%2Cnotifications%2Coffline&response_type=token')
print('Подтвердите вход(чото написать надо кароче, я не знаю как сделать нажатие на кнопку)')
confirm=str(input())
apikey = driver.current_url[45:][0:-31]
driver.close()
print("Токен: "+apikey)
#Альтернативная ссылка
#print('https://oauth.vk.com/token?grant_type=password&client_id=6998450&client_secret=hHbZxrka2uZ6jB1inYsH&username='+login+'&password='+password)
#url = os.environ["https://oauth.vk.com/authorize?client_id=6998450&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends%2Cphotos%20%2Caudio%2Cvideo%2Cdocs%2Cnotes%2Cpages%2Cstatus%2Cwall%2Cgroups%2Cnotifications%2Coffline&response_type=token"]
#parsed = urlparse.urlparse(url)
#print (urlparse.parse_qs(parsed.query)['access_token'])
session = vk.Session(access_token = apikey)
api = vk.API(session,timeout=60)
#print('\nВведите короткую ссылку на паблик или пользователя: \n')
#short_link=str(input())
print('\nСколько постов из каждого паблика вы хотите загрузить?\n')
n = int(input())
print('\n-----------------')
print('\nТематики поиска: \n-новости\n-происшествия\n-события')
print('\nСколько брать пабликов по каждой тематике из каждого города?')
public_count = int(input())
print("\nСколько брать городов?")
city_count = int(input())
#owner_id - если есть id, domain - если есть короткий адрес
#wall_content = api.wall.get(v='5.95',domain=short_link, count=n)
#print(wall_content)
cities = api.database.getCities(country_id=1, need_all=0, count=city_count, v='5.95')['items']
group_ids=''
groups=[]
for city in cities:
    print(city['id'], "\t", city['title'])
print('\n-----------------------------------------------------')
for q in range(len(cities)):
    city_id = cities[q]['id']
    city_name = cities[q]['title']
    group_string = ''
    group_list = ''
    group_id_list = ''
    groups_count = 1
    for keyword in keywords_groups:
        groups=[]
        time.sleep(1)
        # Получаем список IDs групп города удовлетворяющих ключевому слову
        group_ids = [g['id'] for g in api.groups.search(v='5.95', city_id=city_id, q=keyword, sort=2, count=public_count)['items']]

        # Получаем список групп города удовлетворяющих ключевому слову
        for group_id in group_ids:
            time.sleep(1)
            groups.append(api.groups.getById(v='5.95', fields='members_count,contacts', group_id=group_id)[0]['name'])
            group_id_list+=(str(group_id)+", ")

        for group in groups:
            group_string+=('\n'+str(groups_count)+') '+group+'\n')
            group_list+=(group+", ")
            groups_count+=1

        with open('wall_output.txt','a') as out:
            #for key,val in wall_content.items():
            #out.write('{}:{}\n'.format(key,val))
            for group_id in group_ids:
                closed = api.groups.getById(v='5.95', group_id=group_id)[0]['is_closed']
                if (closed == 0):
                    for k in range(n):
                        time.sleep(1)
                        wall_content = api.wall.get(v='5.95', owner_id=int(group_id)*-1, count=n)
                        print("Стена открыта")
                        out.write("Паблик с id ('"+str(-1*wall_content['items'][k]['owner_id'])+"') запостил: \n\n"+wall_content['items'][k]['text']+"\n------------------------------------------\n")
                elif(closed==1 or closed==2):
                    print("Стена закрыта")
    print(city_name + ":\nГруппы " + group_list + "\nС id " + group_id_list + "\n---------------------")
    location = geolocator.geocode(city_name)
    folium.Marker([location.latitude, location.longitude], popup=group_string, tooltip="Нажмите").add_to(m)
m.save('map.html')
webbrowser.open('map.html')
print('\nВывод всех постов в файле wall_output.txt')
print('\nВывод маркеров на карте в файле map.html')
