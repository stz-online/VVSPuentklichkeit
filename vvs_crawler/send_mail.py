import subprocess
import sendgrid
from YamJam import yamjam
from sendgrid.helpers.mail import Email, Content, Mail

keys = yamjam("keys.yaml")

output = subprocess.Popen(["psql", "-U","postgres","-d","vvs_crawler", "-c", "Select * FROM get_highest_n_delays('2016-10-01', '2016-10-20', 20);"],
                          stdout=subprocess.PIPE).communicate()
sg = sendgrid.SendGridAPIClient(apikey=keys['sendgrid']['key'])
from_email = Email(keys['vvs']['from_mail'])
subject = "VVS Report"
to_email = Email(keys['vvs']['email_1'])
content = Content("text/plain", output)
mail = Mail(from_email, subject, to_email, content)
response = sg.client.mail.send.post(request_body=mail.get())


