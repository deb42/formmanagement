from .models import *

def init_reply(answers, type, patient):
    if type == 0:
        hadsresult = Hads(
            patient=patient,
            date="123",
            data=answers,
            anxiety_scale=1,
            depression_scale=1
        )
        return  hadsresult