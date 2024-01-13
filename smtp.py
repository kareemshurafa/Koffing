
import smtplib
# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)
# start TLS for security
s.starttls()
# Authentication
s.login("koffingasthma@gmail.com", "elyp bmsw wage neyw") # sender email, sender password
# message to be sent
message = "Testing again.."
# sending the mail
s.sendmail("koffingasthma@gmail.com", "amirsyahmibhari@gmail.com", message) # sender email, receiver email
# terminating the session
s.quit()
