from pydantic import BaseModel


class HTTPError(BaseModel):
    detail: str

    class Config:
        json_schema_extra = {
            'example': {'detail': 'Failed to process the request.'},
        }


response_400 = {'description': 'Invalid input provided.', 'model': HTTPError}
response_404 = {'description': 'No data found for provided parameters.', 'model': HTTPError}
response_409 = {
    'description': 'Failed to create a new object due to a duplicate entry in the database.',
    'model': HTTPError
}
response_500 = {'description': 'Failed to retrieve data from the database.', 'model': HTTPError}
