import requests
import threading
import queue
from bs4 import BeautifulSoup
import time


if __name__ == "__main__":
    url = "https://images.alexonsager.net/pokemon/fused"
    for i in range(1, 151):
        for j in range(1, 151):
            img_url = '{_root}/{_i}/{_i}.{_j}.png'.format(_root=url, _i=i,_j=j)

            #print("requesting i={_i},j={_j}".format(_i=i,_j=j))
            while True:
                try:
                    r = requests.get(img_url, timeout=5)
                    break
                except requests.exceptions.ConnectionError:
                    #print('i={_i} j={_j} Connection Error'.format(_i=i,_j=j))
                    time.sleep(1)
                except:
                    #print("Unknown err")
                    time.sleep(1)
            img_content = r.content
            number1 = i
            number2 = j

            #print("requesting pokemon name i={_i},j={_j}".format(_i=i,_j=j))
            name_url = "https://pokemon.alexonsager.net/fr/{_i}/{_j}".format(_i=i,_j=j)
            #print("requesting image i={_i},j={_j}".format(_i=i,_j=j))
            while True:
                try:
                    r = requests.get(name_url, timeout=5)
                    break
                except requests.exceptions.ConnectionError:
                    #print('i={_i} j={_j} Connection Error'.format(_i=i,_j=j))
                    time.sleep(1)
                except:
                    #print("Unknown err")
                    time.sleep(1)
            
            
            soup = BeautifulSoup(r.text, 'html.parser')
            res_dir = soup.find_all(id='pk_name')
            name = res_dir[0].text
            filename = './fr/{_i}x{_j} {_pokemon_name}.png'.format(_pokemon_name=name,_i=i,_j=j)
            with open(filename, "wb") as f:
                f.write(img_content)
                f.close()

            #print("i={_i}, j={_j} Complete.".format(_i=i, _j=j))
        print("i={_i} Complete".format(_i=i))
    
