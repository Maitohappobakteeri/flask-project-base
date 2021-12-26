from validate import validate

ignored = ["id"]

template = {
    "username": "strawberry"
}

validate("Current user", ignored, template)
