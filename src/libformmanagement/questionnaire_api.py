from .models import *
from datetime import date



def anxiety_scale(answers, value):
    anxiety_scale = 0
    for i in range(0,answers.__len__(),2):
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



def pbi_score(answers, value, id):
    pbiNew = PbiNew.query.filter_by(patient_id=id).first_or_404()
    pbi_score = 0
    for i in range(0,answers.__len__()-1,1):
        pbi_score += int(value[i][int(answers[i])] - int(pbiNew.__getitem__("data")[i]))
    return pbi_score

def pbi_score_new(answers, value):
    pbi_score = 0
    for i in range(0,answers.__len__(),1):
        pbi_score += int(value[i][int(answers[i])])
    return pbi_score


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

    elif type == TYPE_PBI_FOLLOWUP:
        pbiFolloupResult = PbiFollowUp(
            patient=patient,
            date=date.today(),
            data=answers,
            score = pbi_score(answers, value, patient["id"])
        )
        return pbiFolloupResult

    elif type == TYPE_PBI_NEW:
        pbiNewResult = PbiNew(
            patient=patient,
            date=date.today(),
            data=answers,
            score = pbi_score_new(answers, value)
        )
        return pbiNewResult

    else: return 404

