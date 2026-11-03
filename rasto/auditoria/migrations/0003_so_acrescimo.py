from django.db import migrations

# O registo de auditoria só aceita INSERT (ADR-09, base técnica 4.2). O trigger recusa UPDATE e DELETE
# mesmo vindos da própria aplicação. TRUNCATE também é recusado.
SQL = """
CREATE OR REPLACE FUNCTION auditoria_so_acrescimo() RETURNS trigger AS $$
BEGIN
    RAISE EXCEPTION 'O registo de auditoria só aceita acréscimos (% recusado).', TG_OP;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER auditoria_sem_alteracao
    BEFORE UPDATE OR DELETE ON auditoria_registoauditoria
    FOR EACH ROW EXECUTE FUNCTION auditoria_so_acrescimo();

CREATE TRIGGER auditoria_sem_truncate
    BEFORE TRUNCATE ON auditoria_registoauditoria
    FOR EACH STATEMENT EXECUTE FUNCTION auditoria_so_acrescimo();
"""

REVERSO = """
DROP TRIGGER IF EXISTS auditoria_sem_alteracao ON auditoria_registoauditoria;
DROP TRIGGER IF EXISTS auditoria_sem_truncate ON auditoria_registoauditoria;
DROP FUNCTION IF EXISTS auditoria_so_acrescimo();
"""


class Migration(migrations.Migration):
    dependencies = [("auditoria", "0002_initial")]
    operations = [migrations.RunSQL(SQL, REVERSO)]
