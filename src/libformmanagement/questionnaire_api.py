from .models import *
from datetime import date



def anxiety_scale(answers, value):
    anxiety_scale = 0
    for i in range(0,answers.__len__(),2):
        print(int(value[i][int(answers[i])]))
        anxiety_scale += int(value[i][int(answers[i])])
    return anxiety_scale


def depression_scale(answers, value):
    depression_scale = 0
    for i in range(1,answers.__len__(),2):
        depression_scale += int(value[i][int(answers[i])])
    return depression_scale


def dlqi_score(answers, value):
    dlqi_score = 0
    for i in range(0,answers.__len__(),1):
        dlqi_score += int(value[i][int(answers[i])])
    return dlqi_score



def init_reply(answers, type, patient, value):
    if type == TYPE_HADS:
        hadsresult = Hads(
            patient=patient,
            date=date.today(),
            data=answers,
            anxiety_scale=anxiety_scale(answers, value),
            depression_scale=depression_scale(answers, value)
        )
        return  hadsresult

    elif type == TYPE_DLQI:
        dlqiresult = Dlqi(
            patient=patient,
            date=date.today(),
            data=answers,
            score=dlqi_score(answers, value)
        )
        return dlqiresult

    elif type == TYPE_PBI:
        pbiresult = Pbi(
            patient=patient,
            date=date.today(),
            data=answers,
        )
        return pbiresult

    else: return 404

