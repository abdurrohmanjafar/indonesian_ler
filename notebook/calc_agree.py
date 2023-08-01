import json
from nltk import agreement

with open(f'agree-data/fariz.res.json', 'r', encoding="utf8") as a1:
    with open(f'agree-data/jafar.res.json', 'r', encoding="utf8") as a2:
        with open(f'agree-data/admin.res.json', 'r', encoding="utf8") as a3:
            rater1 = []
            for ln in a1:
                data = json.loads(ln)
                rater1.extend(data['text-tags'])
            rater2 = []
            for ln in a2:
                data = json.loads(ln)
                rater2.extend(data['text-tags'])
            rater3 = []
            for ln in a3:
                data = json.loads(ln)
                rater3.extend(data['text-tags'])

            taskdata = [[0, str(i), str(rater1[i])] for i in range(0, len(rater1))] + \
                       [[1, str(i), str(rater2[i])] for i in range(0, len(rater2))] + \
                       [[2, str(i), str(rater3[i])] for i in range(0, len(rater3))]
            ratingtask = agreement.AnnotationTask(data=taskdata)
            print("fleiss " + str(ratingtask.multi_kappa()))
