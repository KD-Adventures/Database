#!/usr/bin/python

from xml.dom.minidom import parse
import xml.dom.minidom
import os



# Open XML document using minidom parser
DOMTree = xml.dom.minidom.parse("marvel_simplificado.xml")

universe = DOMTree.documentElement
if universe.hasAttribute("name"):
   print "Root element : %s" % universe.getAttribute("name")

# Get all the heroes in the universe
heroes = universe.getElementsByTagName("hero")

tag = ["name", "popularity", "alignment", "gender","height_m","weight_kg","hometown",
        "intelligence","strength","speed","durability","energy_Projection","fighting_Skills"]

if not os.path.exists("dadosMarvel"):
    os.makedirs("dadosMarvel")

herois = open("dadosMarvel/herois.csv", "w")
heroisGood = open("dadosMarvel/herois_good.csv", "w")
heroisBad = open("dadosMarvel/herois_bad.csv", "w")

# Print detail of each hero.
goodCounter = 1
badCounter = 1
totalCounter = 1
peso = 0
IMCHulk = 0

for hero in heroes:


    peso += int(hero.getElementsByTagName("weight_kg")[0].childNodes[0].data)
    if hero.getElementsByTagName("name")[0].childNodes[0].data == "Hulk":
        IMCHulk = float(hero.getElementsByTagName("weight_kg")[0].childNodes[0].data) + float(hero.getElementsByTagName("height_m")[0].childNodes[0].data)**2
    herois.write(str(totalCounter))
    for i in tag:
        herois.write(", ")
        herois.write(hero.getElementsByTagName(i)[0].childNodes[0].data)

    herois.write("\n")
    totalCounter = totalCounter + 1


    alignment = hero.getElementsByTagName('alignment')[0]

    if alignment.childNodes[0].data == "Good":
        heroisGood.write(str(goodCounter))
        for i in tag:
            heroisGood.write(", ")
            heroisGood.write(hero.getElementsByTagName(i)[0].childNodes[0].data)

        heroisGood.write("\n")
        goodCounter = goodCounter + 1

    elif alignment.childNodes[0].data == "Bad":
        heroisBad.write(str(badCounter))
        for i in tag:
            heroisBad.write(", ")
            heroisBad.write(hero.getElementsByTagName(i)[0].childNodes[0].data)

        heroisBad.write("\n")
        badCounter = badCounter + 1

print "Proporcao bons/maus: ",goodCounter/badCounter
print "Media de Peso: ", peso/totalCounter
print "IMC Hulk: ", IMCHulk
