import os
import time
import json
import requests
import threading

# Taking JSON file path and folder name

print('*********')
json_name = input('Enter json file name. >>>  ')
print('*********')
dir_name = input('Please enter your directory name for downloading pictures. >>> ')

# Start time of the program

t1 = time.time()

pic_names = []
urls_list = []
thread_list = []

# Taking JSON URL's and defining pictures name

try:
    parent_dir = os.getcwd()
    path = os.path.join(parent_dir, dir_name) 
    os.mkdir(path)

    with open(json_name, 'r') as f:
        data = json.load(f)
    for i in data.values():
        for j in i:
            a = list(j.values())[0]
            urls_list.append(a)

    for i in range(1, len(urls_list) + 1):
        name = 'picture_' + str(i) + '.jpeg'
        pic_names.append(name)

except FileExistsError:
    print('*********')
    print('Folder with the same name already exists.')
    pass  

# Downloading images and importing to the created folder

def download_images(url, name):
    try:
        r = requests.get(url)
        out = open(f'{path}/{name}', 'wb')
        out.write(r.content)
        out.close()
        print(f'{name} downloaded !')
    except requests.exceptions.RequestException as e:
        print('Somthing went wrong with URLs.')

# Using threading

for i in range(0, len(urls_list)):
    t = threading.Thread(target = download_images, args = (urls_list[i], pic_names[i]))
    thread_list.append(t)
    t.start()
for j in thread_list:
    j.join()

# End time of the project

t2 = time.time()

print('*********') 

# Calculating time for the project

print(f'The program ends in {t2 - t1} seconds.')

# Deleting folder if it's empty

if os.path.exists(path) and len(os.listdir(path)) == 0:
    print(f'Folder {dir_name} deleted because it is empty.')
    os.rmdir(path)
