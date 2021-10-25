# ⚙ Testing

## 💡 Running Tests

### On the Docker image

- Required to test methods that access the database.

1. Start the docker image for the back-end (PyCharm debug or just Docker Compose).
2. Open a CLI inside the docker image.
    - This can be done by going into Docker Desktop and clicking CLI on the `chessboard` image on port 1337.
3. Inside the CLI, run `python3 -m pytest` to run the tests.
4. Update tests in `project/tests` & repeat from step 1 to test them.

## 📝 Coding Tests

1. To import other modules in `src`, use `project.src.foldername.filename` to reference the path.
2. Prefix your filenames with `test` - your files should follow the `test_*.py` naming scheme.
3. Prefix your testing methods with `test` - your methods should follow the `test_*()` naming scheme
4. Use `assert` inside the methods for your tests. (ex: `assert user.first_name == "Joe"`)
5. 