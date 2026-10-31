/** Header shared by every window: a title and a one-line description. */

import { h } from "./dom.js";

export function buildPageHeader(title, subtitle) {
    /** Build the header of a window. */
    return h("header", { class: "page-header" }, h("h1", {}, title), h("p", {}, subtitle));
}