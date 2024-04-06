# Files Endpoints
CTFd Version: `3.7.0`

Last Updated: 30/3/2024


## Models
- [`File` Model](#file-model)


## Endpoints
- [`GET /files`](#get-files)
- [`POST /files`](#post-files)
- [`GET /files/{file_id}`](#get-filesfile_id)
- [`DELETE /files/{file_id}`](#delete-filesfile_id)


## `File` Model
Represents a file in the CTFd database.

```json
{
    "id": 1,
    "type": "string",
    "location": "string",
    "sha1sum": "string",
}
```

| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the file |
| `type` | `string` | The type of the file. Possible values are `"standard"`, `"challenge"` and `"page"` |
| `location` | `string` | The location of the file |
| `sha1sum` | `string` | The SHA1 checksum of the file |


## `ChallengeFile` Model
Represents a file associated with a challenge in the CTFd database.

```json
{
    "id": 1,
    "type": "challenge",
    "location": "string",
    "sha1sum": "string",
    "challenge_id": 1
}
```

| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the file |
| `type` | `string` | The type of the file. Has to be set to `"challenge"` |
| `location` | `string` | The location of the file |
| `sha1sum` | `string` | The SHA1 checksum of the file |
| `challenge_id` | `int` | The ID of the challenge that the file is associated with |


## `PageFile` Model
Represents a file associated with a page in the CTFd database.

```json
{
    "id": 1,
    "type": "page",
    "location": "string",
    "sha1sum": "string",
    "page_id": 1
}
```

| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the file |
| `type` | `string` | The type of the file. Has to be set to `"page"` |
| `location` | `string` | The location of the file |
| `sha1sum` | `string` | The SHA1 checksum of the file |
| `page_id` | `int` | The ID of the page that the file is associated with |


## `GET /files`
!!! note
    This endpoint is only accessible to admins.

Endpoint to get all files in bulk. Can be filtered by `type` and `location`.

### Query Parameters
| Name | Type | Description |
| ---- | ---- | ----------- |
| `type` | `string` | The type of the file to filter by. Possible values are `"standard"`, `"challenge"` and `"page"` |
| `location` | `string` | The location of the file to filter by |
| `q` | `string` | A search query to match against the given `field`. If this is specified, `field` must also be specified |
| `field` | `string` | The field to search against, can be either `type` or `location`. If this is specified, `q` must also be specified. |

### Response
- `200 OK` - The files were retrieved successfully
    - `list[`[`File`](#file-model)`|`[`ChallengeFile`](#challengefile-model)`|`[`PageFile`](#pagefile-model)`]`
        ```json
        {
            "success": true,
            "data": [
                {
                    "id": 1,
                    "type": "string",
                    "location": "string",
                    "sha1sum": "string",
                },
                {
                    "id": 1,
                    "type": "challenge",
                    "location": "string",
                    "sha1sum": "string",
                    "challenge_id": 1
                },
                {
                    "id": 1,
                    "type": "page",
                    "location": "string",
                    "sha1sum": "string",
                    "page_id": 1
                }
            ]
        }
        ```

- `400 Bad Request` - An error occurred processing the provided or stored data
    - `application/json`
        ```json
        {
            "success": false,
            "errors": [
                "string"
            ]
        }
        ```

- `403 Forbidden` - You are not allowed to access this endpoint
    - `application/json`
        ```json
        {
            "message": "string"
        }
        ```

## `POST /files`
!!! note
    This endpoint is only accessible to admins.

Endpoint to create a new file.

### Multipart Form Parameters
??? info "Fun Fact"
    This is the only endpoint that accepts multipart form data when using an API key for authentication. In fact, there is logic in the [source code](https://github.com/CTFd/CTFd/blob/master/CTFd/utils/initialization/__init__.py#L288-L293) written specifically for this endpoint.
    ```python title="CTFd/utils/initialization/__init__.py" linenums="283" hl_lines="6-11"
        @app.before_request
        def tokens():
            token = request.headers.get("Authorization")
            if token and (
                request.mimetype == "application/json"
                # Specially allow multipart/form-data for file uploads
                or (
                    request.endpoint == "api.files_files_list"
                    and request.method == "POST"
                    and request.mimetype == "multipart/form-data"
                )
            ):
                ...
    ```


!!! warning
    If the `location` field is set to a path where a file already exists, the existing file will be overwritten. 

| Field Name | Description |
| ---------- | ----------- |
| `file` | The file(s) to upload. This can be specified multiple times to upload multiple files. |
| `challenge_id` (Optional) | The ID of the challenge to associate the file(s) with. This is required if the file is a challenge file. If both `challenge_id` and `challenge` is specified, `challenge_id` will be used. |
| `challenge` (Optional) | The ID of the challenge to associate the file(s) with. This is required if the file is a challenge file. If both `challenge_id` and `challenge` is specified, `challenge_id` will be used. |
| `page_id` (Optional) | The ID of the page(s) to associate the file with. This is required if the file is a page file. If both `page_id` and `page` is specified, `page_id` will be used. |
| `page` (Optional) | The ID of the page to associate the file(s) with. This is required if the file is a page file. If both `page_id` and `page` is specified, `page_id` will be used. |
| `type` (Optional) | The type of the file(s). Possible values are `"standard"`, `"challenge"` and `"page"`. Defaults to `"standard"` |
| `location` | The location of the file. If multiple files are specified, this field cannot be set. |

### Response
- `200 OK` - The file was created successfully
    - `list[`[`File`](#file-model)`|`[`ChallengeFile`](#challengefile-model)`|`[`PageFile`](#pagefile-model)`]`
        ```json
        {
            "success": true,
            "data": [
                {
                    "id": 1,
                    "type": "string",
                    "location": "string",
                    "sha1sum": "string",
                },
                {
                    "id": 1,
                    "type": "challenge",
                    "location": "string",
                    "sha1sum": "string",
                    "challenge_id": 1
                },
                {
                    "id": 1,
                    "type": "page",
                    "location": "string",
                    "sha1sum": "string",
                    "page_id": 1
                }
            ]
        }
        ```

- `400 Bad Request` - An error occurred processing the provided or stored data
    - `application/json`
        ```json
        {
            "success": false,
            "errors": [
                "string"
            ]
        }
        ```

- `403 Forbidden` - You are not allowed to access this endpoint
    - `application/json`
        ```json
        {
            "message": "string"
        }
        ```


## `GET /files/{file_id}`
!!! note
    This endpoint is only accessible to admins.

Endpoint to get a specific file.

### Response
- `200 OK` - The file was retrieved successfully
    - [`File`](#file-model) | [`ChallengeFile`](#challengefile-model) | [`PageFile`](#pagefile-model)
        ```json
        {
            "success": true,
            "data": {
                "id": 1,
                "type": "string",
                "location": "string",
                "sha1sum": "string",
            }
        }
        ```
        ```json
        {
            "success": true,
            "data": {
                "id": 1,
                "type": "challenge",
                "location": "string",
                "sha1sum": "string",
                "challenge_id": 1
            }
        }
        ```
        ```json
        {
            "success": true,
            "data": {
                "id": 1,
                "type": "page",
                "location": "string",
                "sha1sum": "string",
                "page_id": 1
            }
        }
        ```

- `400 Bad Request` - An error occurred processing the provided or stored data
    - `application/json`
        ```json
        {
            "success": false,
            "errors": [
                "string"
            ]
        }
        ```

- `403 Forbidden` - You are not allowed to access this endpoint
    - `application/json`
        ```json
        {
            "message": "string"
        }
        ```

- `404 Not Found` - The file does not exist
    - `application/json`
        ```json
        {
            "message": "string"
        }
        ```


## `DELETE /files/{file_id}`
!!! note
    This endpoint is only accessible to admins.

Endpoint to delete a specific file.

### Response
- `200 OK` - The file was deleted successfully
    - `application/json`
        ```json
        {
            "success": true
        }
        ```

- `400 Bad Request` - An error occurred processing the provided or stored data
    - `application/json`
        ```json
        {
            "success": false,
            "errors": [
                "string"
            ]
        }
        ```

- `403 Forbidden` - You are not allowed to access this endpoint
    - `application/json`
        ```json
        {
            "message": "string"
        }
        ```

- `404 Not Found` - The file does not exist
    - `application/json`
        ```json
        {
            "message": "string"
        }
        ```
