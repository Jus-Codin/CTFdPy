# Topics Endpoints
CTFd Version: `3.7.0`

Last Updated: 30/3/2024


## Models
- [`Topic` Model](#topic-model)
- [`ChallengeTopic` Model](#challengetopic-model)


## Endpoints
- [`GET /topics`](#get-topics)
- [`POST /topics`](#post-topics)
- [`DELETE /topics`](#delete-topics)
- [`GET /topics/{topic_id}`](#get-topicstopic_id)
- [`DELETE /topics/{topic_id}`](#delete-topicstopic_id)


## `Topic` Model
Represents a topic in the CTFd database.

```json
{
    "id": 1,
    "value": "string"
}
```

| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the topic |
| `value` | `string` | The value of the topic |


## `ChallengeTopic` Model
Represents a topic associated with a challenge in the CTFd database. This is essentially a reference between a [`Topic`](#topic-model) and a [`Challenge`](#challenge-model).

```json
{
    "id": 1,
    "challenge_id": 1,
    "challenge": 1,
    "topic_id": 1,
    "topic": 1
}
```

| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the challenge-topic association |
| `challenge_id` | `int` | The ID of the challenge |
| `challenge` | `int` | The ID of the challenge |
| `topic_id` | `int` | The ID of the topic |
| `topic` | `int` | The ID of the topic |


## `GET /topics`
!!! note
    This endpoint is only accessible to admins.

Endpoint to get topics in bulk. Can be filtered by `value`.

### Query Parameters
| Name | Type | Description |
| ---- | ---- | ----------- |
| `value` | `string` | The value of the topic to get topics for |
| `q` | `string` | A search query to match against the given `field`. If this is specified, `field` must also be specified |
| `field` | `string` | The field to search against, can only be set to `value`. If this is specified, `q` must also be specified. |

### Response
- `200 OK` - The topics were successfully retrieved
    - `list[`[`Topic`](#topic-model)`]`
        ```json
        {
            "success": true,
            "data": [
                {
                    "id": 1,
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

- `403 Forbidden` - You are not allowed to access this endpoint
    - `application/json`
        ```json
        {
            "message": "string"
        }

### Return Values
| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the topic |
| `value` | `string` | The value of the topic |


## `POST /topics`
!!! note
    This endpoint is only accessible to admins.

Endpoint to create a new [`Topic`](#topic-model) and/or a [`ChallengeTopic`](#challengetopic-model).

### JSON Parameters
!!! info
    If `type` is not set to `"challenge"`, it will return a `400 Bad Request` response. However, if there is no topic with the specified `value`, a new topic will still be created.

| Name | Type | Description |
| ---- | ---- | ----------- |
| `value` | `string` | The value of the topic to create. If a topic with the same value does not exist, a new [`Topic`](#topic-model) will be created |
| `topic_id` | `int` | The ID of the topic to associate with a challenge. If `value` is specified, this field is ignored |
| `type` | `string` | The type of the topic to create. Can only be `"challenge"` |

### Response
- `200 OK` - The challenge topic was created successfully
    - [`ChallengeTopic`](#challengetopic-model)
        ```json
        {
            "success": true,
            "data": {
                "id": 1,
                "challenge_id": 1,
                "challenge": 1,
                "topic_id": 1,
                "topic": 1
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
            ] // (1)!
        }
        ```

        1. If a [`Topic`](#topic-model) is created but `type` is not set to `"challenge"`, the `errors` field will not exist

- `403 Forbidden` - You do not have the access to create topics
    - `application/json`
        ```json
        {
            "message": "string"
        }
        ```

- `404 Not Found` - The topic with the specified `topic_id` does not exist
    - `application/json`
        ```json
        {
            "success": false,
            "message": "string"
        }
        ```

### Return Values
| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the challenge-topic association |
| `challenge_id` | `int` | The ID of the challenge |
| `challenge` | `int` | The ID of the challenge |
| `topic_id` | `int` | The ID of the topic |
| `topic` | `int` | The ID of the topic |


## `DELETE /topics`

!!! note
    This endpoint is only accessible to admins.

Endpoint to delete a [`ChallengeTopic`](#challengetopic-model).

### Query Parameters
| Name | Type | Description |
| ---- | ---- | ----------- |
| `type` | `string` | The type of the topic to delete. Can only be `"challenge"` |
| `target_id` | `int` | The ID of the topic to delete. |

### Response
- `200 OK` - The topic was deleted successfully
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
            ] // (1)!
        }
        ```

        1. If `type` is not set to `"challenge"`, the `errors` field will not exist

- `403 Forbidden` - You do not have the access to delete topics
    - `application/json`
        ```json
        {
            "message": "string"
        }
        ```

- `404 Not Found` - The topic with the specified `target_id` does not exist
    - `application/json`
        ```json
        {
            "message": "string"
        }
        ```

## `GET /topics/{topic_id}`
!!! note
    This endpoint is only accessible to admins.

Endpoint to get a specific topic.

### Response
- `200 OK` - The topic was successfully retrieved
    - [`Topic`](#topic-model)
        ```json
        {
            "success": true,
            "data": {
                "id": 1,
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

- `403 Forbidden` - You are not allowed to access this endpoint
    - `application/json`
        ```json
        {
            "message": "string"
        }
        ```

- `404 Not Found` - The topic with the specified `topic_id` does not exist
    - `application/json`
        ```json
        {
            "success": false,
            "message": "string"
        }
        ```

### Return Values
| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the topic |
| `value` | `string` | The value of the topic |


## `DELETE /topics/{topic_id}`
!!! note
    This endpoint is only accessible to admins.

Endpoint to delete a [`Topic`](#topic-model).

### Response
- `200 OK` - The topic was deleted successfully
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

- `403 Forbidden` - You do not have the access to delete topics
    - `application/json`
        ```json
        {
            "message": "string"
        }
        ```

- `404 Not Found` - The topic with the specified `topic_id` does not exist
    - `application/json`
        ```json
        {
            "success": false,
            "message": "string"
        }
        ```
