import requests
import threading
import queue
from bs4 import BeautifulSoup
import time

global io_task_queue
io_task_queue = queue.Queue()
global exit_flag
exit_flag = 0
global pokemon_dict
pokemon_dict = {}

class pokemon:
    def __init__(self, number1, number2, name, img_content):
        self.number1 = number1
        self.number2 = number2
        self.name = name
        self.img_content = img_content

class io_thread (threading.Thread):
    def run(self):
        while not exit_flag:
            if not queue.Empty():
                pokemon_info = io_task_queue.get()
                filename = '{_pokemon_name}.png'.format(_pokemon_name=pokemon_info.name)
                with open(filename, "wb") as f:
                    f.write(pokemon_info.img_content)
                    f.close()
            
            

class get_thread (threading.Thread):
    def run(self):
        url = "https://images.alexonsager.net/pokemon/fused"
        for i in range(1, 151):
            for j in range(1, 151):
                img_url = '{_root}/{_i}/{_i}.{_j}.png'.format(_root=url, _i=i,_j=j)
                r = requests.get(img_url, timeout=30)
                img_content = r.content
                number1 = i
                number2 = j
                
                name_url = "https://pokemon.alexonsager.net/zh/{_i}/{_j}".format(_i=i,_j=j)
                r = requests.get(name_url, timeout=30)
                soup = BeautifulSoup(r.text, 'html.parser')
                res_dir = soup.find_all(id='pk_name')
                name = res_dir[0].text
                if j == 1:
                    pokemon_dict[i] = name
                io_task_queue.put(pokemon(number1, number2, name, img_content))
                pass


        exit_flag = 1
    


if __name__ == "__main__":
    url = "https://images.alexonsager.net/pokemon/fused"
    for i in range(3, 151):
        t = 1
        if i == 3:
            t = 100
        for j in range(t, 151):
            img_url = '{_root}/{_i}/{_i}.{_j}.png'.format(_root=url, _i=i,_j=j)

            print("requesting i={_i},j={_j}".format(_i=i,_j=j))
            while True:
                try:
                    r = requests.get(img_url, timeout=5)
                    break
                except requests.exceptions.ConnectionError:
                    print('i={_i} j={_j} Connection Error'.format(_i=i,_j=j))
                    time.sleep(1)
                except:
                    print("Unknown err")
                    time.sleep(1)
            img_content = r.content
            number1 = i
            number2 = j

            #print("requesting pokemon name i={_i},j={_j}".format(_i=i,_j=j))
            name_url = "https://pokemon.alexonsager.net/zh/{_i}/{_j}".format(_i=i,_j=j)
            #print("requesting image i={_i},j={_j}".format(_i=i,_j=j))
            while True:
                try:
                    r = requests.get(name_url, timeout=5)
                    break
                except requests.exceptions.ConnectionError:
                    print('i={_i} j={_j} Connection Error'.format(_i=i,_j=j))
                    time.sleep(1)
                except:
                    print("Unknown err")
                    time.sleep(1)
            
            
            soup = BeautifulSoup(r.text, 'html.parser')
            res_dir = soup.find_all(id='pk_name')
            name = res_dir[0].text
            if j == 1:
                pokemon_dict[i] = name
            filename = '{_i}x{_j} {_pokemon_name}.png'.format(_pokemon_name=name,_i=i,_j=j)
            with open(filename, "wb") as f:
                f.write(img_content)
                f.close()

            print("i={_i}, j={_j} Complete.".format(_i=i, _j=j))
    
