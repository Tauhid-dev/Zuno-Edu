import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import RootLayout from "../../../apps/web/src/app/layout";
import Page from "../../../apps/web/src/app/page";

describe("web boot skeleton", () => {
  it("renders a semantic document without private or business UI", () => {
    const html = renderToStaticMarkup(<RootLayout><Page /></RootLayout>);
    expect(html).toContain('<html lang="en">');
    expect(html).toContain("<main><h1>Zuno Edu</h1></main>");
    expect(html).not.toMatch(/<form|<input|<button|<a\s/);
  });
});
