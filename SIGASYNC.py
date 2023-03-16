## Google Admin & Snipe-IT ##
## GUI Version 0.0.1       ##
## By: Dylan Addis-Thielen ##
##          Broken!!       ##

import time
import requests
import json
import pickle
import os.path
from tkinter import *
from tqdm import tqdm
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Configure Variables
creds = None
SCOPES = ['https://www.googleapis.com/auth/admin.directory.device.chromeos']
url = 'http://snipeit.milan.k12.in.us'
api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjQyNDI1NzAwMTU4YTY3OTAxOWU1Nzc3ZmE3NjkxNzg5YjU5NzE1ZmYzOTZkMjA5Yjg1ZDdlOWJlYTQ4OTA1ODZkOGFlZDUyMThhODE2MGNmIn0.eyJhdWQiOiIxIiwianRpIjoiNDI0MjU3MDAxNThhNjc5MDE5ZTU3NzdmYTc2OTE3ODliNTk3MTVmZjM5NmQyMDliODVkN2U5YmVhNDg5MDU4NmQ4YWVkNTIxOGE4MTYwY2YiLCJpYXQiOjE2MTI1NDI5NjYsIm5iZiI6MTYxMjU0Mjk2NiwiZXhwIjoxNjQ0MDc4OTY2LCJzdWIiOiIxIiwic2NvcGVzIjpbXX0.b3Os-VfEYJ2EaHgVyjCnAcvzqec3t_BcxySMQOrZeQ_eGxnb1lTIq8sytFRqL3NmMdEDzuclFBi2R8ceU6tiF1Qne7VLc36AhPFWIKbfJV8n2PuXhNkoWattOvo9aqgIOZ5lvC9MOBzjxaQkE6W13CJmWNXYudUZd_7H-9l_x_mI5lf2cfehcFZeLjLWbRjUz56tiiZ90W52pgcwOUcPfTtwubrdHr1bt-Ocp25cpK1JbDZamDoHGmKE3Pp-YrkJvDpDdT5HnxuRcjnHSD6dfmeSRgCEx5a3e7g_Ei2Vn6BBHWsipfYrMQOyDeIn_wh8_iMqFNx3BdgNq_vJkOb-RxxTxmnD2RooXQYq3JY6xQvv7i_oK0-pZKcd2jQbJFY8omSZjepHGfprTnGSUVWGp7vJx1pkIvDBHqourcZtMOs4tkybr1soW1L-3Djhx5q9Vo7pEHIUY4dT9kQSzx2NDPFIZLeLpL90N6LqgWebjJfWRhg0orxq9s9nSNhTBffkhX4jsG1AYfxo1v-bawwG5MTXYtDKW7x9DvjaLCbRZWjOtxPXg9UkE1d9TIfH64KLvKahcbQrw7drWLw_EKwnTHmZ_S7dgs6IjsirN7YneXLjd6SnrrurFQIjo0iwE4MQiIcIe_V1yb4CMky6hMWSf4G1MGpXgc3UMN8dA5X1ozM'


## functions



# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.

if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)
service = build('admin', 'directory_v1', credentials=creds)

def Get_UserByID(ID):
	ID = str(ID)
	link = url+'/api/v1/users/'+ID
	key = {"Authorization": "Bearer "+api_key}
	data =  json.loads(requests.request("Get", link, headers=key).text)
	return data

def Search_User(search, limit=50, offset=0, sort="created_at", order="desc"):
	Query= {"search":search,"limit":limit,"offset":offset,"sort":sort,"order":order}
	link = url+'/api/v1/users'
	key = {"Authorization": "Bearer "+api_key}
	data =  json.loads(requests.request("Get", link, headers=key, params=Query).text)
	return data

def Get_DevByID(ID):
	ID = str(ID)
	link = url+'/api/v1/hardware/'+ID
	key = {"Authorization": "Bearer "+api_key}
	data =  json.loads(requests.request("Get", link, headers=key).text)
	return data

def Get_DevBySN(SN):
	link = url+'/api/v1/hardware/byserial/'+SN
	key = {"Authorization": "Bearer "+api_key}
	data =  json.loads(requests.request("Get", link, headers=key).text)
	return data

def Get_DevByTag(TAG):
	TAG = str(TAG)
	link = url+'/api/v1/hardware/bytag/'+TAG
	key = {"Authorization": "Bearer "+api_key}
	data =  json.loads(requests.request("Get", link, headers=key).text)
	return data

def CheckOut_Dev(DEVID, USERID):
	payload = {"assigned_user":USERID}
	link = url+"/api/v1/hardware/"+DEVID+"/checkout"
	key = {"Authorization": "Bearer "+api_key}
	print(payload, link)
	data =  requests.request("POST", link, json=payload, headers=key).text
	print(data)

def Get_Models(limit=50, offset=0, sort='created_at', order='asc'):
	qstring={"limit":limit,"offset":offset,"sort":sort,"order":"asc"}
	link = url+'/api/v1/models'
	key = {"Authorization": "Bearer "+api_key}
	data =  json.loads(requests.request("Get", link, headers=key, params=qstring).text)
	return data

def Post_Dev(Tag, status, modelID, name=None):
	request=service.chromeosdevices().get(customerId='03jujx15', deviceId=ID, projection='FULL')
	response=request.execute()
	return response

def Patch_DevByID(ID, payload):
	##Remember Payload == {}
	ID=str(ID)
	link = url+'/api/v1/hardware/'+ID
	key = {"Authorization": "Bearer "+api_key,"Content-Type": "application/json"}
	data =  json.loads(requests.request("PATCH", link, json=payload, headers=key).text)
	return data

def Get_Cross(ID):
	request=service.chromeosdevices().get(customerId='03jujx15', deviceId=ID, projection='FULL')
	response=request.execute()
	return response

def Get_All_Cross():
	request=service.chromeosdevices().list(customerId='03jujx15', orderBy='serialNumber', projection='FULL')
	response=request.execute()
	cross=response.get('chromeosdevices', [])
	listcros=[]
	end=False
	if not cross:
		print('No crome devices found.')
	else:
		while not end:
			cross=response.get('chromeosdevices', [])
			listcros=listcros+cross
			print("\r"+str(len(listcros)), end="\r")
			nextpage=service.chromeosdevices().list_next(previous_request=request, previous_response=response)
			if nextpage==None:
				break
			response=nextpage.execute()
		return listcros

def Print_Cross(crosslist):
	for cross in crosslist:
		try:
			print(cross['serialNumber'], cross['annotatedAssetId'])
		except KeyError:
			pass

def Update_Admin(ID, location, asset, user):
	body={"annotatedLocation": location, "annotatedAssetId": asset, "annotatedUser": user}
	request=service.chromeosdevices().patch(customerId='03jujx15', deviceId=ID, body=None, projection=None)
	response=request.execute()
	return response

def Update_Cross(LC):
	NAS=0
	NEX=0
	NAG=0
	UPD=0
	MACH=0
	for cross in tqdm(LC):
		for attempt in range(4):
			time.sleep(.5)
			try:
				snipeitrep=Get_DevBySN(cross["serialNumber"])
				if snipeitrep['total'] == 0:
					#print('No Asset in Snipe-IT')
					NAS = NAS+1
					pass
				else:
					if "annotatedAssetId" in cross:
						if cross['annotatedAssetId'] != '':
							scross=snipeitrep['rows'][0]
							if scross['asset_tag'] == cross['annotatedAssetId']:
								#print('Matching record!')
								MACH = MACH+1
								pass
							else:
								sas = Get_DevByTag(cross["annotatedAssetId"])
								if 'messages' in sas:
									if sas['messages'] == "Asset not found":
										Patch_DevByID(scross['id'], {'asset_tag': cross['annotatedAssetId'], })
										#print('Record Updated')
										UPD=UPD+1
										pass
								else:
									#print('Asset Tag Already Exists. SN', cross["serialNumber"])
									NEX=NEX+1
						else:
							#print('No Asset in Google Admin!')
							NAG=NAG+1
					else:
						#print('No Asset in Google Admin!')
						NAG=NAG+1
			except:
				#print("To Fast. Waiting to try again")
				time.sleep(15)
			else:
				break
	print("Update Compleat!")
	print("Updated Assets: "+str(MACH))
	print("Assets Not in Snipe-IT: "+str(NAS))
	print("Asset Tags Allready in Snipe-IT: "+str(NEX))
	print("No Asset Tags in Google Admin: "+str(NAG))

def Update_All():
	Update_Cross(Get_All_Cross())
def Update_G():
	tag=sAT.get()
	Device=Get_DevByTag(tag)
	sdev=Get_Cross(Device['custom_fields']['Device ID']['value'])
	Update_Cross([sdev])

def Update_S():
	tag=gAT.get()
	Device=Get_DevByTag(tag)
	User = Search_User(search=gUSR.get())
	dev = str(Device['id'])
	usr = str(User['rows'][0]['id'])
	CheckOut_Dev(dev, usr)
def Get_GAD():
	ID = sGAD.get()
	Device=Get_Cross(ID)
	gGAD.delete(0,END)
	gGAD.insert(0,Device["deviceId"])
	gAT.delete(0,END)
	gAT.insert(0,Device['annotatedAssetId'])
	gSN.delete(0,END)
	gSN.insert(0,Device["serialNumber"])
	gLoc.delete(0,END)
	gLoc.insert(0,Device["orgUnitPath"])
	gUSR.delete(0,END)
	gUSR.insert(0,Device['annotatedUser'])
def Get_SIT():
	tag=sAT.get()
	Device=Get_DevByTag(tag)
	sSN.delete(0,END)
	sSN.insert(0,Device['serial'])
	sGAD.delete(0,END)
	sGAD.insert(0,Device['custom_fields']['Device ID']['value'])
	sLoc.delete(0,END)
	sLoc.insert(0,Device['location']["name"])
	sUSR.delete(0,END)
	sUSR.insert(0,Device['assigned_to']["name"])

CheckOut_Dev('2567', '2815')
#Print_Cross(Get_All_Cross())
#Update_Cross([Get_Cross('f484afb5-4b2c-4a08-ad06-c67b903fc8df')])
#Update_Cross(Get_All_Cross())
root = Tk()

#Label
root.title('Google Admin & Snipe-IT')
Label(root, text='Google Admin ID').grid(row=0)
Label(root, text='Asset Tag').grid(row=1)
Label(root, text='Serial Number').grid(row=2)
Label(root, text='Location').grid(row=3)
Label(root, text='User').grid( row=4)

##input
gGAD=Entry(root)
gAT= Entry(root)
gSN= Entry(root)
gLoc=Entry(root)
gUSR=Entry(root)
gGAD.grid(row=0, column=1)
gAT.grid(row=1, column=1)
gSN.grid(row=2, column=1)
gLoc.grid(row=3, column=1)
gUSR.grid(row=4, column=1)

sGAD=Entry(root)
sAT= Entry(root)
sSN= Entry(root)
sLoc=Entry(root)
sUSR=Entry(root)
sGAD.grid(row=0, column=2)
sAT.grid(row=1, column=2)
sSN.grid(row=2, column=2)
sLoc.grid(row=3, column=2)
sUSR.grid(row=4, column=2)
##Buttons
Button(root, text="Sync All", command=Update_All).grid(row=0, column=3)
Button(root, text="Update Google").grid(row=6, column=1)
Button(root, text="Update Snipe-IT", command=Update_S).grid(row=6, column=2)
Button(root, text="Get From Google Admin", command=Get_GAD).grid(row=7, column=1)
Button(root, text="Get From Snipe-IT", command=Get_SIT).grid(row=7, column=2)

root.mainloop()