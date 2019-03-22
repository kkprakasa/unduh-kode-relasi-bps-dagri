import urllib2
import json
import csv

headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36' }
prov = [11,12,13,14,15,16,17,18,19,21,31,32,33,34,35,36,51,52,53,61,62,63,64,65,71,72,73,74,75,76,81,82,91,94]
desa=[]
for i in prov:
	req = urllib2.Request('https://sig-dev.bps.go.id/restBridging/getwilayahperiode/level/kabupaten/parent/'+str(i)+'/periode/20181', None, headers)
	dres = urllib2.urlopen(req)
	dhtml = json.loads(dres.read())
	for j in dhtml:
		req = urllib2.Request('https://sig-dev.bps.go.id/restBridging/getwilayahperiode/level/kecamatan/parent/'+j['kode_bps']+'/periode/20181', None, headers)
		dres = urllib2.urlopen(req)
		dhtml2 = json.loads(dres.read())
		#if 'desa' in vars():
		for key in j.keys():
			j[key+'_kabkot'] = j.pop(key)
		for n in dhtml2:
			print('memproses :'+ j['nama_bps_kabkot'])
			req = urllib2.Request('https://sig-dev.bps.go.id/restBridging/getwilayahperiode/level/desa/parent/'+n['kode_bps']+'/periode/20181', None, headers)
			dres = urllib2.urlopen(req)
			dhtml3 = json.loads(dres.read())
			for key in n.keys():
				n[key+'_kec'] = n.pop(key)
			n.update(j)
			# desa.append(n)
			for k in dhtml3:
				for key in k.keys():
					k[key+'_deskel']=k.pop(key)
				k.update(n)
				desa.append(k)
				print('selesai memproses '+ j['nama_bps_kabkot']+' kecamatan : '+ n['nama_bps_kec']+' desa : '+k['nama_bps_deskel'])

head = desa[0].keys()
with open('data-relasi-baru1112.csv', 'wb') as o_f:
    d_w = csv.DictWriter(o_f, head)
    d_w.writeheader()
    d_w.writerows(desa)
    	
# req = urllib2.Request('https://sig-dev.bps.go.id/restBridging/getwilayahperiode/level/kecamatan/parent/1202/periode/20181', None, headers)
# dres = urllib2.urlopen(req)
# dhtml = dres.read()