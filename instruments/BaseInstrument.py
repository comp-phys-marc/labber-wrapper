import json
from jsonschema import validate, ValidationError


class BaseInstrument:

    def __init__(self, name, address, client, schema, to_validate=True):
        self.client = client
        self.instr = self.client.connectToInstrument(name, address)

        self.schema = json.loads(schema)
        self.config = self.instr.getLocalInitValuesDict()

        if to_validate:

            # check that the provided schema matches the provided device definition
            validate(schema=self.schema, instance=self.config)

    def set_value(self, key, val, validating=False):
        previous = self.config[key]
        self.config[key] = val

        # check that the proposed change is compliant with the schema
        try:
            if validating:
                validate(schema=self.schema, instance=self.config)
            self.instr.setValue(key, val)
        except ValidationError as e:
            # gracefully recover from errors i.e. trying to set voltages too high
            self.config[key] = previous
            print(str(e))
