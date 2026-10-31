/** Transient alert messages floating over the page. */

import { h } from "./dom.js";

export class AlertCenter {
  /** Shows dismissible Bootstrap alerts that disappear on their own. */
    constructor(durationMs = 5000) {
        this.durationMs = durationMs;
        this.container = h("div", { class: "alert-stack", "aria-live": "polite" });
        document.body.append(this.container);
    }

    show(message, type = "danger") {
        /** Show an alert of the given Bootstrap type, such as "danger" or "success". */
        const alert = h(
            "div",
            { class: `alert alert-${type} alert-dismissible shadow-sm mb-0`, role: "alert" },
            message,
            h("button", { type: "button", class: "btn-close", "data-bs-dismiss": "alert", "aria-label": "Close" })
        );

        this.container.append(alert);
        setTimeout(() => alert.remove(), this.durationMs);
    }
}