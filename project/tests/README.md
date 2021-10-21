# ⚙ Testing

## 💡 Testing
### Installing all `requirements.txt` packages locally (recommended)
- Requires python installed on local machine.
1. Run `pip install -r requirements.txt --user` in your local machine terminal.
   - Only required to install everything once!
2. Move into the `project` folder (`cd project`).
3. Run tests with `python -m pytest`.
   - Must be in `project` folder for this to work.
4. Update tests in `project/tests` & repeat step 3 to test them.

### Without locally installing all `requirements.txt` packages (pain)
1. Restart the Docker image to update your changes.
2. Open the PyCharm `Python Console`.
3. Run `import os; os.chdir('project')`.
4. Test by running `os.system('python -m pytest')`.
5. Update tests in `project/tests` & restart from step 1 to test them.