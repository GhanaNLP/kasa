# Contributing to Kasa

We’re excited to have you join the **Kasa** project! Your contributions are key to advancing this Python library that supports African language translation, Speech-to-Text (STT), and Text-to-Speech (TTS) models built by the Ghana NLP team. 

Below, you'll find a guide to help you contribute smoothly.

## Table of Contents
- [Setting Up Your Development Environment](#setting-up-your-development-environment)
- [Coding Standards and Best Practices](#coding-standards-and-best-practices)
- [Testing Your Code](#testing-your-code)
- [Submitting a Pull Request](#submitting-a-pull-request)
- [Understanding the Project Structure](#understanding-the-project-structure)
- [Useful Resources](#useful-resources)

## Setting Up Your Development Environment
Make sure to create a virtual environment, then proceed.

1. **Clone the Repository:**
   Start by cloning the repository and switch to the kasa directory on your local machine:
   ```bash
   git clone https://github.com/GhanaNLP/kasa.git
   cd kasa
   ```

2. **Install Dependencies:**
   Make sure Python 3.8 or higher is installed. Run:
   ```bash
   pip install .
   ```

3. **Set Up Development Tools (Optional but Recommended):**
   Use code linters and formatters like `black` and `flake8` for consistent code style:
   ```bash
   pip install black flake8
   ```

   We like clean contributions
   

## Coding Standards and Best Practices

- **Follow PEP 8**: Ensure your code aligns with the PEP 8 Python style guide.
- **Use Type Hints**: Add type annotations to improve code readability and aid type checkers.
- **Docstrings and Comments**:
  - Use docstrings to describe the purpose and parameters of classes and functions.
  - Add comments to explain complex or non-intuitive parts of the code.

## Testing Your Code

Testing is non-negotiable to maintain the quality of Kasa. Place your test scripts in the `tests/` directory and name them following the format `test_<feature>.py`.

1. **Run All Tests:**
   ```bash
   pytest tests/
   ```

2. **Add New Test Cases:**
   If your feature or bug fix requires new tests, create them to ensure comprehensive coverage.

## Submitting a Pull Request

1. **Push Your Changes:**
   ```bash
   git push origin <branch-name>
   ```

2. **Create the Pull Request:**
   Head over to [Kasa’s GitHub repository](https://github.com/GhanaNLP/kasa) and create a pull request. Make sure to:
   - Use a clear and descriptive title.
   - Write a brief summary of the changes.
   - Tag project maintainers or relevant team members for review.

3. **Address Feedback:**
   Respond to feedback from reviewers and make any requested changes.

4. **Merging**:
   Once approved, your pull request will be merged. Remember, **never push directly to the main branch**.

## Understanding the Project Structure

Here's an overview of important directories and files:

- **`kasa/`**: Main library code.
- **`examples/`**: Ready-to-run examples to showcase various features.
- **`notebooks/`**: Jupyter notebooks for prototyping and proofs of concept.
- **`tests/`**: Contains unit tests to ensure code stability.
- **`setup.py`**: Lists package dependencies and metadata.
- **`HISTORY.md`**: Contains version updates and planned features.
- **`CONTRIBUTION.md`**: This contribution guide.

## Useful Resources

- **Documentation and Code Reference**: For deeper understanding, refer to `README.md` and inline comments.
- **Community and Support**: For questions or help, reach out to the [Ghana NLP team](https://github.com/GhanaNLP) or open a discussion in the Issues tab.

---

We’re grateful for your time and effort in helping Kasa grow. 

Every contribution, big or small, helps us improve!
