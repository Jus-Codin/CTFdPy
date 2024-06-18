# Hints Endpoints
CTFd Version: `3.7.0`

Last Updated: 30/3/2024


## Endpoints
- [`GET /hints`](#get-hints)
- [`POST /hints`](#post-hints)
- [`GET /hints/{hint_id}`](#get-hintshint_id)
- [`PATCH /hints/{hint_id}`](#patch-hintshint_id)
- [`DELETE /hints/{hint_id}`](#delete-hintshint_id)


### `GET /hints`
!!! note "This endpoint is only accessible to admins."

Endpoint to get hints in bulk. Can be filtered by `type`, `challenge_id`, `content` and `cost`

#### Query Parameters
| Name | Type | Description |
| ---- | ---- | ----------- |
| `type` | `string` | The type of hint to get, seems to always be `"standard"` |
| `challenge_id` | `int` | The ID of the challenge to get hints for |
| `content` | `string` | The content of the hint to match |
| `cost` | `int` | The cost of the hint to match |
| `q` | `string` | A search query to match against the given `field`. If this is specified, `field` must also be specified |
| `field` | `string` | The field to search against, can be either `type` or `content`. If this is specified, `q` must also be specified. |

#### Response
- `200 OK` - The hints were successfully retrieved
    - `list[`[`LockedHint`](#lockedhint-model)`]`
        ```json
        {
            "success": true,
            "data": [
                {
                    "id": 1,
                    "type": "string",
                    "challenge": 1,
                    "challenge_id": 1,
                    "cost": 1
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

#### Return Values
| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the hint |
| `type` | `string` | The type of the hint, seems to always be `"standard"` |
| `challenge` | `int` | The ID of the challenge the hint is for (I'm not sure why this field exists) |
| `challenge_id` | `int` | The ID of the challenge the hint is for |
| `cost` | `int` | The cost of the hint |


### `POST /hints`
!!! note "This endpoint is only accessible to admins."

Endpoint to create a new hint.

#### JSON Parameters
| Name | Type | Description |
| ---- | ---- | ----------- |
| `type` | `string` | The type of the hint, seems to always be `"standard"` |
| `challenge_id` | `int` | The ID of the challenge the hint is for |
| `content` | `string` | The content of the hint |
| `cost` | `int` | The cost of the hint |
| `requirements` (Optional) | `dict` | The hint's requirements. This dictionary has a single item, `prerequisites`, which is a list of hint IDs required to unlock before this one. |


#### Response
- `200 OK` - The hint was successfully created
    - [`Hint`](#hint-model)
        ```json
        {
            "success": true,
            "data": {
                "id": 1,
                "type": "string",
                "challenge": 1,
                "challenge_id": 1,
                "content": "string",
                "html": "string",
                "cost": 1,
                "requirements": {
                    "prerequisites": [
                        1
                    ]
                }
            }
        }
        ```

- `403 Forbidden` - You are not allowed to access this endpoint
    - `application/json`
        ```json
        {
            "message": "string"
        }
        ```

#### Return Values
| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the hint |
| `type` | `string` | The type of the hint, seems to always be `"standard"` |
| `challenge` | `int` | The ID of the challenge the hint is for (I'm not sure why this field exists) |
| `challenge_id` | `int` | The ID of the challenge the hint is for |
| `content` | `string` | The content of the hint |
| `html` | `string` | The HTML content of the hint |
| `cost` | `int` | The cost of the hint |
| `requirements` | `dict` | The hint's requirements. This dictionary has a single item, `prerequisites`, which is a list of hint IDs required to unlock before this one. (Optional) |


### `GET /hints/{hint_id}`
Endpoint to get a hint by its ID.

#### Response
- `200 OK` - The hint was successfully retrieved

    === "Hint"
        ```json
        {
            "success": true,
            "data": {
                "id": 1,
                "type": "string",
                "challenge": 1,
                "challenge_id": 1,
                "content": "string",
                "html": "string",
                "cost": 1,
                "requirements": {
                    "prerequisites": [
                        1
                    ]
                }
            }
        }
        ```

    === "Locked Hint"
        ```json
        {
            "success": true,
            "data": {
                "id": 1,
                "type": "string",
                "challenge": 1,
                "challenge_id": 1,
                "cost": 1
            }
        }
        ```

    === "Unlocked Hint"
        ```json
        {
            "success": true,
            "data": {
                "id": 1,
                "type": "string",
                "challenge": 1,
                "challenge_id": 1,
                "content": "string",
                "html": "string",
                "cost": 1
            }
        }
        ```

- `403 Forbidden` - You are not allowed to view that hint
    - `application/json`
        ```json
        {
            "success": false,
            "errors": [
                {}
            ]
        }
        ```

- `404 Not Found` - The hint was not found
    - `application/json`
        ```json
        {
            "message": "string"
        }
        ```

#### Return Values
=== "Hint"
    | Name | Type | Description |
    | ---- | ---- | ----------- |
    | `id` | `int` | The ID of the hint |
    | `type` | `string` | The type of the hint, seems to always be `"standard"` |
    | `challenge` | `int` | The ID of the challenge the hint is for (I'm not sure why this field exists) |
    | `challenge_id` | `int` | The ID of the challenge the hint is for |
    | `content` | `string` | The content of the hint |
    | `html` | `string` | The HTML content of the hint |
    | `cost` | `int` | The cost of the hint |
    | `requirements` | `dict` | The hint's requirements. This dictionary has a single item, `prerequisites`, which is a list of hint IDs required to unlock before this one. (Optional) |

=== "Locked Hint"
    | Name | Type | Description |
    | ---- | ---- | ----------- |
    | `id` | `int` | The ID of the hint |
    | `type` | `string` | The type of the hint, seems to always be `"standard"` |
    | `challenge` | `int` | The ID of the challenge the hint is for (I'm not sure why this field exists) |
    | `challenge_id` | `int` | The ID of the challenge the hint is for |
    | `cost` | `int` | The cost of the hint |

=== "Unlocked Hint"
    | Name | Type | Description |
    | ---- | ---- | ----------- |
    | `id` | `int` | The ID of the hint |
    | `type` | `string` | The type of the hint, seems to always be `"standard"` |
    | `challenge` | `int` | The ID of the challenge the hint is for (I'm not sure why this field exists) |
    | `challenge_id` | `int` | The ID of the challenge the hint is for |
    | `content` | `string` | The content of the hint |
    | `html` | `string` | The HTML content of the hint |
    | `cost` | `int` | The cost of the hint |


### `PATCH /hints/{hint_id}`
!!! note "This endpoint is only accessible to admins."

Endpoint to update a hint by its ID.

#### JSON Parameters

!!! danger
    The effect of changing the values for `type` and `challenge_id` is unknown. Changing these values is not recommended.

| Name | Type | Description |
| ---- | ---- | ----------- |
| `type` | `string` | The type of the hint, seems to always be `"standard"` |
| `challenge_id` | `int` | The ID of the challenge the hint is for |
| `content` | `string` | The content of the hint |
| `cost` | `int` | The cost of the hint |
| `requirements` (Optional) | `dict` | The hint's requirements. This dictionary has a single item, `prerequisites`, which is a list of hint IDs required to unlock before this one. |

#### Response
- `200 OK` - The hint was successfully updated
    - [`Hint`](#hint-model)
        ```json
        {
            "success": true,
            "data": {
                "id": 1,
                "type": "string",
                "challenge": 1,
                "challenge_id": 1,
                "content": "string",
                "html": "string",
                "cost": 1,
                "requirements": {
                    "prerequisites": [
                        1
                    ]
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

- `403 Forbidden` - You are not allowed to access this endpoint
    - `application/json`
        ```json
        {
            "message": "string"
        }
        ```

- `404 Not Found` - The hint was not found
    - `application/json`
        ```json
        {
            "message": "string"
        }
        ```

#### Return Values
| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the hint |
| `type` | `string` | The type of the hint, seems to always be `"standard"` |
| `challenge` | `int` | The ID of the challenge the hint is for (I'm not sure why this field exists) |
| `challenge_id` | `int` | The ID of the challenge the hint is for |
| `content` | `string` | The content of the hint |
| `html` | `string` | The HTML content of the hint |
| `cost` | `int` | The cost of the hint |
| `requirements` | `dict` | The hint's requirements. This dictionary has a single item, `prerequisites`, which is a list of hint IDs required to unlock before this one. (Optional) |


### `DELETE /hints/{hint_id}`
!!! note "This endpoint is only accessible to admins."

Endpoint to delete a hint by its ID.

#### Response
- `200 OK` - The hint was successfully deleted
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

- `404 Not Found` - The hint with the given ID does not exist
    - `application/json`
        ```json
        {
            "message": "string"
        }
        ```


## Models
- [`Hint` Model](#hint-model)
- [`LockedHint` Model](#lockedhint-model)
- [`UnlockedHint` Model](#unlockedhint-model)


### `Hint` Model
Represents a hint.

```json
{
    "id": 1,
    "type": "string",
    "challenge": 1,
    "challenge_id": 1,
    "content": "string",
    "html": "string",
    "cost": 1,
    "requirements": {
        "prerequisites": [
            1
        ]
    }
}
```

| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the hint |
| `type` | `string` | The type of the hint, seems to always be `"standard"` |
| `challenge` | `int` | The ID of the challenge the hint is for (I'm not sure why this field exists) |
| `challenge_id` | `int` | The ID of the challenge the hint is for |
| `content` | `string` | The content of the hint |
| `html` | `string` | The HTML content of the hint |
| `cost` | `int` | The cost of the hint |
| `requirements` | `dict` | The hint's requirements. This dictionary has a single item, `prerequisites`, which is a list of hint IDs required to unlock before this one. (Optional) |


### `LockedHint` Model
Represents a hint locked for the current user.

```json
{
    "id": 1,
    "type": "string",
    "challenge": 1,
    "challenge_id": 1,
    "cost": 1
}
```

| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the hint |
| `type` | `string` | The type of the hint, seems to always be `"standard"` |
| `challenge` | `int` | The ID of the challenge the hint is for (I'm not sure why this field exists) |
| `challenge_id` | `int` | The ID of the challenge the hint is for |
| `cost` | `int` | The cost of the hint |


### `UnlockedHint` Model
Represents a hint unlocked for the current user.

```json
{
    "id": 1,
    "type": "string",
    "challenge": 1,
    "challenge_id": 1,
    "content": "string",
    "html": "string",
    "cost": 1
}
```

| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the hint |
| `type` | `string` | The type of the hint, seems to always be `"standard"` |
| `challenge` | `int` | The ID of the challenge the hint is for (I'm not sure why this field exists) |
| `challenge_id` | `int` | The ID of the challenge the hint is for |
| `content` | `string` | The content of the hint |
| `html` | `string` | The HTML content of the hint |
| `cost` | `int` | The cost of the hint |
        