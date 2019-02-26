import pytest
import uuid


@pytest.fixture
def tmp_file(request, tmp_path):
    # setting up template file mock
    filename = str(uuid.uuid4())[:10]
    directory = tmp_path / "sub"
    directory.mkdir()
    fil = directory / filename
    request.cls.tmp_file = fil
