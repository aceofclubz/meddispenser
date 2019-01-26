# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Admin(models.Model):
    adminid = models.AutoField(db_column='adminID', primary_key=True)  # Field name made lowercase.
    adminuser = models.CharField(db_column='adminUser', max_length=45)  # Field name made lowercase.
    adminpass = models.CharField(db_column='adminPass', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'admin'


class Medicine(models.Model):
    mid = models.AutoField(primary_key=True)
    medname = models.CharField(db_column='medName', max_length=45, blank=True, null=True)  # Field name made lowercase.
    count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'medicine'


class Transaction(models.Model):
    tid = models.AutoField(primary_key=True)
    medid = models.ForeignKey(Medicine, models.DO_NOTHING, db_column='medID', blank=True, null=True)  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userID', blank=True, null=True)  # Field name made lowercase.
    datetime = models.DateTimeField(blank=True, null=True)
    presentcount = models.IntegerField(db_column='presentCount', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'transaction'


class User(models.Model):
    uid = models.CharField(primary_key=True, max_length=43)
    fn = models.CharField(max_length=45, blank=True, null=True)
    ln = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'
