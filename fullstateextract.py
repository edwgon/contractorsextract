from selenium import webdriver
import time
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import os
import psycopg2
import re
import hashlib
from datetime import datetime, date


class inicio():
	def datet(self,date):
		ldate = str(date).split("/")
		day = ldate[0]
		month = ldate[1]
		year = ldate[2]
		newdate = str(year)+"-"+str(month)+"-"+str(day)
		return newdate
	def exp(self, exp, text):
		strdes = exp.findall(text)
		numran = len(strdes)
		if numran == 0:
			strdes =[]
			strdes.append(None)
		strdesm = str(strdes[0])
		return strdesm
	def newbro(self,path,browser):
		browseri = webdriver.Chrome()
		browseri = browser
		#search_page = browseri.get(self.URL)
		selectp = browseri.find_element_by_xpath(path)
		selectp.click()
		ressint = browseri.page_source
		bsobjetoint = BeautifulSoup(ressint, 'html.parser')
		self.facility_name = browseri.find_element_by_xpath("//*[@id='view:_id1:_id200:nameCF1']")
		print("Name"+str(self.facility_name.text))
		self.location = browseri.find_element_by_xpath("//*[@id='view:_id1:_id200:facilityAddressCF1']")
		print("Location"+str(self.location.text))
		llocation = self.location.text
		llocation = str(llocation).split(",")
		self.address = str(llocation[0]).upper()
		self.link = browseri.find_element_by_xpath("//*[@id='view:_id1:_id200:googleMapsCF1']/a")
		self.city = str(llocation[1]).upper()
		statet = str(llocation[2])
		self.state = self.exp(self.patronstate, statet)
		self.state = str(self.state).strip()
		self.zip = str(statet).replace(self.state,'')
		self.zip = str(self.zip).strip()
		print("City"+str(self.city)+"\nState"+str(self.state)+"\nZip"+str(self.zip))
		self.facility_permit_number = browseri.find_element_by_xpath("//*[@id='view:_id1:_id200:permitNumberCF1']")
		print("Permit Number"+str(self.facility_name.text))
		self.facility_last_inspectiont = browseri.find_element_by_xpath("//*[@id='view:_id1:_id200:lastInspectionCF1']")
		self.facility_last_inspection = self.datet(self.facility_last_inspectiont.text)
		print("Last inspection"+str(self.facility_last_inspection))
		self.facility_type = browseri.find_element_by_xpath("//*[@id='view:_id1:_id200:subTypeCF1']")
		print("Type"+str(self.facility_type.text))
		self.facility_status = browseri.find_element_by_xpath("//*[@id='view:_id1:_id200:statusCF1']")
		print("Status"+str(self.facility_status.text))
		self.phone = browseri.find_element_by_xpath("//*[@id='view:_id1:_id200:phoneCF1']")
		print("Phone"+str(self.phone.text)+"\nLink"+str(self.link.get_attribute("href")))
		divinsphis = browseri.find_element_by_xpath("//*[@id='view:_id1:uiContainer']/div/div[2]/div/div[2]/table")
		patencode = str(self.address)+str(self.facility_name)
		id_license = hashlib.md5(patencode.encode())
		id_licensem = id_license.hexdigest()
		id_licensem = str(id_licensem)	
		self.facility_name = self.facility_name.text
		self.location =  self.location.text
		self.link = self.link.get_attribute("href")
		self.address = self.address
		self.city = self.city
		self.state = self.state
		self.zip = self.zip
		self.phone = self.phone.text
		self.facility_permit_number = self.facility_permit_number.text
		self.facility_last_inspection = self.facility_last_inspection
		self.facility_type = self.facility_type.text
		self.facility_status = self.facility_status.text
		urlpage = browseri.current_url
		self.facility_link = urlpage
		self.idfacility = str(urlpage).replace('http://www.healthspace.com/Clients/Michigan/Central/web.nsf/formFacility.xsp?id=', '')
		self.idfacility = str(self.idfacility)
		self.ahora = datetime.now()
		self.ahora = self.ahora.strftime(self.formato_fecha)
		#hora = self.ahora.strftime(self.formato_hora)
		#self.ahora = str(self.ahora)
		try:
			sqlinsf = """INSERT INTO extract.restaurants_mi_fullstate_facilities (facility_id, facility_name, location, google_maps_link, address, city, state, zip, phone, facility_permit_number, facility_last_inspection, facility_type, facility_status, facility_link, created_date, updated_date) 
			VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (facility_id) 
			DO 
			UPDATE
			SET facility_id = EXCLUDED.facility_id;"""
			cursorinsf = self.con.cursor()
			cursorinsf.execute(sqlinsf, (str(self.idfacility), str(self.facility_name), str(self.location), str(self.link), str(self.address), str(self.city), str(self.state), str(self.zip), str(self.phone), str(self.facility_permit_number), str(self.facility_last_inspection), str(self.facility_type), str(self.facility_status),str(self.facility_link), str(self.ahora), str(self.ahora)))
			self.con.commit()
			print("Inserting Facility data")
		except Exception as excinsf:
			print("Error Insertar Facility"+str(excinsf))
		#print(divinsphis)
		tabvio = divinsphis.find_elements_by_tag_name('tr')
		itab = 0
		for itabvio in tabvio:
			print("Vio_______")
			xpathvio = "//*[@id='view:_id1:_id200:_id253:repeatInspections:"+str(itab)+":repeatInspectionsTR']"
			urlint = browseri.current_url
			print(urlint)
			print(xpathvio)
			self.newbroi(urlint, xpathvio, itab)
			
			itab += 1

		#time.sleep(5)}

		browseri.quit()
	def newbroi(self,urlpath,xpath,nuym):
		tabnum = int(nuym)
		tabnum = tabnum + 1
		browserivio = webdriver.Chrome()
		search_pagevio = browserivio.get(urlpath)
		selectvio = browserivio.find_element_by_xpath(xpath)
		selectvio.click()
		ressintvio = browserivio.page_source
		bsobjetointvio = BeautifulSoup(ressintvio, 'html.parser')
		print("VIOInt____")
		#print(bsobjetointvio)
		self.inspection_datet = browserivio.find_element_by_xpath("//*[@id='view:_id1:_id200:_id224:inspectionDateCF1']")
		self.inspection_date = self.datet(self.inspection_datet.text)
		print("Inspection Date"+str(self.inspection_date))

		self.year_round_facility = browserivio.find_element_by_xpath("//*[@id='view:_id1:_id200:_id224:allYearRoundCF1']")
		print("Yaear Round"+str(self.year_round_facility.text))

		self.complexity_rating = browserivio.find_element_by_xpath("//*[@id='view:_id1:_id200:_id224:riskRatingEB1']")
		print("complexity_rating"+str(self.complexity_rating.text))

		self.inspection_type = browserivio.find_element_by_xpath("//*[@id='view:_id1:_id200:_id224:inspTypeCF1']")
		print("inspection_type"+str(self.inspection_type.text))

		self.re_inspection_required = browserivio.find_element_by_xpath("//*[@id='view:_id1:_id200:_id224:fuiReqCF1']")
		print("re_inspection_required"+str(self.re_inspection_required.text))
		selectstatus = browserivio.find_element_by_xpath("//*[@id='view:_id1:_id200:_id224:_id270:panelHeaderToggleButton']")
		selectstatus.click()
		self.license_status = browserivio.find_element_by_xpath("//*[@id='view:_id1:_id200:_id224:inspectionEnforcementCF1']")
		print("license_status"+str(self.license_status.text))
		inspection_dateid = str(self.inspection_date).replace("-",'')
		patencodeins = str(self.idfacility)+str(inspection_dateid)
		idins = hashlib.md5(patencodeins.encode())
		idins_licensem = idins.hexdigest()
		idins_licensem = str(idins_licensem)
		self.inspection_id = str(idins_licensem)+str(tabnum)
		selectcertificate = browserivio.find_element_by_xpath("//*[@id='view:_id1:_id200:_id224:_id279:_id281:panelHeaderToggleButton']")
		selectcertificate.click()
		tablacerti = browserivio.find_element_by_xpath("//*[@id='view:_id1:_id200:_id224:_id279:certMgrPanelBody']/table")
		incert = tablacerti.find_elements_by_tag_name('tr')
		itcerti = int(len(incert))
		print("lar"+str(itcerti))
		#certified_manager_namet = browserivio.find_element_by_xpath("")
		#certificate_numbert = browserivio.find_element_by_xpath("")
		#certificate_expirationt = browserivio.find_element_by_xpath("")
		#self.certified_manager_name = None
		#self.certificate_number = None
		#self.certificate_expiration = None
		#self.ins_id = str(self.inspection_id)
		self.inspection_date = str(self.inspection_date)
		self.year_round_facility = str(self.year_round_facility.text)
		self.complexity_rating = str(self.complexity_rating.text)
		self.inspection_type = str(self.inspection_type.text)
		self.re_inspection_required = str(self.re_inspection_required.text)
		self.license_status = str(self.license_status.text)

		print("Ahora"+str(self.ahora))
		urlintin = browserivio.current_url#http://www.healthspace.com/Clients/Michigan/Central/web.nsf/formInspection.xsp?databaseName=Quail/HealthSpace%21%21Clients%5CMichigan%5CCentral%5CCentral_Michigan_EHS_Live.nsf&documentId=EFF512C6DEEFCB58852582400067D185&id=5538cab072d0fa948825791800797ae3&action=openDocument
		self.inspection_id = str(urlintin).replace('http://www.healthspace.com/Clients/Michigan/Central/web.nsf/formInspection.xsp?databaseName=Quail/HealthSpace%21%21Clients%5CMichigan%5CCentral%5CCentral_Michigan_EHS_Live.nsf', '')
		sepai = int(str(self.inspection_id).find('&documentId='))
		sepaf = int(str(self.inspection_id).find('&id='))
		print(str(sepai)+"ddddd"+str(sepaf))
		print(str(self.inspection_id[sepai:sepaf]))
		self.inspection_id = str(self.inspection_id[sepai:sepaf])
		self.inspection_id = str(self.inspection_id).replace('&documentId=', '')
		print((self.inspection_id+self.inspection_date+self.year_round_facility+self.complexity_rating+self.inspection_type+self.re_inspection_required+self.re_inspection_required+self.license_status))
		try:
			sqlinsi = """INSERT INTO extract.restaurants_mi_fullstate_inspections (inspection_id, facility_id, inspection_date, year_round_facility, complexity_rating, inspection_type, re_inspection_required, license_status, created_date, updated_date) 
			VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (inspection_id) 
			DO 
			UPDATE
			SET inspection_id = EXCLUDED.inspection_id;"""
			cursorinsi = self.con.cursor()
			cursorinsi.execute(sqlinsi,(self.inspection_id, str(self.idfacility), self.inspection_date, self.year_round_facility, self.complexity_rating, self.inspection_type , self.re_inspection_required, self.license_status , str(self.ahora), str(self.ahora)))
			self.con.commit()
			print("Inserting Inspection data")
		except Exception as excinsi:
			print("Error Insertar Inspection"+str(excinsi))

		tablecertifiedman = browserivio.find_element_by_xpath("//*[@id='view:_id1:_id200:_id224:_id279:certMgrPanelBody']/table")
		trscert = tablecertifiedman.find_elements_by_tag_name('tr')
		lentabcert = int(len(trscert))
		print("NUMM"+str(lentabcert))
		selectviotab = browserivio.find_element_by_xpath("//*[@id='view:_id1:_id200:inspViolationsTabLink']")
		selectviotab.click()#
		#numdescvio = browserivio.find_element_by_xpath("//*[@id='view:_id1:_id200:_id339:repeat1:0:_id345:violationSectionCF1']")
		#anndescvio = browservio.find_element_by_xpath("//*[@id'view:_id1:_id200:_id339:repeat1:0:_id345:violationCodeCF']")
		#descanndescvio = browservio.find_element_by_xpath("//*[@id='view:_id1:_id200:_id339:repeat1:0:_id345:violationDescriptionCF1']")
		listitdesvio = browserivio.find_element_by_xpath("//*[@id='view:_id1:_id200:_id339:repeat1']")
		try:
			un = browserivio.find_element_by_xpath("//*[@id='view:_id1:_id200:inspCreatePanelViolations']/div[1]")
			numviosobs = browserivio.find_element_by_id("view:_id1:_id200:_id339:repeat1")
			divsviosobs = numviosobs.find_elements_by_tag_name("div")
			
			inumviosobs = int(len(divsviosobs))
			print("VIOS"+str(inumviosobs))
			itviosobs = 1
			while itviosobs <= inumviosobs:
				itot = int(itviosobs)-1
				print("NUMMM"+str(itviosobs))
				idvio = str(self.inspection_id)+"1-"+str(itviosobs)
				xpathviosobs = "//*[@id='view:_id1:_id200:_id339:repeat1']/div["+str(itviosobs)+"]"
				print("XPATHobs"+xpathviosobs)
				itnumviosobs = browserivio.find_element_by_xpath(xpathviosobs)
				anndesobs = browserivio.find_element_by_xpath("//*[@id='view:_id1:_id200:_id339:repeat1']/div["+str(itviosobs)+"]/div[1]")
				obsdesobs = browserivio.find_element_by_xpath("//*[@id='view:_id1:_id200:_id339:repeat1']/div["+str(itviosobs)+"]/div[2]/div[1]")			
				cordesobs = browserivio.find_element_by_xpath("//*[@id='view:_id1:_id200:_id339:repeat1']/div["+str(itviosobs)+"]/div[2]/div[2]")
				desdesobs = browserivio.find_element_by_xpath("//*[@id='view:_id1:_id200:_id339:repeat1:"+str(itot)+":_id345:violationDescriptionCF1']")
				viosec = browserivio.find_element_by_xpath("//*[@id='view:_id1:_id200:_id339:repeat1:"+str(itot)+":_id345:violationSectionCF1']")
				if desdesobs != '':
					self.violation_desc = desdesobs.text
				else:
					self.violation_desc = None
				if viosec != '':
					self.violation_section = viosec.text
				else:
					self.violation_section = None
				#//*[@id="view:_id1:_id200:_id339:repeat1:0:_id345:violationCodeCF1"]
				viocode = browserivio.find_element_by_xpath("//*[@id='view:_id1:_id200:_id339:repeat1:0:_id345:violationCodeCF1']")
				if viocode != '':
					self.violation_code = viocode.text
				if anndesobs != '':
					self.violation_description = anndesobs.text
				if obsdesobs != '':
					self.violation_observation = obsdesobs.text
				if cordesobs != '':
					self.violation_correction = cordesobs.text
				selvio = browserivio.find_element_by_xpath("//*[@id='view:_id1:_id200:_id339:repeat1:"+str(itot)+":_id345:violationCritSetLink1']")
				selvio.click()
				time.sleep(2)
				coretype = browserivio.find_element_by_xpath("//*[@id='view:_id1:_id200:_id339:_id391:violTypeModalBody']/h3")
				if coretype != '':
					self.violation_priority_type = coretype.text
				coredes = browserivio.find_element_by_xpath("//*[@id='view:_id1:_id200:_id339:_id391:violTypeModalBody']/p")
				if coredes != '':
					self.violation_priority = coredes.text
				closecore = browserivio.find_element_by_xpath("//*[@id='view:_id1:_id200:_id339:_id391:violTypeModalCloseButton']")
				closecore.click()
				anndesobs = anndesobs.text
				obsdesobs = obsdesobs.text
				cordesobs = cordesobs.text
				itviosobs += 1
				itotv = "1-"+str(itot)+str(self.inspection_id)
				print("VV\n"+str(itot)+ "VV\n"+str(self.violation_section)+ "VV\n"+self.violation_section+ "VV\n"+self.violation_code+ "VV\n"+self.violation_description+ "VV\n"+self.violation_observation+ "VV\n"+self.violation_correction+ "VV\n"+"Observed violation"+"VV\n"+str(self.violation_priority_type)+ "VV\n"+str(self.violation_priority)+ "VV\n"+str(self.ahora)+ "VV\n"+str(self.ahora))
				try:
					sqlinsv = """INSERT INTO extract.restaurants_mi_fullstate_inspections_violations (violation_id, inspection_id, violation_section, violation_code, violation_description, violation_complete_description, violation_observation, violation_correction, violation_annotation_type, violation_priority_type, violation_priority_description, created_date, updated_date) 
					VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (violation_id) 
					DO 
					UPDATE
					SET violation_id = EXCLUDED.violation_id;"""
					cursorinsv = self.con.cursor()
					cursorinsv.execute(sqlinsv,(str(itotv),str(self.inspection_id),str(self.violation_section),str(self.violation_code),str(self.violation_desc),str(self.violation_description),str(self.violation_observation) , str(self.violation_correction),'Observed violation' ,str(self.violation_priority_type),str(self.violation_priority),str(self.ahora),str(self.ahora)))
					self.con.commit()
					print("Inserting Violation Observed data")
				except Exception as excinsi:
					print("Error Insertar Violation Observed"+str(excinsi))
				print("-_-_-_DESC VIO OBSERVED\n"+str(itviosobs)+"ss\nAnn"+str(anndesobs)+"\nObs"+str(obsdesobs)+"\nCor"+str(cordesobs))
		except Exception as exviodesobs:
			print("Error violations Observed Description"+str(exviodesobs))
			anndesobs = None
			obsdesobs = None
			cordesobs = None
		try:
			dos = browserivio.find_element_by_xpath("//*[@id='view:_id1:_id200:inspCreatePanelViolations']")
			numvioscor = browserivio.find_element_by_id("view:_id1:_id200:_id339:correctedViolationsRepeat")
			divsvioscor = numvioscor.find_elements_by_tag_name("div")
			
			inumvioscor = int(len(divsvioscor))
			print("VIOS"+str(inumvioscor))
			itvioscor = 1
			while itvioscor <= inumvioscor:
				itotc = int(itvioscor)-1
				itotvc = "2-"+str(itotc)+str(self.inspection_id)
				print("NUMMM"+str(itvioscor))
				idvioc = str(self.inspection_id)+"2-"+str(itvioscor)
				if itvioscor == 1:
					xpathvioscor = "//*[@id='view:_id1:_id200:inspCreatePanelViolations']/div"
				else:
					xpathvioscor = "//*[@id='view:_id1:_id200:inspCreatePanelViolations']/div["+str(itvioscor)+"]"
				print("XPATHcor"+xpathvioscor)
				itnumvios = browserivio.find_element_by_xpath(xpathvioscor)
				if itvioscor == 1:
					anndescor = browserivio.find_element_by_xpath("//*[@id='view:_id1:_id200:_id339:correctedViolationsRepeat']/div/div[1]")
					obsdescor = browserivio.find_element_by_xpath("//*[@id='view:_id1:_id200:_id339:correctedViolationsRepeat']/div/div[2]/div[2]")		
					cordescor = browserivio.find_element_by_xpath("//*[@id='view:_id1:_id200:_id339:correctedViolationsRepeat']/div/div[2]/div[1]")
				else:
					anndescor = browserivio.find_element_by_xpath("//*[@id='view:_id1:_id200:_id339:correctedViolationsRepeat']/div["+str(itvioscor)+"]/div[1]")
					obsdescor = browserivio.find_element_by_xpath("//*[@id='view:_id1:_id200:_id339:correctedViolationsRepeat']/div["+str(itvioscor)+"]/div[2]/div[2]")		
					cordescor = browserivio.find_element_by_xpath("//*[@id='view:_id1:_id200:_id339:correctedViolationsRepeat']/div["+str(itvioscor)+"]/div[2]/div[1]")
				itviocor = int(itvioscor)-1
				viosecc = browserivio.find_element_by_xpath("//*[@id='view:_id1:_id200:_id339:correctedViolationsRepeat:"+str(itotc)+":_id365:violationSectionCF1']")
				if viosec != '':
					self.violation_section = viosec.text
				else:
					self.violation_section = None
				viocodec = browserivio.find_element_by_xpath("//*[@id='view:_id1:_id200:_id339:correctedViolationsRepeat:"+str(itotc)+":_id365:violationCodeCF1']")
				if viocodec != '':
					self.violation_code = viocodec.text
				else:
					self.violation_code = None
				viodesc = browserivio.find_element_by_xpath("//*[@id='view:_id1:_id200:_id339:correctedViolationsRepeat:"+str(itotc)+":_id365:violationDescriptionCF1']")
				if viodesc != '':
					self.violation_desc = viodesc.text
				else:
					self.violation_desc = None
				
				if anndescor != '':
					self.violation_description = anndescor.text
				else:
					self.violation_description = None
				if obsdescor != '':
					self.violation_observation = obsdescor.text
				else:
					self.violation_observation = None
				if cordescor != '':
					self.violation_correction = cordescor.text
				else:
					self.violation_correction = None
				selviocor = browserivio.find_element_by_xpath("//*[@id='view:_id1:_id200:_id339:correctedViolationsRepeat:"+str(itviocor)+":_id365:violationCritSetLink1']")
				anndescor = anndescor.text
				obsdescor = obsdescor.text
				cordescor = cordescor.text
				selviocor.click()
				time.sleep(2)
				coretype = browserivio.find_element_by_xpath("//*[@id='view:_id1:_id200:_id339:_id391:violTypeModalBody']/h3")
				if coretype != '':
					self.violation_priority_type = coretype.text
				coredes = browserivio.find_element_by_xpath("//*[@id='view:_id1:_id200:_id339:_id391:violTypeModalBody']/p")
				if coredes != '':
					self.violation_priority = coredes.text
				itvioscor += 1
				print("-_-_-_DESC VIO CORRECTED\n"+str(itvioscor)+"ss\nAnn"+str(anndescor)+"\nObs"+str(obsdescor)+"\nCor"+str(cordescor))
				try:
					sqlinsvc = """INSERT INTO extract.restaurants_mi_fullstate_inspections_violations (violation_id, inspection_id, violation_section, violation_code, violation_description, violation_complete_description, violation_observation, violation_correction, violation_annotation_type, violation_priority_type, violation_priority_description, created_date, updated_date) 
					VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (violation_id) 
					DO 
					UPDATE
					SET violation_id = EXCLUDED.violation_id;"""
					cursorinsvc = self.con.cursor()
					cursorinsvc.execute(sqlinsvc,(str(itotvc),str(self.inspection_id),str(self.violation_section),str(self.violation_code),str(self.violation_desc),str(self.violation_description),str(self.violation_observation) , str(self.violation_correction),'Corrected violation' ,str(self.violation_priority_type),str(self.violation_priority),str(self.ahora),str(self.ahora)))
					self.con.commit()
					print("Inserting Violation Corrected data")
				except Exception as excinsic:
					print("Error Insertar Violation Corrected"+str(excinsic))
		except Exception as exviodescor:
			print("Error violations Corrected Description"+str(exviodescor))
			anndescor = None
			obsdescor = None
			cordescor = None
		browserivio.quit()
	def inipags(self,browserini):	
		#self.next = True
		browser = webdriver.Chrome()
		browser = browserini
		#while next == True:
		#//*[@id="view:_id1:_id247:pager6__Next__lnk"]
		ressi = browser.page_source
		bsobjetoi = BeautifulSoup(ressi, 'html.parser')
		searching_form = bsobjetoi.findAll("form", {"id":"view:_id1"})
		div1 = searching_form[0].findAll('div', {"id": "view:_id1:uiContainer"})
		div2 = div1[0].findAll('div', {"class": "row"})
		div3 = div2[0].findAll('div', {"class": "panel panel-default"})
		divi = div3[1]
		listtrs = divi.findAll('tr')
		self.i = 0
		for ilisttrs in listtrs:
			print("___________"+str(self.i))
			iteraselect = " //*[@id='view:_id1:_id247:repeatFacilities:"+str(self.i)+":td1']"
			print(iteraselect)
			self.newbro(iteraselect,browser)
			self.i += 1
		browser.quit()
	def __init__(self):
		#self.i = 0
		self.formato_fecha = "%Y-%m-%d"
		self.formato_hora = "%H:%M:%S"
		self.inicio = datetime.now()
		self.ahora = datetime.now()
		self.patronstate = re.compile('([A-Z]{2})')
		#facility variables
		self.idfacility = None
		self.facility_name = None
		self.link = None
		self.location =  None
		self.address = None
		self.city = None
		self.state = None
		self.zip = None
		self.phone = None
		self.facility_permit_number = None
		self.facility_last_inspection = None
		self.facility_type = None
		self.facility_status = None
		self.facility_link = None

		#inspection variables
		self.inspection_id = None
		self.inspection_date = None
		self.year_round_facility = None
		self.complexity_rating = None
		self.inspection_type = None
		self.re_inspection_required = None
		self.license_status = None

		#certified manager variables
		self.certified_manager_name = None
		self.certificate_number = None
		self.certificate_expiration = None


		#violation variables
		self.violation_id = None
		self.violation_section = None
		self.violation_code = None
		self.violation_description = None
		self.violation_desc = None
		self.violation_observation = None
		self.violation_correction = None
		self.violation_annotation = None
		self.violation_annotation_type = None
		self.violation_priority_type = None
		self.violation_priority = None

		self.userdb = os.environ['USERLOCALD']
		self.hostdb = os.environ['HOSTLOCALKD']
		self.portbd = os.environ['PORTLOCALD']
		self.passdb = os.environ['PSELOCALD']
		self.base = os.environ['BDLOCALD']
		self.userdbr = os.environ['USERRISKD']
		self.hostdbr = os.environ['HOSTRISKD']
		self.portbdr = os.environ['PORTRISKD']
		self.passdbr = os.environ['PSERISKD']
		self.baser = os.environ['BDRISKD']
		try:
		    self.con = psycopg2.connect("dbname="+self.base+" user="+self.userdb+" host="+self.hostdb+" password="+self.passdb+"")
		    print("DB Local Host Connection")
		except:
		    #print("Conexion:"+str(con))
		    print("Unable to connect to the local host database")
		    quit()
		try:
		    self.con2 = psycopg2.connect("dbname="+self.baser+" user="+self.userdbr+" host="+self.hostdbr+" password="+self.passdbr+"")
		    print("DB Amazon Risk Connection")
		except:
		    #print("Conexion:"+str(con))
		    print("Unable to connect to the Amazon database")
		    quit()
		browserini = webdriver.Chrome()
		self.URL = 'http://www.healthspace.com/Clients/Michigan/Central/web.nsf/module_facilities.xsp?module=Food'
		search_page = browserini.get(self.URL)
		lselectp = ["//*[@id='view:_id1:_id247:_id248:firstLetterRepeat1:4:alphaPagerLink1']"]
		self.liselectp = None
		for ilselectp in lselectp:
			liselectp = browserini.find_element_by_xpath(ilselectp)
			try:
				liselectp.click()
				self.next = True
				self.inipags(browserini)
			except Exception as epags:
				self.next = False
				print("Error Itera Pags| "+str(epags))
		browserini.quit()
if __name__ == '__main__':
    inicio()
