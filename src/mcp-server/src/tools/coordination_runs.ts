/** MCP tools for Trinity's thin coordination-run correlation primitive. */

import { z } from "zod";
import { TrinityClient } from "../client.js";
import type { McpAuthContext } from "../types.js";

const statuses = ["active", "waiting", "blocked", "completed", "cancelled"] as const;
const resourceTypes = ["execution", "operator_queue"] as const;

export function createCoordinationRunTools(
  client: TrinityClient,
  requireApiKey: boolean,
) {
  const getClient = (auth?: McpAuthContext): TrinityClient => {
    if (requireApiKey) {
      if (!auth?.mcpApiKey) throw new Error("MCP API key authentication required");
      const scoped = new TrinityClient(client.getBaseUrl());
      scoped.setToken(auth.mcpApiKey);
      return scoped;
    }
    return client;
  };

  const resolveAgent = (auth: McpAuthContext | undefined, specified?: string): string => {
    if (specified) return specified;
    if (auth?.scope === "agent" && auth.agentName) return auth.agentName;
    throw new Error("agent_name is required for non-agent-scoped keys");
  };

  const checkAccess = async (
    api: TrinityClient,
    auth: McpAuthContext | undefined,
    agentName: string,
    mutation: boolean,
  ): Promise<string | undefined> => {
    if (auth?.scope !== "agent" || !auth.agentName || auth.agentName === agentName) {
      return undefined;
    }
    if (mutation) {
      return `Agent '${auth.agentName}' may only mutate its own coordination runs`;
    }
    const permitted = await api.getPermittedAgents(auth.agentName);
    return permitted.includes(agentName)
      ? undefined
      : `Agent '${auth.agentName}' does not have permission to access '${agentName}'`;
  };

  const contextSchema = z.record(z.string(), z.unknown());
  const agentSchema = z.string().optional().describe(
    "Coordination owner. Agent-scoped keys default to their bound agent.",
  );
  const errorJson = (error: unknown) => JSON.stringify({
    error: error instanceof Error ? error.message : String(error),
  });

  return {
    createCoordinationRun: {
      name: "create_coordination_run",
      description:
        "Create a durable business-work correlation record. Trinity tracks generic lifecycle and links; context and workflow transitions remain agent-owned.",
      parameters: z.object({
        agent_name: agentSchema,
        outcome: z.string().min(1).max(2000),
        root_execution_id: z.string().min(1).optional(),
        context: contextSchema.optional(),
      }),
      execute: async (params: any, context?: { session?: McpAuthContext }) => {
        const auth = context?.session;
        const api = getClient(auth);
        try {
          const agentName = resolveAgent(auth, params.agent_name);
          const denied = await checkAccess(api, auth, agentName, true);
          if (denied) return JSON.stringify({ error: "Access denied", reason: denied });
          const { agent_name: _agentName, ...body } = params;
          return JSON.stringify(await api.createCoordinationRun(agentName, body), null, 2);
        } catch (error) {
          return errorJson(error);
        }
      },
    },

    listCoordinationRuns: {
      name: "list_coordination_runs",
      description: "List an agent's coordination runs, optionally filtered by generic lifecycle status.",
      parameters: z.object({
        agent_name: agentSchema,
        status: z.enum(statuses).optional(),
        limit: z.number().int().min(1).max(500).optional().default(100),
      }),
      execute: async (params: any, context?: { session?: McpAuthContext }) => {
        const auth = context?.session;
        const api = getClient(auth);
        try {
          const agentName = resolveAgent(auth, params.agent_name);
          const denied = await checkAccess(api, auth, agentName, false);
          if (denied) return JSON.stringify({ error: "Access denied", reason: denied });
          return JSON.stringify(await api.listCoordinationRuns(agentName, {
            status: params.status,
            limit: params.limit,
          }), null, 2);
        } catch (error) {
          return errorJson(error);
        }
      },
    },

    getCoordinationRun: {
      name: "get_coordination_run",
      description: "Get one coordination run and its linked execution/operator-queue resources.",
      parameters: z.object({ agent_name: agentSchema, run_id: z.string().min(1) }),
      execute: async (params: any, context?: { session?: McpAuthContext }) => {
        const auth = context?.session;
        const api = getClient(auth);
        try {
          const agentName = resolveAgent(auth, params.agent_name);
          const denied = await checkAccess(api, auth, agentName, false);
          if (denied) return JSON.stringify({ error: "Access denied", reason: denied });
          return JSON.stringify(await api.getCoordinationRun(agentName, params.run_id), null, 2);
        } catch (error) {
          return errorJson(error);
        }
      },
    },

    updateCoordinationRun: {
      name: "update_coordination_run",
      description: "Compare-and-set generic lifecycle, outcome, or opaque context using expected_version.",
      parameters: z.object({
        agent_name: agentSchema,
        run_id: z.string().min(1),
        expected_version: z.number().int().min(1),
        status: z.enum(statuses).optional(),
        outcome: z.string().min(1).max(2000).optional(),
        context: contextSchema.optional(),
      }),
      execute: async (params: any, context?: { session?: McpAuthContext }) => {
        const auth = context?.session;
        const api = getClient(auth);
        try {
          const agentName = resolveAgent(auth, params.agent_name);
          const denied = await checkAccess(api, auth, agentName, true);
          if (denied) return JSON.stringify({ error: "Access denied", reason: denied });
          const { agent_name: _agentName, run_id: runId, ...body } = params;
          return JSON.stringify(await api.updateCoordinationRun(agentName, runId, body), null, 2);
        } catch (error) {
          return errorJson(error);
        }
      },
    },

    attachCoordinationResource: {
      name: "attach_coordination_resource",
      description: "Idempotently link an existing execution or operator-queue item to a coordination run.",
      parameters: z.object({
        agent_name: agentSchema,
        run_id: z.string().min(1),
        resource_type: z.enum(resourceTypes),
        resource_id: z.string().min(1),
        role: z.string().min(1).max(100),
      }),
      execute: async (params: any, context?: { session?: McpAuthContext }) => {
        const auth = context?.session;
        const api = getClient(auth);
        try {
          const agentName = resolveAgent(auth, params.agent_name);
          const denied = await checkAccess(api, auth, agentName, true);
          if (denied) return JSON.stringify({ error: "Access denied", reason: denied });
          const { agent_name: _agentName, run_id: runId, ...body } = params;
          return JSON.stringify(await api.attachCoordinationResource(agentName, runId, body), null, 2);
        } catch (error) {
          return errorJson(error);
        }
      },
    },
  };
}
