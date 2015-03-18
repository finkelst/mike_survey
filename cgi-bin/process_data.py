#!/usr/bin/env python

import random
import subprocess
import os.path
import cgi
import json
from datetime import date, time, datetime

vowel_sounds = ['0-IY.wav', '1-IH.wav', '2-EY.wav', '3-EH.wav', '4-ER.wav', '5-AE.wav', '6-AAW.wav', '7-AA.wav', '8-AH.wav', '9-OA.wav', '10-UH.wav', '11-UW.wav']
leadIn = 'leadIn.wav'
fillIn = 'fillIn.wav'
schwa = 'schwa.wav'

form = cgi.FieldStorage()
data = {}

id_number = form['id_number'].value
filename = str(id_number) + '-data.csv'



if 'demo_response1' in form:	#determine first time demo
	if os.path.isfile("../data/user_data.csv"): #determine if this is the first user to take the survey and write headers
		f = open('../data/user_data.csv', 'a')
		f.write(str(id_number) + ', ')
		f.write(form['demo_response1'].value + ', ')
		f.write(form['demo_response2'].value + ', ')
		f.write(form['demo_response3'].value)
		f.write('\n')
		f.close()
	else:
		f = open('../data/user_data.csv', 'a')
		f.write('user_id' + ', ')
		f.write('rel_ed' + ', ')
		f.write('rel_music' + ', ')
		f.write('rel_rap' + ', ')
		f.write('\n')
		f.write(str(id_number) + ', ')
		f.write(form['demo_response1'].value + ', ')
		f.write(form['demo_response2'].value + ', ')
		f.write(form['demo_response3'].value)
		f.write('\n')
		f.close()
	
if 'vowel_pattern' in form:	#determine whether this the first stimulus of this session
	if os.path.isfile('../data/' + filename): #determine if this is the first time this user has taken survey and write headers
		f = open('../data/' + filename, 'a')
		f.write(str(id_number) + ', ')
		f.write(form['response'].value + ', ')
		f.write(form['test_case'].value + ', ')
		f.write(form['vowel_pattern'].value)
		f.write('\n')
		f.close()
	else:
		f = open('../data/' + filename, 'a')
		f.write('user_id' + ', ')
		f.write('response_value' + ', ')
		f.write('test_case' + ', ')
		f.write('vowel_1' + ', ')
		f.write('vowel_2' + ', ')
		f.write('vowel_3' + ', ')
		f.write('vowel_4' + ', ')
		f.write('vowel_5' + ', ')
		f.write('vowel_6' + ', ')
		f.write('\n')
		f.write(str(id_number) + ', ')
		f.write(form['response'].value + ', ')
		f.write(form['test_case'].value + ', ')
		f.write(form['vowel_pattern'].value)
		f.write('\n')
		f.close()

def main():
	runTestCase(0, 0)	#dummy arguments for now

def runTestCase(respondentNum, fileName):
	audio = generateWaveFile(defineStimulus(respondentNum, random.randint(0, 4), fileName))

def generateWaveFile(lines):

	#sox command concatenates 12 vowel sounds and writes them to trialStim.wav
	#blf changed filepaths for localhost build. might have to replace everything with absolute paths later
	cmd = ['sox', '../files/leadIn.wav']
	line1 = lines[0]
	line2 = lines[1]
	for v in line1:
		cmd.append('../files/' + v)
	cmd.append('../files/fillIn.wav')
	for u in line2:
		cmd.append('../files/' + u)
	#blf added a new folder to hold all of the wav files	
	cmd.append('../stims/' + str(id_number) +'-trialStim.wav')
	#run the command on the command line
	subprocess.call(cmd,shell=True) #this is for windows 
	#subprocess.call(cmd)
	#subprocess.call(['chmod', 'a+x', 'trialStim.wav'])
	f = open('../testout.txt', 'w')
	f.write(str(cmd))
	f.close()

def defineStimulus(respondentNum, testCaseNumber, fileName):
	vowels = vowel_sounds
# 	unstressedVowels = vowels_unstressed
	x = vowels.pop(random.randint(0,11))
	z = vowels.pop(random.randint(0,10))
	y = vowels.pop(random.randint(0,9))
	a = vowels.pop(random.randint(0,8))
	b = vowels.pop(random.randint(0,7))
	c = vowels.pop(random.randint(0,6))
	d = vowels.pop(random.randint(0,5))
	e = vowels.pop(random.randint(0,4))
	f = vowels.pop(random.randint(0,3))
	alt1 = vowels.pop(random.randint(0,2))
	alt2 = vowels.pop(random.randint(0,1))
# 	alt3 = vowels.pop(random.randint(0,4))


	testCaseNumber = testCaseNumber % 5
	line1 = [x, y, z]
	if testCaseNumber == 0:
		line2 = [alt1, y, alt2]
	elif testCaseNumber == 1:
		line2 = [x, y, alt2]
	elif testCaseNumber == 2:
		line2 = [alt1, y, z]
	elif testCaseNumber == 3:
		line2 = [x, alt1, z]
	elif testCaseNumber == 4:
		line2 = [x, y, z]

# 	stimulusPat = [line1, line2]
	# print 'Test Case: ' + str(testCaseNumber) + ', '.join(line1)
	# print ', '.join(line2)

	vowel_pattern = [line1, line2]
	flattened = [item for sublist in vowel_pattern for item in sublist]
	data['vowel_pattern'] = ", ".join(str(e) for e in flattened)
	data['test_case_number'] = testCaseNumber


	return vowel_pattern


	###TODO: write headers to response file or database


main()
f = open('../testout2.txt', 'w')
f.write(str(data))
f.close()
print "Content-type: application/json"
print
print json.dumps(data)