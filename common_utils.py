from urllib.parse import quote
from django.core.mail import EmailMultiAlternatives
import urllib.request as urllib2


def send_sms(contact_no, msg_body):
    try:
        quoted_text = quote(msg_body)
        sms_url = 'http://api.bizsms.pk/api-send-branded-sms.aspx?username=pnd@bizsms.pk&pass=p5890hg99&text=' + \
                  quoted_text + '&masking=P&DD-FERRP&destinationnum=' + contact_no + '&language=English'
        response = urllib2.urlopen(sms_url)
        html = response.msg
        if html == 'OK':
            return 'SMS sent!'
        else:
            return 'SMS not sent!'
    except Exception as e:
        return e


# msg body accepts plain text and html also
def send_email(email_id, subject, msg_body):
    try:
        msg = EmailMultiAlternatives(subject, msg_body, None, [email_id])
        msg.attach_alternative(msg_body, "text/html")
        msg.send()
        return {"Email sent."}
    except Exception as e:
        return e
