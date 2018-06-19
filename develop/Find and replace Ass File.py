#import c4d

" v01"

a = 'texto:test'

b = 'test'

c = []

if b in a:
	print True
	c = a.split(':')
	print c[0]

else:
	print False