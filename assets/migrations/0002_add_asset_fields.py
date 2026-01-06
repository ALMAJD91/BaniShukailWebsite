from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='category',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='asset',
            name='assigned_to',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='asset',
            name='purchase_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='status',
            field=models.CharField(
                choices=[('In use', 'In use'), ('Under maintenance', 'Under maintenance'), ('Retired', 'Retired')],
                default='In use',
                max_length=20
            ),
        ),
    ]
