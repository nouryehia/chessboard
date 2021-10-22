# ⚙ Testing

## 💡 Testing
### Installing all `requirements.txt` packages locally (recommended)
- Requires python installed on local machine.
1. Run `pip install -r requirements.txt --user` in your local machine terminal.
   - Only required to install everything once!
2. Run tests with `python -m pytest`.
   - Must be in root folder for this to work.
3. Update tests in `project/tests` & repeat step 2 to test them.

### Without locally installing all `requirements.txt` packages (pain)
1. Restart the Docker image to update your changes.
2. Open the PyCharm `Python Console`.
3. Run `import os`.
4. Test by running `os.system('python -m pytest')`.
5. Update tests in `project/tests` & restart from step 1 to test them.

## 📝 Coding Tests
1. To import other modules in `src`, use `project.src.foldername.filename` to reference the path. 
2. Prefix your filenames with `test` - your files should follow the `test_*.py` naming scheme.
3. Prefix your testing methods with `test` - your methods should follow the `test_*()` naming scheme
4. Use `assert` for your tests. (ex: `assert user.first_name == "Joe"`)