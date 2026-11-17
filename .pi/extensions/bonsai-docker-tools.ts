import { Type } from "typebox";
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { installLifecycleTools } from "./bonsai-docker-tools-core.mjs";

export default function (pi: ExtensionAPI) {
  installLifecycleTools(pi, Type);
}
