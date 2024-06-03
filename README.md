# Flashcards Application

## Screenshots
![login](https://raw.githubusercontent.com/tommilewski/flashcards-project/master/screenshots/login.jpg)

![register](https://raw.githubusercontent.com/tommilewski/flashcards-project/master/screenshots/register.jpg)

![menu](https://raw.githubusercontent.com/tommilewski/flashcards-project/master/screenshots/menu.jpg)

![create](https://raw.githubusercontent.com/tommilewski/flashcards-project/master/screenshots/create.jpg)

![my](https://raw.githubusercontent.com/tommilewski/flashcards-project/master/screenshots/my.jpg)

![search](https://raw.githubusercontent.com/tommilewski/flashcards-project/master/screenshots/search.jpg)

![details](https://raw.githubusercontent.com/tommilewski/flashcards-project/master/screenshots/details.jpg)

## Endpoints

| Endpoint                             | Method | Description                                      |
|--------------------------------------|--------|--------------------------------------------------|
| /register                            | POST   | Register a new user                              |
| /login                               | POST   | Log in an existing user                          |
| /flashcards                          | GET    | Get all flashcards                               |
| /flashcards/<string:username>        | GET    | Get all flashcards by username                   |
| /flashcards/add                      | POST   | Add a new flashcard                              |
| /flashcards/search/<string:name>     | GET    | Find flashcards by title (case-insensitive)      |
| /flashcards/delete/<int:flashcard_id>| DELETE | Delete a flashcard by ID                         |
| /flashcards/edit/<int:flashcard_id>  | PUT    | Edit a flashcard by ID                           |

## Usage

### Register

Request Body:
```json
{
    "username": "example_user",
    "password": "example_password"
}
```

### Login
Request Body:
```json
{
    "username": "example_user",
    "password": "example_password"
}
```

### POST /flashcards/add

Request Body
```json
{
    "username": "example_user",
    "title": "Example Title",
    "content": {"What is the capital of France?":"Paris"}
}
```

### GET /flashcards
```json
[
    {
        "id": 1,
        "title": "Example Title",
        "content": {"What is the capital of France?":"Paris"}
        "username": "example_user"
    },
    {
        "id": 2,
        "title": "Another Title",
        "content": {"What is the capital of France?":"Paris"}
        "username": "example_user"
    }
]
```
