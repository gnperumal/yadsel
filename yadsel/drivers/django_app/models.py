from django.db import models

class YadselHistory(models.Model):
    version_number = models.IntegerField()
    change_date = models.DateTimeField()
    errors = models.IntegerField(default=0, blank=True)
    version_space = models.CharField(max_length=50, null=True, blank=True)

    def __unicode__(self):
        return "%d - %s" %(self.version_number, self.change_date)

    class Meta:
        db_table = 'yadsel_history'

    class Admin:
        pass

class YadselLog(models.Model):
    version_number = models.IntegerField()
    log_date = models.DateTimeField()
    msg = models.TextField()
    version_space = models.CharField(max_length=50, null=True, blank=True)

    def __unicode__(self):
        return "%d - %s" %(self.version_number, self.log_date)

    class Meta:
        db_table = 'yadsel_log'

    class Admin:
        pass

