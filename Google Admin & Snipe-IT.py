## Google Admin & Snipe-IT ##
## By: Dylan Addis-Thielen ##
##       03/17/2023        ##

import csv # To do a CSV Import to Google Admin.
import time #To convert times in update life cycle
import requests #To send and recieve requests from SnipeIT
import json #Used to format SnipeIT requests
import pickle #Used to store Google Admin Auth
import os.path #Used to locate Auth Pickle
import cProfile
import keyfile #rename 'keyfile (Example).py' to 'keyfile.py' then add your enviroment vairiables
from datetime import datetime #To convert times in update life cycle
from tqdm import tqdm #progress Bar
from googleapiclient.discovery import build #Used to Setup Google Admin Connection
from google_auth_oauthlib.flow import InstalledAppFlow #Used to auth Google Admin
from google.auth.transport.requests import Request #Used to get information from Google Admin


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


## functions

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

def Print_Cross(crosslist): #Print all the information for devices in crosslist
	for cross in crosslist:
		try:
			print(
				cross
			)
		except KeyError:
			pass

def Update_Cross(CL): #Update Devices from Googe admin to SnipeIT
	#Setup Reporter Vairiables
	NAS=0
	NEX=0
	NAG=0
	UPD=0
	MACH=0
	for cross in tqdm(CL):
		for attempt in range(2): #Try 4 Times per device
			try:
				snipeitrep=Get_DevBySN(cross["serialNumber"]) #Check SnipeIT
				if 'messages' in snipeitrep: #Is there a message
					if snipeitrep['messages'] == 'Asset does not exist.': #Ensure device SN is not in SnipeIT
						if "annotatedAssetId" in cross: #Is there an Asset Tag in Google Admin
							if cross['annotatedAssetId'] != '': #If the Tag is not Blank in Google Admin
								Make_Dev({ #Make a new device in SnipeIT
											"archived": False,
											"depreciate": False,
											"requestable": False,
											"last_audit_date": "null",
											"asset_tag": cross['annotatedAssetId'],
											"status_id": Asset_State,
											"model_id": model_id,
											"serial": cross['serialNumber'],
											"name": cross["model"],
											AUED: datetime.utcfromtimestamp(int(cross["autoUpdateExpiration"])/1000).strftime('%m-%Y')
											})

								if 'annotatedUser' in cross: #Check for User
									if cross['annotatedUser'] != '': #Is User blank?
										dev = Get_DevByTag(cross['annotatedAssetId'])
										usr = Get_UserBySearch(cross['annotatedUser'])
										Chkout_Dev( #Checkout Device to User in cross['annotatedUser']
											dev['rows'][0]['id'], ##Locate Devie ID in SnipeIT
											usr['rows'][0]['id'] ##Locate User ID in SnipeIT
											)
									
									
							else: #If there is a blank Asset Tag in Google Admin
								NAG=NAG+1 #Report the missing Asset Tag in Goolge
						else: #If there is no Asset Tag in Google Admin
							NAG=NAG+1 #Report the missing Asset Tag in Google
						NAS = NAS+1 #Report a missing Device in SnipeIT
						pass
					else: #We go some other error
						print(snipeitrep['messages'])
				else: #SN is in SnipeIT
					if "annotatedAssetId" in cross: #Is there an Asset Tag in Google Admin
						if cross['annotatedAssetId'] != '': #Is that tag Blank
							scross=snipeitrep['rows'][0]
							if scross['asset_tag'] == cross['annotatedAssetId']: #Do the Asset Tags match in Google Admin and SnipeIT
								Patch_DevByID(scross['id'], { #If SN and Asset Tag Match, Update Device info
									"name": cross["model"],
									"model_id": model_id,
									"status_id": Asset_State,
									AUED: datetime.utcfromtimestamp(int(cross["autoUpdateExpiration"])/1000).strftime('%m-%Y')})
								
								if 'annotatedUser' in cross: #Check for User
									if cross['annotatedUser'] != '': #Is User blank?
										dev = Get_DevByTag(cross['annotatedAssetId'])
										usr = Get_UserBySearch(cross['annotatedUser'])
										Chkin_Dev(dev['rows'][0]['id'])
										Chkout_Dev( #Checkout Device to User in cross['annotatedUser']
											dev['rows'][0]['id'], ##Locate Devie ID in SnipeIT
											usr['rows'][0]['id'] ##Locate User ID in SnipeIT
											)


								MACH = MACH+1 #Report the Device has been updated
								pass
							else: #If the Tags Do not match
								sas = Get_DevByTag(cross["annotatedAssetId"]) #Look for the Tag in SnipeIT
								if 'messages' in sas:
									if sas['messages'] == "Asset not found": #Asset Tag not in SnipeIT
										Patch_DevByID(scross['id'], { #Update Devie in SnipeIT with the new Asset Tag
											"asset_tag": cross['annotatedAssetId'],
											"serial": cross['serialNumber'],
											"name": cross['model'],
											"model_id": model_id,
											"status_id": Asset_State,
											AUED: datetime.utcfromtimestamp(int(cross['autoUpdateExpiration'])/1000).strftime('%m-%Y')})

										if 'annotatedUser' in cross: #Check for User
											if cross['annotatedUser'] != '': #Is User blank?
												dev = Get_DevByTag(cross['annotatedAssetId'])
												usr = Get_UserBySearch(cross['annotatedUser'])
												Chkout_Dev( #Checkout Device to User in cross['annotatedUser']
													dev['rows'][0]['id'], ##Locate Devie ID in SnipeIT
													usr['rows'][0]['id'] ##Locate User ID in SnipeIT
													)


										UPD=UPD+1 #Report an updated device in SnipeIT
										pass
								else:
									NEX=NEX+1 #Report Conflicting Tags in SnipeIT and Google Admin
						else:
							NAG=NAG+1 #Report Blank Tag in Google Admin
					else:
						NAG=NAG+1 #Report Missing Tag in Goolge Admin
			except: #There was an error in updating this device
				time.sleep(30)
			else:
				break
	print("Update Compleat!")
	print("Updated Assets: "+str(MACH))
	print("Assets Not in Snipe-IT: "+str(NAS))
	print("Asset Tags Allready in Snipe-IT: "+str(NEX))
	print("No Asset Tags in Google Admin: "+str(NAG))

def Update_Dev(CL): #Update Devices from SnipeIT to Google Admin
	#Setup Reporter Vairiables
	NEX=0
	for cross in tqdm(CL):
		for attempt in range(4): #Try 4 Times per device
			#time.sleep(.5)
			try:
				snipeitrep=Get_DevBySN(cross["serialNumber"]) #Get Device From SnipeIT with SN
				if snipeitrep["total"] == 1: #Ensure only one SN is in SnipeIT
					if cross['annotatedAssetId'] == snipeitrep['rows']['asset_tag']: #Ensure the Asset Tags Match
						try: #Try updating all information
							Patch_Cross(
								snipeitrep['rows'][0]['location']['name'], 
								snipeitrep['rows'][0]['assigned_to']['email'], 
								snipeitrep['rows'][0]['notes'], 
								cross['deviceId'] 
								)
							Set_Ou(
								snipeitrep['rows']['location']['name'],
								cross['deviceId']
								)
						except:
							try: #Try updating minimal information
								Patch_Cross(
									snipeitrep['rows']['location']['name'], 
									'NA', 
									snipeitrep['rows']['notes'], 
									cross['deviceId'] 
									)
							except: #Update Failed due to one or more missing fields. Placing Device in root OU
								Set_Ou('/', cross['deviceId'])
					else: #Asset Tags do not match
						NEX=NEX+1 #Report the missing Asset Tag in Google
					pass
				else: #Device is not in SnipeIT or More than one with SN
					#Report the Error
					pass
			except: #There was an error locating the Device
				time.sleep(15)
			else:
				break
	#Check Device SN in Snipe for matcing Asset Tag
		#Check if Device is assigned to User in SnipeIT
			#Check if Google User matches SnipeIT
		#Update Device in Google Admin
		#Move Device in Google Admin to OU
	#No Match, in snipeIT
		#Is there a Device with the Asset Tag from Google in SnipeIT
		#If there is not a match, report the device
		#If there is a match of Asset Tag
			#Report back the two devices
	print("Update Compleat!")

Update_Cross(Get_All_Cross()) #Update all Google Admin Devices into SnipeIT
#Print_Cross([Get_Cross('1f701cdb-9820-43e5-a28b-db85a45f4cc5')]) #Print info for a Specific Device by Google Admin ID from Google Admin
#Update_Cross([Get_Cross('6daa5cb0-4942-43cf-927e-0068e33090a6')]) #Update a specific Device from Google Admin into SnipeIT
#print(Get_Cross_ID(["BDCNFN3"])) #Print info for a Specific Device by SN from Google Admin
#print(Set_Ou('Devices',Get_Cross_ID(['2T85YM3']))) #Set Device 2T85YM3 to the OU Devices
#print(Get_All_Ou()) #Print info for all Devices in Google Admin
#print(Get_DevBySN("BDCNFN3"))
#cProfile.run("Update_Cross(Get_All_Cross())")

