## Google Admin & Snipe-IT ##
## By: Dylan Addis-Thielen ##
##       04/24/2023        ##


import time #To convert times in update life cycle
from GASS import * # Google Admin Snipe-IT Sync Definitions
from datetime import datetime #To convert times in update life cycle
from tqdm import tqdm #progress Bar
from googleapiclient.discovery import build #Used to Setup Google Admin Connection
from google_auth_oauthlib.flow import InstalledAppFlow #Used to auth Google Admin
from google.auth.transport.requests import Request #Used to get information from Google Admin


## functions
def Update_Cross(CL): #Update Devices from Googe admin to SnipeIT
	#Setup Reporter Vairiables
	NAS=0
	NEX=0
	NAG=0
	UPD=0
	MACH=0
	ERR=[]
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
			except Exception as e: #There was an error in updating this device
				if e == 'list index out of range':
					ERR=ERR+cross
					pass
				#time.sleep(60) #API Reset timer
			else:
				break
	print("Update Complete!")
	print("Updated Assets: "+str(MACH))
	print("Assets Not in Snipe-IT: "+str(NAS))
	print("Asset Tags Already in Snipe-IT: "+str(NEX))
	print("No Asset Tags in Google Admin: "+str(NAG))
	print("Failed devices "+ERR)

def Update_Dev(CL): #Update Devices from SnipeIT to Google Admin
	#Setup Reporter Vairiables
	NEX=0
	ERROR=0
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
								ERROR=ERROR+1
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
	print("Update Complete!")
	print("Errored devices "+str(ERROR))
	print("Asset Tags missing in Google Admin: "+str(NEX))

Update_Cross(Get_All_Cross()) #Update all Google Admin Devices into SnipeIT

