import jsonschema

FileSchema = {
    "type": "array",
    "items": {
        "oneOf": [
            {
                "timestamp": {"type": "timestamp"},
                "translation_id": {"type": "string"},
                "source_language": {"type": "string"},
                "target_language": {"type": "string"},
                "client_name": {"type": "string"},
                "event_name": {"type": "string"},
                "nr_words": {"type": "integer"},
                "duration": {"type": "integer"},
            }
        ]
    }
}


def validation_json_schema(json):
    try:
        jsonschema.validate(json, FileSchema)
    except:
        print(f"JSON schema corrupted")
        return None
    return json
