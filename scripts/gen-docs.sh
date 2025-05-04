#!/usr/bin/env bash
set -euo pipefail

# Directorio de destino de los MD
DST=docs

# Lista de módulos a documentar
MODULES=(
  crmsync.syncer.syncer
  crmsync.syncer.assembler.policy_assembler
  crmsync.syncer.assembler.core.pipeline
  crmsync.syncer.assembler.core.step
  crmsync.syncer.assembler.factories.base
  crmsync.syncer.assembler.factories.address
  crmsync.syncer.assembler.factories.bank_account
  crmsync.syncer.assembler.factories.contact
  crmsync.syncer.assembler.factories.customer
  crmsync.syncer.assembler.factories.item
  crmsync.syncer.assembler.factories.salesorder
  crmsync.syncer.assembler.handlers.address
  crmsync.syncer.assembler.handlers.bank_account
  crmsync.syncer.assembler.handlers.base
  crmsync.syncer.assembler.handlers.contact
  crmsync.syncer.assembler.handlers.customer
  crmsync.syncer.assembler.handlers.item
  crmsync.syncer.assembler.handlers.salesorder
  crmsync.syncer.assembler.linkers.address
  crmsync.syncer.assembler.linkers.base
  crmsync.syncer.assembler.linkers.contact
  crmsync.syncer.assembler.linkers.document
  crmsync.syncer.assembler.resolvers.simple_name
  crmsync.syncer.utils.comparator
  crmsync.syncer.utils.entry_parser_doc_simple
  crmsync.syncer.utils.entry_parser_doc
  crmsync.syncer.utils.entry_parser_issue

  crmsync.database.base
  crmsync.database.engine
  crmsync.database.unit_of_work
  crmsync.database.models.vtigercrm_contactcf
  crmsync.database.models.vtigercrm_contactdetails
  crmsync.database.models.vtigercrm_crmentity
  crmsync.database.models.vtigercrm_salesorder
  crmsync.database.models.vtigercrm_salesordercf
  crmsync.database.models.vtigercrm_ticketcf
  crmsync.database.models.vtigercrm_troubletickets
  crmsync.database.services.query
)

echo "Generating docs into $DST …"

for mod in "${MODULES[@]}"; do
  # Convierte punto a slash y añade .md
  out_file="$DST/${mod//./\/}.md"
  mkdir -p "$(dirname "$out_file")"
  {
    # Título del módulo
    echo "# ${mod##*.}"
    # Genera el Markdown con TOC
    pydoc-markdown -I . -m "$mod" --render-toc
  } > "$out_file"
  echo "  ✓ $out_file"
done

echo "Done!"
