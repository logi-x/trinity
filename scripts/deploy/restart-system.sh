#!/bin/bash

set -e

cd "$(dirname "$0")/../.."

# Read version from VERSION file
VERSION=$(cat VERSION 2>/dev/null || echo "latest")
VERSION=$(echo "$VERSION" | tr -d '[:space:]')

echo "====================================="
echo "Restarting Trinity Agent Base Image"
echo "Version: $VERSION"
echo "====================================="
echo ""

# Restart with version tag and latest tag
docker exec trinity-backend python3 -c "
import asyncio
from services.docker_service import get_agent_container
from services.agent_service.lifecycle import recreate_container_with_updated_config

# agent_name -> NEW image tag after your custom rebuild
IMAGE = {
    'logix-system': 'trinity-agent-base:${VERSION}',
    'cornelius': 'trinity-agent-base:${VERSION}',
    'atlas': 'trinity-agent-base:${VERSION}',
    'howa':    'trinity-agent-base:howa-php84-${VERSION}',
    'experts': 'trinity-agent-base:experts-node26-${VERSION}'
}

async def main():
    for name, image in IMAGE.items():
        c = get_agent_container(name)
        if not c:
            print('skip (not found):', name)
            continue
        # Pin new image before recreate (recreate reads Config.Image from attrs)
        c.attrs.setdefault('Config', {})['Image'] = image
        await recreate_container_with_updated_config(name, c, 'system')
        print('recreated', name, '->', image)

asyncio.run(main())
"

echo ""
echo "✅ Containers restarted successfully:"
echo "   - logix-system-${VERSION}"
echo "   - cornelius-${VERSION}"
echo "   - atlas-${VERSION}"
echo "   - experts-node26-${VERSION}"
echo "   - howa-php84-${VERSION}"
echo ""

