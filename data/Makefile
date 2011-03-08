YEAR = 2011
TITLES = AA BB CC DD EE FF GG HH II JJ KK LL MM NN OO PP QQ RR SS TT UU VV WW XX YY ZZ 

default: ${TITLES}

clean:
	rm -f ${TITLES}

.DEFAULT:
	ftp http://filmguide.wifilmfest.org/tixSYS/${YEAR}/xslguide/Title/XML/$@
