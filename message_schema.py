# This is the message post schema to be validated against
MESSAGE_SCHEMA = {
    "type" : "object",
    "properties" : {
        "recipient" : {"type" : "number"},
        "originator" : {"type" : "string"},
        "message" : {"type" : "string"}
    },
    "required": ["recipient", "originator", "message"]
}
