

class simconf():

	def parse_config(self,config,filename,quota=0):

		options = {}
		
		f = open(filename)
		for line in f:

			if '=' in line:

				option, value = line.split('=', 1)
				
				for key in config:

					if option.strip()==key:

						if quota ==1:
							options[key]=value.strip().strip("\"")
						else:
							options[key]=value.strip()

						print ("parse_config echo:",value.strip())

		f.close()
		return options

	    #print options

	def save_config(self,config,filename,quota=0):

		with open(filename, 'r') as file:
			data = file.readlines()

			for index, line in enumerate(data):

				if '=' in line:
				
					option, value = line.split('=', 1)

					for key in config:
					
						if option.strip()==key:
							if quota ==1:
								data[index] = option+"="+"\""+config[key]+"\"\n"
							else:
								data[index] = option+"="+config[key]+"\n"

		#print (data)
		file.close()

		with open(filename, 'w') as file:
			file.writelines( data )
		file.close()
#with open('stats.txt', 'r') as file:
	#data = file.readlines()
#with open('stats.txt', 'w') as file:
#    file.writelines( data )