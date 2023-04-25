## Google Admin & Snipe-IT ##
## By: Dylan Addis-Thielen ##
##       04/25/2023        ##


import time #To convert times in update life cycle
from GASS import * # Google Admin Snipe-IT Sync Definitions
from datetime import datetime #To convert times in update life cycle
from tqdm import tqdm #progress Bar


## functions
#Update Devices from Googe admin to SnipeIT
def Update_Cross(CL): 
	#Setup Reporter Vairiables
	NAS=0
	NEX=0
	NAG=0
	UPD=0
	MACH=0
	ERR=[]
	for cross in tqdm(CL):
		#Try 4 Times per device
		for attempt in range(2): 
			try:
				#Check SnipeIT
				snipeitrep=Get_DevBySN(cross["serialNumber"]) 
				#Is there a message
				if 'messages' in snipeitrep: 
					#Ensure device SN is not in SnipeIT
					if snipeitrep['messages'] == 'Asset does not exist.': 
						#Is there an Asset Tag in Google Admin
						if "annotatedAssetId" in cross: 
							#If the Tag is not Blank in Google Admin
							if cross['annotatedAssetId'] != '': 
								#Make a new device in SnipeIT
								Make_Dev({ 
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
								#Check for User
								if 'annotatedUser' in cross: 
									#Is User blank?
									if cross['annotatedUser'] != '': 
										dev = Get_DevByTag(cross['annotatedAssetId'])
										usr = Get_UserBySearch(cross['annotatedUser'])
										#Checkout Device to User in cross['annotatedUser']
										Chkout_Dev( 
											#Locate Devie ID in SnipeIT
											dev['rows'][0]['id'], 
											#Locate User ID in SnipeIT
											usr['rows'][0]['id'] 
											)
									
							#If there is a blank Asset Tag in Google Admin
							else: 
								#Report the missing Asset Tag in Goolge
								NAG=NAG+1 
						#If there is no Asset Tag in Google Admin
						else: 
							#Report the missing Asset Tag in Google
							NAG=NAG+1 
						#Report a missing Device in SnipeIT
						NAS = NAS+1 
						pass
					#We go some other error
					else: 
						print(snipeitrep['messages'])
				#SN is in SnipeIT
				else: 
					#Is there an Asset Tag in Google Admin
					if "annotatedAssetId" in cross: 
						#Is that tag Blank
						if cross['annotatedAssetId'] != '': 
							scross=snipeitrep['rows'][0]
							#Do the Asset Tags match in Google Admin and SnipeIT
							if scross['asset_tag'] == cross['annotatedAssetId']: 
								#If SN and Asset Tag Match, Update Device info
								Patch_DevByID(scross['id'], { 
									"name": cross["model"],
									"model_id": model_id,
									"status_id": Asset_State,
									AUED: datetime.utcfromtimestamp(int(cross["autoUpdateExpiration"])/1000).strftime('%m-%Y')})
								#Check for User
								if 'annotatedUser' in cross: 
									#Is User blank?
									if cross['annotatedUser'] != '': 
										dev = Get_DevByTag(cross['annotatedAssetId'])
										usr = Get_UserBySearch(cross['annotatedUser'])
										Chkin_Dev(dev['rows'][0]['id'])
										#Checkout Device to User in cross['annotatedUser']
										Chkout_Dev( 
											#Locate Devie ID in SnipeIT
											dev['rows'][0]['id'], 
											#Locate User ID in SnipeIT
											usr['rows'][0]['id'] 
											)

								#Report the Device has been updated
								MACH = MACH+1 
								pass
							#If the Tags Do not match
							else: 
								#Look for the Tag in SnipeIT
								sas = Get_DevByTag(cross["annotatedAssetId"]) 
								if 'messages' in sas:
									#Asset Tag not in SnipeIT
									if sas['messages'] == "Asset not found": 
										#Update Devie in SnipeIT with the new Asset Tag
										Patch_DevByID(scross['id'], { 
											"asset_tag": cross['annotatedAssetId'],
											"serial": cross['serialNumber'],
											"name": cross['model'],
											"model_id": model_id,
											"status_id": Asset_State,
											AUED: datetime.utcfromtimestamp(int(cross['autoUpdateExpiration'])/1000).strftime('%m-%Y')})
										#Check for User
										if 'annotatedUser' in cross: 
											#Is User blank?
											if cross['annotatedUser'] != '': 
												dev = Get_DevByTag(cross['annotatedAssetId'])
												usr = Get_UserBySearch(cross['annotatedUser'])
												#Checkout Device to User in cross['annotatedUser']
												Chkout_Dev( 
													#Locate Devie ID in SnipeIT
													dev['rows'][0]['id'], 
													#Locate User ID in SnipeIT
													usr['rows'][0]['id'] 
													)

										#Report an updated device in SnipeIT
										UPD=UPD+1 
										pass
								else:
									#Report Conflicting Tags in SnipeIT and Google Admin
									NEX=NEX+1 
						else:
							#Report Blank Tag in Google Admin
							NAG=NAG+1 
					else:
						#Report Missing Tag in Goolge Admin
						NAG=NAG+1 
			#There was an error in updating this device
			except Exception as e: 
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

#Update Devices from SnipeIT to Google Admin
def Update_Dev(CL): 
	#Setup Reporter Vairiables
	NEX=0
	ERROR=0
	for cross in tqdm(CL):
		#Try 4 Times per device
		for attempt in range(4): 
			#time.sleep(.5)
			try:
				#Get Device From SnipeIT with SN
				snipeitrep=Get_DevBySN(cross["serialNumber"]) 
				#Ensure only one SN is in SnipeIT
				if snipeitrep["total"] == 1: 
					#Ensure the Asset Tags Match
					if cross['annotatedAssetId'] == snipeitrep['rows']['asset_tag']: 
						#Try updating all information
						try: 
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
							#Try updating minimal information
							try: 
								Patch_Cross(
									snipeitrep['rows']['location']['name'], 
									'NA', 
									snipeitrep['rows']['notes'], 
									cross['deviceId'] 
									)
							#Update Failed due to one or more missing fields. Placing Device in root OU
							except: 
								Set_Ou('/', cross['deviceId'])
								ERROR=ERROR+1
					#Asset Tags do not match
					else: 
						#Report the missing Asset Tag in Google
						NEX=NEX+1 
					pass
				#Device is not in SnipeIT or More than one with SN
				else: 
					#Report the Error
					pass
			#There was an error locating the Device
			except: 
				time.sleep(15)
			else:
				break
	print("Update Complete!")
	print("Errored devices "+str(ERROR))
	print("Asset Tags missing in Google Admin: "+str(NEX))

#Update all Google Admin Devices into SnipeIT
Update_Cross(Get_All_Cross()) 

