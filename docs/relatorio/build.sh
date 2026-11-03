#!/usr/bin/env bash
# Gera docs/relatorio/TCC_Rasto.docx a partir de src/ (fonte da verdade). Correr a partir da pasta docs/relatorio/.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p build
python3 src/build.py modelo/tcc_exemplo.docx build/pass1.docx
if command -v soffice >/dev/null 2>&1; then
  # 2.ª passagem: números de página reais no índice e nas listas
  soffice --headless --convert-to pdf --outdir build build/pass1.docx >/dev/null 2>&1
  python3 src/pages.py build/pass1.pdf
  python3 src/build.py modelo/tcc_exemplo.docx build/pass2.docx build/pages.json
  python3 src/prune.py build/pass2.docx TCC_Rasto.docx
  soffice --headless --convert-to pdf --outdir build TCC_Rasto.docx >/dev/null 2>&1
  echo "PDF de verificação: build/TCC_Rasto.pdf"
else
  python3 src/prune.py build/pass1.docx TCC_Rasto.docx
  echo "LibreOffice não encontrado: o índice fica com 0; o Word actualiza-o ao abrir (aceitar 'actualizar campos')."
fi
echo "Gerado: docs/relatorio/TCC_Rasto.docx"
