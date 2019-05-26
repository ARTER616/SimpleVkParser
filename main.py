import vk
import webbrowser
#print('Введите ваш логин: \n')
#login=str(input())
#print('Введите ваш пароль: \n')
#password=str(input())
print('Дайте приложению необходимые разрешения, а после скопируйте токен.\n')
print('------------------\n')
webbrowser.open('https://oauth.vk.com/authorize?client_id=6998450&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends%2Cphotos%20%2Caudio%2Cvideo%2Cdocs%2Cnotes%2Cpages%2Cstatus%2Cwall%2Cgroups%2Cnotifications%2Coffline&response_type=token')
#Альтернативная ссылка
#print('https://oauth.vk.com/token?grant_type=password&client_id=6998450&client_secret=hHbZxrka2uZ6jB1inYsH&username='+login+'&password='+password)
print('Вставьте токен: \n')
apikey=str(input())
#apikey = 'b23f06c86fdc0ad3280b97f776da3806102e218777e3d8dc80670e6f089985899883fa88b213a9db0030e'
session = vk.Session(access_token = apikey)
api = vk.API(session,timeout=60)
print('\nВведите короткую ссылку на паблик или пользователя: \n')
short_link=str(input())
print('\nСколько постов вы хотите загрузить?\n')
n = int(input())
#owner_id - если есть id, domain - если есть короткий адрес
wall_content = api.wall.get(v='5.95',domain=short_link, count=n)
print(wall_content)
with open('wall_output.txt','w') as out:
    #for key,val in wall_content.items():
       #out.write('{}:{}\n'.format(key,val))
     for k in range(n):
        out.write("Паблик/пользователь с id ('")
        out.write(str(wall_content['items'][k]['owner_id']))
        out.write("') запостил: ")
        out.write("\n")
        out.write(wall_content['items'][k]['text'])
        out.write("\n")
        out.write("------------------------------------------")
        out.write("\n")
print('\nКорректный вывод в файле wall_output.txt')
