import { describe, it, expect } from "vitest";
import { render } from "@testing-library/react";
import App from "./app/App";

describe("ShopFlow Frontend App", () => {
  it("renders the application without crashing", () => {
    const { container } = render(<App />);
    expect(container).toBeDefined();
  });
});
