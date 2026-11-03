from django.db import migrations

PAPEIS = [
    ("startup", "Startup"),
    ("investidor", "Investidor"),
    ("entidade", "Entidade validadora"),
    ("admin", "Administração"),
]


def semear(apps, schema_editor):
    Papel = apps.get_model("contas", "Papel")
    for codigo, nome in PAPEIS:
        Papel.objects.update_or_create(codigo=codigo, defaults={"nome": nome})


class Migration(migrations.Migration):
    dependencies = [("contas", "0001_initial")]
    operations = [migrations.RunPython(semear, migrations.RunPython.noop)]
