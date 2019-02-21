from twilio.rest import Client

def send_msg(text):

    act_sid = "AC036f1a9ceb42f28e68e1ceb9a45e31de"
    autho_token = "e5337a7bc963f6e7af386433a6314a9c"

    twilio_no = "+19202801868"

    client = Client(act_sid, autho_token)

    message = client.messages.create(body=text,
                                     from_=twilio_no,
                                     to="+639772452907",
                                     )

