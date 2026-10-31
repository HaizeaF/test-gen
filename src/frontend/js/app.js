/** Composition root of the frontend: creates the shared services and starts the router. */

import { ApiClient } from "./api_client.js";
import { ResourceApi } from "./resource_api.js";
import { AlertCenter } from "./alert_center.js";
import { ConfirmDialog } from "./confirm_dialog.js";
import { EntityForm } from "./entity_form.js";
import { NavBar } from "./nav_bar.js";
import { ENTITIES } from "./entity_definitions.js";
import { buildRoutes } from "./routes.js";
import { Router } from "./router.js";

const DEFAULT_PATH = "/data";


export class App {
    /** Wires every piece of the frontend together. */
    constructor({ apiBaseUrl }) {
        this.apiBaseUrl = apiBaseUrl;
    }

    start() {
        /** Build the services, draw the navigation bar and show the window of the current URL. */
        const client = new ApiClient(this.apiBaseUrl);
        const apis = Object.fromEntries(ENTITIES.map((entity) => [entity.key, new ResourceApi(client, entity.path)]));
        const routes = buildRoutes({ apis, alerts: new AlertCenter(), form: new EntityForm(), confirm: new ConfirmDialog() });

        const navBar = new NavBar(document.querySelector("#navbar"), routes, DEFAULT_PATH);
        navBar.render();

        new Router({
            routes,
            outlet: document.querySelector("#view"),
            defaultPath: DEFAULT_PATH,
            onNavigate: (route) => navBar.setActive(route.path)
        }).start();
    }
}