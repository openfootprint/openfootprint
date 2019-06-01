# Generated by Django 2.2.1 on 2019-06-01 10:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('source_name', models.CharField(db_index=True, max_length=250, verbose_name='Name')),
                ('source_country', models.CharField(db_index=True, max_length=2, verbose_name='Country')),
                ('latitude', models.FloatField(blank=True, null=True, verbose_name='Latitude')),
                ('longitude', models.FloatField(blank=True, null=True, verbose_name='Longitude')),
                ('country', models.CharField(blank=True, max_length=2, null=True, verbose_name='Country')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('kind', models.CharField(choices=[('employee', 'Employee'), ('attendee', 'Attendee'), ('other', 'Other')], default='other', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('slug', models.SlugField(max_length=100, verbose_name='Slug')),
                ('kind', models.CharField(choices=[('company', 'Company'), ('event', 'Event'), ('household', 'Household')], default='company', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='core.Project')),
            ],
        ),
        migrations.CreateModel(
            name='TransportMode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
            ],
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Name')),
                ('area', models.FloatField(blank=True, null=True)),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='core.Location')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='venues', to='core.Project')),
                ('tags', models.ManyToManyField(to='core.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='TransportStep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('from_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='core.Location')),
                ('mode', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.TransportMode')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transportsteps', to='core.Project')),
                ('to_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='core.Location')),
                ('transport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transportsteps', to='core.TransportMode')),
            ],
        ),
        migrations.CreateModel(
            name='Transport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Name')),
                ('roundtrip', models.BooleanField(default=True)),
                ('frequency', models.CharField(choices=[('none', 'N times'), ('workday', 'Every work day'), ('perweek', 'N per week'), ('permonth', 'N per month'), ('peryear', 'N per year')], default='none', max_length=30)),
                ('frequency_n', models.IntegerField(default=1)),
                ('weight', models.FloatField(default=1.0)),
                ('done_at', models.DateTimeField(blank=True, null=True)),
                ('return_at', models.DateTimeField(blank=True, null=True)),
                ('from_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='core.Location')),
                ('person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Person')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transports', to='core.Project')),
                ('tags', models.ManyToManyField(to='core.Tag')),
                ('to_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='core.Location')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='main_venue',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='core.Venue'),
        ),
        migrations.AddField(
            model_name='person',
            name='main_venue',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='persons', to='core.Venue'),
        ),
        migrations.AddField(
            model_name='person',
            name='origin_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.Location'),
        ),
        migrations.AddField(
            model_name='person',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='persons', to='core.Project'),
        ),
        migrations.AddField(
            model_name='person',
            name='tags',
            field=models.ManyToManyField(to='core.Tag'),
        ),
        migrations.CreateModel(
            name='Footprint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('version', models.CharField(max_length=50, verbose_name='CR version')),
                ('footprint', models.FloatField(blank=True, null=True, verbose_name='Footprint in gCO2e')),
                ('raw_json', models.TextField(verbose_name='Raw JSON')),
                ('starts_at', models.DateTimeField(blank=True, null=True)),
                ('ends_at', models.DateTimeField(blank=True, null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='footprints', to='core.Project')),
            ],
        ),
        migrations.CreateModel(
            name='Extra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Name')),
                ('kind', models.CharField(choices=[('co2e', 'Raw CO2e in g'), ('wh', 'Watt hours')], default='co2e', max_length=30)),
                ('param_f1', models.FloatField(blank=True, null=True)),
                ('param_f2', models.FloatField(blank=True, null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='extras', to='core.Project')),
                ('tags', models.ManyToManyField(blank=True, to='core.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='DataPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('wh', models.FloatField()),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='powerdatapoints', to='core.Project')),
                ('venue', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='core.Venue')),
            ],
        ),
    ]