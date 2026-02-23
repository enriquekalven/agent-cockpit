import os
import shutil
import sys

# Add src to path
sys.path.append(os.path.abspath('src'))

from agent_ops_cockpit.ops.dashboard import generate_fleet_dashboard

# Mock results for 5 agents
results = {
    '/agents/travel-concierge': 0,
    '/agents/portfolio-manager': 1,
    '/agents/security-sentinel': 0,
    '/agents/finops-optimizer': 1,
    '/agents/customer-support': 0
}

# Run generation
# Note: This will create .cockpit/fleet_dashboard.html
generate_fleet_dashboard(results)

# Copy it to public/fleet-dashboard-sample.html
os.makedirs('public', exist_ok=True)
shutil.copy('.cockpit/fleet_dashboard.html', 'public/fleet-dashboard-sample.html')
print("Sample fleet dashboard generated at public/fleet-dashboard-sample.html")
