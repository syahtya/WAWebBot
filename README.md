# WAWebBot

## Requirment
- pip3
- driver selenium ( for example use Gecko a.k.a Gecko)
- mysql-connector 
## Please Note
- use for development only
- Do at Your Own Risk ( Account will be suspend from WA.inc)
- Tested and Running on Ubuntu 18.04

## How to Use
- note :
1. edit environment config.json
2. run `./install.sh`
3. use API to insert data to be sent on WAWebBot 
- link project https://github.com/syahtya/microservice_sender

4. at config.json lin 21 to 24 : 
- line 21 is Parrent of HTML Class Box 
- line 22 is Child of HTML Class Box line 21
- line 23 is Child of HTML Class TextBox line 22
- line 24 is HTML Class for button Send
### run with Python
- you must install some library
```python
pip3 install  selenium mysql-connector
```
- to run 
```python
python3 main.py
```

### run with Executable
```python
./main
```
