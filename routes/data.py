from fastapi import APIRouter


data_router = APIRouter(
    prefix="api/data"
)

@data_router.post("/upload/{id}")
def upload_file(id):
    
    ## verfiy the file using datacontroller

    ## if the file isn't valid return error
    return