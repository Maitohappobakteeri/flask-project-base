from validate import validate

ignored = ["id", "created_at"]

template = {
    "message": "Blueberry!"
}

validate("New example", ignored, template)
