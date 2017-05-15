DEFAULT_CONFIG = {
    "influxURL": "http://localhost:8086",
    "database": "load_testing",
    "min_wait": 1000,
    "max_wait": 3000,
    "readWeight": 1,
    "writeWeight": 50,
    "filename": "batchData.txt",
    "minBatchSize": 5000,
    "maxBatchSize": 10000,
    "numMeasurements": 1,
    "measurements": [],
    "minTags": 1,
    "maxTags": 1,
    "tags": [],
    "maxTagValueLength": 12,
    "minFields": 1,
    "maxFields": 1,
    "maxFieldStrValueLength": 12,
    "maxFieldNumericValue": 1000000,
    "maxDecimalValueLength": 3,
    "fields": [],
    "fieldTypeWeights": [{
        "string": 40
    },
        {
            "int": 25
        },
        {
            "float": 25
        },
        {
            "boolean": 10
        }
    ]
}