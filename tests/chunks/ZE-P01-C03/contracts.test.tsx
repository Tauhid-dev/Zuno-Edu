import { expect, test } from "vitest";
import type { components, paths } from "../../../packages/contracts/src/index";

test("generated health and error shapes reflect the implemented OpenAPI", () => {
  type Health = paths["/api/v1/health"]["get"]["responses"][200]["content"]["application/json"];
  const health: Health = { status: "ok" };
  const problem: components["schemas"]["Error"] = {
    code: "VALIDATION_ERROR", message: "Check the request.",
    request_id: "018fdcb0-76dd-4a81-a476-903a62dc0d76",
  };
  expect(problem).not.toHaveProperty("field_errors");
  expect(health.status).toBe("ok");
});
