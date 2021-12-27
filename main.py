import requests
from time import *
import realhttp

base_url = "http://192.168.1.254/api/v1"
user = "sabar"
password = "menanti"

accessToken = "Your Access Token"
roomId = "Your Room ID"

bot_token = 'Your Telegram Bot Token'
bot_chatID = 'Your Telegram Bot Chat ID'

def get_ticket():
    headers = {"content-type": "application/json"}
    data = {"username": user, "password": password}

    response = requests.post(base_url+"/ticket", headers=headers, json=data)
    ticket = response.json()
    service_ticket = ticket["response"]["serviceTicket"]
    return service_ticket

def get_network_health():
    ticket = get_ticket()
    headers = {"X-Auth-Token": ticket}
    response = requests.get(base_url+"/assurance/health", headers=headers)
    health = response.json()
    network_health = health['response'][0]['networkDevices']['totalPercentage']
    return network_health

def get_network_issues():
    ticket = get_ticket()
    headers = {'Accept': 'application/yang-data+json', 'X-Auth-Token': ticket}
    issues = requests.get(url = base_url + "/assurance/health-issues", headers=headers)
    issue_details = issues.json()
    devices = len(issue_details['response'])
    output = "Peringatan! Terjadi gangguan akses ke "+ str(devices) +" perangkat berikut:\n"
    output += "-"*60 +"\n"
    output += "NO. | PERANGKAT | WAKTU | DESKRIPSI\n"
    output +="-"*60 +"\n"
    number=1
    for device in issue_details['response']:
        output += ""+ str(number) +". | "+ device['issueSource'] +" | "+ device['issueTimestamp'] +" | "+ device['issueDescription'] +"\n"
        number +=1
    return output

def onHTTPDone(status, data, replyHeader): 
	if status == 200:
		print("Pesan Network Issues sukses dikirim!")
	else:
		print("Pesan Network Issues gagal dikirim!")

def escape_underscore(txt):
        return txt.replace("_", "-")
        
if __name__ == "__main__":
	network_health = get_network_health()
	if int(network_health) < 100:
		issues = get_network_issues()
		print(issues)
		http = realhttp.RealHTTPClient()
        
        #headers = {"Authorization":"Bearer "+accessToken, "Content-Type":"application/json"}
        #message = {"roomId":roomId, "markdown":'**Permasalahan Jaringan :**'+'\n'+ '>'+ issues}
        #http.postWithHeader(webex_url, message, headers)
        
        issues = escape_underscore(issues)
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + issues
        http.get(send_text)
        
        http.onDone(onHTTPDone)
        while True:
			sleep(5)
	else:
		print("Persentase Network Health: "+ network_health +"%")
