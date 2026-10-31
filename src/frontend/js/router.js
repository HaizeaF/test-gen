/** Hash-based router that shows one view at a time. */

export class Router {
    /** Maps the URL hash to a route, mounts its view and unmounts the previous one. */
    constructor({ routes, outlet, defaultPath, onNavigate }) {
        this.routes = routes;
        this.outlet = outlet;
        this.defaultPath = defaultPath;
        this.onNavigate = onNavigate;
        this.currentView = null;
    }

    start() {
        /** Listen to hash changes and show the view of the current hash. */
        window.addEventListener("hashchange", () => this.#navigate());

        return this.#navigate();
    }

    #resolve() {
        /** Find the route of the current hash, falling back to the default one. */
        const path = window.location.hash.slice(1);

        return this.routes.find((route) => route.path === path) ?? this.routes.find((route) => route.path === this.defaultPath);
    }

    async #navigate() {
        /** Replace the current view with the one of the resolved route. */
        const route = this.#resolve();

        this.currentView?.unmount();
        this.currentView = route.createView();
        this.onNavigate(route);
        await this.currentView.mount(this.outlet);
    }
}