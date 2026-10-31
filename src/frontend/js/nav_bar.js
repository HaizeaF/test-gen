/** Navigation bar shared by every window of the frontend. */

import { h } from "./dom.js";

export class NavBar {
  /** Draws one link per route and highlights the one of the current window. */
    constructor(container, routes, homePath) {
        this.container = container;
        this.routes = routes;
        this.homePath = homePath;
        this.links = new Map();
    }

    render() {
        /** Draw the brand and the links. */
        for (const route of this.routes) {
            this.links.set(route.path, this.#buildLink(route));
        }

        this.container.replaceChildren(
            h(
                "nav",
                { class: "navbar navbar-expand app-navbar" },
                h(
                    "div",
                    { class: "container-xxl" },
                    h("a", { class: "navbar-brand d-flex align-items-center gap-2", href: `#${this.homePath}` }, h("i", { class: "bi bi-mortarboard-fill" }), "TestGen"),
                    h("ul", { class: "navbar-nav ms-auto gap-1" }, ...[...this.links.values()].map((link) => h("li", { class: "nav-item" }, link)))
                )
            ),
        );
    }

    setActive(path) {
        /** Highlight the link of the given path and clear the rest. */
        for (const [linkPath, link] of this.links) {
            link.classList.toggle("active", linkPath === path);
        }
    }

    #buildLink(route) {
         /** Build the link of one route. */
        return h("a", { class: "nav-link d-flex align-items-center gap-2", href: `#${route.path}` }, h("i", { class: `bi ${route.icon}` }), route.label);
    }
}