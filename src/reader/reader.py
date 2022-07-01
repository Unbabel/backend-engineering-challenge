from decimal import *

import pandas as pd
import pandas_schema
from pandas_schema import Column
from pandas_schema.validation import CustomElementValidation

decimal_validation = [CustomElementValidation(lambda d: _check_decimal(d), 'is not decimal')]
int_validation = [CustomElementValidation(lambda i: _check_int(i), 'is not integer')]
null_validation = [CustomElementValidation(lambda d: d is not None, 'this field cannot be null')]


def do_validation(df: pd.DataFrame) -> pd.DataFrame:
    schema = pandas_schema.Schema([
        Column('timestamp', null_validation),
        Column('translation_id', null_validation),
        Column('source_language', null_validation),
        Column('target_language', null_validation),
        Column('client_name', null_validation),
        Column('event_name', null_validation),
        Column('duration', int_validation + null_validation),
        Column('nr_words', int_validation + null_validation),
    ])

    errors = schema.validate(df)

    errors_index_rows = [e.row for e in errors]
    data_clean = df.drop(index=errors_index_rows)
    pd.DataFrame({'col': errors}).to_json('files/errors.json')
    return data_clean


def read(input_file: str) -> pd.DataFrame:
    df = pd.read_json(input_file)
    data_clean = do_validation(df)
    return data_clean


def _check_decimal(dec) -> bool:
    try:
        Decimal(dec)
    except InvalidOperation:
        return False
    return True


def _check_int(num) -> bool:
    try:
        int(num)
    except ValueError:
        return False
    return True
