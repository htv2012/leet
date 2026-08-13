import pathlib
import string

QUERY = """query questionData($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionId
    questionFrontendId
    boundTopicId
    title
    titleSlug
    content
    translatedTitle
    translatedContent
    isPaidOnly
    difficulty
    likes
    dislikes
    isLiked
    similarQuestions
    contributors {
      username
      profileUrl
      avatarUrl
      __typename
    }
    langToValidPlayground
    topicTags {
      name
      slug
      translatedName
      __typename
    }
    companyTagStats
    codeSnippets {
      lang
      langSlug
      code
      __typename
    }
    stats
    hints
    solution {
      id
      canSeeDetail
      __typename
    }
    status
    sampleTestCase
    metaData
    judgerAvailable
    judgeType
    mysqlSchemas
    enableRunCode
    enableTestMode
    envInfo
    libraryUrl
    __typename
  }
}
"""


# Appendix to the pyproject, this is a string.Template content
PYPROJECT_APPENDIX = """
[tool.pytest.ini_options]
pythonpath = [".", "../../_common"]

log_cli = true
log_cli_level = "WARNING"
log_file = "$log_file_path"
log_file_level = "DEBUG"
"""


SETTINGS = """{
    "python.testing.pytestArgs": [
        "."
    ],
    "python.testing.unittestEnabled": false,
    "python.testing.pytestEnabled": true
}
"""

IMPORTS = {
    "TreeNode": "tree",
    "ListNode": "list_node",
    "Optional": "typing",
    "List": "typing",
    "Dict": "typing",
}


def get_template(name: str):
    here = pathlib.Path(__file__).parent
    template = here / "artifacts" / name
    with open(template) as stream:
        content = stream.read()
    return content


def write_file(root: pathlib.Path, name: str, content: str | None = None):
    target = root / name
    content = content or get_template(name)
    target.write_text(content)


def update_pyproject(root: pathlib.Path, log_file_path: str):
    target = root / "pyproject.toml"
    assert target.exists()

    template = string.Template(PYPROJECT_APPENDIX)
    appendix = template.safe_substitute(log_file_path=log_file_path)

    with open(target, "at") as stream:
        stream.write(appendix)
