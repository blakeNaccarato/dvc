import pytest

from tests.unit.repo.experiments.conftest import (  # noqa, pylint disable=unused-argument
    checkpoint_stage,
    exp_stage,
    failed_exp_stage,
    test_queue,
)


@pytest.fixture
def http_auth_patch(mocker):
    from dulwich.client import HTTPUnauthorized

    url = "https://0.0.0.0"
    client = mocker.MagicMock()
    client.get_refs.side_effect = HTTPUnauthorized("", url)
    client.send_pack.side_effect = HTTPUnauthorized("", url)

    patch = mocker.patch("dulwich.client.get_transport_and_path")
    patch.return_value = (client, url)
    return url


@pytest.fixture(params=[True, False])
def workspace(request, test_queue) -> bool:  # noqa
    return request.param


@pytest.fixture
def params_repo(tmp_dir, scm, dvc):
    (tmp_dir / "params.yaml").dump(
        {"foo": [{"bar": 1}, {"baz": 2}], "goo": {"bag": 3.0}, "lorem": False}
    )
    dvc.run(
        cmd="echo foo",
        params=["params.yaml:"],
        name="foo",
    )
    scm.add(["dvc.yaml", "dvc.lock", "copy.py", "params.yaml"])
    scm.commit("init")
