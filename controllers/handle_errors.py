from fastapi import  HTTPException

def response_error(detail, code):
    return HTTPException(status_code=code, detail=detail)