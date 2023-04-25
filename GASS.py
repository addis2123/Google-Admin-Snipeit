## Google Admin & Snipe-IT ##
## By: Dylan Addis-Thielen ##
##       04/25/2023        ##

import csv # To do a CSV Import to Google Admin.
import requests #To send and recieve requests from SnipeIT
import json #Used to format SnipeIT requests
import keyfile #rename 'keyfile (Example).py' to 'keyfile.py' then add your enviroment vairiables
from googleapiclient.discovery import build #Used to Setup Google Admin Connection
from google_auth_oauthlib.flow import InstalledAppFlow #Used to auth Google Admin
from google.auth.transport.requests import Request #Used to get information from Google Admin
import pickle #Used to store Google Admin Auth
import os.path #Used to locate Auth Pickle
from datetime import datetime #To convert times in update life cycle
from tqdm import tqdm #progress Bar



# Setup Variables
creds = None 
SCOPES = keyfile.SCOPES
customerId = keyfile.COSTID
url = keyfile.URL
api_key = keyfile.API_KEY
AUED=keyfile.AUED
model_id = keyfile.CHRMOD
Asset_State = keyfile.STATESN

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

#Variables
url = keyfile.URL
api_key = keyfile.API_KEY
Asset_State = keyfile.STATESN

#Find a User by there SnipeIT ID#
def Get_UserByID(ID): 
	ID = str(ID)
	link = url+'/api/v1/users/'+ID
	key = {"Authorization": "Bearer "+api_key}
	data =  json.loads(requests.request("Get", link, headers=key).text)
	return data 

#Find Users by information in SnipeIT
def Get_UserBySearch(TERM): 
	TERM = TERM.replace('@','%40')
	TERM = TERM.replace(' ','%20')
	link = url+'/api/v1/users?search='+TERM
	key = {"Authorization": "Bearer "+api_key}
	data =  json.loads(requests.request("Get", link, headers=key).text)
	return data

#Return All Locations in SnipeIT
def Get_All_Loc(): 
	link = url+'/api/v1/locations'
	key = {"Authorization": "Bearer "+api_key}
	data =  json.loads(requests.request("Get", link, headers=key).text)
	return data 

#Return Location with Name
def Get_Loc(NAME): 
	NAME = str(NAME)
	link = url+'/api/v1/locations?name='+NAME
	key = {"Authorization": "Bearer "+api_key}
	data =  json.loads(requests.request("Get", link, headers=key).text)
	return data 

#Make Location NAME
def Make_Loc(NAME): 
	##Remember Payload == {}
	link = url+'/api/v1/locations'
	key = {"Accept": "application/json", "Authorization": "Bearer "+api_key,"Content-Type": "application/json"}
	data =  json.loads(requests.request("POST", link, json={'name': NAME}, headers=key).text)
	return data

#Find a Device by its SnipeIT ID#
def Get_DevByID(ID): 
	ID = str(ID)
	link = url+'/api/v1/hardware/'+ID
	key = {"Authorization": "Bearer "+api_key}
	data =  json.loads(requests.request("Get", link, headers=key).text)
	return data

#Find a Device by its SN in SnipeIT
def Get_DevBySN(SN): 
	link = url+'/api/v1/hardware/byserial/'+SN
	key = {"Authorization": "Bearer "+api_key}
	data =  json.loads(requests.request("Get", link, headers=key).text)
	return data

#Find a Device by its Asset Tag in SnipeIT
def Get_DevByTag(TAG): 
	TAG = str(TAG)
	link = url+'/api/v1/hardware/bytag/'+TAG
	key = {"Authorization": "Bearer "+api_key}
	data =  json.loads(requests.request("Get", link, headers=key).text)
	return data

#Update a Device in SnipeIT by the ID#
def Patch_DevByID(ID, payload): 
	##Remember Payload == {}
	ID=str(ID)
	link = url+'/api/v1/hardware/'+ID
	key = {"Authorization": "Bearer "+api_key,"Content-Type": "application/json"}
	data =  json.loads(requests.request("PATCH", link, json=payload, headers=key).text)
	return data

#Make a new Device in SnipeIT
def Make_Dev(payload): 
	##Remember Payload == {}
	link = url+'/api/v1/hardware'
	key = {"Accept": "application/json", "Authorization": "Bearer "+api_key,"Content-Type": "application/json"}
	data =  json.loads(requests.request("POST", link, json=payload, headers=key).text)
	return data

#check in a Device in SnipeIT by the ID#
def Chkin_Dev(ID):
	##Remember Payload == {}
	ID=str(ID)
	payload={"status_id": Asset_State}
	link = url+'/api/v1/hardware/'+ID+'/checkin'
	key = {"Accept": "application/json", "Authorization": "Bearer "+api_key,"Content-Type": "application/json"}
	data =  json.loads(requests.request("POST", link, json=payload, headers=key).text)
	return data

#check out a Device in SnipeIT by the ID# and User ID#
def Chkout_Dev(ID,USR):
	##Remember Payload == {}
	ID=str(ID) #Must be the DeviceID in SnipeIT
	USR=int(USR) #Must be the UserID in SnipeIT
	payload={
		"checkout_to_type": "user",
		"status_id": Asset_State,
		"assigned_user": USR
		}
	link = url+'/api/v1/hardware/'+ID+'/checkout'
	key = {"Accept": "application/json", "Authorization": "Bearer "+api_key,"Content-Type": "application/json"}
	data =  json.loads(requests.request("POST", link, json=payload, headers=key).text)
	return data

#Get OU info by OrgPath in Google Admin
def Get_Ou(OrgPath): 
	request=service.orgunits().get(customerId = customerId, orgUnitPath=OrgPath)
	response=request.execute()
	return response

#Get all OUs in Goolge Admin
def Get_All_Ou(): 
	request=service.orgunits().list(customerId = customerId, type='all')
	response=request.execute()
	return response

#Set the OU of a Device by OrgPath and Device ID
def Set_Ou(Org, ID): 
	request=service.chromeosdevices().moveDevicesToOu(customerId = customerId, orgUnitPath=Org, body={"deviceIds":ID})
	response=request.execute()
	return response

#Get Device in Google Admin by DeviceID
def Get_Cross(ID): 
	request=service.chromeosdevices().get(customerId = customerId, deviceId=ID, projection='FULL')
	response=request.execute()
	return response

#Update a Device in Google Admin
def Patch_Cross(ANOLOC, ANOUSR, NOTES, ASSET, ID): 
	UPDT={
		"annotatedLocation":ANOLOC,
		 "annotatedUser":ANOUSR,
		 "notes":NOTES,
		 "annotatedAssetId":ASSET
		}
	request=service.chromeosdevices().patch(customerId = customerId, deviceId=ID, body=UPDT, projection='FULL')
	response=request.execute()
	return response

#Using CSV, Update chromebooks in Google Admin CSV must have data in order (Anotated Location, Anotated User, Notes, Annotated Asset ID, Device ID)
def Update_G_Csv(CSV): 
	#Get the CSV File
	with open(CSV, mode ='r')as file: 
		#Read the CSV File
		csvFile = csv.reader(file) 
		#Read the data one line at a time
		for line in tqdm(csvFile): 
			try:
				#Update all fields based on the CSV. 
				Patch_Cross(line[0], line[1], line[2], line[3], line[4]) 
			except:
				#Print the lines that failed.
				print(line) 

#Get the Device ID from Google Admin by SN
def Get_Cross_ID(SL): 
	CL=Get_All_Cross()
	DIC={}
	CrossID=[]
	for cross in tqdm(CL):
		DIC[cross['serialNumber']] = cross["deviceId"]
	for SN in SL:
		CrossID.append(DIC[SN])
	return CrossID

#Get all Google Admin Devices
def Get_All_Cross(): 
	print("Gathering Chromebooks...")
	request=service.chromeosdevices().list(customerId = customerId, orderBy='serialNumber', projection='FULL')
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

#Print all the information for devices in crosslist
def Print_Cross(crosslist): 
	for cross in crosslist:
		try:
			print(
				cross
			)
		except KeyError:
			pass

