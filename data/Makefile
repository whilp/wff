YEAR = 2011
XML = AA.xml BB.xml CC.xml DD.xml EE.xml FF.xml GG.xml HH.xml II.xml JJ.xml KK.xml LL.xml MM.xml NN.xml OO.xml PP.xml QQ.xml RR.xml SS.xml TT.xml UU.xml VV.xml WW.xml XX.xml YY.xml ZZ.xml 
JSON = ${XML:R/\.xml$/.json/}

.SUFFIXES: .xml .json

default: ${XML}

clean:
	rm -f ${XML} ${JSON}

.xml.json:
	./extract.py ${.IMPSRC} > ${.TARGET}

.DEFAULT:
	curl -s -o ${.TARGET} http://filmguide.wifilmfest.org/tixSYS/${YEAR}/xslguide/Title/XML/${.TARGET:R}
