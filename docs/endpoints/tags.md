# Tags Endpoints
CTFd Version: `3.7.0`

Last Updated: 30/3/2024


## Models
- [`TagUserView` Model](#taguserview-model)
- [`Tag` Model](#tag-model)


## Endpoints
- [`GET /tags`](#get-tags)
- [`POST /tags`](#post-tags)
- [`GET /tags/{tag_id}`](#get-tagstag_id)
- [`PATCH /tags/{tag_id}`](#patch-tagstag_id)
- [`DELETE /tags/{tag_id}`](#delete-tagstag_id)


## `TagUserView` Model
Represents a tag when viewed by a regular user.

```json
{
    "value": "string"
}
```

| Name | Type | Description |
| ---- | ---- | ----------- |
| `value` | `string` | The value of the tag |


## `Tag` Model
Represents a tag in the CTFd database.

```json
{
    "id": 1,
    "challenge": 1,
    "challenge_id": 1,
    "value": "string"
}
```

| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the tag |
| `challenge` | `int` | The challenge that the tag is associated with (I'm not sure why this field exists) |
| `challenge_id` | `int` | The challenge that the tag is associated with |
| `value` | `string` | The value of the tag |


## `GET /tags`
!!! note
    This endpoint is only accessible to admins.

Endpoint to get all tags in bulk. Can be filtered by `challenge_id` and `value`.

### Query Parameters
| Name | Type | Description |
| ---- | ---- | ----------- |
| `challenge_id` | `int` | The ID of the challenge to get tags for |
| `value` | `string` | The value of the tag to filter by |
| `q` | `string` | A search query to match against the given `field`. If this is specified, `field` must also be specified |
| `field` | `string` | The field to search against, can be either `challenge_id` or `value`. If this is specified, `q` must also be specified. |

### Response
- `200 OK` - The tags were retrieved successfully
    - `list[`[`Tag`](#tag-model)`]`
        ```json
        {
            "success": true,
            "data": [
                {
                    "id": 1,
                    "challenge": 1,
                    "challenge_id": 1,
                    "value": "string"
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

- `403 Forbidden` - You do not have the access to view tags
    - `application/json`
        ```json
        {
            "message": "string"
        }
        ```

### Return Values
| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the tag |
| `challenge` | `int` | The challenge that the tag is associated with (I'm not sure why this field exists) |
| `challenge_id` | `int` | The challenge that the tag is associated with |
| `value` | `string` | The value of the tag |


## `POST /tags`
!!! note
    This endpoint is only accessible to admins.

Endpoint to create a new tag.

### JSON Parameters
| Name | Type | Description |
| ---- | ---- | ----------- |
| `challenge_id` | `int` | The ID of the challenge to associate the tag with |
| `value` | `string` | The value of the tag |

### Response
- `200 OK` - The tag was created successfully
    - [`Tag`](#tag-model)
        ```json
        {
            "success": true,
            "data": {
                "id": 1,
                "challenge": 1,
                "challenge_id": 1,
                "value": "string"
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

- `403 Forbidden` - You do not have the access to create tags
    - `application/json`
        ```json
        {
            "message": "string"
        }
        ```

### Return Values
| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the tag |
| `challenge` | `int` | The challenge that the tag is associated with (I'm not sure why this field exists) |
| `challenge_id` | `int` | The challenge that the tag is associated with |
| `value` | `string` | The value of the tag |


## `GET /tags/{tag_id}`
!!! note
    This endpoint is only accessible to admins.

Endpoint to get a specific tag.

### Response
- `200 OK` - The tag was retrieved successfully
    - [`Tag`](#tag-model)
        ```json
        {
            "success": true,
            "data": {
                "id": 1,
                "challenge": 1,
                "challenge_id": 1,
                "value": "string"
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

- `403 Forbidden` - You do not have the access to view tags
    - `application/json`
        ```json
        {
            "message": "string"
        }
        ```

### Return Values
| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the tag |
| `challenge` | `int` | The challenge that the tag is associated with (I'm not sure why this field exists) |
| `challenge_id` | `int` | The challenge that the tag is associated with |
| `value` | `string` | The value of the tag |


## `PATCH /tags/{tag_id}`
!!! note
    This endpoint is only accessible to admins.

Endpoint to update a specific tag.

### JSON Parameters
!!! danger
    The effect of changing the `challenge_id` field is unknown. Changing this field is not recommended.

| Name | Type | Description |
| ---- | ---- | ----------- |
| `challenge_id` | `int` | The ID of the challenge to associate the tag with |
| `value` | `string` | The value of the tag |

### Response
- `200 OK` - The tag was updated successfully
    - [`Tag`](#tag-model)
        ```json
        {
            "success": true,
            "data": {
                "id": 1,
                "challenge": 1,
                "challenge_id": 1,
                "value": "string"
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

- `403 Forbidden` - You do not have the access to update tags
    - `application/json`
        ```json
        {
            "message": "string"
        }
        ```

### Return Values
| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the tag |
| `challenge` | `int` | The challenge that the tag is associated with (I'm not sure why this field exists) |
| `challenge_id` | `int` | The challenge that the tag is associated with |
| `value` | `string` | The value of the tag |


## `DELETE /tags/{tag_id}`
!!! note
    This endpoint is only accessible to admins.

Endpoint to delete a specific tag.

### Response
- `200 OK` - The tag was deleted successfully
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

- `403 Forbidden` - You do not have the access to delete tags
    - `application/json`
        ```json
        {
            "message": "string"
        }
        ```
