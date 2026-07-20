docker volume create --name agent-experts-workspace && \
docker run --rm -it -v agent-logix-experts-workspace:/from -v agent-experts-workspace:/to alpine ash -c "cd /from ; cp -av . /to" && \
docker volume rm agent-logix-experts-workspace

```bash
docker exec trinity-backend python3 -c "
from database import db
k = db.create_agent_mcp_api_key('experts', 'admin', 'Bootstrap after missing container')
assert k, 'failed'
print(k.api_key)
"
```

trinity_mcp_g_2mXyi9fg9tejSx3MZmhCpa4rg1sbAAeN8HgbPbmSc

```bash
# Stop/remove current shell
docker rm -f agent-experts

export IMAGE='trinity-agent-base:experts-node26-0.8.3'   # your tag
export VOL='agent-logix-experts-workspace'               # or the volume you used
export MCP_KEY="$(docker exec trinity-backend python3 -c "
from database import db
k = db.create_agent_mcp_api_key('experts', 'admin', 'rebootstrap with ENABLE_AGENT_UI')
print(k.api_key)
")"

docker create \
  --name agent-experts \
  --network trinity-agent-network \
  --label trinity.platform=agent \
  --label trinity.agent-name=experts \
  --label trinity.agent-runtime=claude-code \
  --label trinity.ssh-port=2240 \
  --label trinity.cpu=16 \
  --label trinity.memory=32g \
  -v "${VOL}:/home/developer" \
  -e AGENT_NAME=experts \
  -e AGENT_TYPE=project \
  -e ENABLE_AGENT_UI=true \
  -e ENABLE_SSH=true \
  -e AGENT_SERVER_PORT=8000 \
  -e TMPDIR=/home/developer/.tmp \
  -e TRINITY_BACKEND_URL=http://backend:8000 \
  -e TRINITY_MCP_URL=http://mcp-server:8080/mcp \
  -e TRINITY_MCP_API_KEY="${MCP_KEY}" \
  "${IMAGE}"

docker start agent-experts
```

```bash
docker exec trinity-backend python3 -c "
import asyncio
from services.docker_service import get_agent_container
from services.agent_service.lifecycle import recreate_container_with_updated_config

async def main():
    c = get_agent_container('experts')
    assert c, 'agent-experts missing'
    await recreate_container_with_updated_config('experts', c, 'system')
    print('recreated experts')

asyncio.run(main())
"
```
