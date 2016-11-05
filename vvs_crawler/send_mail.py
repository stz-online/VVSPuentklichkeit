import subprocess
import sendgrid
from YamJam import yamjam


keys = yamjam("keys.yaml")

output = subprocess.Popen(["psql", "-U","postgres","-d","vvs_crawler", "-c", "Select * FROM get_highest_n_delays('2016-10-01', '2016-10-20', 20);"],
                          stdout=subprocess.PIPE).communicate()
subject = "VVS Report"
client = sendgrid.SendGridClient(keys['sendgrid']['key'])
message = sendgrid.Mail()

message.add_to(keys['vvs']['email_1'])
message.set_from(keys['vvs']['from_mail'])
message.set_subject("VVS Report")
message.set_html(output)

client.send(message)




