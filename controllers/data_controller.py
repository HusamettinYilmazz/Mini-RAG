from fastapi import UploadFile


def verify_file(file: UploadFile):

    if file.content_type not in ["pdf", "txt"]:
        return False
    if file.size > "5MB": ## build config file for these values
        return False

    return True