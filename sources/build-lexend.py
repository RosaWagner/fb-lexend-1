# License: Apache 2.0

from __future__ import print_function

# from glyphNameFormatter.data import name2unicode_AGD
from mutatorMath.ufo.document import DesignSpaceDocumentWriter, DesignSpaceDocumentReader
from designSpaceDocument import DesignSpaceDocument, SourceDescriptor, InstanceDescriptor, AxisDescriptor, RuleDescriptor
#from fontTools.designspaceLib import DesignSpaceDocument, SourceDescriptor, InstanceDescriptor, AxisDescriptor, RuleDescriptor

from fontmake.font_project import FontProject
from fontTools.varLib import build
from fontTools.varLib.mutator import instantiateVariableFont
from defcon import Font
import shutil
from distutils.dir_util import copy_tree
import os

	
def buildDesignSpace(sources, instances, axes):
	# use DesignSpaceDocument because it supports axis labelNames
	doc = DesignSpaceDocument()
	
	for source in sources:
		s = SourceDescriptor()
		s.path = source["path"]
		s.name = source["name"]
		s.copyInfo = source["copyInfo"]
		s.location = source["location"]
		s.familyName = source["familyName"]
		s.styleName = source["styleName"]
		doc.addSource(s)
	
	for instance in instances:
		i = InstanceDescriptor()
		i.location = instance["location"]
		i.familyName = instance["familyName"]
		i.styleName = instance["styleName"]
		doc.addInstance(i)
	
	for axis in axes:
		a = AxisDescriptor()
		a.minimum = axis["minimum"]
		a.maximum = axis["maximum"]
		a.default = axis["default"]
		a.name = axis["name"]
		a.tag = axis["tag"]
		for languageCode, labelName in axis["labelNames"].items():
			a.labelNames[languageCode] = labelName
		a.map = axis["map"]
		doc.addAxis(a)
		
	return doc

def buildGlyphSet(dflt, fonts):
	# fill the glyph set with default glyphs
	for font in fonts:
		for glyph in dflt:
			glyphName = glyph.name
			if glyphName not in font and glyphName not in composites:
				font.insertGlyph(glyph)
				font[glyphName].lib['com.typemytype.robofont.mark'] = [0, 0, 0, 0.25] # dark grey

# def buildComposites(composites, fonts):
# 	# build the composites
# 	for font in fonts:
# 		for glyphName in composites.keys():
# 			font.newGlyph(glyphName)
# 			composite = font[glyphName]
# 			composite.unicode = name2unicode_AGD[glyphName]
			
# 			value = composites[glyphName]
# 			items = value.split("+")
# 			base = items[0]
# 			items = items[1:]
	
# 			component = composite.instantiateComponent()
# 			component.baseGlyph = base
# 			baseGlyph = font[base]
# 			composite.width = baseGlyph.width
# 			composite.appendComponent(component)
	
# 			for item in items:
# 				baseName, anchorName = item.split("@")
# 				component = composite.instantiateComponent()
# 				component.baseGlyph = baseName
# 				anchor = _anchor = None
# 				for a in baseGlyph.anchors:
# 					if a["name"] == anchorName:
# 						anchor = a
# 				for a in font[baseName].anchors:
# 					if a["name"] == "_"+anchorName:
# 						_anchor = a
# 				if anchor and _anchor:
# 					x = anchor["x"] - _anchor["x"]
# 					y = anchor["y"] - _anchor["y"]
# 					component.move((x, y))
# 				composite.appendComponent(component)
# 			composite.lib['com.typemytype.robofont.mark'] = [0, 0, 0, 0.5] # grey

def setGlyphOrder(glyphOrder, fonts):
	# set the glyph order
	for font in fonts:
		font.glyphOrder = glyphOrder

def clearAnchors(fonts):
	# set the glyph order
	for font in fonts:
		for glyph in font:
		    glyph.clearAnchors()

def saveMasters(fonts, master_dir="master_ufo"):
	# save in master_ufo directory
	for font in fonts:
		path = os.path.join(master_dir, os.path.basename(font.path))

		#added this check because the "master_ufo" folder is getting removed at the beginning of this script
		if not os.path.exists(path):
			os.makedirs(path)
		font.save(path)

with open("sources/Lexend.enc") as enc:
	glyphOrder = enc.read().splitlines()


print ("Cleaning up...")

# clean up previous build
if os.path.exists("instances"):
	shutil.rmtree("instances", ignore_errors=True)
if os.path.exists("master_ttf"):
	shutil.rmtree("master_ttf", ignore_errors=True)
if os.path.exists("master_ufo"):
	shutil.rmtree("master_ufo", ignore_errors=True)
if os.path.exists("master_ttf_interpolatable"):
	shutil.rmtree("master_ttf_interpolatable", ignore_errors=True)

# Remove temporary 1-drawings
if os.path.exists("sources/1-drawings"):
	shutil.rmtree("sources/1-drawings", ignore_errors=True)


# New
src = {	"sources",
		}
	

src_dir = "sources/1-drawings"
master_dir = "master_ufo"
instance_dir = "instances"

# Copy sources to temporary 1-drawings
for source in src:
	copy_tree(source, src_dir)


# use a temporary designspace to build instances with mutator math
familyName = "Lexend"
tmpDesignSpace = "tmp.designspace"
doc = DesignSpaceDocumentWriter(tmpDesignSpace)
# sources
doc.addSource(path="sources/1-drawings/Lexend-Regular.ufo", name="Lexend-Regular.ufo", location=dict( wdth=100 ), styleName="Regular", familyName=familyName, copyLib=True, copyGroups=True, copyInfo=True, copyFeatures=True, muteKerning=False, muteInfo=False, mutedGlyphNames=None)

# axes
# doc.addAxis(tag="wght", name="wght", minimum=300, maximum=800, default=500, warpMap=None)
doc.addAxis(tag="wdth", name="wdth", minimum=100, maximum=125, default=100, warpMap=None)
# doc.addAxis(tag="opsz", name="opsz", minimum=8, maximum=144, default=14, warpMap=None)


# instances
instances = [
#	dict(fileName="instances/Amstelvar-Roman-opsz144-wght100-wdth125.ufo", location=dict(wght=100, wdth=125, opsz=04), styleName="opsz144-wght100-wdth125", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),
#	dict(fileName="instances/Amstelvar-Roman-opsz144-wght100-wdth075.ufo", location=dict(wght=100, wdth=87, opsz=04), styleName="opsz144-wght100-wdth075", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),
#	dict(fileName="instances/Amstelvar-Roman-opsz144-wght100-wdth50.ufo", location=dict(wght=100, wdth=75, opsz=04), styleName="opsz144-wght100-wdth50", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),
	
#	dict(fileName="instances/Amstelvar-Roman-opsz144-wght900-wdth125.ufo", location=dict(wght=900, wdth=125, opsz=04), styleName="opsz144-wght900-wdth125", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),
#	dict(fileName="instances/Amstelvar-Roman-opsz144-wght900-wdth075.ufo", location=dict(wght=900, wdth=76, opsz=04), styleName="opsz144-wght900-wdth075", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),
#	dict(fileName="instances/Amstelvar-Roman-opsz144-wght900-wdth50.ufo", location=dict(wght=900, wdth=75, opsz=04), styleName="opsz144-wght900-wdth50", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),
	
#	dict(fileName="instances/Amstelvar-Roman-opsz144-wdth125.ufo", location=dict(wght=400, wdth=125, opsz=04), styleName="opsz144-wdth125", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),
#	dict(fileName="instances/Amstelvar-Roman-opsz144-wdth075.ufo", location=dict(wght=400, wdth=80, opsz=04), styleName="opsz144-wdth075", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),
#	dict(fileName="instances/Amstelvar-Roman-opsz144-wdth50.ufo", location=dict(wght=400, wdth=75, opsz=04), styleName="opsz144-wdth50", familyName=familyName, postScriptFontName=None, styleMapFamilyName=None, styleMapStyleName=None),
]
for instance in instances:
	doc.startInstance(**instance)
	doc.writeInfo()
	doc.writeKerning()
	doc.endInstance()

doc.save()
# read and process the designspace
doc = DesignSpaceDocumentReader(tmpDesignSpace, ufoVersion=2, roundGeometry=False, verbose=False)
print ("Reading DesignSpace...")
doc.process(makeGlyphs=True, makeKerning=True, makeInfo=True)
os.remove(tmpDesignSpace) # clean up

# update the instances with the source fonts
# print str(instances) + ' instances! '
for instance in instances:
	fileName = os.path.basename(instance["fileName"])
	source_path = os.path.join(src_dir, fileName)
	instance_path = os.path.join(instance_dir, fileName)
	source_font = Font(source_path)
	instance_font = Font(instance_path)
	# insert the source glyphs in the instance font
	for glyph in source_font:
		instance_font.insertGlyph(glyph)
	master_path = os.path.join(master_dir, fileName)
	instance_font.save(master_path)

designSpace = "sources/Lexend.designspace"
sources = [
	dict(path="master_ufo/Lexend-Regular.ufo", name="Lexend-Regular.ufo", location=dict( wght=500, wdth=100, SPAC=100, LXND=0 ), styleName="Regular", familyName=familyName, copyInfo=True),
	
##	Weight 
	dict(path="master_ufo/Lexend-wght100.ufo", name="Lexend-wght100.ufo", location=dict(wght=100, wdth=100, SPAC=100, LXND=0 ), styleName="wght100", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/Lexend-wght300.ufo", name="Lexend-wght300.ufo", location=dict(wght=300, wdth=100, SPAC=100, LXND=0 ), styleName="wght300", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/Lexend-wght800.ufo", name="Lexend-wght800.ufo", location=dict(wght=800, wdth=100, SPAC=100, LXND=0 ), styleName="wght800", familyName=familyName, copyInfo=False),

#	Width
	dict(path="master_ufo/Lexend-wght500-wdth125-SPACmin.ufo", name="Lexend-wght500-wdth125-SPACmin.ufo", location=dict( wght=500, wdth=125, SPAC=100, LXND=0 ), styleName="wght500-wdth125-SPACmin", familyName=familyName, copyInfo=False),
	
	#SPAC
	dict(path="master_ufo/Lexend-wght500-wdth100-SPACmax.ufo", name="Lexend-wght500-wdth100-SPACmax.ufo", location=dict( wght=500, wdth=100, SPAC=125, LXND=0 ), styleName="wght500-wdth100-SPACmax", familyName=familyName, copyInfo=False),
	dict(path="master_ufo/Lexend-wght500-wdth125-SPACmax.ufo", name="Lexend-wght500-wdth125-SPACmax.ufo", location=dict( wght=500, wdth=125, SPAC=125, LXND=0), styleName="wght500-wdth125-SPACmax", familyName=familyName, copyInfo=False),
	
	#SPCG
# 	dict(path="master_ufo/Lexend-Regular.ufo", name="Lexend-Regular.ufo", location=dict( SPCG=0 ), styleName="wght500-wdth110-SPACmin", familyName=familyName, copyInfo=False),
# 	dict(path="master_ufo/Lexend-wght500-wdth125-SPACmax.ufo", name="Lexend-wght500-wdth125-SPACmax.ufo", location=dict( SPCG=1 ), styleName="wght500-wdth125-SPACmax", familyName=familyName, copyInfo=False),
	
	#LXND
	dict(path="master_ufo/Lexend-LXND1.ufo", name="Lexend-LXND1.ufo", location=dict( wght=500, wdth=100, SPAC=100, LXND=1 ), styleName="LXND1", familyName=familyName, copyInfo=False),

]
#instances = []
axes = [
	
	dict(minimum=100, maximum=800, default=500, name="wght", tag="wght", labelNames={"en": "wght"}, map=[]),
	dict(minimum=100, maximum=125, default=100, name="wdth", tag="wdth", labelNames={"en": "wdth"}, map=[]),
	dict(minimum=100, maximum=125, default=100, name="SPAC", tag="SPAC", labelNames={"en": "SPAC"}, map=[]),
#  	dict(minimum=0, maximum=1, default=0, name="SPCG", tag="SPCG", labelNames={"en": "SPCG"}, map=[]),
	dict(minimum=0, maximum=1, default=0, name="LXND", tag="LXND", labelNames={"en": "LXND"}, map=[]),
# 	dict(minimum=8, maximum=144, default=14, name="opsz", tag="opsz", labelNames={"en": "opsz"}, map=[ (8.0, -1), (14.0, 0), (24.0, 0.077), (36.0, 0.492), (84.0, 0.946), (144.0, 1.0) ]),
# 	dict(minimum=-1, maximum=1, default=0, name="GRAD", tag="GRAD", labelNames={"en": "GRAD"}, map=[]),
# 	dict(minimum=324, maximum=640, default=562, name="XTRA", tag="XTRA", labelNames={"en": "XTRA"}, map=[]),
# 	dict(minimum=18, maximum=263, default=176, name="XOPQ", tag="XOPQ", labelNames={"en": "XOPQ"}, map=[]),
# 	dict(minimum=15, maximum=132, default=124, name="YOPQ", tag="YOPQ", labelNames={"en": "YOPQ"}, map=[]),
# 	dict(minimum=420, maximum=570, default=500, name="YTLC", tag="YTLC", labelNames={"en": "YTLC"}, map=[]),
# 	dict(minimum=500, maximum=1000, default=750, name="YTUC", tag="YTUC", labelNames={"en": "YTUC"}, map=[]),
# 	dict(minimum=500, maximum=983, default=767, name="YTAS", tag="YTAS", labelNames={"en": "YTAS"}, map=[]),
# 	dict(minimum=-500, maximum=-138, default=-240, name="YTDE", tag="YTDE", labelNames={"en": "YTDE"}, map=[]),
# 	dict(minimum=425, maximum=1000, default=760, name="YTFI", tag="YTFI", labelNames={"en": "YTFI"}, map=[]),

]

doc = buildDesignSpace(sources, instances, axes)


doc.write(designSpace)

default = "Lexend-Regular.ufo"
# load the default font
default_path = os.path.join(src_dir, default)
dflt = Font(default_path)

sources = [source.name for source in doc.sources]
# take the default out of the source list
sources.remove(default)

print ("Building masters...")

# load font objects
fonts = []
accentFonts = []
for fileName in sources:
	source_path = os.path.join(src_dir, fileName)
	master_path = os.path.join(master_dir, fileName)
	if os.path.exists(master_path):
		# use this updated instance
		font = Font(master_path)
	else:
		font = Font(source_path)
	if fileName not in ['Lexend-Regular']:
	    accentFonts.append(font)
	fonts.append(font)
	
#buildGlyphSet(dflt, fonts)
allfonts = [dflt]+fonts
#buildComposites(composites, accentFonts)
setGlyphOrder(glyphOrder, allfonts)
#clearAnchors(allfonts)
saveMasters(allfonts)

# build Variable Font

ufos = [font.path for font in allfonts]
project = FontProject()
project.run_from_ufos(
	ufos, 
	output=("ttf-interpolatable"), # FIXME this also build master_ttf and should not.
	remove_overlaps=False, 
	reverse_direction=False, 
	use_production_names=False)

#temp changed rel path to work in same dir, was:  ../fonts/Amstelvar-Roman-VF.ttf
outfile = "Lexend[wdth-SPAC-LXND].ttf"

#make folder if it doesn't exist
destFolder = "fonts"
if not os.path.exists(destFolder):
    os.makedirs(destFolder)
outfile = os.path.join(destFolder, outfile)



finder = lambda s: s.replace("master_ufo", "master_ttf").replace(".ufo", ".ttf")



varfont, _, _ = build(designSpace, finder)
print ("Saving Variable Font...")
varfont.save(outfile)

print ("Cleaning up...")

# clean up previous build
if os.path.exists("instances"):
	shutil.rmtree("instances", ignore_errors=True)
if os.path.exists("master_ttf"):
	shutil.rmtree("master_ttf", ignore_errors=True)
if os.path.exists("master_ufo"):
	shutil.rmtree("master_ufo", ignore_errors=True)
if os.path.exists("master_ttf_interpolatable"):
	shutil.rmtree("master_ttf_interpolatable", ignore_errors=True)

# Remove temporary 1-drawings
if os.path.exists("sources/1-drawings"):
	shutil.rmtree("sources/1-drawings", ignore_errors=True)

print ("DONE!")

# SUBSET COMMAND
# pyftsubset Amstelvar-Roman-VF.ttf --text-file=ascii-subset.txt --output-file=Amstelvar-Roman-subset-VF.ttf
