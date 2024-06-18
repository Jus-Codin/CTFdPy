# Users Endpoints
CTFd Version: `3.7.1`

Last Updated: 4/6/2024

## Endpoints
- [`GET /users`](#get-users)
- [`POST /users`](#post-users)
- [`GET /users/me`](#get-users-me)
- [`PATCH /users/me`](#patch-users-me)
- [`GET /users/me/awards`](#get-users-me-awards)
- [`GET /users/me/fails`](#get-users-me-fails)
- [`GET /users/me/solves`](#get-users-me-solves)
- [`GET /users/{user_id}`](#get-usersuser_id)
- [`PATCH /users/{user_id}`](#patch-usersuser_id)
- [`DELETE /users/{user_id}`](#delete-usersuser_id)
- [`GET /users/{user_id}/awards`](#get-usersuser_idawards)
- [`POST /users/{user_id}/email`](#post-usersuser_idemail)
- [`GET /users/{user_id}/fails`](#get-usersuser_idfails)
- [`GET /users/{user_id}/solves`](#get-usersuser_idsolves)


### `GET /users`
!!! warning
    This endpoint only returns users that are visible to the user by default. To get all users, set the `view` query parameter to `"admin"`.

!!! warning
    The data returned by this endpoint only contains a part of each user's details. To get the full details of a user as an admin, use the [`GET /users/{user_id}`](#get-usersintuser_id) endpoint.

!!! warning
    If there is more than 50 results, the response will be paginated. To get the next page of results, set the `page` query parameter to the page number.

Endpoint to get users in bulk. Can be filtered by `affiliation`, `country` and `bracket`.

#### Query Parameters
!!! Note
    `field` can be set to `email` only if the user is an admin.

| Name | Type | Description |
| ---- | ---- | ----------- |
| `affiliation` | `string` | The affiliation of the user to get users for |
| `country` | `string` | The country of the user to get users for |
| `bracket` | `int` | The bracket of the user to get users for |
| `q` | `string` | A search query to match against the given `field`. If this is specified, `field` must also be specified |
| `field` | `string` | The field to search against, can be either `name`, `website`, `country`, `bracket`, `affiliation` or `email`. If this is specified, `q` must also be specified |
| `view` | `string` | The view of the users to output. If set to `"admin"`, it will show all users including `hidden` and `banned` users. |
| `page` | `int` | The page number to get results for |

#### Response
- `list[`[`UserListing`](#userlisting-model)`]`
    ```json
    {
        "success": true,
        "data": [
            {
                "id": 1,
                "oauth_id": 1,
                "name": "string",
                "website": "string",
                "affiliation": "string",
                "country": "string",
                "bracket_id": 1,
                "team_id": 1,
                "fields": [ ]
            }
        ]
    }
    ```


### `POST /users`
!!! note "This endpoint is only accessible to admins."

Endpoint to create a new user.

#### Query Parameters
| Name | Type | Description |
| ---- | ---- | ----------- |
| `notify` | `bool` | Whether to send the user an email containing their credentials |

#### JSON Parameters
| Name | Type | Description |
| ---- | ---- | ----------- |
| `name` | `string` | The name of the user |
| `email` | `string` | The email of the user |
| `password` | `string` | The password of the user |
| `type` | `string` | The type of the user. Can be either `"user"` or `"admin"` |
| `website` | `string` | The website of the user |
| `affiliation` | `string` | The affiliation of the user |
| `country` | `string` | The country of the user |
| `bracket_id` | `int` | The bracket ID of the user |
| `hidden` | `bool` | Whether the user is hidden |
| `banned` | `bool` | Whether the user is banned |
| `verified` | `bool` | Whether the user is verified |
| `language` | `string` | The language of the user |
| `fields` | `list` | The fields of the user |

#### Response
- [`User`](#user-model)
    ```json
    {
        "success": true,
        "data": {
            "id": 1,
            "oauth_id": 1,
            "name": "string",
            "password": "string",
            "email": "string",
            "type": "string",
            "secret": "string",
            "website": "string",
            "affiliation": "string",
            "country": "string",
            "bracket_id": 1,
            "hidden": true,
            "banned": true,
            "verified": true,
            "language": "string",
            "team_id": 1,
            "fields": [ ],
            "created": "string"
        }
    }
    ```


### `GET /users/me`
Endpoint to get the current user's details.

#### Response
- [`UserPrivateView`](#userprivateview-model)
    ```json
    {
        "success": true,
        "data": {
            "id": 1,
            "oauth_id": 1,
            "name": "string",
            "email": "string",
            "website": "string",
            "affiliation": "string",
            "country": "string",
            "bracket_id": 1,
            "language": "string",
            "team_id": 1,
            "fields": [ ],
            "place": 1,
            "score": 1
        }
    }
    ```


### `PATCH /users/me`
Endpoint to update the current user's details.

#### JSON Parameters
!!! warning
    If you want to update the `email` or `password` and you are not an admin, the `confirm` field containing your current password must be provided.

| Name | Type | Description |
| ---- | ---- | ----------- |
| `name` | `string` | The name of the user |
| `email` | `string` | The email of the user |
| `password` | `string` | The password of the user |
| `website` | `string` | The website of the user |
| `affiliation` | `string` | The affiliation of the user |
| `country` | `string` | The country of the user |
| `bracket_id` | `int` | The bracket ID of the user |
| `language` | `string` | The language of the user |
| `fields` | `list` | The fields of the user |
| `confirm` | `string` | The current password of the user. If you want to update the `email` or `password` and you are not an admin, this field must be provided. |

#### Response
- [`UserPrivateView`](#userprivateview-model)
    ```json
    {
        "success": true,
        "data": {
            "id": 1,
            "oauth_id": 1,
            "name": "string",
            "email": "string",
            "website": "string",
            "affiliation": "string",
            "country": "string",
            "bracket_id": 1,
            "language": "string",
            "team_id": 1,
            "fields": [ ],
            "place": 1,
            "score": 1
        }
    }
    ```

### `GET /users/me/awards`
Endpoint to get the awards of the current user.

#### TODO


### `GET /users/me/fails`
Endpoint to get the fails of the current user.

#### TODO


### `GET /users/me/solves`
Endpoint to get the solves of the current user.

#### TODO


### `GET /users/{user_id}`
!!! note
    If you are not an admin, this endpoint will only return the public view of the user.

Endpoint to get a user's details.

#### Response
=== "Admin View"

    ```json
    {
        "success": true,
        "data": {
            "id": 1,
            "oauth_id": 1,
            "name": "string",
            "email": "string",
            "type": "string",
            "secret": "string",
            "website": "string",
            "affiliation": "string",
            "country": "string",
            "bracket_id": 1,
            "hidden": true,
            "banned": true,
            "verified": true,
            "language": "string",
            "team_id": 1,
            "fields": [ ],
            "created": "string",
            "place": 1,
            "score": 1
        }
    }
    ```

=== "Public View"

    ```json
    {
        "success": true,
        "data": {
            "id": 1,
            "oauth_id": 1,
            "name": "string",
            "website": "string",
            "affiliation": "string",
            "country": "string",
            "bracket_id": 1,
            "team_id": 1,
            "fields": [ ],
            "place": 1,
            "score": 1
        }
    }
    ```


### `PATCH /users/{user_id}`
!!! note "This endpoint is only accessible to admins."

Endpoint to update a user's details.

#### JSON Parameters
| Name | Type | Description |
| ---- | ---- | ----------- |
| `name` | `string` | The name of the user |
| `email` | `string` | The email of the user |
| `type` | `string` | The type of the user. Can be either `"user"` or `"admin"` |
| `secret` | `string` | The secret of the user |
| `website` | `string` | The website of the user |
| `affiliation` | `string` | The affiliation of the user |
| `country` | `string` | The country of the user |
| `bracket_id` | `int` | The bracket ID of the user |
| `hidden` | `bool` | Whether the user is hidden |
| `banned` | `bool` | Whether the user is banned |
| `verified` | `bool` | Whether the user is verified |
| `language` | `string` | The language of the user |
| `fields` | `list` | The fields of the user |

#### Response
- [`UserAdminView`](#useradminview-user-model)
    ```json
    {
        "success": true,
        "data": {
            "id": 1,
            "oauth_id": 1,
            "name": "string",
            "email": "string",
            "type": "string",
            "secret": "string",
            "website": "string",
            "affiliation": "string",
            "country": "string",
            "bracket_id": 1,
            "hidden": true,
            "banned": true,
            "verified": true,
            "language": "string",
            "team_id": 1,
            "fields": [ ],
            "created": "string",
            "place": 1,
            "score": 1
        }
    }
    ```

### `DELETE /users/{user_id}`
!!! note "This endpoint is only accessible to admins."

Endpoint to delete a user.

#### Response
```json
{
    "success": true
}
```


### `GET /users/{user_id}/awards`
Endpoint to get the awards of a user.

#### TODO


### `POST /users/{user_id}/email`
!!! note "This endpoint is only accessible to admins."

Endpoint to send an email to a user.

#### JSON Parameters
| Name | Type | Description |
| ---- | ---- | ----------- |
| `text` | `string` | The text of the email to send |

#### Response
```json
{
    "success": true
}
```


### `GET /users/{user_id}/fails`
Endpoint to get the fails of a user.

#### TODO


### `GET /users/{user_id}/solves`
Endpoint to get the solves of a user.

#### TODO


## Models
- [`User` Model](#user-model)
- [`UserAdminView` Model](#useradminview-model)
- [`UserPublicView` Model](#userpublicview-model)
- [`UserPrivateView` Model](#userprivateview-model)


### `User` Model
Represents a user in the CTFd database

```json
{
    "id": 1,
    "oauth_id": 1,
    "name": "string",
    "password": "string",
    "email": "string",
    "type": "string",
    "secret": "string",
    "website": "string",
    "affiliation": "string",
    "country": "string",
    "bracket_id": 1,
    "hidden": true,
    "banned": true,
    "verified": true,
    "language": "string",
    "team_id": 1,
    "fields": [ ],
    "created": "string"
}
```

| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the user |
| `oauth_id` | `int` | The OAuth ID of the user |
| `name` | `string` | The name of the user |
| `password` | `string` | The password of the user |
| `email` | `string` | The email of the user |
| `type` | `string` | The type of the user. Can be either `"user"` or `"admin"` |
| `secret` | `string` | The secret of the user |
| `website` | `string` | The website of the user |
| `affiliation` | `string` | The affiliation of the user |
| `country` | `string` | The country of the user |
| `bracket_id` | `int` | The bracket ID of the user |
| `hidden` | `bool` | Whether the user is hidden |
| `banned` | `bool` | Whether the user is banned |
| `verified` | `bool` | Whether the user is verified |
| `language` | `string` | The language of the user |
| `team_id` | `int` | The team ID of the user |
| `fields` | `list` | The fields of the user |
| `created` | `string` | The creation date of the user |


### `UserListing` Model
Represents a public view of a user in the CTFd database

```json
{
    "id": 1,
    "oauth_id": 1,
    "name": "string",
    "website": "string",
    "affiliation": "string",
    "country": "string",
    "bracket_id": 1,
    "team_id": 1,
    "fields": [ ]
}
```

| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the user |
| `oauth_id` | `int` | The OAuth ID of the user |
| `name` | `string` | The name of the user |
| `website` | `string` | The website of the user |
| `affiliation` | `string` | The affiliation of the user |
| `country` | `string` | The country of the user |
| `bracket_id` | `int` | The bracket ID of the user |
| `team_id` | `int` | The team ID of the user |
| `fields` | `list` | The fields of the user |


### `UserAdminView` Model
Represents a user in the CTFd database

```json
{
    "id": 1,
    "oauth_id": 1,
    "name": "string",
    "email": "string",
    "type": "string",
    "secret": "string",
    "website": "string",
    "affiliation": "string",
    "country": "string",
    "bracket_id": 1,
    "hidden": true,
    "banned": true,
    "verified": true,
    "language": "string",
    "team_id": 1,
    "fields": [ ],
    "created": "string",
    "place": 1,
    "score": 1
}
```

| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the user |
| `oauth_id` | `int` | The OAuth ID of the user |
| `name` | `string` | The name of the user |
| `email` | `string` | The email of the user |
| `type` | `string` | The type of the user. Can be either `"user"` or `"admin"` |
| `secret` | `string` | The secret of the user |
| `website` | `string` | The website of the user |
| `affiliation` | `string` | The affiliation of the user |
| `country` | `string` | The country of the user |
| `bracket_id` | `int` | The bracket ID of the user |
| `hidden` | `bool` | Whether the user is hidden |
| `banned` | `bool` | Whether the user is banned |
| `verified` | `bool` | Whether the user is verified |
| `language` | `string` | The language of the user |
| `team_id` | `int` | The team ID of the user |
| `fields` | `list` | The fields of the user |
| `created` | `string` | The creation date of the user |
| `place` | `int` | The place of the user |
| `score` | `int` | The score of the user |


### `UserPublicView` Model
Represents a public view of a user in the CTFd database

```json
{
    "id": 1,
    "oauth_id": 1,
    "name": "string",
    "website": "string",
    "affiliation": "string",
    "country": "string",
    "bracket_id": 1,
    "team_id": 1,
    "fields": [ ],
    "place": 1,
    "score": 1
}
```

| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the user |
| `oauth_id` | `int` | The OAuth ID of the user |
| `name` | `string` | The name of the user |
| `website` | `string` | The website of the user |
| `affiliation` | `string` | The affiliation of the user |
| `country` | `string` | The country of the user |
| `bracket_id` | `int` | The bracket ID of the user |
| `team_id` | `int` | The team ID of the user |
| `fields` | `list` | The fields of the user |
| `place` | `int` | The place of the user |
| `score` | `int` | The score of the user |


### `UserPrivateView` Model
Represents a private view of a user in the CTFd database

```json
{
    "id": 1,
    "oauth_id": 1,
    "name": "string",
    "email": "string",
    "website": "string",
    "affiliation": "string",
    "country": "string",
    "bracket_id": 1,
    "language": "string",
    "team_id": 1,
    "fields": [ ],
    "place": 1,
    "score": 1
}
```

| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `int` | The ID of the user |
| `oauth_id` | `int` | The OAuth ID of the user |
| `name` | `string` | The name of the user |
| `email` | `string` | The email of the user |
| `website` | `string` | The website of the user |
| `affiliation` | `string` | The affiliation of the user |
| `country` | `string` | The country of the user |
| `bracket_id` | `int` | The bracket ID of the user |
| `language` | `string` | The language of the user |
| `team_id` | `int` | The team ID of the user |
| `fields` | `list` | The fields of the user |
| `place` | `int` | The place of the user |
| `score` | `int` | The score of the user |
