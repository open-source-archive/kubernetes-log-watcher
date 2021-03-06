import pytest

from mock import MagicMock

from kube_log_watcher.template_loader import load_template
from kube_log_watcher.main import BUILTIN_AGENTS

from kube_log_watcher.agents import BaseWatcher

from .conftest import CLUSTER_ID


def test_base_watcher_not_implemented(monkeypatch):
    agent = BaseWatcher(CLUSTER_ID, load_template)

    with pytest.raises(NotImplementedError):
        agent.name

    with pytest.raises(NotImplementedError):
        agent.add_log_target({})

    with pytest.raises(NotImplementedError):
        agent.remove_log_target('123')

    with pytest.raises(NotImplementedError):
        agent.flush()

    # Raise on exit
    with pytest.raises(NotImplementedError):
        with agent:
            pass


@pytest.mark.parametrize('klass', list(BUILTIN_AGENTS.values()))
def test_builtin_agents_sanity(monkeypatch, klass):
    attrs = ('name', 'add_log_target', 'remove_log_target', 'flush')

    init = MagicMock()
    init.return_value = None

    monkeypatch.setattr(klass, '__init__', init)

    agent = klass(CLUSTER_ID, load_template)

    for attr in attrs:
        assert hasattr(agent, attr) is True
