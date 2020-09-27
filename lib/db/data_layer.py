# Copyright (C) 2020 Andy Koch - All Rights Reserved

import logging
import os
from typing import Optional, Generator
from urllib.parse import quote_plus

from pymongo import MongoClient
from pymongo.client_session import ClientSession
from pymongo.errors import ConnectionFailure
from pymongo.results import InsertOneResult, UpdateResult
from tenacity import retry, TryAgain, stop_after_delay, wait_random, wait_fixed, RetryError

_logger = logging.getLogger(__name__)


@retry(wait=wait_fixed(3) + wait_random(0, 2), stop=stop_after_delay(90))
def configure_client(server: str = None, port: str = None, user: str = None, password: str = None) -> Optional[MongoClient]:
    # todo: use dynaconf lib!
    # todo: set app name param in client!

    # region check for defaults
    if server is None:
        server = os.getenv('MONGODB_SERVER')
    if port is None:
        port = os.getenv('MONGODB_PORT')
    if user is None:
        user = quote_plus(os.getenv('MONGODB_USER'))
    if password is None:
        password = quote_plus(os.getenv('MONGODB_PASS'))
    # endregion

    uri = f'mongodb://{user}:{password}@{server}:{port}'
    client = MongoClient(uri, serverSelectionTimeoutMS=3000)

    try:
        client.admin.command('ismaster')
    except ConnectionFailure:
        _logger.exception(f'Connecting to db server: "{server}:{port}" failed!')
        raise TryAgain
    else:
        return client


def find_documents(db_name: str, collection_name: str, query: Optional[dict] = None, projection: Optional[dict] = None) -> Generator[dict, None, None]:
    _logger.info(f'Searching for documents '
                 f'in db: "{db_name}/{collection_name}" '
                 f'by query: "{query}" '
                 f'by projection: "{projection}"..')

    try:
        client = configure_client()
    except RetryError:
        _logger.exception(f'Tried to connect multiple times, surrendering now!')
    else:
        db = client[db_name]
        collection = db[collection_name]

        with client.start_session() as session:
            cursor = collection.find(query, projection, no_cursor_timeout=True, session=session)

            for document in cursor:
                yield document

                _refresh_session(client, session)

            cursor.close()


def _refresh_session(client: MongoClient, session: ClientSession):
    _logger.info(f'Refreshing db session..')
    client.admin.command('refreshSessions', [session.session_id], session=session)


def find_document(db_name: str, collection_name: str, query: Optional[dict] = None, projection: Optional[dict] = None) -> dict:
    # todo: implement (without session)
    raise NotImplementedError


def insert_document(db_name: str, collection_name: str, document: dict) -> InsertOneResult:
    # todo: implement (without session, with transaction)
    raise NotImplementedError


def update_document(db_name: str, collection_name: str, query: Optional[dict] = None, update: Optional[dict] = None) -> UpdateResult:
    # todo: implement (without session, with transaction)
    raise NotImplementedError
