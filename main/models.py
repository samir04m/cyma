from django.contrib.auth import get_user_model
from django.db import models

class Questionnaire(models.Model):
    name = models.CharField(max_length=200)
    ipAddress = models.CharField(max_length=100, db_index=True)
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
    depressionScore = models.IntegerField(default=0)
    anxietyScore = models.IntegerField(default=0)
    stressScore = models.IntegerField(default=0)
    globalScore = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        self.depressionScore = self.getDepressionScore()
        self.anxietyScore = self.getAnxietyScore()
        self.stressScore = self.getStressScore()
        self.globalScore = self.getGlobalScore()
        super().save(*args, **kwargs)

    def getDepressionScore(self):
        return sum([self.value3, self.value5, self.value10, self.value13, self.value16, self.value17, self.value21])

    def getAnxietyScore(self):
        return sum([self.value2, self.value4, self.value7, self.value9, self.value15, self.value19, self.value20])

    def getStressScore(self):
        return sum([self.value1, self.value6, self.value8, self.value11, self.value12, self.value14, self.value18])

    def getGlobalScore(self):
        return self.getDepressionScore() + self.getAnxietyScore() + self.getStressScore()

class RegistrationToken(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    token = models.CharField(max_length=6, unique=True, db_index=True)
    active = models.BooleanField(default=True, db_index=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    user_registration_date = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['-creation_date']
        
    def __str__(self):
        return f"{self.name} - {self.token} - {self.active}"

class QueryTimeLog(models.Model):
    description = models.CharField(max_length=250)
    query_id = models.IntegerField(db_index=True)
    results_count = models.IntegerField(db_index=True)
    milliseconds = models.FloatField()
    query_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-query_time']

    def __str__(self):
        return f"{self.description} - {self.results_count} - {self.milliseconds} - {self.query_time}"
