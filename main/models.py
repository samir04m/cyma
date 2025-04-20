from django.db import models

class Questionnaire(models.Model):
    name = models.CharField(max_length=200)
    value1 = models.IntegerField()
    value2 = models.IntegerField()
    value3 = models.IntegerField()
    value4 = models.IntegerField()
    value5 = models.IntegerField()
    value6 = models.IntegerField()
    value7 = models.IntegerField()
    value8 = models.IntegerField()
    value9 = models.IntegerField()
    value10 = models.IntegerField()
    value11 = models.IntegerField()
    value12 = models.IntegerField()
    value13 = models.IntegerField()
    value14 = models.IntegerField()
    value15 = models.IntegerField()
    value16 = models.IntegerField()
    value17 = models.IntegerField()
    value18 = models.IntegerField()
    value19 = models.IntegerField()
    value20 = models.IntegerField()
    value21 = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def getDepressionScore(self):
        return sum([self.value3, self.value5, self.value10, self.value13, self.value16, self.value17, self.value21])

    def getAnxietyScore(self):
        return sum([self.value2, self.value4, self.value7, self.value9, self.value15, self.value19, self.value20])

    def getStressScore(self):
        return sum([self.value1, self.value6, self.value8, self.value11, self.value12, self.value14, self.value18])

    def getGlobalScore(self):
        return self.getDepressionScore() + self.getAnxietyScore() + self.getStressScore()


