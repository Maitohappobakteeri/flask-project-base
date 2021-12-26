from validate import validate

ignored = ["id", "created_at"]

template = {
    "message": "Edited"
}

validate("Edited example", ignored, template)
