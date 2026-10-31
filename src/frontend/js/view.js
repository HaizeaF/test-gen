/** Base class of the windows of the application. */

export class View {
    /** Contract every window follows so the router can show and discard it. */
    async mount(outlet) {
        throw new Error(`${this.constructor.name} must implement mount().`);
    }

    /** Release whatever the window holds when the user leaves it. */
    unmount() {}
}