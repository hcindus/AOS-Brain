import sys
sys.path.insert(0, '/root/.openclaw/workspace/psd/sales-automation')
from service import SalesAutomationService

# Initialize service to check routes
service = SalesAutomationService()
print("Routes registered:")
for route in service.app.router.routes():
    print(f"  {route.method} {route.resource}")
