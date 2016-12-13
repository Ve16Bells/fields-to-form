import re
outputFile = open('output/output.ejs', 'w')
previousCategory = ""

def inputPCat(category):
	category = category.rstrip().lower()
	if category == 'ground_/_landing_X_/_belfry':
		return 'landings[landing_id]' # to be dynamic
	elif category == 'tower_exterior':
		return 'bellTower'
	elif category == 'exterior_base / exterior_shaft / exterior_belfry / exterior_roof':
		return 'bellTower' # to be dynamic
	elif category == 'bellx':
		return 'bells[bell_id]'
	elif category == 'bell info':
		return '[bells]'
	else:
		print (category)
		return 'bellTower'

def output(str):
	# print(str)
	outputFile.write(str)


def writePage(category):
	# write into new file
	global outputFile
	seq = [
		'output/', category.rstrip(), '.htm'
	]
	outputFileName = "".join(seq)
	outputFile = open(outputFileName, 'w')

	seq = [
		'<div id="', category.rstrip(), 'Data">\n'
	]
	str = "".join(seq)
	output(str)

def writeAccordion(line):
	seq = [
		'\t<div class="ui fluid accordion">\n',
			'\t\t<div class="title">\n',
				'\t\t\t<h2>', line.rstrip() ,'</h2>\n',
			'\t\t</div>\n',
			'\t\t<div class="content whitePaddedContent">\n',
			'\t\t</div>\n',
	]
	str = "".join(seq)
	output(str)

def writeAccordSection(line):
	seq = [
		'\t\t<div class="title">\n',
			'\t\t\t<i class="dropdown icon"></i>\n',
			'\t\t\t', line.rstrip(), '\n',
		'\t\t</div>\n',
		'\t\t<div class="content whitePaddedContent">\n'
	]
	str = "".join(seq)
	output(str)

def writeDivs(line):
	str = '</div>\n'

	for x in range (1, len(line.rstrip()) ):
		str =  '\t' + str

	if len(line.rstrip()) == 2:
		str =  str + '\n'
	if len(line.rstrip()) == 1:
		str =  str + '\n\n\n'

	output(str)

def writeField(line):
	lineArr = line.split(':')
	section = ""
	# lineArr[0] = 'Base_' + lineArr[0];

	if (len(lineArr) == 1): # normal text field
		section = get_Text_Field(lineArr[0]);
		output(section);
		return

	if "bool" in lineArr[1]:
		section = get_Bool_Field(lineArr[0]);
	elif "rating" in lineArr[1]:
		section = get_Rating_Field(lineArr[0]);
	elif "select" in lineArr[1]:
		section = get_Select_Field(lineArr[0], lineArr[1]);
	elif "textarea" in lineArr[1]:
		section = get_TextArea_Field(lineArr[0]);

	output(section)

def get_Text_Field(field):
	global previousCategory
	category = inputPCat(previousCategory).rstrip();
	seq = [
		'\t\t\t<div class="field">\n',
		'\t\t\t\t<label>', field.rstrip().replace("_", " "), '</label>\n',
		'\t\t\t\t<input type="text"  ng-model="', category ,'[\'', field.rstrip(),'\']" placeholder="', field.rstrip(),'">\n',
		'\t\t\t</div>\n\n'
	]
	str = "".join(seq)
	return str

def get_TextArea_Field(field):
	global previousCategory
	category = inputPCat(previousCategory).rstrip();
	seq = [
		'\t\t\t<div class="field">\n',
		'\t\t\t\t<label>', field.rstrip().replace("_", " "), '</label>\n',
		'\t\t\t\t<textarea ng-model="', category ,'[\'', field.rstrip(),'\']"  rows="2"></textarea>\n',
		'\t\t\t</div>\n\n'
	]
	str = "".join(seq)
	return str

def get_Bool_Field(field):
	global previousCategory
	category = inputPCat(previousCategory).rstrip();
	seq = [
		'\t\t\t<div class="inline field">\n',
		'\t\t\t\t<div class="ui checkbox">\n',
		'\t\t\t\t\t<input type="checkbox" ng-model="', category ,'[\'', field.rstrip() ,'\']" ng-true-value="\'YES\'" ng-false-value="\'NO\'">\n',
		'\t\t\t\t\t<label>', field.rstrip().replace("_", " ") ,':<span class="inputValue"> {{ ', category ,'[\'', field.rstrip() ,'\'] }}</span></label>\n',
		'\t\t\t\t</div>\n',
		'\t\t\t</div>\n\n'
	]
	str = "".join(seq)
	return str

def get_Rating_Field(field):
	global previousCategory
	category = inputPCat(previousCategory).rstrip();

	seq = [
		'\t\t\t<div class="field">\n',
		'\t\t\t\t<label>', field.rstrip().replace("_", " ") ,':<span class="inputValue"> {{ ', category ,'[\'', field.rstrip() ,'\'] }}</span></label>\n',
		'\t\t\t\t<input class="rating" type="range" ng-model="', category ,'[\'', field.rstrip() ,'\']" min="0"  max="5">\n',
		'\t\t\t</div>\n\n'
	]
	str = "".join(seq)
	return str

def get_Select_Field(field, selects):
	global previousCategory
	category = inputPCat(previousCategory).rstrip();
	arrOfSelect = selects.split('(')[1].split(')')[0].split(', ')

	startSeq = [
		'\t\t\t<div class="field">\n',
		'\t\t\t\t<label>', field.rstrip().replace("_", " ") ,':<span class="inputValue"> {{ ', category ,'[\'', field.rstrip() ,'\'] }}</span></label>\n',
		'\t\t\t\t<select class="select" ng-model="', category ,'[\'', field.rstrip() ,'\']">\n',
	]

	midSeq = [] 
	for selection in arrOfSelect:
		tempstr = '\t\t\t\t\t<option value="'+ selection + '"> '+ selection +' </option>\n'
		midSeq.append( tempstr )


	endSeq = [
		'\t\t\t\t</select>\n',
		'\t\t\t</div>\n\n'
	]
	str = "".join(startSeq) + "".join(midSeq) + "".join(endSeq)
	return str


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
def handleLine(line):
	global previousCategory
	regNewPage = re.compile("^#[^#]") #
	regNewAccordion = re.compile("^##[^#]") ##
	regNewAccordSection = re.compile("^###[^#]") ###
	regEndDivs = re.compile(">")
	regEmpty = re.compile("^$| ")

	if regNewPage.match(line):
		writePage(line.split(" ",1)[1])
	elif regNewAccordion.match(line):
		previousCategory = line.split(" ",1)[1]
		writeAccordion(line.split(" ",1)[1])
	elif regNewAccordSection.match(line):
		writeAccordSection(line.split(" ",1)[1])
	elif regEndDivs.match(line):
		writeDivs(line)
	elif regEmpty.match(line):
		pass # do nothing if empty
	else:
		writeField(line)

""" 

"""