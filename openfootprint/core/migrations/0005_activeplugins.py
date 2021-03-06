# Generated by Django 2.2.1 on 2019-08-12 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("core", "0004_address_status")]

    operations = [
        migrations.CreateModel(
            name="ActivePlugins",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, verbose_name="Name")),
                (
                    "settings",
                    models.TextField(
                        blank=True, null=True, verbose_name="JSON settings"
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="active_plugins",
                        to="core.Project",
                    ),
                ),
            ],
        )
    ]
