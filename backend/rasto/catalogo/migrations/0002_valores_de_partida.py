"""Valores de partida do catálogo e da compatibilidade. Configuráveis no admin interno (D-04, D-05).
Sectores: lista de partida [S], a validar com a hipótese H-04. Províncias: divisão administrativa recente (21)
[CONFIRMAR lista oficial]. Fases: base de UX (Ideia, Pré-seed, Seed, Série A ou mais)."""

from django.db import migrations

SECTORES = ["Agritech", "Fintech", "Edtech", "Healthtech", "E-commerce e retalho", "Logística e mobilidade",
            "Energia e ambiente", "Software e serviços para empresas", "Media e entretenimento", "Outro"]
FASES = [("ideia", "Ideia", "Ainda sem produto"), ("pre_seed", "Pré-seed", "Produto inicial e primeiros clientes"),
         ("seed", "Seed", "Receita recorrente e equipa a crescer"), ("serie_a", "Série A ou mais", "Crescimento comprovado")]
PROVINCIAS = [("BGO", "Bengo"), ("BGU", "Benguela"), ("BIE", "Bié"), ("CAB", "Cabinda"), ("CDO", "Cuando"),
              ("CBG", "Cubango"), ("CNO", "Cuanza Norte"), ("CUS", "Cuanza Sul"), ("CNN", "Cunene"), ("HUA", "Huambo"),
              ("HUI", "Huíla"), ("ICB", "Icolo e Bengo"), ("LUA", "Luanda"), ("LNO", "Lunda Norte"), ("LSU", "Lunda Sul"),
              ("MAL", "Malanje"), ("MOX", "Moxico"), ("MXL", "Moxico Leste"), ("NAM", "Namibe"), ("UIG", "Uíge"),
              ("ZAI", "Zaire")]
RISCOS = [("baixo", "Baixo"), ("medio", "Médio"), ("alto", "Alto")]


def semear(apps, schema_editor):
    Item = apps.get_model("catalogo", "ItemCatalogo")
    for i, nome in enumerate(SECTORES):
        codigo = nome.lower().split(" ")[0].replace("-", "")
        Item.objects.update_or_create(tipo="sector", codigo=codigo, defaults={"nome": nome, "ordem": i})
    for i, (codigo, nome, descricao) in enumerate(FASES, start=1):
        Item.objects.update_or_create(tipo="fase", codigo=codigo, defaults={"nome": nome, "ordem": i, "descricao": descricao})
    Item.objects.update_or_create(tipo="geografia", codigo="AO", defaults={"nome": "Angola (todas as províncias)", "ordem": 0})
    for i, (codigo, nome) in enumerate(PROVINCIAS, start=1):
        Item.objects.update_or_create(tipo="geografia", codigo=codigo, defaults={"nome": nome, "ordem": i})
    for i, (codigo, nome) in enumerate(RISCOS, start=1):
        Item.objects.update_or_create(tipo="risco", codigo=codigo, defaults={"nome": nome, "ordem": i})
    Config = apps.get_model("compatibilidade", "ConfiguracaoCompatibilidade")
    if not Config.objects.exists():
        Config.objects.create(versao=1, activa=True, nota="Valores de partida (base de UX 6.5): 40/25/25/10, risco 0.")


class Migration(migrations.Migration):
    dependencies = [("catalogo", "0001_initial"), ("compatibilidade", "0001_initial")]
    operations = [migrations.RunPython(semear, migrations.RunPython.noop)]
