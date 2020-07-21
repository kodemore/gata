from typing import Any, Dict, Optional, Union

from .errors import FormatValidationError
from .base_mapping import Mapping
from .stringformat import StringFormat

BSON_SUPPORT = True


try:
    import bson
except ImportError:
    BSON_SUPPORT = False


if BSON_SUPPORT:

    def validate_object_id(value: Any) -> bson.ObjectId:
        try:
            return bson.ObjectId(value)
        except Exception:
            raise FormatValidationError(expected_format=StringFormat.OBJECT_ID)

    class ObjectIdMapping(Mapping):
        def validate(self, value: Any) -> Any:
            return validate_object_id(value)

        def serialise(self, value: Any, mapping: Optional[Dict[str, Union[Dict, str, bool]]] = None) -> Any:
            return str(value)

        def deserialise(self, value: Any) -> Any:
            return bson.ObjectId(value)
