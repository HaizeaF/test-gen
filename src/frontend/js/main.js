/** Entry point of the frontend. */

import { API_BASE_URL } from "./config.js";
import { App } from "./app.js";

new App({ apiBaseUrl: API_BASE_URL }).start();