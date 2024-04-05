# Comments Endpoints
CTFd Version: `3.7.0`

Last Updated: 30/3/2024


## Models
- [`Comment` Model](#comment-model)
- [`ChallengeComment` Model](#challengecomment-model)
- [`UserComment` Model](#usercomment-model)
- [`TeamComment` Model](#teamcomment-model)
- [`PageComment` Model](#pagecomment-model)


## Endpoints
- [`GET /comments`](#get-comments)
- [`POST /comments`](#post-comments)
- [`DELETE /comments/{comment_id}`](#delete-commentscomment_id)


## `Comment` Model
Represents a comment in the CTFd database.

```json
{
    "id": 1,
    "type": "standard",
    "content": "string",
    "date": "string",
    "author_id": 1,
    "author": {
        "name": "string"
    },
    "html": "string"
}
```

| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the comment |
| `type` | `string` | The type of the comment. Possible values are `#!python "standard"`, `#!python "challenge"`, `#!python "user"`, `#!python "team"`, `#!python "page"` |
| `content` | `string` | The content of the comment |
| `date` | `string` | The date the comment was created in ISO 8601 format |
| `author_id` | `int` | The ID of the author of the comment |
| `author` | `dict` | The author of the comment |
| `html` | `string` | The HTML content of the comment |


## `ChallengeComment` Model
Represents a comment for a challenge in the CTFd database.

```json
{
    "id": 1,
    "type": "challenge",
    "content": "string",
    "date": "string",
    "author_id": 1,
    "author": {
        "name": "string"
    },
    "html": "string",
    "challenge_id": 1
}
```

| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the comment |
| `type` | `string` | The type of the comment. Possible values are `#!python "standard"`, `#!python "challenge"`, `#!python "user"`, `#!python "team"`, `#!python "page"` |
| `content` | `string` | The content of the comment |
| `date` | `string` | The date the comment was created in ISO 8601 format |
| `author_id` | `int` | The ID of the author of the comment |
| `author` | `dict` | The author of the comment |
| `html` | `string` | The HTML content of the comment |
| `challenge_id` | `int` | The ID of the challenge the comment is associated with |


## `UserComment` Model
Represents a comment for a user in the CTFd database.

```json
{
    "id": 1,
    "type": "user",
    "content": "string",
    "date": "string",
    "author_id": 1,
    "author": {
        "name": "string"
    },
    "html": "string",
    "user_id": 1
}
```

| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the comment |
| `type` | `string` | The type of the comment. Possible values are `#!python "standard"`, `#!python "challenge"`, `#!python "user"`, `#!python "team"`, `#!python "page"` |
| `content` | `string` | The content of the comment |
| `date` | `string` | The date the comment was created in ISO 8601 format |
| `author_id` | `int` | The ID of the author of the comment |
| `author` | `dict` | The author of the comment |
| `html` | `string` | The HTML content of the comment |
| `user_id` | `int` | The ID of the user the comment is associated with |


## `TeamComment` Model
Represents a comment for a team in the CTFd database.

```json
{
    "id": 1,
    "type": "team",
    "content": "string",
    "date": "string",
    "author_id": 1,
    "author": {
        "name": "string"
    },
    "html": "string",
    "team_id": 1
}
```

| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the comment |
| `type` | `string` | The type of the comment. Possible values are `#!python "standard"`, `#!python "challenge"`, `#!python "user"`, `#!python "team"`, `#!python "page"` |
| `content` | `string` | The content of the comment |
| `date` | `string` | The date the comment was created in ISO 8601 format |
| `author_id` | `int` | The ID of the author of the comment |
| `author` | `dict` | The author of the comment |
| `html` | `string` | The HTML content of the comment |
| `team_id` | `int` | The ID of the team the comment is associated with |


## `PageComment` Model
Represents a comment for a page in the CTFd database.

```json
{
    "id": 1,
    "type": "page",
    "content": "string",
    "date": "string",
    "author_id": 1,
    "author": {
        "name": "string"
    },
    "html": "string",
    "page_id": 1
}
```

| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the comment |
| `type` | `string` | The type of the comment. Possible values are `#!python "standard"`, `#!python "challenge"`, `#!python "user"`, `#!python "team"`, `#!python "page"` |
| `content` | `string` | The content of the comment |
| `date` | `string` | The date the comment was created in ISO 8601 format |
| `author_id` | `int` | The ID of the author of the comment |
| `author` | `dict` | The author of the comment |
| `html` | `string` | The HTML content of the comment |
| `page_id` | `int` | The ID of the page the comment is associated with |


## `GET /comments`
!!! note
    This endpoint is only accessible to admins.

Endpoint to get comments in bulk. Limited to 50 comments per request. Can be filtered by `challenge_id`, `user_id`, `team_id` and `page_id`.

### Query Parameters
| Name | Type | Description |
| ---- | ---- | ----------- |
| `challenge_id` | `int` | The ID of the challenge to get comments for |
| `user_id` | `int` | The ID of the user to get comments for |
| `team_id` | `int` | The ID of the team to get comments for |
| `page_id` | `int` | The ID of the page to get comments for |
| `q` | `string` | A search query to match against the given `field`. If this is specified, `field` must also be specified |
| `field` | `string` | The field to search against, can be either only `content`. If this is specified, `q` must also be specified. |
| `page` | `int` | The page number to retrieve. Defaults to 1 |

### Response
- `200 OK` - The comments were retrieved successfully
    - `list[`[`Comment`](#comment-model)`|`[`ChallengeComment`](#challengecomment-model)`|`[`UserComment`](#usercomment-model)`|`[`TeamComment`](#teamcomment-model)`|`[`PageComment`](#pagecomment-model)`]`
        ```json
        {
            "success": true,
            "meta": {
                "pagination": {
                    "page": 1,
                    "next": 1,
                    "prev": 1,
                    "pages": 1,
                    "per_page": 50,
                    "total": 1
                }
            },
            "data": [
                {
                    "id": 1,
                    "type": "standard",
                    "content": "string",
                    "date": "string",
                    "author_id": 1,
                    "author": {
                        "name": "string"
                    },
                    "html": "string"
                },
                {
                    "id": 1,
                    "type": "challenge",
                    "content": "string",
                    "date": "string",
                    "author_id": 1,
                    "author": {
                        "name": "string"
                    },
                    "html": "string",
                    "challenge_id": 1
                },
                {
                    "id": 1,
                    "type": "user",
                    "content": "string",
                    "date": "string",
                    "author_id": 1,
                    "author": {
                        "name": "string"
                    },
                    "html": "string",
                    "user_id": 1
                },
                {
                    "id": 1,
                    "type": "team",
                    "content": "string",
                    "date": "string",
                    "author_id": 1,
                    "author": {
                        "name": "string"
                    },
                    "html": "string",
                    "team_id": 1
                },
                {
                    "id": 1,
                    "type": "page",
                    "content": "string",
                    "date": "string",
                    "author_id": 1,
                    "author": {
                        "name": "string"
                    },
                    "html": "string",
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

- `403 Forbidden` - You do not have the access to view comments
    - `application/json`
        ```json
        {
            "message": "string"
        }
        ```

### Return Values
| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the comment |
| `type` | `string` | The type of the comment. Possible values are `#!python "standard"`, `#!python "challenge"`, `#!python "user"`, `#!python "team"`, `#!python "page"` |
| `content` | `string` | The content of the comment |
| `date` | `string` | The date the comment was created in ISO 8601 format |
| `author_id` | `int` | The ID of the author of the comment |
| `author` | `dict` | The author of the comment |
| `html` | `string` | The HTML content of the comment |
| `challenge_id` | `int` | The ID of the challenge the comment is associated with |
| `user_id` | `int` | The ID of the user the comment is associated with |
| `team_id` | `int` | The ID of the team the comment is associated with |
| `page_id` | `int` | The ID of the page the comment is associated with |


## `POST /comments`
!!! note
    This endpoint is only accessible to admins.

Endpoint to create a new comment.

### JSON Parameters
!!! Note
    It is not possible to post a comment as another user by setting `author_id` to a different value. The `author_id` field is ignored and the comment is always created as the currently authenticated user.

| Name | Type | Description |
| ---- | ---- | ----------- |
| `content` | `string` | The content of the comment |
| `type` (Optional) | `string` | The type of the comment. Possible values are `#!python "standard"`, `#!python "challenge"`, `#!python "user"`, `#!python "team"`, `#!python "page"` |
| `author_id` (Optional) | `int` | The ID of the author of the comment |
| `date` (Optional) | `string` | The date the comment was created in ISO 8601 format |
| `challenge_id` (Optional) | `int` | The ID of the challenge to associate the comment with |
| `user_id` (Optional) | `int` | The ID of the user to associate the comment with |
| `team_id` (Optional) | `int` | The ID of the team to associate the comment with |
| `page_id` (Optional) | `int` | The ID of the page to associate the comment with |

### Response
- `200 OK` - The comment was created successfully
    - [`Comment`](#comment-model)
        ```json
        {
            "success": true,
            "data": {
                "id": 1,
                "type": "standard",
                "content": "string",
                "date": "string",
                "author_id": 1,
                "author": {
                    "name": "string"
                },
                "html": "string"
            }
        }
        ```
    - [`ChallengeComment`](#challengecomment-model)
        ```json
        {
            "success": true,
            "data": {
                "id": 1,
                "type": "challenge",
                "content": "string",
                "date": "string",
                "author_id": 1,
                "author": {
                    "name": "string"
                },
                "html": "string",
                "challenge_id": 1
            }
        }
        ```
    - [`UserComment`](#usercomment-model)
        ```json
        {
            "success": true,
            "data": {
                "id": 1,
                "type": "user",
                "content": "string",
                "date": "string",
                "author_id": 1,
                "author": {
                    "name": "string"
                },
                "html": "string",
                "user_id": 1
            }
        }
        ```
    - [`TeamComment`](#teamcomment-model)
        ```json
        {
            "success": true,
            "data": {
                "id": 1,
                "type": "team",
                "content": "string",
                "date": "string",
                "author_id": 1,
                "author": {
                    "name": "string"
                },
                "html": "string",
                "team_id": 1
            }
        }
        ```
    - [`PageComment`](#pagecomment-model)
        ```json
        {
            "success": true,
            "data": {
                "id": 1,
                "type": "page",
                "content": "string",
                "date": "string",
                "author_id": 1,
                "author": {
                    "name": "string"
                },
                "html": "string",
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

### Return Values
| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the comment |
| `type` | `string` | The type of the comment. Possible values are `#!python "standard"`, `#!python "challenge"`, `#!python "user"`, `#!python "team"`, `#!python "page"` |
| `content` | `string` | The content of the comment |
| `date` | `string` | The date the comment was created in ISO 8601 format |
| `author_id` | `int` | The ID of the author of the comment |
| `author` | `dict` | The author of the comment |
| `html` | `string` | The HTML content of the comment |
| `challenge_id` | `int` | The ID of the challenge the comment is associated with |
| `user_id` | `int` | The ID of the user the comment is associated with |
| `team_id` | `int` | The ID of the team the comment is associated with |
| `page_id` | `int` | The ID of the page the comment is associated with |


## `DELETE /comments/{comment_id}`
!!! note
    This endpoint is only accessible to admins.

Endpoint to delete a [`Comment`](#comment-model).

### Response
- `200 OK` - The comment was deleted successfully
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

- `404 Not Found` - The comment with the specified `comment_id` does not exist
    - `application/json`
        ```json
        {
            "success": false,
            "message": "string"
        }
        ```
