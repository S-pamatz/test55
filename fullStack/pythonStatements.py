

from app import db
#create the database file, if it doesn't exist. 
db.create_all()




#import major model
from app.models import Major

# creater a major
newMajor = Major(name='CptS',department='School of EECS')
db.session.add(newMajor)
newMajor = Major(name='CE',department='Civil Engineering')
db.session.add(newMajor)
db.session.commit()
Major.query.all()
for m in Major.query.all():
    print(m)






# import db models
from app.models import Class

#create class objects and write them to the database
newClass = Class(coursenum='322',major='CptS',title='Software Engineering')
db.session.add(newClass)
newClass = Class(coursenum='315',major='CE',title='Fluid Mechanics')
db.session.add(newClass)
db.session.commit()

# query and print classes
allClasses=Class.query.all()
Class.query.filter_by(major='CptS').all()
Class.query.filter_by(major='CptS').first()
Class.query.filter_by(major='CptS').order_by(Class.title).all()
Class.query.filter_by(major='CptS').count()

mymajor=Major.query.filter_by(name='CptS').first()
for c in mymajor.classes:
    print(c.title)

#Class.query.filter_by(coursenum='322').all()
#Class.query.filter_by(coursenum='322').first()
#myclasses = Class.query.order_by(Class.coursenum.desc()).all()
#for c in myclasses:
 #   print(c.coursenum)
