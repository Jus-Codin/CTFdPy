# Challenges Endpoints
CTFd Version: `3.7.0`

Last Updated: 30/3/2024


## Models
- [`Challenge` Model](#challenge-model)
- [`DynamicChallenge` Model](#dynamicchallenge-model)
- [`PartialChallenge` Model](#partialchallenge-model)
- [`HiddenChallenge` Model](#hiddenchallenge-model)
- [`LockedChallengeHint` Model](#lockedchallengehint-model)
- [`UnlockedChallengeHint` Model](#unlockedchallengehint-model)
- [`ChallengeAttemptResult` Model](#challengeattemptresult-model)
- [`ChallengeType` Model](#challengetype-model)
- [`ChallengeFileResponse` Model](#challengefileresponse-model)
- [`ChallengeRequirements` Model](#challengerequirements-model)
- [`ChallengeSolvesResponse` Model](#challengesolvesresponse-model)
- [`ChallengeTopicResponse` Model](#challengetopicresponse-model)


### `Challenge` Model
Represents a challenge returned by the [`GET /challenges/{challenge_id}`](#get-challengeschallenge_id) endpoint.

```json
{
    "id": 1,
    "name": "string",
    "value": 1,
    "description": "string",
    "connection_info": "string",
    "next_id": 1,
    "category": "string",
    "state": "string",
    "max_attempts": 1,
    "type": "standard",
    "type_data": {
        "id": "standard",
        "name": "standard",
        "templates": {
            "create": "string",
            "update": "string",
            "view": "string"
        },
        "scripts": {
            "create": "string",
            "update": "string",
            "view": "string"
        }
    },
    "solves": 1,
    "solved_by_me": true,
    "attempts": 1,
    "files": [
        "string"
    ],
    "tags": [
        "string"
    ],
    "hints": [{ }],
    "view": "string"
}
```

| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the challenge |
| `name` | `string` | The name of the challenge |
| `value` | `int` | The value of the challenge |
| `description` | `string` | The description of the challenge |
| `connection_info` | `string` | The connection information of the challenge |
| `next_id` | `int` | The ID of the next challenge |
| `category` | `string` | The category of the challenge |
| `state` | `string` | The state of the challenge. Possible values are `"visible"`, `"hidden"`, and `"locked"` |
| `max_attempts` | `int` | The maximum number of attempts for the challenge |
| `type` | `string` | The type of the challenge. Possible values are `"standard"` and `"dynamic"` |
| `type_data` | `dict[str, Any]` | The data associated with the challenge type. Used internally by the frontend |
| `solves` | `int` | The number of solves for the challenge |
| `solved_by_me` | `bool` | Whether or not the current user has solved the challenge |
| `attempts` | `int` | The number of attempts the current user has made on the challenge |
| `files` | `list[str]` | A list of files associated with the challenge |
| `tags` | `list[str]` | A list of tags associated with the challenge |
| `hints` | `list[` [`LockedChallengeHint`](#lockedchallengehint-model)<code>&#124;</code>[`UnlockedChallengeHint`](#unlockedchallengehint-model)`]` | A list of hints associated with the challenge |
| `view` | `string` | The view of the challenge. Used internally by the frontend |


### `DynamicChallenge` Model
Represents a challenge with a dynamic value. This model is returned by [`GET /challenges`](#get-challenges).

```json
{
    "id": 1,
    "name": "string",
    "value": 1, // (1)!
    "initial": 1,
    "decay": 1,
    "minimum": 1,
    "function": "string",
    "description": "string",
    "connection_info": "string",
    "next_id": 1,
    "category": "string",
    "state": "string",
    "max_attempts": 1,
    "type": "dynamic",
    "type_data": {
        "id": "dynamic",
        "name": "dynamic",
        "templates": {
            "create": "string",
            "update": "string",
            "view": "string"
        },
        "scripts": {
            "create": "string",
            "update": "string",
            "view": "string"
        }
    },
    "solves": 1,
    "solved_by_me": true,
    "attempts": 1,
    "files": [
        "string"
    ],
    "tags": [
        "string"
    ],
    "hints": [{ }],
    "view": "string"
}
```

1. The `value` field is read-only and represents the current value of the challenge. This value is calculated based on the `initial`, `decay`, and `minimum` fields.

!!! bug "As of CTFd `3.7.0`, the `function` field is not returned by the API."

| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the challenge |
| `name` | `string` | The name of the challenge |
| `value` | `int` | The value of the challenge. This is read-only for dynamic challenges |
| `initial` | `int` | The initial value of the challenge |
| `decay` | `int` | The decay rate of the challenge |
| `minimum` | `int` | The minimum value of the challenge |
| `function` | `string` | The function used to calculate the value of the challenge. Possible values are `"logarithmic"` and `"linear"` |
| `description` | `string` | The description of the challenge |
| `connection_info` | `string` | The connection information of the challenge |
| `next_id` | `int` | The ID of the next challenge |
| `category` | `string` | The category of the challenge |
| `state` | `string` | The state of the challenge. Possible values are `"visible"`, `"hidden"`, and `"locked"` |
| `max_attempts` | `int` | The maximum number of attempts for the challenge |
| `type` | `Literal["dynamic"]` | The type of the challenge. Has to be `"dynamic"` for dynamic challenges |
| `type_data` | `dict[str, Any]` | The data associated with the challenge type. Used internally by the frontend |
| `solves` | `int` | The number of solves for the challenge |
| `solved_by_me` | `bool` | Whether or not the current user has solved the challenge |
| `attempts` | `int` | The number of attempts the current user has made on the challenge |
| `files` | `list[str]` | A list of files associated with the challenge |
| `tags` | `list[str]` | A list of tags associated with the challenge |
| `hints` | `list[` [`LockedChallengeHint`](#lockedchallengehint-model)<code>&#124;</code>[`UnlockedChallengeHint`](#unlockedchallengehint-model)`]` | A list of hints associated with the challenge |
| `view` | `string` | The view of the challenge. Used internally by the frontend |


### `PartialChallenge` Model
Represents a challenge with only partial details. This model is returned by [`GET /challenges`](#get-challenges).

```json
{
    "id": 1,
    "type": "string",
    "name": "string",
    "value": 1,
    "solves": 1,
    "solved_by_me": true,
    "category": "string",
    "tags": [
        "string"
    ],
    "template": "string",
    "script": "string"
}
```

| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the challenge |
| `type` | `string` | The type of the challenge. Possible values are `"standard"` and `"dynamic"` |
| `name` | `string` | The name of the challenge |
| `value` | `int` | The value of the challenge |
| `solves` | `int` | The number of solves for the challenge |
| `solved_by_me` | `bool` | Whether or not the current user has solved the challenge |
| `category` | `string` | The category of the challenge |
| `tags` | `list[str]` | A list of tags associated with the challenge |
| `template` | `string` | The template of the challenge. Used internally by the frontend |
| `script` | `string` | The script of the challenge. Used internally by the frontend |



### `HiddenChallenge` Model
Represents a challenge with details hidden from the user. This is used for challenges with requirements not yet fulfilled by the user.

!!! warning
    This model is a hard-coded response and should not be confused with a [`Challenge`][challenge-model] that has `state` set to `"hidden"`.

```json
{
    "id": 1,
    "type": "hidden",
    "name": "???",
    "value": 0,
    "solves": null,
    "solved_by_me": false,
    "category": "???",
    "tags": [],
    "template": "",
    "script": ""
}
```

| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the challenge |
| `type` | `string` | The type of the challenge. Will always be `"hidden"` |
| `name` | `string` | The name of the challenge. Will always be `"???"` |
| `value` | `int` | The value of the challenge. Will always be `0` |
| `solves` | `int` | The number of solves for the challenge. Will always be `None` |
| `solved_by_me` | `bool` | Whether or not the current user has solved the challenge. Will always be `False` |
| `category` | `string` | The category of the challenge. Will always be `"???"` |
| `tags` | `list[str]` | A list of tags associated with the challenge. Will always be `[]` |
| `template` | `string` | The template of the challenge. Will always be `""` |
| `script` | `string` | The script of the challenge. Will always be `""` |


### `ChallengeRequirements` Model
Represents the requirements before a challenge can be accessed by a user.

```json
{
    "prerequisites": [
        1
    ],
    "anonymize": false
}
```

| Name | Type | Description |
| ---- | ---- | ----------- |
| `prerequisites` | `list[int]` | A list of challenge IDs that must be solved before this challenge can be accessed |
| `anonymize` | `bool` | Whether or not to anonymize the challenge instead of hiding it if the `prerequisites` are not met. If not specified, defaults to `False` |


### `LockedChallengeHint` Model
Represents a hint that is locked for the current user.

```json
{
    "id": 1,
    "cost": 1
}
```

| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the hint |
| `cost` | `int` | The cost of the hint |


### `UnlockedChallengeHint` Model
Represents a hint that is unlocked for the current user.

```json
{
    "id": 1,
    "cost": 1,
    "content": "string"
}
```

| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the hint |
| `cost` | `int` | The cost of the hint |
| `content` | `string` | The content of the hint |


### `ChallengeAttemptResult` Model
Represents the response from sending a challenge attempt.

```json
{
    "status": "string",
    "message": "string" // (1)!
}
```

1. The message sometimes might be `#!json null`

| Name | Type | Description |
| ---- | ---- | ----------- |
| `status` | `string` | The status of the attempt |
| `message` | `string` | The message from the attempt |

??? info "Challenge Attempt Statuses"
    | Status | Description | Status Code |
    | ------ | ----------- | ----------- |
    | `correct` | The attempt was correct | `200` |
    | `incorrect` | The attempt was incorrect or you have 0 tries left for this challenge | `200 / 403` |
    | `authentication_required` | The user must log in to send an attempt | `403` |
    | `paused` | The CTF is paused | `403` |
    | `ratelimited` | The user is submitting attempts too quickly | `429` |
    | `already_solved` | The challenge has already been solved by the user or the user's team | `200` |


### `ChallengeType` Model
Represents a challenge type.

```json
{
    "id": "string",
    "name": "string",
    "templates": {
        "create": "string",
        "update": "string",
        "view": "string"
    },
    "scripts": {
        "create": "string",
        "update": "string",
        "view": "string"
    },
    "create": "string"
}
```

| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `string` | The ID of the challenge type |
| `name` | `string` | The name of the challenge type |
| `templates` | `dict[str, str]` | A dictionary of templates for creating, updating, and viewing challenges of this type |
| `scripts` | `dict[str, str]` | A dictionary of scripts for creating, updating, and viewing challenges of this type |
| `create` | `string` | The tempate for creating challenges of this type |


### `ChallengeFileResponse` Model
Represents a file associated with a challenge.

```json
{
    "id": 1,
    "type": "challenge",
    "location": "string"
}
```

| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the file |
| `type` | `Literal["challenge"]` | The type of the file. Will always be `"challenge"` |
| `location` | `string` | The location of the file |


### `ChallengeSolvesResponse` Model
Represents a solve for a challenge

```json
{
    "account_id": 1,
    "name": "string",
    "date": "string",
    "account_url": "string"
}
```

| Name | Type | Description |
| ---- | ---- | ----------- |
| `account_id` | `int` | The ID of the account that solved the challenge |
| `name` | `string` | The name of the account that solved the challenge |
| `date` | `string` | The date the challenge was solved |
| `account_url` | `string` | The URL of the account that solved the challenge |


### `ChallengeTopicResponse` Model
Represents a topic associated with a challenge.

```json
{
    "id": 1,
    "challenge_id": 1,
    "topic_id": 1,
    "value": "string"
}
```

| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the challenge-topic association |
| `challenge_id` | `int` | The ID of the challenge |
| `topic_id` | `int` | The ID of the topic |
| `value` | `string` | The value of the topic |


## Endpoints
- [`GET /challenges`](#get-challenges)
- [`POST /challenges`](#post-challenges)
- [`POST /challenges/attempt`](#post-challengesattempt)
- [`GET /challenges/types`](#get-challengestypes)
- [`GET /challenges/{challenge_id}`](#get-challengeschallenge_id)
- [`PATCH /challenges/{challenge_id}`](#patch-challengeschallenge_id)
- [`DELETE /challenges/{challenge_id}`](#delete-challengeschallenge_id)
- [`GET /challenges/{challenge_id}/files`](#get-challengeschallenge_idfiles)
- [`GET /challenges/{challenge_id}/flags`](#get-challengeschallenge_idflags)
- [`GET /challenges/{challenge_id}/hints`](#get-challengeschallenge_idhints)
- [`GET /challenges/{challenge_id}/requirements`](#get-challengeschallenge_idrequirements)
- [`GET /challenges/{challenge_id}/solves`](#get-challengeschallenge_idsolves)
- [`GET /challenges/{challenge_id}/tags`](#get-challengeschallenge_idtags)
- [`GET /challenges/{challenge_id}/topics`](#get-challengeschallenge_idtopics)


### `GET /challenges`
!!! info
    This endpoint only returns challenges that are visible to the user by default. To get all challenges, set the `view` query parameter to `"admin"`.

!!! warning
    The data returned by this endpoint only contains a part of each challenge's details. To get the full details of a challenge, use the [`GET /challenges/{challenge_id}`](#get-challengeschallenge_id) endpoint.

Endpoint to get challenges in bulk. Can be filtered by `name`, `max_attempts`, `value`, `category`, `type` and `state`.

#### Query Parameters
| Name | Type | Description |
| ---- | ---- | ----------- |
| `name` | `string` | The name of the challenge to get challenges for |
| `max_attempts` | `int` | The maximum number of attempts for the challenge to get challenges for |
| `value` | `int` | The value of the challenge to get challenges for |
| `category` | `string` | The category of the challenge to get challenges for |
| `type` | `string` | The type of the challenge to get challenges for |
| `state` | `string` | The state of the challenge to get challenges for. Possible values are `"visible"`, `"hidden"`, and `"locked"` |
| `q` | `string` | A search query to match against the given `field`. If this is specified, `field` must also be specified |
| `field` | `string` | The field to search against, can be either `name`, `description`, `category`, `type` or `state`. If this is specified, `q` must also be specified |
| `view` | `string` | The view of the challenges to output. If set to `"admin"`, it will show all challenges including `hidden` and `locked` challenges. |

#### Response
- `200 OK` - The challenges were successfully retrieved
    - `list[`[`PartialChallenge`](#partialchallenge-model)`]`
        ```json
        {
            "success": true,
            "data": [
                {
                    "id": 1,
                    "type": "string",
                    "name": "string",
                    "value": 1,
                    "solves": 1,
                    "solved_by_me": true,
                    "category": "string",
                    "tags": [
                        "string"
                    ],
                    "template": "string",
                    "script": "string"
                }
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
| `id` | `int` | The ID of the challenge |
| `type` | `string` | The type of the challenge. Possible values are `"standard"` and `"dynamic"` |
| `name` | `string` | The name of the challenge |
| `value` | `int` | The value of the challenge |
| `solves` | `int` | The number of solves for the challenge |
| `solved_by_me` | `bool` | Whether or not the current user has solved the challenge |
| `category` | `string` | The category of the challenge |
| `tags` | `list[str]` | A list of tags associated with the challenge |
| `template` | `string` | The template of the challenge. Used internally by the frontend |
| `script` | `string` | The script of the challenge. Used internally by the frontend |


### `POST /challenges`
!!! note "This endpoint is only accessible to admins."

Endpoint to create a new challenge. Accepts either form data or JSON data.

#### JSON / Multipart Form Parameters
=== "Standard Challenges"

    | Name | Type | Description |
    | ---- | ---- | ----------- |
    | `name` | `string` | The name of the challenge |
    | `value` | `int` | The value of the challenge |
    | `description` | `string` | The description of the challenge |
    | `connection_info` | `string` | The connection information of the challenge |
    | `next_id` | `int` | The ID of the next challenge |
    | `category` | `string` | The category of the challenge |
    | `state` | `string` | The state of the challenge. Possible values are `"visible"`, `"hidden"`, and `"locked"` |
    | `max_attempts` | `int` | The maximum number of attempts for the challenge |
    | `type` | `Literal["standard"]` | The type of the challenge. Has to be `"standard"` for standard challenges |

=== "Dynamic Challenges"

    | Name | Type | Description |
    | ---- | ---- | ----------- |
    | `name` | `string` | The name of the challenge |
    | `initial` | `int` | The initial value of the challenge |
    | `decay` | `int` | The decay rate of the challenge |
    | `minimum` | `int` | The minimum value of the challenge |
    | `function` | `string` | The function used to calculate the value of the challenge. Possible values are `"logarithmic"` and `"linear"` |
    | `description` | `string` | The description of the challenge |
    | `connection_info` | `string` | The connection information of the challenge |
    | `next_id` | `int` | The ID of the next challenge |
    | `category` | `string` | The category of the challenge |
    | `state` | `string` | The state of the challenge. Possible values are `"visible"`, `"hidden"`, and `"locked"` |
    | `max_attempts` | `int` | The maximum number of attempts for the challenge |
    | `type` | `Literal["dynamic"]` | The type of the challenge. Has to be `"dynamic"` for dynamic challenges |


#### Response
- `200 OK` - The hint was created successfully

    === "Standard Challenges"

        ```json
        {
            "success": true,
            "data": {
                "id": 1,
                "name": "string",
                "value": 1,
                "description": "string",
                "connection_info": "string",
                "next_id": 1,
                "category": "string",
                "state": "string",
                "max_attempts": 1,
                "type": "standard",
                "type_data": {
                    "id": "standard",
                    "name": "standard",
                    "templates": {
                        "create": "string",
                        "update": "string",
                        "view": "string"
                    },
                    "scripts": {
                        "create": "string",
                        "update": "string",
                        "view": "string"
                    }
                }
            }
        }
        ```

    === "Dynamic Challenges"

        ```json
        {
            "success": true,
            "data": {
                "id": 1,
                "name": "string",
                "value": 1,
                "initial": 1,
                "decay": 1,
                "minimum": 1,
                "function": "string",
                "description": "string",
                "connection_info": "string",
                "next_id": 1,
                "category": "string",
                "state": "string",
                "max_attempts": 1,
                "type": "dynamic",
                "type_data": {
                    "id": "dynamic",
                    "name": "dynamic",
                    "templates": {
                        "create": "string",
                        "update": "string",
                        "view": "string"
                    },
                    "scripts": {
                        "create": "string",
                        "update": "string",
                        "view": "string"
                    }
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

#### Return Values
=== "Standard Challenges"

    | Name | Type | Description |
    | ---- | ---- | ----------- |
    | `id` | `int` | The ID of the challenge |
    | `name` | `string` | The name of the challenge |
    | `value` | `int` | The value of the challenge |
    | `description` | `string` | The description of the challenge |
    | `connection_info` | `string` | The connection information of the challenge |
    | `next_id` | `int` | The ID of the next challenge |
    | `category` | `string` | The category of the challenge |
    | `state` | `string` | The state of the challenge. Possible values are `"visible"`, `"hidden"`, and `"locked"` |
    | `max_attempts` | `int` | The maximum number of attempts for the challenge |
    | `type` | `string` | The type of the challenge. Possible values are `"standard"` and `"dynamic"` |
    | `type_data` | `dict[str, Any]` | The data associated with the challenge type. Used internally by the frontend |

=== "Dynamic Challenges"

    | Name | Type | Description |
    | ---- | ---- | ----------- |
    | `id` | `int` | The ID of the challenge |
    | `name` | `string` | The name of the challenge |
    | `value` | `int` | The value of the challenge |
    | `initial` | `int` | The initial value of the challenge |
    | `decay` | `int` | The decay rate of the challenge |
    | `minimum` | `int` | The minimum value of the challenge |
    | `function` | `string` | The function used to calculate the value of the challenge. Possible values are `"logarithmic"` and `"linear"` |
    | `description` | `string` | The description of the challenge |
    | `connection_info` | `string` | The connection information of the challenge |
    | `next_id` | `int` | The ID of the next challenge |
    | `category` | `string` | The category of the challenge |
    | `state` | `string` | The state of the challenge. Possible values are `"visible"`, `"hidden"`, and `"locked"` |
    | `max_attempts` | `int` | The maximum number of attempts for the challenge |
    | `type` | `string` | The type of the challenge. Possible values are `"standard"` and `"dynamic"` |
    | `type_data` | `dict[str, Any]` | The data associated with the challenge type. Used internally by the frontend |


### `POST /challenges/attempt`
Endpoint to send a challenge attempt.

#### JSON / Multipart Form Parameters
| Name | Type | Description |
| ---- | ---- | ----------- |
| `challenge_id` | `int` | The ID of the challenge to attempt |
| `submission` | `string` | The submission for the challenge |

#### Response

!!! info "Refer to [`ChallengeAttemptResult`](#challengeattemptresult-model) for possible responses"

!!! warning
    Even when the response code is `200 OK`, the `success` field might be `False` if the attempt was not successful. Additionally, the `success` field does not mean that the attempt was correct. The only way to tell that the attempt is correct is when the `status` field is `"correct"`.

- `200 OK` - The attempt was successful
    - [`ChallengeAttemptResult`](#challengeattemptresult-model)
        ```json
        {
            "success": true, // (1)!
            "data": {
                "status": "string",
                "message": "string"
            }
        }
        ```

        1. This may not always be `True`.

#### Return Values
| Name | Type | Description |
| ---- | ---- | ----------- |
| `status` | `string` | The status of the attempt |
| `message` | `string` | The message from the attempt |

Refer to [`ChallengeAttemptResult`](#challengeattemptresult-model) for possible responses.


### `GET /challenges/types`
Endpoint to get the available challenge types.

#### Response
- `200 OK` - The challenge types were successfully retrieved
    - `list[`[`ChallengeType`](#challengetype-model)`]`
        ```json
        {
            "success": true,
            "data": [
                {
                    "id": "string",
                    "name": "string",
                    "templates": {
                        "create": "string",
                        "update": "string",
                        "view": "string"
                    },
                    "scripts": {
                        "create": "string",
                        "update": "string",
                        "view": "string"
                    },
                    "create": "string"
                }
            ]
        }
        ```

#### Return Values
| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `string` | The ID of the challenge type |
| `name` | `string` | The name of the challenge type |
| `templates` | `dict[str, str]` | A dictionary of templates for creating, updating, and viewing challenges of this type |
| `scripts` | `dict[str, str]` | A dictionary of scripts for creating, updating, and viewing challenges of this type |
| `create` | `string` | The tempate for creating challenges of this type |


### `GET /challenges/{challenge_id}`
Endpoint to get a challenge by ID.

#### Response
- `200 OK` - The challenge was successfully retrieved

    === "Standard Challenge"

        ```json
        {
            "success": true,
            "data": {
                "id": 1,
                "name": "string",
                "value": 1,
                "description": "string",
                "connection_info": "string",
                "next_id": 1,
                "category": "string",
                "state": "string",
                "max_attempts": 1,
                "type": "standard",
                "type_data": {
                    "id": "standard",
                    "name": "standard",
                    "templates": {
                        "create": "string",
                        "update": "string",
                        "view": "string"
                    },
                    "scripts": {
                        "create": "string",
                        "update": "string",
                        "view": "string"
                    }
                }
            }
        }
        ```

    === "Dynamic Challenge"

        ```json
        {
            "success": true,
            "data": {
                "id": 1,
                "name": "string",
                "value": 1,
                "initial": 1,
                "decay": 1,
                "minimum": 1,
                "function": "string",
                "description": "string",
                "connection_info": "string",
                "next_id": 1,
                "category": "string",
                "state": "string",
                "max_attempts": 1,
                "type": "dynamic",
                "type_data": {
                    "id": "dynamic",
                    "name": "dynamic",
                    "templates": {
                        "create": "string",
                        "update": "string",
                        "view": "string"
                    },
                    "scripts": {
                        "create": "string",
                        "update": "string",
                        "view": "string"
                    }
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

- `404 Not Found` - The challenge was not found
    - `application/json`
        ```json
        {
            "message": "string"
        }
        ```

- `500 Internal Server Error` - The underlying challenge type is not installed
    - `application/json`
        ```json
        {
            "message": "string"
        }
        ```

#### Return Values

=== "Standard Challenge"

    | Name | Type | Description |
    | ---- | ---- | ----------- |
    | `id` | `int` | The ID of the challenge |
    | `name` | `string` | The name of the challenge |
    | `value` | `int` | The value of the challenge |
    | `description` | `string` | The description of the challenge |
    | `connection_info` | `string` | The connection information of the challenge |
    | `next_id` | `int` | The ID of the next challenge |
    | `category` | `string` | The category of the challenge |
    | `state` | `string` | The state of the challenge. Possible values are `"visible"`, `"hidden"`, and `"locked"` |
    | `max_attempts` | `int` | The maximum number of attempts for the challenge |
    | `type` | `string` | The type of the challenge. Possible values are `"standard"` and `"dynamic"` |
    | `type_data` | `dict[str, Any]` | The data associated with the challenge type. Used internally by the frontend |

=== "Dynamic Challenge"

    | Name | Type | Description |
    | ---- | ---- | ----------- |
    | `id` | `int` | The ID of the challenge |
    | `name` | `string` | The name of the challenge |
    | `value` | `int` | The value of the challenge |
    | `initial` | `int` | The initial value of the challenge |
    | `decay` | `int` | The decay rate of the challenge |
    | `minimum` | `int` | The minimum value of the challenge |
    | `function` | `string` | The function used to calculate the value of the challenge. Possible values are `"logarithmic"` and `"linear"` |
    | `description` | `string` | The description of the challenge |
    | `connection_info` | `string` | The connection information of the challenge |
    | `next_id` | `int` | The ID of the next challenge |
    | `category` | `string` | The category of the challenge |
    | `state` | `string` | The state of the challenge. Possible values are `"visible"`, `"hidden"`, and `"locked"` |
    | `max_attempts` | `int` | The maximum number of attempts for the challenge |
    | `type` | `string` | The type of the challenge. Possible values are `"standard"` and `"dynamic"` |
    | `type_data` | `dict[str, Any]` | The data associated with the challenge type. Used internally by the frontend |
    

### `PATCH /challenges/{challenge_id}`
!!! note "This endpoint is only accessible to admins."

Endpoint to update a challenge by ID.

#### JSON Parameters
!!! warning
    The `"locked"` challenge state is not documented. Setting challenges to `"locked"` is not recommended.

=== "Standard Challenges"
    | Name | Type | Description |
    | ---- | ---- | ----------- |
    | `name` | `string` | The name of the challenge |
    | `value` | `int` | The value of the challenge |
    | `description` | `string` | The description of the challenge |
    | `connection_info` | `string` | The connection information of the challenge |
    | `next_id` | `int` | The ID of the next challenge |
    | `category` | `string` | The category of the challenge |
    | `state` | `string` | The state of the challenge. Possible values are `"visible"`, `"hidden"`, and `"locked"` |
    | `max_attempts` | `int` | The maximum number of attempts for the challenge |

=== "Dynamic Challenges"
    | Name | Type | Description |
    | ---- | ---- | ----------- |
    | `name` | `string` | The name of the challenge |
    | `initial` | `int` | The initial value of the challenge |
    | `decay` | `int` | The decay rate of the challenge |
    | `minimum` | `int` | The minimum value of the challenge |
    | `function` | `string` | The function used to calculate the value of the challenge. Possible values are `"logarithmic"` and `"linear"` |
    | `description` | `string` | The description of the challenge |
    | `connection_info` | `string` | The connection information of the challenge |
    | `next_id` | `int` | The ID of the next challenge |
    | `category` | `string` | The category of the challenge |
    | `state` | `string` | The state of the challenge. Possible values are `"visible"`, `"hidden"`, and `"locked"` |
    | `max_attempts` | `int` | The maximum number of attempts for the challenge |

#### Response
- `200 OK` - The challenge was successfully retrieved

    === "Standard Challenges"
    
        ```json
        {
            "success": true,
            "data": {
                "id": 1,
                "name": "string",
                "value": 1,
                "description": "string",
                "connection_info": "string",
                "next_id": 1,
                "category": "string",
                "state": "string",
                "max_attempts": 1,
                "type": "standard",
                "type_data": {
                    "id": "standard",
                    "name": "standard",
                    "templates": {
                        "create": "string",
                        "update": "string",
                        "view": "string"
                    },
                    "scripts": {
                        "create": "string",
                        "update": "string",
                        "view": "string"
                    }
                }
            }
        }
        ```

    === "Dynamic Challenges"

        ```json
        {
            "success": true,
            "data": {
                "id": 1,
                "name": "string",
                "value": 1,
                "initial": 1,
                "decay": 1,
                "minimum": 1,
                "function": "string",
                "description": "string",
                "connection_info": "string",
                "next_id": 1,
                "category": "string",
                "state": "string",
                "max_attempts": 1,
                "type": "dynamic",
                "type_data": {
                    "id": "dynamic",
                    "name": "dynamic",
                    "templates": {
                        "create": "string",
                        "update": "string",
                        "view": "string"
                    },
                    "scripts": {
                        "create": "string",
                        "update": "string",
                        "view": "string"
                    }
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

- `404 Not Found` - The challenge was not found
    - `application/json`
        ```json
        {
            "message": "string"
        }
        ```

#### Return Values
=== "Standard Challenges"

    | Name | Type | Description |
    | ---- | ---- | ----------- |
    | `id` | `int` | The ID of the challenge |
    | `name` | `string` | The name of the challenge |
    | `value` | `int` | The value of the challenge |
    | `description` | `string` | The description of the challenge |
    | `connection_info` | `string` | The connection information of the challenge |
    | `next_id` | `int` | The ID of the next challenge |
    | `category` | `string` | The category of the challenge |
    | `state` | `string` | The state of the challenge. Possible values are `"visible"`, `"hidden"`, and `"locked"` |
    | `max_attempts` | `int` | The maximum number of attempts for the challenge |
    | `type` | `string` | The type of the challenge. Possible values are `"standard"` and `"dynamic"` |
    | `type_data` | `dict[str, Any]` | The data associated with the challenge type. Used internally by the frontend |

=== "Dynamic Challenges"

    | Name | Type | Description |
    | ---- | ---- | ----------- |
    | `id` | `int` | The ID of the challenge |
    | `name` | `string` | The name of the challenge |
    | `value` | `int` | The value of the challenge |
    | `initial` | `int` | The initial value of the challenge |
    | `decay` | `int` | The decay rate of the challenge |
    | `minimum` | `int` | The minimum value of the challenge |
    | `function` | `string` | The function used to calculate the value of the challenge. Possible values are `"logarithmic"` and `"linear"` |
    | `description` | `string` | The description of the challenge |
    | `connection_info` | `string` | The connection information of the challenge |
    | `next_id` | `int` | The ID of the next challenge |
    | `category` | `string` | The category of the challenge |
    | `state` | `string` | The state of the challenge. Possible values are `"visible"`, `"hidden"`, and `"locked"` |
    | `max_attempts` | `int` | The maximum number of attempts for the challenge |
    | `type` | `string` | The type of the challenge. Possible values are `"standard"` and `"dynamic"` |
    | `type_data` | `dict[str, Any]` | The data associated with the challenge type. Used internally by the frontend |


### `DELETE /challenges/{challenge_id}`
!!! note "This endpoint is only accessible to admins."

Endpoint to delete a challenge by ID.

#### Response
- `200 OK` - The challenge was successfully deleted
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

- `404 Not Found` - The challenge was not found
    - `application/json`
        ```json
        {
            "message": "string"
        }
        ```

#### Return Values
None


### `GET /challenges/{challenge_id}/files`
!!! note "This endpoint is only accessible to admins."

Endpoint to get the files associated with a challenge by ID.

#### Response
- `200 OK` - The files were successfully retrieved
    - `list[`[`ChallengeFileResponse`](#challenge-modelchallengefileresponse-model)`]`
        ```json
        {
            "success": true,
            "data": [
                {
                    "id": 1,
                    "type": "challenge",
                    "location": "string"
                }
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

- `404 Not Found` - The challenge was not found
    - `application/json`
        ```json
        {
            "message": "string"
        }
        ```

#### Return Values
| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the file |
| `type` | `string` | The type of the file, can only be `"challenge"` |
| `location` | `string` | The location of the file |


### `GET /challenges/{challenge_id}/flags`
!!! note "This endpoint is only accessible to admins."

Endpoint to get the flags associated with a challenge by ID.

#### Response
- `200 OK` - The flags were successfully retrieved
    - `list[`[`Flag`][flag-model]`]`
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

- `403 Forbidden` - You are not allowed to access this endpoint
    - `application/json`
        ```json
        {
            "message": "string"
        }
        ```

- `404 Not Found` - The challenge was not found
    - `application/json`
        ```json
        {
            "message": "string"
        }
        ```

#### Return Values
| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the flag |
| `challenge_id` | `int` | The ID of the challenge the flag is for |
| `type` | `string` | The type of the flag, can be either `"static"` or `"regex"` |
| `content` | `string` | The content of the flag |
| `data` | `string` | The data of the flag, seems to only be used for the flag's case-insensitivity, can be either `"case_insensitive"` or `""` |


### `GET /challenges/{challenge_id}/hints`
!!! note "This endpoint is only accessible to admins."

Endpoint to get the hints associated with a challenge by ID.

#### Response
- `200 OK` - The hints were successfully retrieved
    - `list[`[`Hint`][hint-model]`]`
        ```json
        {
            "success": true,
            "data": [
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
            ]
        }
        ```json
        {
            "success": true,
            "data": [
                {
                    "id": 1,
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

- `404 Not Found` - The challenge was not found
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


### `GET /challenges/{challenge_id}/requirements`
!!! note "This endpoint is only accessible to admins."

Endpoint to get the requirements associated with a challenge by ID.

#### Response
- `200 OK` - The requirements were successfully retrieved
    - [`ChallengeRequirements`](#challengerequirements-model)
        ```json
        {
            "success": true,
            "data": {
                "prerequisites": [
                    1
                ],
                "anonymize": false
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

- `404 Not Found` - The challenge was not found
    - `application/json`
        ```json
        {
            "message": "string"
        }
        ```

#### Return Values
| Name | Type | Description |
| ---- | ---- | ----------- |
| `prerequisites` | `list[int]` | A list of prerequisite challenge IDs |
| `anonymize` | `bool` | Whether or not to anonymize the challenge |


### `GET /challenges/{challenge_id}/solves`
Endpoint to get the solves associated with a challenge by ID.

#### Query Parameters
| Name | Type | Description |
| `preview` | bool | If the CTF is currently frozen, the user is an admin, and this is set to `True`, the response will only contain the solves prior to the freeze time. |

#### Response
- `200 OK` - The solves were successfully retrieved
    - `list[`[`ChallengeSolvesResponse`](#challengesolvesresponse-model)`]`
        ```json
        {
            "success": true,
            "data": [
                {
                    "account_id": 1,
                    "name": "string",
                    "date": "string",
                    "account_url": "string"
                }
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

- `404 Not Found` - The challenge was not found
    - `application/json`
        ```json
        {
            "message": "string"
        }
        ```

#### Return Values
| Name | Type | Description |
| ---- | ---- | ----------- |
| `account_id` | `int` | The ID of the account that solved the challenge |
| `name` | `string` | The name of the account that solved the challenge |
| `date` | `string` | The date the challenge was solved |
| `account_url` | `string` | The URL of the account that solved the challenge |


### `GET /challenges/{challenge_id}/tags`
!!! note "This endpoint is only accessible to admins."

Endpoint to get the tags associated with a challenge by ID.

#### Response
- `200 OK` - The tags were successfully retrieved
    - `list[`[`Tag`][tag-model]`]`
        ```json
        {
            "success": true,
            "data": [
                {
                    "id": 1,
                    "challenge_id": 1,
                    "value": "string"
                }
            ]
        }`
        ```

- `403 Forbidden` - You are not allowed to access this endpoint
    - `application/json`
        ```json
        {
            "message": "string"
        }
        ```

- `404 Not Found` - The challenge was not found
    - `application/json`
        ```json
        {
            "message": "string"
        }
        ```

#### Return Values
| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the tag |
| `challenge_id` | `int` | The ID of the challenge |
| `value` | `string` | The value of the tag |


### `GET /challenges/{challenge_id}/topics`
!!! note "This endpoint is only accessible to admins."

Endpoint to get the topics associated with a challenge by ID.

#### Response
- `200 OK` - The topics were successfully retrieved
    - `list[`[`ChallengeTopicResponse`](#challengetopicresponse-model)`]`
        ```json
        {
            "success": true,
            "data": [
                {
                    "id": 1,
                    "challenge_id": 1,
                    "topic_id": 1,
                    "value": "string"
                }
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

- `404 Not Found` - The challenge was not found
    - `application/json`
        ```json
        {
            "message": "string"
        }
        ```

#### Return Values
| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the challenge-topic association |
| `challenge_id` | `int` | The ID of the challenge |
| `topic_id` | `int` | The ID of the topic |
| `value` | `string` | The value of the topic |
