## Google Admin & Snipe-IT ##
## By: Dylan Addis-Thielen ##
##       03/17/2023        ##

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

def Get_UserByID(ID): #Find a User by there SnipeIT ID#
	ID = str(ID)
	link = url+'/api/v1/users/'+ID
	key = {"Authorization": "Bearer "+api_key}
	data =  json.loads(requests.request("Get", link, headers=key).text)
	return data 

def Get_UserBySearch(TERM): #Find Users by information in SnipeIT
	TERM = TERM.replace('@','%40')
	TERM = TERM.replace(' ','%20')
	link = url+'/api/v1/users?search='+TERM
	key = {"Authorization": "Bearer "+api_key}
	data =  json.loads(requests.request("Get", link, headers=key).text)
	return data

def Get_All_Loc(): #Return All Locations in SnipeIT
	link = url+'/api/v1/locations'
	key = {"Authorization": "Bearer "+api_key}
	data =  json.loads(requests.request("Get", link, headers=key).text)
	return data 

def Get_Loc(NAME): #Return Location with Name
	NAME = str(NAME)
	link = url+'/api/v1/locations?name='+NAME
	key = {"Authorization": "Bearer "+api_key}
	data =  json.loads(requests.request("Get", link, headers=key).text)
	return data 

def Make_Loc(NAME): #Make Location NAME
	##Remember Payload == {}
	link = url+'/api/v1/locations'
	key = {"Accept": "application/json", "Authorization": "Bearer "+api_key,"Content-Type": "application/json"}
	data =  json.loads(requests.request("POST", link, json={'name': NAME}, headers=key).text)
	return data

def Get_DevByID(ID): #Find a Device by its SnipeIT ID#
	ID = str(ID)
	link = url+'/api/v1/hardware/'+ID
	key = {"Authorization": "Bearer "+api_key}
	data =  json.loads(requests.request("Get", link, headers=key).text)
	return data

def Get_DevBySN(SN): #Find a Device by its SN in SnipeIT
	link = url+'/api/v1/hardware/byserial/'+SN
	key = {"Authorization": "Bearer "+api_key}
	data =  json.loads(requests.request("Get", link, headers=key).text)
	return data

def Get_DevByTag(TAG): #Find a Device by its Asset Tag in SnipeIT
	TAG = str(TAG)
	link = url+'/api/v1/hardware/bytag/'+TAG
	key = {"Authorization": "Bearer "+api_key}
	data =  json.loads(requests.request("Get", link, headers=key).text)
	return data

def Patch_DevByID(ID, payload): #Update a Device in SnipeIT by the ID#
	##Remember Payload == {}
	ID=str(ID)
	link = url+'/api/v1/hardware/'+ID
	key = {"Authorization": "Bearer "+api_key,"Content-Type": "application/json"}
	data =  json.loads(requests.request("PATCH", link, json=payload, headers=key).text)
	return data

def Make_Dev(payload): #Make a new Device in SnipeIT
	##Remember Payload == {}
	link = url+'/api/v1/hardware'
	key = {"Accept": "application/json", "Authorization": "Bearer "+api_key,"Content-Type": "application/json"}
	data =  json.loads(requests.request("POST", link, json=payload, headers=key).text)
	return data

def Chkin_Dev(ID):
	##Remember Payload == {}
	ID=str(ID)
	payload={"status_id": Asset_State}
	link = url+'/api/v1/hardware/'+ID+'/checkin'
	key = {"Accept": "application/json", "Authorization": "Bearer "+api_key,"Content-Type": "application/json"}
	data =  json.loads(requests.request("POST", link, json=payload, headers=key).text)
	return data

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

def Get_Ou(OrgPath): #Get OU info by OrgPath in Google Admin
	request=service.orgunits().get(customerId = customerId, orgUnitPath=OrgPath)
	response=request.execute()
	return response

def Get_All_Ou(): #Get all OUs in Goolge Admin
	request=service.orgunits().list(customerId = customerId, type='all')
	response=request.execute()
	return response

def Set_Ou(Org, ID): #Set the OU of a Device by OrgPath and Device ID
	request=service.chromeosdevices().moveDevicesToOu(customerId = customerId, orgUnitPath=Org, body={"deviceIds":ID})
	response=request.execute()
	return response

def Get_Cross(ID): #Get Device in Google Admin by DeviceID
	request=service.chromeosdevices().get(customerId = customerId, deviceId=ID, projection='FULL')
	response=request.execute()
	return response

def Patch_Cross(ANOLOC, ANOUSR, NOTES, ASSET, ID): #Update a Device in Google Admin
	UPDT={
		"annotatedLocation":ANOLOC,
		 "annotatedUser":ANOUSR,
		 "notes":NOTES,
		 "annotatedAssetId":ASSET
		}
	request=service.chromeosdevices().patch(customerId = customerId, deviceId=ID, body=UPDT, projection='FULL')
	response=request.execute()
	return response

def Update_G_Csv(CSV): # Using CSV, Update chromebooks in Google Admin CSV must have data in order (Anotated Location, Anotated User, Notes, Annotated Asset ID, Device ID)
	with open(CSV, mode ='r')as file: # Get the CSV File
		csvFile = csv.reader(file) # Read the CSV File
		for lines in tqdm(csvFile): # Read the data one line at a time
			try:
				Patch_Cross(lines[0], lines[1], lines[2], lines[3], lines[4]) #Update all fields based on the CSV. 
			except:
				print(lines) # Print the lines that failed.

def Get_Cross_ID(SL): #Get the Device ID from Google Admin by SN
	CL=Get_All_Cross()
	DIC={}
	CrossID=[]
	for cross in tqdm(CL):
		DIC[cross['serialNumber']] = cross["deviceId"]
	for SN in SL:
		CrossID.append(DIC[SN])
	return CrossID

def Get_All_Cross(): #Get all Google Admin Devices
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
			#print("\r"+str(len(listcros)), end="\r")
			nextpage=service.chromeosdevices().list_next(previous_request=request, previous_response=response)
			if nextpage==None:
				break
			response=nextpage.execute()
		return listcros

def Print_Cross(crosslist): #Print all the information for devices in crosslist
	for cross in crosslist:
		try:
			print(
				cross
			)
		except KeyError:
			pass

