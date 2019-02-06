# keyakiSS
Scripts to collect data from Keyakizaka46's website

### **get_profile.py**

Download profile pictures in the highest quality possible, and collect the members' profile in and save in in a single JSON file

<img src="https://i.imgur.com/UX9pMhp.png" height="30%"  width="30%">
<img src="https://i.imgur.com/rvTspI6.png"  height="75%" width="75%" >
<br/ >

Dependency
- Beautiful Soup [link](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)

To start you either can clone this repo or just download the script
```
$ git clone https://github.com/garakuta7/keyakiSS.git
or
$ wget https://raw.githubusercontent.com/garakuta7/keyakiSS/master/get_profile.py
```

Usage
```
$ python3 get_profile.py -h
usage: get_profile.py [-h] [-i IMAGE] [-d DATA]

Get Keyakizaka46 data profile and pictures

optional arguments:
  -h, --help            show this help message and exit
  -i IMAGE, --image IMAGE
                        specify the path to save the image
  -d DATA, --data DATA  specify the path to save the profile data
```
To run the script with default directory
```
$ python3 get_profile.py
```

>Note: Script will not run with Python2, so make sure you use Python3

Feel free to contribute by submitting a pull request.

If you have any question, contact me on twitter [@garakutadayo](https://twitter.com/garakutadayo)
