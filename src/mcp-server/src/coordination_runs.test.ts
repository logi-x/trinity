import { describe, it } from "node:test";
import { strict as assert } from "node:assert";

import { createCoordinationRunTools } from "./tools/coordination_runs.js";
import type { TrinityClient } from "./client.js";


const agentCtx = (agentName: string) => ({
  session: { scope: "agent", agentName } as any,
});


describe("coordination run MCP tools", () => {
  it("defaults create to the bound agent", async () => {
    const calls: any[] = [];
    const tools = createCoordinationRunTools({
      createCoordinationRun: async (agentName: string, body: any) => {
        calls.push({ agentName, body });
        return { id: "cr_1", owner_agent: agentName, ...body } as any;
      },
    } as unknown as TrinityClient, false);

    const output = JSON.parse(await tools.createCoordinationRun.execute(
      { outcome: "Ship a campaign", context: { stage: "intake" } },
      agentCtx("atlas"),
    ));

    assert.equal(output.id, "cr_1");
    assert.deepEqual(calls, [{
      agentName: "atlas",
      body: { outcome: "Ship a campaign", context: { stage: "intake" } },
    }]);
  });

  it("agent-scoped keys cannot mutate a sibling's run", async () => {
    let called = false;
    const tools = createCoordinationRunTools({
      updateCoordinationRun: async () => {
        called = true;
        return {} as any;
      },
    } as unknown as TrinityClient, false);

    const output = JSON.parse(await tools.updateCoordinationRun.execute(
      {
        agent_name: "marketing",
        run_id: "cr_1",
        expected_version: 1,
        status: "waiting",
      },
      agentCtx("atlas"),
    ));

    assert.equal(output.error, "Access denied");
    assert.equal(called, false);
  });
});
