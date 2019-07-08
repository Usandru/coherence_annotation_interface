## Code by Jesper Rugård Jensen

from bs4 import BeautifulSoup
import requests
import random
import csv

folketinget = "https://www.ft.dk"
url = "https://www.ft.dk/da/dokumenter/dokumentlister/referater?numberOfDays=-1000&pageSize=400"
anden_dag = "https://www.ft.dk/forhandlinger/20181/20181M092_2019-05-03_1000.htm"
test_url = "https://www.ft.dk/forhandlinger/20181/20181M093_2019-05-07_1300.htm"

def hent_tale_urler(url):
	result = requests.get(url)
	soup = BeautifulSoup(markup=result.content, features='html.parser')
	urler = soup.find_all('tr', "listespot-wrapper__data-item")
	return urler

def hent_taler(url):
	result = requests.get(url)
	soup = BeautifulSoup(markup=result.content, features='html.parser')
	taler = soup.select("p.TalerTitelMedTaleType,p.TalerTitel,p.Tekst,p.TekstIndryk,p.Tid,p.TekstLuft")
	return taler

def sammensaet_taler(taler):
	return_contents = [["header"],[],[], []]
	contents = ["Tid", "Taler", "Indhold", 0]
	seneste_tid = ""
	for i in range(len(taler)): 
		if taler[i].get("class") == ["Tid"]:
			seneste_tid = taler[i].get_text()		
		else:
			if "Taler" in taler[i].get("class")[0]:
				return_contents.append(contents.copy())
				contents[0] = seneste_tid[4:].strip('\n')
				contents[1] = taler[i].get_text().strip('\n')
				contents[2] = ""
				contents[3] = 0
			else:
				contents[2] += taler[i].get_text() + " LINEBREAK "
				contents[3] += len(taler[i].get_text().split())
	
	return_contents.append(contents.copy())
	return return_contents

def filtrer_tale(taler, talende, ikke_talende, mini, maxi) :
	return list( filter(lambda t: len(t) == 4 and
	 (not talende or any(x in t[1] for x in talende)) and
	 (not ikke_talende or not any(x in t[1] for x in ikke_talende)) and 
	  t[3] >= mini and t[3] <= maxi , taler))	

#Hent urler fra forside i folketinget
urler = hent_tale_urler(url)

#for u in urler:
#	print(u.get("data-url"))

print(len(urler))


for url_end in urler:
	full_url = folketinget + url_end.get("data-url")
	current_data = hent_taler(full_url)
	structured_data = sammensaet_taler(current_data)
	filtered_data = filtrer_tale(structured_data, [], ["ormand"], 40, 60)

	print(full_url)
	print(len(filtered_data))

	with open('./output/{}.csv'.format(full_url[full_url.rfind('/')+1:full_url.rfind('.')]), mode='w', encoding='utf-8') as curr_file:
		curr_writer = csv.writer(curr_file, delimiter=',', quotechar='"',quoting=csv.QUOTE_ALL)
		for t in filtered_data:
			curr_writer.writerow(t)
		curr_file.close()

""" #Find en tilfældig side
indeks = random.randrange(len(urler))
random_url = folketinget + urler[indeks].get("data-url")

print(random_url)
taler = hent_taler(random_url)
sammensatte_taler = sammensaet_taler(taler)
rest_taler = filtrer_tale(sammensatte_taler, [], ["Pia", "ormand"],  25, 200)

for t in rest_taler:
	print(t)
	print("-----------")
print(len(sammensatte_taler))
print(len(rest_taler))

with open('urler_file.csv', mode='w') as urler_file:
	urler_writer = csv.writer(urler_file, delimiter=';', quotechar='"',quoting=csv.QUOTE_ALL)
	for t in urler :
		urler_writer.writerow([folketinget + t.get("data-url")])

	urler_file.close()

with open('taler_file-{}.csv'.format(random_url[random_url.rfind('/')+1:random_url.rfind('.')]), mode='w') as taler_file:
	taler_writer = csv.writer(taler_file, delimiter=',', quotechar='"',quoting=csv.QUOTE_ALL)
	for t in rest_taler :
		taler_writer.writerow(t)
	taler_file.close() """