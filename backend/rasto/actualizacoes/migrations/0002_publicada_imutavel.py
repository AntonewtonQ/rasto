from django.db import migrations

# Actualização publicada não muda (base técnica 4.2, OWASP A08): o trigger recusa UPDATE de uma linha publicada.
# DELETE continua possível para a eliminação de dados a pedido do titular (RF35), que apaga a startup inteira.
SQL = """
CREATE OR REPLACE FUNCTION actualizacao_publicada_imutavel() RETURNS trigger AS $$
BEGIN
    IF OLD.estado = 'publicada' THEN
        RAISE EXCEPTION 'Uma actualização publicada não se altera; publique uma correcção.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER actualizacao_sem_alteracao
    BEFORE UPDATE ON actualizacoes_actualizacao
    FOR EACH ROW EXECUTE FUNCTION actualizacao_publicada_imutavel();
"""

REVERSO = """
DROP TRIGGER IF EXISTS actualizacao_sem_alteracao ON actualizacoes_actualizacao;
DROP FUNCTION IF EXISTS actualizacao_publicada_imutavel();
"""


class Migration(migrations.Migration):
    dependencies = [("actualizacoes", "0001_initial")]
    operations = [migrations.RunSQL(SQL, REVERSO)]
