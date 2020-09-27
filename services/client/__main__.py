# Copyright (C) 2020 Andy Koch - All Rights Reserved

from lib.db.data_layer import find_documents
from lib.logging.root_logger import get_root_logger

_logger = get_root_logger()


def main():
    db_name = 'local'
    collection_name = 'startup_log'

    for document in find_documents(db_name, collection_name):
        _logger.info(f'document id: {document.get("_id")}')

    # todo: show GridFS example


if __name__ == '__main__':
    main()
