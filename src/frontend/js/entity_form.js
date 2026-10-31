/** Modal form built on the fly from a list of field definitions. */

import { h } from "./dom.js";
import { ModalDialog } from "./modal_dialog.js";

export class EntityForm {
    /** Shows a modal with a form and hands the submitted values to a callback. */
    constructor() {
        this.dialog = new ModalDialog({ asForm: true, size: "modal-lg" });
        this.errorElement = h("div", { class: "alert alert-danger d-none", role: "alert" });
        this.fieldsElement = h("div", { class: "row g-3" });
        this.submitButton = h("button", { type: "submit", class: "btn btn-primary" }, "Save");
        this.fields = [];
        this.onSubmit = null;

        this.dialog.bodyElement.append(this.errorElement, this.fieldsElement);
        this.dialog.footerElement.append(
        h("button", { type: "button", class: "btn btn-light", "data-bs-dismiss": "modal" }, "Cancel"),
            this.submitButton
        );
        this.dialog.content.addEventListener("submit", (event) => this.#handleSubmit(event));
    }

    open({ title, fields, choices = {}, values = {}, onSubmit }) {
        /** Open the form with the given fields, current values and the callback that saves them. */
        this.fields = fields;
        this.onSubmit = onSubmit;
        this.#showError("");
        this.fieldsElement.replaceChildren(
            ...fields.map((field) => this.#buildField(field, choices[field.name] ?? [], values[field.name])),
        );
        this.dialog.show(title);
    }

    async #handleSubmit(event) {
        /** Save the values, closing the modal on success or showing the error inside it on failure. */
        event.preventDefault();
        this.#showError("");
        this.submitButton.disabled = true;

        try {
            await this.onSubmit(this.#readValues());
            this.dialog.hide();
        } catch (error) {
            this.#showError(error.message);
        } finally {
            this.submitButton.disabled = false;
        }
    }

    #readValues() {
        /** Collect the values of the form with the type each field expects. */
        const values = {};

        for (const field of this.fields) {
            const input = this.fieldsElement.querySelector(`[name='${field.name}']`);

            if (field.type === "checkbox") {
                values[field.name] = input.checked;
            } else {
                values[field.name] = field.numeric ? Number(input.value) : input.value.trim();
            }
        }

        return values;
    }

    #showError(message) {
        /** Show an error message inside the modal, or hide it when the message is empty. */
        this.errorElement.textContent = message;
        this.errorElement.classList.toggle("d-none", !message);
    }

    #buildField(field, choices, value) {
        /** Build a field with its label and input, in a column as wide as the field asks for. */
        const id = `field-${field.name}`;
        const isSwitch = field.type === "checkbox";
        const input = this.#buildInput(field, id, choices, value);
        const label = h("label", { for: id, class: isSwitch ? "form-check-label" : "form-label fw-medium" }, field.label);

        return h(
            "div",
        { class: field.span ? `col-12 col-md-${field.span}` : "col-12" },
            isSwitch ? h("div", { class: "form-check form-switch" }, input, label) : [label, input],
        );
    }

    #buildInput(field, id, choices, value) {
        /** Build the input element that matches the type of the field. */
        const common = { id, name: field.name, required: field.required };

        if (field.type === "checkbox") {
            return h("input", { ...common, type: "checkbox", role: "switch", class: "form-check-input", checked: Boolean(value) });
        }

        if (field.type === "select") {
            return h(
                "select",
                { ...common, class: "form-select", value: value === undefined ? "" : String(value) },
                h("option", { value: "" }, "Select…"),
                ...choices.map((choice) => h("option", { value: String(choice.value) }, choice.label))
            );
        }

        if (field.type === "textarea") {
            return h("textarea", { ...common, class: "form-control", rows: 3, value: value ?? "" });
        }

        return h("input", { ...common, type: "text", class: "form-control", value: value ?? "" });
    }
}