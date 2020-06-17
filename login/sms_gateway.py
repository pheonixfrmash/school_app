import urllib.request
import urllib.parse
apikey = 'lfcJMsQDjXU-HTJijkkeebdBq6Ker1SOw1VCliyl9d'
 
def sendSMS(apikey, numbers, sender, message):
    data =  urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
        'message' : message, 'sender': sender})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return(fr)

resp =  sendSMS(apikey,917709385314 ,'TXTLCL', '315748')
print(resp)