import os
import shutil
import tempfile
import unittest
from agent_ops_cockpit.ops.migration import MigrationEngine

class TestMigrationHops(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.agent_path = os.path.join(self.tmp_dir, 'agent.py')
        # Start with legacy OpenAI
        with open(self.agent_path, 'w') as f:
            f.write("import openai\nprint('Hello world')")
        self.engine = MigrationEngine(self.tmp_dir)

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def test_multi_cloud_full_hops(self):
        """
        REGRESSION: OpenAI -> Claude -> Google -> Microsoft -> AWS -> back to Google.
        Ensure headers and imports correctly transition without stale artifacts.
        """
        # 1. Hop: OpenAI -> Anthropic (Claude)
        self.engine.hydrate_agent(self.agent_path, 'anthropic')
        with open(self.agent_path, 'r') as f:
            content = f.read()
        self.assertIn("Sovereign Alignment: Optimized for Anthropic Claude", content)
        self.assertIn("import anthropic", content)
        self.assertNotIn("import openai", content)

        # 2. Hop: Anthropic -> Google
        self.engine.hydrate_agent(self.agent_path, 'google')
        with open(self.agent_path, 'r') as f:
            content = f.read()
        self.assertIn("Sovereign Alignment: Optimized for Google Cloud Run", content)
        self.assertIn("import vertexai", content)
        self.assertNotIn("import anthropic", content)

        # 3. Hop: Google -> Microsoft (Azure)
        self.engine.hydrate_agent(self.agent_path, 'microsoft')
        with open(self.agent_path, 'r') as f:
            content = f.read()
        self.assertIn("Sovereign Alignment: Optimized for Microsoft Azure OpenAI", content)
        self.assertIn("from openai import AzureOpenAI", content)
        self.assertNotIn("import vertexai", content)

        # 4. Hop: Microsoft -> AWS
        self.engine.hydrate_agent(self.agent_path, 'aws')
        with open(self.agent_path, 'r') as f:
            content = f.read()
        self.assertIn("Sovereign Alignment: Optimized for AWS App Runner", content)
        self.assertIn("import boto3", content)
        self.assertNotIn("AzureOpenAI", content)

        # 5. Hop: AWS -> back to Google
        self.engine.hydrate_agent(self.agent_path, 'google')
        with open(self.agent_path, 'r') as f:
            content = f.read()
        self.assertIn("Sovereign Alignment: Optimized for Google Cloud Run", content)
        self.assertIn("import vertexai", content)
        self.assertNotIn("import boto3", content)
        self.assertNotIn("AWS App Runner", content)

if __name__ == '__main__':
    unittest.main()
