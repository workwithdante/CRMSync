# CRMSync


[![pypi](https://img.shields.io/pypi/v/crmsync.svg)](https://pypi.org/project/crmsync/)
[![python](https://img.shields.io/pypi/pyversions/crmsync.svg)](https://pypi.org/project/crmsync/)
[![Build Status](https://github.com/mabecenter-it/crmsync/actions/workflows/dev.yml/badge.svg)](https://github.com/mabecenter-it/crmsync/actions/workflows/dev.yml)
[![codecov](https://codecov.io/gh/mabecenter-it/crmsync/branch/main/graphs/badge.svg)](https://codecov.io/github/mabecenter-it/crmsync)



Skeleton project created by Cookiecutter PyPackage for mabecenter


* Documentation: <https://mabecenter-it.github.io/crmsync>
* GitHub: <https://github.com/mabecenter-it/crmsync>
* PyPI: <https://pypi.org/project/crmsync/>
* Free software: MIT


## Features

* TODO

## Documentation Catalog

### General

*   [API Reference](docs/api.md)
*   [Changelog](docs/changelog.md)
*   [Contributing](docs/contributing.md)
*   [Index](docs/index.md)
*   [Installation](docs/installation.md)
*   [Usage](docs/usage.md)

### crmsync.database

*   [Base](docs/crmsync/database/base.md)
*   [Engine](docs/crmsync/database/engine.md)
*   [Unit of Work](docs/crmsync/database/unit_of_work.md)

### crmsync.database.models

*   [ContactCF](docs/crmsync/database/models/vtigercrm_contactcf.md)
*   [ContactDetails](docs/crmsync/database/models/vtigercrm_contactdetails.md)
*   [Crmentity](docs/crmsync/database/models/vtigercrm_crmentity.md)
*   [Salesorder](docs/crmsync/database/models/vtigercrm_salesorder.md)
*   [SalesorderCF](docs/crmsync/database/models/vtigercrm_salesordercf.md)
*   [TicketCF](docs/crmsync/database/models/vtigercrm_ticketcf.md)
*   [Troubletickets](docs/crmsync/database/models/vtigercrm_troubletickets.md)

### crmsync.database.services

*   [Query](docs/crmsync/database/services/query.md)

### crmsync.syncer

*   [Syncer](docs/crmsync/syncer/syncer.md)

### crmsync.syncer.assembler

*   [Policy Assembler](docs/crmsync/syncer/assembler/policy_assembler.md)

### crmsync.syncer.assembler.core

*   [Pipeline](docs/crmsync/syncer/assembler/core/pipeline.md)
*   [Step](docs/crmsync/syncer/assembler/core/step.md)

### crmsync.syncer.assembler.factories

*   [Address](docs/crmsync/syncer/assembler/factories/address.md)
*   [Bank Account](docs/crmsync/syncer/assembler/factories/bank_account.md)
*   [Base](docs/crmsync/syncer/assembler/factories/base.md)
*   [Contact](docs/crmsync/syncer/assembler/factories/contact.md)
*   [Customer](docs/crmsync/syncer/assembler/factories/customer.md)
*   [Item](docs/crmsync/syncer/assembler/factories/item.md)
*   [Salesorder](docs/crmsync/syncer/assembler/factories/salesorder.md)

### crmsync.syncer.assembler.handlers

*   [Address](docs/crmsync/syncer/assembler/handlers/address.md)
*   [Bank Account](docs/crmsync/syncer/assembler/handlers/bank_account.md)
*   [Base](docs/crmsync/syncer/assembler/handlers/base.md)
*   [Contact](docs/crmsync/syncer/assembler/handlers/contact.md)
*   [Customer](docs/crmsync/syncer/assembler/handlers/customer.md)
*   [Item](docs/crmsync/syncer/assembler/handlers/item.md)
*   [Salesorder](docs/crmsync/syncer/assembler/handlers/salesorder.md)

### crmsync.syncer.assembler.linkers

*   [Address](docs/crmsync/syncer/assembler/linkers/address.md)
*   [Base](docs/crmsync/syncer/assembler/linkers/base.md)
*   [Contact](docs/crmsync/syncer/assembler/linkers/contact.md)
*   [Document](docs/crmsync/syncer/assembler/linkers/document.md)

### crmsync.syncer.assembler.resolvers

*   [Simple Name](docs/crmsync/syncer/assembler/resolvers/simple_name.md)

### crmsync.syncer.utils

*   [Comparator](docs/crmsync/syncer/utils/comparator.md)
*   [Entry Parser Doc Simple](docs/crmsync/syncer/utils/entry_parser_doc_simple.md)
*   [Entry Parser Doc](docs/crmsync/syncer/utils/entry_parser_doc.md)
*   [Entry Parser Issue](docs/crmsync/syncer/utils/entry_parser_issue.md)

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) project template.
