# Generated by Django 3.2.4 on 2021-10-08 15:03

import json
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


def convert_variables_to_reduction_arguments(apps, _):
    ReductionRun = apps.get_model("reduction_viewer", "ReductionRun")
    ReductionArguments = apps.get_model("reduction_viewer", "ReductionArguments")

    for run in ReductionRun.objects.all():
        arguments_dict = {}
        arguments_dict["standard_vars"] = {}
        arguments_dict["advanced_vars"] = {}
        arguments_dict["variable_help"] = {
            "standard_vars": {},
            "advanced_vars": {},
        }
        for run_variable in run.run_variables.all():
            var = run_variable.variable
            if not var.is_advanced:
                key = "standard_vars"
            else:
                key = "advanced_vars"
            arguments_dict[key][var.name] = var.value
            arguments_dict["variable_help"][key][var.name] = var.help_text

        arguments_json = json.dumps(arguments_dict, separators=(',', ':'))
        arguments, created = ReductionArguments.objects.get_or_create(raw=arguments_json,
                                                                      start_run=None,
                                                                      experiment_reference=None,
                                                                      instrument=run.instrument)
        run.arguments = arguments
        run.save()


class Migration(migrations.Migration):

    dependencies = [
        ('reduction_viewer', '0010_move_script_into_reductionscript'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReductionArguments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('raw', models.TextField(validators=[django.core.validators.MaxLengthValidator(100000)])),
                ('start_run', models.IntegerField(null=True, blank=True)),
                ('experiment_reference', models.IntegerField(null=True, blank=True)),
                ('instrument', models.ForeignKey('Instrument', on_delete=models.CASCADE, related_name="arguments")),
            ],
        ),
        migrations.AddField(
            model_name='reductionrun',
            name='arguments',
            field=models.ForeignKey(null=True,
                                    on_delete=django.db.models.deletion.CASCADE,
                                    related_name='reduction_runs',
                                    to='reduction_viewer.reductionarguments'),
        ),
        migrations.RunPython(convert_variables_to_reduction_arguments),
        migrations.AlterField(model_name='reductionrun',
                              name='arguments',
                              field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                      related_name='reduction_runs',
                                                      to='reduction_viewer.reductionarguments',
                                                      null=False)),
    ]
