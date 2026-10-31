/** Declarative description of the entities managed in the data window. */

import { h } from "./dom.js";

const MAX_TEXT_LENGTH = 80;

const CORRECT_OPTION_CHOICES = ["a", "b", "c", "d"].map((option) => ({ value: option, label: option.toUpperCase() }));

function truncate(text) {
    /** Shorten a long text so it fits in a table cell. */
    return text.length > MAX_TEXT_LENGTH ? `${text.slice(0, MAX_TEXT_LENGTH)}…` : text;
}

function buildBadge(text) {
    /** Build a soft purple badge around a short text. */
    return h("span", { class: "badge badge-soft rounded-pill" }, text);
}

function buildQuestionStatus(question) {
    /** Build the badges that describe the state of a question, or a dash when there is nothing to report. */
    const badges = [
        question.flagged && h("span", { class: "badge text-bg-warning me-1" }, h("i", { class: "bi bi-flag-fill me-1" }), "Flagged"),
        !question.active && h("span", { class: "badge text-bg-secondary" }, "Inactive"),
    ].filter(Boolean);

    return badges.length ? h("span", {}, ...badges) : "—";
}

export const ENTITIES = [
    {
        key: "topics",
        path: "/topics",
        label: "Topics",
        singular: "topic",
        icon: "bi-bookmarks",
        description: "Topics",
        columns: [{ header: "Name", value: (topic) => topic.name }],
        fields: [{ name: "name", label: "Name", type: "text", required: true }],
    },
    {
        key: "sections",
        path: "/sections",
        label: "Sections",
        singular: "section",
        icon: "bi-diagram-3",
        description: "Sections",
        columns: [
        { header: "Name", value: (section) => section.name },
        { header: "Topic", value: (section) => buildBadge(section.topic_name) },
        ],
        fields: [
        { name: "name", label: "Name", type: "text", required: true },
        {
            name: "topic_id",
            label: "Topic",
            type: "select",
            numeric: true,
            required: true,
            choices: { source: "topics", label: (topic) => topic.name },
        },
        ],
    },
    {
        key: "questions",
        path: "/questions",
        label: "Questions",
        singular: "question",
        icon: "bi-question-circle",
        description: "Questions",
        rowClass: (question) => (question.flagged ? "row-flagged" : ""),
        columns: [
        { header: "Question", value: (question) => truncate(question.text) },
        { header: "Section", value: (question) => question.section_name },
        { header: "Topic", value: (question) => buildBadge(question.topic_name) },
        { header: "Correct", value: (question) => buildBadge(question.correct_option.toUpperCase()) },
        { header: "Status", value: buildQuestionStatus },
        ],
        fields: [
        {
            name: "section_id",
            label: "Section",
            type: "select",
            numeric: true,
            required: true,
            choices: { source: "sections", label: (section) => `${section.topic_name} › ${section.name}` },
        },
        { name: "text", label: "Question", type: "textarea", required: true },
        { name: "option_a", label: "Option A", type: "text", required: true, span: 6 },
        { name: "option_b", label: "Option B", type: "text", required: true, span: 6 },
        { name: "option_c", label: "Option C", type: "text", required: true, span: 6 },
        { name: "option_d", label: "Option D", type: "text", required: true, span: 6 },
        { name: "correct_option", label: "Correct option", type: "select", required: true, choices: { static: CORRECT_OPTION_CHOICES } },
        { name: "active", label: "Active", type: "checkbox", editOnly: true, span: 6 },
        { name: "flagged", label: "Flagged for review", type: "checkbox", editOnly: true, span: 6 },
        ],
    }
];