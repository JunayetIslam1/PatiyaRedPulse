# Generated manually for patient condition field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blood_requests', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloodrequest',
            name='patient_condition',
            field=models.CharField(choices=[('Stable', 'Stable'), ('Critical', 'Critical'), ('Life Threatening', 'Life Threatening'), ('Surgery', 'Surgery'), ('Accident', 'Accident'), ('Maternity', 'Maternity'), ('Other', 'Other')], default='Stable', max_length=20),
        ),
    ]