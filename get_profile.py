import os
import json
import urllib
import argparse
import collections
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

BASE_SRC='http://www.keyakizaka46.com/s/k46o/artist/'

MAX_MEMBER=52
NULL_MEMBERS={2,10,16,19 } #Add Grads

IMAGE_DST='images/'
JSON_DST='keyaki.json'

def simple_get(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    print(e)


def process_image(html, num):
    """Get the image link and download fullsize
    @params:
        object html: BeautifulSoup object that contain tags from profile link
        string num: member's number; image would be named after
    """
    if not os.path.exists(IMAGE_DST):
        os.makedirs(IMAGE_DST)
    img_box = html.find("div", {"class": "box-profile_img"})
    img_link = img_box.find("img")['src']

    dl = img_link.replace("/400_320_102400", '')
    name_file = IMAGE_DST + num + ".jpg"
    try:
        urllib.request.urlretrieve(dl, name_file)
    except URLError:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))


def get_profile(html):
    """Get the image link and gather the profile details
    @params:
        object html:BeautifulSoup object that contain tags from profile link
    @return:
        object: a dictionary that contains all the profile data
    """
    profile_dict = collections.OrderedDict()
    profile_box = html.find("div", {"class": "box-profile_text"})
    name = profile_box.find("p", {"class": "name"}).text
    profile_dict['name'] = name.strip().replace(" ",'')
    profile_dict['furigana'] = profile_box.find("p",
            {"class": "furigana"}).text.strip()
    profile_dict['en_name'] = profile_box.find("span",
            {"class": "en"}).text.replace("\u3000", " ")

    info_box = profile_box.find("div", {"class": "box-info"})
    all_info = info_box.findAll("dt")

    info_arr = []
    for info in all_info:
        info_arr.append(info.text.strip())

    # TO DO: Improve this as it's more than 80 char
    profile_dict['birthday'], profile_dict['horoscope'], profile_dict['height'], profile_dict['birthplace'], profile_dict['blood_type'] = info_arr
    return profile_dict


def process_html():
    """Read the profile links, download profile image,
    get profile data and dumps into json
    """
    print("Gathering members' profile")
    data = collections.OrderedDict()
    for i in range(1, MAX_MEMBER+1):
        if i not in NULL_MEMBERS:
            num = str(i)
            if ( len(num) == 1):
                num = '0' + num
            html_address = BASE_SRC + num
            raw_html = simple_get(html_address)
            html = BeautifulSoup(raw_html, 'html.parser')
            process_image(html, num)
            data[num] = get_profile(html)
    with open(JSON_DST, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)
    print("All members' profile have been saved")
    print("Images are saved in:", IMAGE_DST)
    print("Profiles are saved in:", JSON_DST)


def main():
    global IMAGE_DST
    global JSON_DST
    parser = argparse.ArgumentParser(description='Get Keyakizaka46 data profile and pictures')
    parser.add_argument('-i', '--image',
                    help='specify the path to save the image')
    parser.add_argument('-d', '--data',
                    help='specify the path to save the profile data')
    args = parser.parse_args()
    if args.image:
        if args.image[len(args.image)-1] != '/':
            args.image += '/'
        IMAGE_DST = args.image
    if args.data:
        if args.data[len(args.data)-1] != '/':
            args.data += '/'        
        JSON_DST = args.data + JSON_DST
    process_html()

if __name__ == "__main__":
    main()
