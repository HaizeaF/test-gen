/** Window to view, create, edit and delete topics, sections and questions. */

import { buildPageHeader } from "./page_header.js";
import { EntityTable } from "./entity_table.js";
import { h } from "./dom.js";
import { View } from "./view.js";

export class DataView extends View {
    /** Coordinates the tabs, tables, form and confirmation of every entity. */
    constructor({ definitions, apis, form, confirm, alerts }) {
        super();
        this.definitions = definitions;
        this.apis = apis;
        this.form = form;
        this.confirm = confirm;
        this.alerts = alerts;
        this.items = {};
        this.tables = {};
        this.counters = {};
    }

    async mount(outlet) {
        /** Draw the header, the tabs and the panes, then load the data. */
        const tabs = this.#buildTabs();
        const panes = this.#buildPanes();

        outlet.replaceChildren(
            buildPageHeader("Data", "Manage the topics, sections and questions your quizzes are built from."),
            tabs,
            panes
        );
        await this.refresh();
    }

    async refresh() {
        /** Reload every entity, because a change in one can alter the names shown in the others. */
        try {
            const results = await Promise.all(this.definitions.map((definition) => this.apis[definition.key].list()));

            this.definitions.forEach((definition, index) => {
                this.items[definition.key] = results[index];
                this.tables[definition.key].render(results[index]);
                this.counters[definition.key].textContent = String(results[index].length);
            });
        } catch (error) {
            this.alerts.show(error.message);
        }
    }

    #buildTabs() {
        /** Build the pills that switch between entities, each with a counter. */
        return h(
            "ul",
            { class: "nav nav-pills tab-pills mb-4 gap-1", role: "tablist" },
            ...this.definitions.map((definition, index) => {
                this.counters[definition.key] = h("span", { class: "badge badge-soft rounded-pill ms-2" }, "0");

                return h(
                    "li",
                    { class: "nav-item", role: "presentation" },
                    h(
                        "button",
                        {
                            class: `nav-link d-flex align-items-center ${index === 0 ? "active" : ""}`,
                            type: "button",
                            role: "tab",
                            "data-bs-toggle": "pill",
                            "data-bs-target": `#pane-${definition.key}`,
                        },
                        h("i", { class: `bi ${definition.icon} me-2` }),
                        definition.label,
                        this.counters[definition.key],
                    )
                );
            }),
        );
    }

    #buildPanes() {
        /** Build one pane per entity with its card, its "new" button and its table. */
        return h(
            "div",
            { class: "tab-content" },
            ...this.definitions.map((definition, index) => {
                const tableContainer = h("div");

                this.tables[definition.key] = new EntityTable(definition, tableContainer, {
                    onEdit: (item) => this.#openForm(definition, item),
                    onDelete: (item) => this.#remove(definition, item)
                });

                return h(
                    "div",
                    { class: `tab-pane fade ${index === 0 ? "show active" : ""}`, id: `pane-${definition.key}`, role: "tabpanel" },
                    h(
                        "section",
                        { class: "surface-card" },
                        h(
                        "div",
                        { class: "surface-card-header" },
                        h("h2", {}, definition.description),
                        h(
                            "button",
                            { type: "button", class: "btn btn-primary", onclick: () => this.#openForm(definition) },
                            h("i", { class: "bi bi-plus-lg me-1" }),
                            `New ${definition.singular}`,
                        ),
                        ),
                        tableContainer,
                    )
                );
            }),
        );
    }

    #openForm(definition, item = null) {
        /** Open the form to create an item, or to edit one when it is given. */
        const isEdit = item !== null;
        const fields = definition.fields.filter((field) => isEdit || !field.editOnly);
        const api = this.apis[definition.key];

        this.form.open({
            title: `${isEdit ? "Edit" : "New"} ${definition.singular}`,
            fields,
            choices: this.#resolveChoices(fields),
            values: item ?? {},
            onSubmit: async (values) => {
                await (isEdit ? api.update(item.id, values) : api.create(values));
                await this.refresh();
                this.alerts.show(`The ${definition.singular} was saved.`, "success");
            }
        });
    }

    async #remove(definition, item) {
        /** Delete an item after asking for confirmation. */
        const confirmed = await this.confirm.ask({
            title: `Delete ${definition.singular}`,
            message: `This ${definition.singular} will be permanently deleted.`,
        });

        if (!confirmed) {
            return;
        }

        try {
            await this.apis[definition.key].remove(item.id);
            await this.refresh();
            this.alerts.show(`The ${definition.singular} was deleted.`, "success");
        } catch (error) {
            this.alerts.show(error.message);
        }
    }

    #resolveChoices(fields) {
        /** Build the options of every select field, either fixed or taken from another entity. */
        const choices = {};

        for (const field of fields.filter((candidate) => candidate.type === "select")) {
            choices[field.name] =
                field.choices.static ??
                this.items[field.choices.source].map((item) => ({ value: item.id, label: field.choices.label(item) }));
        }

        return choices;
    }
}