# Generated by Django 3.1.1 on 2020-11-08 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataprocessor', '0010_flowcell_qc_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='samplesrundata',
            name='sample_id',
            field=models.CharField(help_text='SampleID', max_length=20),
        ),
    ]
