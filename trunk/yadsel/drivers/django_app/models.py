from django.db import models

class YadselHistory(models.Model):
    version_number = models.IntegerField()
    change_date = models.DateTimeField()
    errors = models.IntegerField(default=0, blank=True)

    def __unicode__(self):
        return "%d - %s" %(self.version_number, self.change_date)

    class Admin:
        pass

class YadselLog(models.Model):
    version_number = models.IntegerField()
    log_date = models.DateTimeField()
    msg = models.TextField()

    def __unicode__(self):
        return "%d - %s" %(self.version_number, self.log_date)

    class Admin:
        pass

