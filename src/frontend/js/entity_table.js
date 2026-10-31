/** Table that lists the items of one entity with edit and delete buttons. */

import { h } from "./dom.js";

export class EntityTable {
    /** Renders the items of an entity following its definition. */
    constructor(definition, container, { onEdit, onDelete }) {
        this.definition = definition;
        this.container = container;
        this.handlers = { onEdit, onDelete };
    }

    render(items) {
        /** Draw the given items, or an empty state when there are none. */
        this.container.replaceChildren(items.length ? this.#buildTable(items) : this.#buildEmptyState());
    }

    #buildEmptyState() {
        /** Build the message shown when the entity has no items. */
        return h(
            "div",
            { class: "empty-state" },
            h("i", { class: `bi ${this.definition.icon}` }),
            h("h3", {}, `No ${this.definition.label.toLowerCase()} yet`),
            h("p", { class: "mb-0" }, `Create the first ${this.definition.singular} to get started.`)
        );
    }

    #buildTable(items) {
        /** Build the table with its header and one row per item. */
        const headers = [...this.definition.columns.map((column) => column.header), "Actions"];

        return h(
            "div",
            { class: "table-responsive" },
            h(
                "table",
                { class: "table table-hover align-middle data-table" },
                h("thead", {}, h("tr", {}, ...headers.map((header) => h("th", { scope: "col", class: header === "Actions" ? "text-end" : "" }, header)))),
                h("tbody", {}, ...items.map((item) => this.#buildRow(item))),
            )
        );
    }

    #buildRow(item) {
        /** Build the row of one item, highlighted when the definition asks for it. */
        return h(
            "tr",
            { class: this.definition.rowClass?.(item) },
            ...this.definition.columns.map((column) => h("td", {}, column.value(item))),
            h("td", { class: "text-end text-nowrap" }, this.#buildActions(item))
        );
    }

    #buildActions(item) {
        /** Build the edit and delete buttons of one item. */
        return h(
            "div",
            { class: "btn-group btn-group-sm" },
            this.#buildButton("Edit", "bi-pencil", "btn-outline-primary", () => this.handlers.onEdit(item)),
            this.#buildButton("Delete", "bi-trash", "btn-outline-danger", () => this.handlers.onDelete(item))
        );
    }

    #buildButton(label, icon, styleClass, onClick) {
        /** Build one icon button with an accessible label. */
        return h(
            "button",
            { type: "button", class: `btn ${styleClass}`, title: label, "aria-label": label, onclick: onClick },
            h("i", { class: `bi ${icon}` })
        );
    }
}