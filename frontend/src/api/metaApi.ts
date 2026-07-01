import { getJson } from "./httpClient";
import type { MetaResponse } from "../types/meta";

export function fetchMeta(): Promise<MetaResponse> {
  return getJson<MetaResponse>("/api/v1/meta");
}
