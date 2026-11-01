import importlib.util
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, call

AGENT_PATH = Path(__file__).resolve().parents[1] / "RA_langchain" / "agent.py"
spec = importlib.util.spec_from_file_location("research_agent", AGENT_PATH)
agent_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(agent_module)


class ResearchChatTests(unittest.TestCase):
    def test_query_payload_and_visible_answer(self):
        agent = Mock()
        agent.invoke.return_value = {"messages": [SimpleNamespace(content="Evidence-based answer")]}
        output = Mock()
        agent_module.run_chat(agent, Mock(side_effect=["  What is attention?  ", "exit"]), output)
        agent.invoke.assert_called_once_with({
            "messages": [{"role": "user", "content": "What is attention?"}]
        })
        output.assert_called_once_with("Evidence-based answer")

    def test_exit_variants_never_invoke_agent(self):
        for query in ["exit", "EXIT", "  Exit  "]:
            with self.subTest(query=query):
                agent, output = Mock(), Mock()
                agent_module.run_chat(agent, Mock(return_value=query), output)
                agent.invoke.assert_not_called()
                output.assert_not_called()

    def test_empty_queries_do_not_call_model(self):
        agent = Mock()
        agent_module.run_chat(agent, Mock(side_effect=["", " \t ", "exit"]), Mock())
        agent.invoke.assert_not_called()

    def test_terminal_closure_exits_cleanly(self):
        for error in [EOFError, KeyboardInterrupt]:
            with self.subTest(error=error):
                agent = Mock()
                agent_module.run_chat(agent, Mock(side_effect=error), Mock())
                agent.invoke.assert_not_called()

    def test_multiple_independent_queries(self):
        agent = Mock()
        agent.invoke.side_effect = [
            {"messages": [SimpleNamespace(content="First answer")]},
            {"messages": [SimpleNamespace(content="Second answer")]},
        ]
        output = Mock()
        agent_module.run_chat(agent, Mock(side_effect=["First question", "Second question", "exit"]), output)
        self.assertEqual(agent.invoke.call_args_list, [
            call({"messages": [{"role": "user", "content": "First question"}]}),
            call({"messages": [{"role": "user", "content": "Second question"}]}),
        ])
        self.assertEqual(output.call_args_list, [call("First answer"), call("Second answer")])


if __name__ == "__main__":
    unittest.main()
