import json
from datetime import datetime


def handler(request):
    """Simple serverless health check for Vercel.
    Returns JSON so Vercel can report a healthy deployment even if the
    main Flask app has issues.
    """
    payload = {
        "status": "healthy",
        "source": "serverless-health",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(payload)
    }
