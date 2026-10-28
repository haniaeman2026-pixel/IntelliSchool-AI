import unittest, tempfile, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import database, agent

class AgentSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory()
        database.DB_PATH=Path(cls.temp.name)/"test.db"
        database.init_db()
    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()
    def test_help(self):
        self.assertTrue(agent.run_agent("What can you do?")["answer"])
    def test_fee_summary(self):
        result=agent.run_agent("Show fee dues","Admin")
        self.assertEqual(result["intent"],"fees")
        self.assertIn("Fee summary",result["answer"])
    def test_update_needs_approval(self):
        result=agent.run_agent("Update attendance for Sara Ahmed to present","Admin")
        self.assertTrue(result["needs_approval"])
        self.assertFalse(result["action_done"])
    def test_student_role_denied_fees(self):
        result=agent.run_agent("Show fee dues","Student")
        self.assertIn("Access denied",result["answer"])

if __name__=="__main__": unittest.main()
