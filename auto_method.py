import urllib.request as urllib
import json
import time
from bs4 import BeautifulSoup


def get_html(url):
    api_arl = 'https://api.instagram.com/oembed/?url='
    url = api_arl + url
    return urllib.urlopen(url).read()


def parse(code):
    code = BeautifulSoup(code, "lxml")
    text = code.find('p').text
    media_id = json.loads(text)['media_id']
    media_link = 'http://75.102.21.228/add?id=' + str(media_id)
    return media_link


def out(media_url):
    code = urllib.urlopen(media_url).read()
    code = BeautifulSoup(code, "lxml")
    text = code.find('p').text
    if text == '0':
        print('Success.')
        return True
    else:
        print('Error occurred. Please try again')
        return False


def check_likes(code):
    code = BeautifulSoup(code, "lxml")
    div_likes = code.find('div', class_='_iuf51 _oajsw')
    try:
        likes = div_likes.find('span', class_='').text
    except:
        likes = -1
        print(div_likes)

    return likes


def add_likes(user_url):
    try:
        html = get_html(user_url)
    except:
        print('Not a valid instagram url !')
        return
    success = out(parse(html))
    return success


def main():
    user_url = input('Paste your image or video link: \n')

    wanted_likes = int(input('How many likes do you want ? (Warning: program makes about 10 likes per minute) \n'
                             + 'More than: '))
    print('Program will work until current likes amount will be more than wanted likes amount !')
    print('It means that after some time your like amount will be more than wanted !')
    current_likes = int(check_likes(urllib.urlopen(user_url).read()))
    if current_likes == -1:
        current_likes = int(input('Enter your current likes'))
    print('Your current likes amount is - ' + str(current_likes))

    likes_need = wanted_likes - current_likes
    # print(likes_need)
    if likes_need > 0:
        sleep = likes_need * 6
        while current_likes < wanted_likes:
            if current_likes > 0:
                add_likes(user_url)
                print('Waiting for ' + str(sleep) + ' seconds')
                time.sleep(sleep)
            current_likes = int(check_likes(urllib.urlopen(user_url).read()))
            if current_likes > 0:
                print('Your current likes amount is - ' + str(current_likes))

    print('OK.')
    print('Your current likes amount is more than - ' + str(wanted_likes) + '(' + str(current_likes) + ')')
    print('And it will be even more than current amount !')

if __name__ == '__main__':
    main()
