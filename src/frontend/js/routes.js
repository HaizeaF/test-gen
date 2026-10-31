/** Registry of the windows of the application. Adding a window means adding an entry here. */

import { ENTITIES } from "./entity_definitions.js";
import { DataView } from "./data_view.js";
import { PlaceholderView } from "./placeholder_view.js";

export function buildRoutes({ apis, alerts, form, confirm }) {
    /** Build the list of routes, giving each view the shared services it needs. */
    return [
        {
        path: "/quiz",
        label: "Quiz",
        icon: "bi-play-circle",
        createView: () =>
            new PlaceholderView({ title: "Quiz", subtitle: "Practice with the topics and sections you choose.", icon: "bi-play-circle" }),
        },
        {
        path: "/data",
        label: "Data",
        icon: "bi-database",
        createView: () => new DataView({ definitions: ENTITIES, apis, form, confirm, alerts }),
        },
        {
        path: "/analytics",
        label: "Analytics",
        icon: "bi-graph-up",
        createView: () =>
            new PlaceholderView({ title: "Analytics", subtitle: "Understand your study habits and weak spots.", icon: "bi-graph-up" }),
        },
    ];
}