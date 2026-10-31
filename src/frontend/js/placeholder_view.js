/** Window shown for sections of the application that are not built yet. */

import { buildPageHeader } from "./page_header.js";
import { h } from "./dom.js";
import { View } from "./view.js";

export class PlaceholderView extends View {
    /** Shows a "coming soon" message under the header of the window. */
    constructor({ title, subtitle, icon }) {
        super();
        this.title = title;
        this.subtitle = subtitle;
        this.icon = icon;
    }

    async mount(outlet) {
        /** Draw the header and the empty state. */
        outlet.replaceChildren(
            buildPageHeader(this.title, this.subtitle),
            h(
                "section",
                { class: "surface-card" },
                h(
                    "div",
                    { class: "empty-state" },
                    h("i", { class: `bi ${this.icon}` }),
                    h("h3", {}, "Coming soon"),
                    h("p", { class: "mb-0" }, "This window is not available yet.")
                )
            )
        );
    }
}