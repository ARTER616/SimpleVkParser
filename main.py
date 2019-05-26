import vk

output = open('wall_output.txt','a')
apikey = 'b23f06c86fdc0ad3280b97f776da3806102e218777e3d8dc80670e6f089985899883fa88b213a9db0030e'
session = vk.Session(access_token = apikey)
api = vk.API(session,timeout=60)
n = 5
#owner_id - если есть id, domain - если есть короткий адрес
wall_content = api.wall.get(v='5.95',domain='gulag.media', count=n)
print(wall_content)
with open('wall_output.txt','a') as out:
    #for key,val in wall_content.items():
       #out.write('{}:{}\n'.format(key,val))
     for k in range(n):
        out.write("Паблик с id ('")
        out.write(str(wall_content['items'][k]['owner_id']))
        out.write("') запостил: ")
        out.write("\n")
        out.write(wall_content['items'][k]['text'])
        out.write("\n")
        out.write("------------------------------------------")
        out.write("\n")
