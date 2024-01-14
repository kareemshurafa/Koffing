import yagmail
yag = yagmail.SMTP('koffingasthma@gmail.com', oauth2_file="~/token.json")
# contents = ['This is the body, and here is just text http://somedomain/image.png',
#             'You can find an audio file attached.']
# yag.send('amirsyahmibhari@gmail.com', 'subject', contents)
yag.send('amirsyahmibhari@gmail.com', subject="Great!")