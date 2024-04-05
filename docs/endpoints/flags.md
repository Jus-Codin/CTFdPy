# Flags Endpoints
CTFd Version: `3.7.0`

Last Updated: 30/3/2024


## Models
- [`Flag` Model](#flag-model)
- [`FlagType` Model](#flagtype-model)


## Endpoints
- [`GET /flags`](#get-flags)
- [`POST /flags`](#post-flags)
- [`GET /flags/types`](#get-flagstypes)
- [`GET /flags/types/{type_name}`](#get-flagstypestype_name)
- [`GET /flags/{flag_id}`](#get-flagsflag_id)
- [`PATCH /flags/{flag_id}`](#patch-flagsflag_id)
- [`DELETE /flags/{flag_id}`](#delete-flagsflag_id)


## `Flag` Model
Represents a flag in the CTFd database.

```json
{
    "id": 1,
    "challenge_id": 1,
    "type": "string",
    "content": "string",
    "data": "string"
}
```

| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the flag |
| `challenge_id` | `int` | The ID of the challenge the flag is for |
| `type` | `string` | The type of the flag, can be either `#!python "static"` or `#!python "regex"` |
| `content` | `string` | The content of the flag |
| `data` | `string` | The data of the flag, seems to only be used for the flag's case-insensitivity, can be either `#!python "case_insensitive"` or `#!python ""` |


## `FlagType` Model
```json
{
    "name": "string",
    "templates": {
        "create": "string",
        "update": "string"
    }
}
```

| Name | Type | Description |
| ---- | ---- | ----------- |
| `name` | `string` | The name of the flag type |
| `templates` | `dict` | The templates for creating and updating flags of this type |


## `GET /flags`
!!! note
    This endpoint is only accessible to admins.

Endpoint to get all flags in bulk. Can be filtered by `challenge_id`, flag `type`, flag `content`, and flag `data`.

### Query Parameters
| Name | Type | Description |
| ---- | ---- | ----------- |
| `challenge_id` | `int` | The ID of the challenge to get flags for |
| `type` | `string` | The type of flag to get |
| `content` | `string` | The content of the flag to match |
| `data` | `string` | The data of the flag to match, seems to only be used for the flag's case-insensitivity, possible values are `case_insensitive` or a blank string |
| `q` | `string` | A search query to match against the given `field`. If this is specified, `field` must also be specified |
| `field` | `string` | The field to search against, can be either `type`, `content` or `data`. If this is specified, `q` must also be specified. |

### Response
- `200 OK` - The flags were successfully retrieved
    - `list[`[`Flag`](#flag-model)`]`
        ```json
        {
            "success": true,
            "data": [
                {
                    "id": 1,
                    "challenge_id": 1,
                    "type": "string",
                    "content": "string",
                    "data": "string"
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

### Return Values
| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the flag |
| `challenge_id` | `int` | The ID of the challenge the flag is for |
| `type` | `string` | The type of the flag, can be either `#!python "static"` or `#!python "regex"` |
| `content` | `string` | The content of the flag |
| `data` | `string` | The data of the flag, seems to only be used for the flag's case-insensitivity, can be either `#!python "case_insensitive"` or `#!python ""` |


## `POST /flags`
!!! note
    This endpoint is only accessible to admins.

Endpoint to create a new flag.

### JSON Parameters
| Name | Type | Description |
| ---- | ---- | ----------- |
| `challenge_id` | `int` | The ID of the challenge the flag is for |
| `type` | `string` | The type of the flag, can be either `#!python "static"` or `#!python "regex"` |
| `content` | `string` | The content of the flag |
| `data` | `string` | The data of the flag, seems to only be used for the flag's case-insensitivity, can be either `#!python "case_insensitive"` or `#!python ""` |

### Response
- `200 OK` - The flag was successfully created
    - [`Flag`](#flag-model)
        ```json
        {
            "success": true,
            "data": {
                "id": 1,
                "challenge_id": 1,
                "type": "string",
                "content": "string",
                "data": "string"
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


### Return Values
| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the flag |
| `challenge_id` | `int` | The ID of the challenge the flag is for |
| `type` | `string` | The type of the flag, can be either `#!python "static"` or `#!python "regex"` |
| `content` | `string` | The content of the flag |
| `data` | `string` | The data of the flag, seems to only be used for the flag's case-insensitivity, can be either `#!python "case_insensitive"` or `#!python ""` |


## `GET /flags/types`
!!! note
    This endpoint is only accessible to admins.

Endpoint to get all flag types.

### Response
- `200 OK` - The flag types were successfully retrieved
    - `dict[str,`[`FlagType`](#flagtype-model)`]`
        ```json
        {
            "success": true,
            "data": {
                "string": {
                    "name": "string",
                    "templates": {
                        "create": "string",
                        "update": "string"
                    }
                }
            }
        }
        ```

### Return Values
| Name | Type | Description |
| ---- | ---- | ----------- |
| `name` | `string` | The name of the flag type |
| `templates` | `dict` | The templates for creating and updating flags of this type |


## `GET /flags/types/{type_name}`
!!! note
    This endpoint is only accessible to admins.

Endpoint to get a specific flag type.

### Response
- `200 OK` - The flag type was successfully retrieved
    - `dict[str,`[`FlagType`](#flagtype-model)`]`
        ```json
        {
            "success": true,
            "data": {
                "string": {
                    "name": "string",
                    "templates": {
                        "create": "string",
                        "update": "string"
                    }
                }
            }
        }
        ```

### Return Values
| Name | Type | Description |
| ---- | ---- | ----------- |
| `name` | `string` | The name of the flag type |
| `templates` | `dict` | The templates for creating and updating flags of this type |


## `GET /flags/{flag_id}`
!!! note
    This endpoint is only accessible to admins.

Endpoint to get a specific flag.

### Response
- `200 OK` - The flag was successfully retrieved
    - [`Flag`](#flag-model)
        ```json
        {
            "success": true,
            "data": {
                "id": 1,
                "challenge_id": 1,
                "type": "string",
                "content": "string",
                "data": "string",
                "templates": {
                    "create": "string",
                    "update": "string"
                }
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

- `404 Not Found` - The flag with the given ID does not exist
    - `application/json`
        ```json
        {
            "message": "string"
        }
        ```

### Return Values
| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the flag |
| `challenge_id` | `int` | The ID of the challenge the flag is for |
| `type` | `string` | The type of the flag, can be either `#!python "static"` or `#!python "regex"` |
| `content` | `string` | The content of the flag |
| `data` | `string` | The data of the flag, seems to only be used for the flag's case-insensitivity, can be either `#!python "case_insensitive"` or `#!python ""` |
| `templates` | `dict` | The templates for creating and updating flags of this type |


## `PATCH /flags/{flag_id}`
!!! note
    This endpoint is only accessible to admins.

Endpoint to update a specific flag.

### JSON Parameters
| Name | Type | Description |
| ---- | ---- | ----------- |
| `challenge_id` | `int` | The ID of the challenge the flag is for |
| `type` | `string` | The type of the flag, can be either `#!python "static"` or `#!python "regex"` |
| `content` | `string` | The content of the flag |
| `data` | `string` | The data of the flag, seems to only be used for the flag's case-insensitivity, can be either `#!python "case_insensitive"` or `#!python ""` |

### Response
- `200 OK` - The flag was successfully updated
    - [`Flag`](#flag-model)
        ```json
        {
            "success": true,
            "data": {
                "id": 1,
                "challenge_id": 1,
                "type": "string",
                "content": "string",
                "data": "string"
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


- `404 Not Found` - The flag with the given ID does not exist
    - `application/json`
        ```json
        {
            "message": "string"
        }
        ```

### Return Values
| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the flag |
| `challenge_id` | `int` | The ID of the challenge the flag is for |
| `type` | `string` | The type of the flag, can be either `#!python "static"` or `#!python "regex"` |
| `content` | `string` | The content of the flag |
| `data` | `string` | The data of the flag, seems to only be used for the flag's case-insensitivity, can be either `#!python "case_insensitive"` or `#!python ""` |


## `DELETE /flags/{flag_id}`
!!! note
    This endpoint is only accessible to admins.

Endpoint to delete a specific flag.

### Response
- `200 OK` - The flag was successfully deleted
    - `application/json`
        ```json
        {
            "success": true
        }
        ```

- `403 Forbidden` - You are not allowed to access this endpoint
    - `application/json`
        ```json
        {
            "message": "string"
        }
        ```


- `404 Not Found` - The flag with the given ID does not exist
    - `application/json`
        ```json
        {
            "message": "string"
        }
        ```
