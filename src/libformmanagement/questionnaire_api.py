from .models import *
from datetime import date


def anxiety_scale(answers, value):
    anxiety_scale = 0
    for i in range(0,answers.__len__(),2):
        print(value[i][int(answers[i])])
        anxiety_scale += int(value[i][int(answers[i])])
    print(anxiety_scale)
    return anxiety_scale


def depression_scale(answers, value):
    depression_scale = 0
    for i in range(1,answers.__len__(),2):
        depression_scale += int(value[i][int(answers[i])])
    return depression_scale


def init_reply(answers, type, patient, value):
    if type == 0:
        hadsresult = Hads(
            patient=patient,
            date=date.today(),
            data=answers,
            anxiety_scale=anxiety_scale(answers, value),
            depression_scale=depression_scale(answers, value)
        )
        return  hadsresult

